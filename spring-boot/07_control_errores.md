# Programación y Plataformas Web

# **Spring Boot – Control Global de Errores y Excepciones**

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg" width="95">
</div>

## Práctica 7 (Spring Boot): Manejo Global de Errores y Excepciones

### Autores

**Pablo Torres**
📧 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)
💻 GitHub: PabloT18


# Introducción

En los temas anteriores, el backend ya cuenta con:

* controladores limpios
* servicios con lógica de negocio
* DTOs validados
* persistencia real con JPA
* arquitectura MVCS

Sin embargo, **un backend no es profesional** si:

* cada error se maneja distinto
* se devuelve texto plano
* se exponen mensajes internos
* se usan `try/catch` en cada método

En este tema se implementa un **sistema global de manejo de errores**, usando los mecanismos nativos de Spring Boot, manteniendo:

* coherencia
* extensibilidad
* separación de responsabilidades
* un único formato de respuesta


# 1. Estructura del paquete `exception`

Se utilizará una estructura clara y escalable:

```
src/main/java/ec/edu/ups/app/
└── exception/
    ├── base/
    │   ├── ApplicationException.java
    │   └── ErrorCode.java
    │
    ├── domain/
    │   ├── NotFoundException.java
    │   ├── ConflictException.java
    │   └── BadRequestException.java
    │
    ├── handler/
    │   └── GlobalExceptionHandler.java
    │
    └── response/
        └── ErrorResponse.java
```

Esta estructura:

* evita clases genéricas mal definidas
* permite crecer sin romper código
* separa dominio, infraestructura y transporte


# 2. Excepción base de la aplicación

## `ApplicationException`

Archivo:
`exception/base/ApplicationException.java`

```java
public abstract class ApplicationException extends RuntimeException {

    private final HttpStatus status;

    protected ApplicationException(HttpStatus status, String message) {
        super(message);
        this.status = status;
    }

    public HttpStatus getStatus() {
        return status;
    }
}
```

Características:

* es la raíz de todas las excepciones del sistema
* obliga a definir un `HttpStatus`
* evita el uso de `RuntimeException` genérica
* no genera respuesta HTTP directamente


# 3. Excepciones de dominio

Las excepciones de dominio **representan errores del negocio**, no técnicos.

## 3.1 Recurso no encontrado

**Descripción:**  
Se lanza cuando se intenta acceder a un recurso que no existe en la base de datos o en el sistema.

**Cuándo usarla:**
- Al buscar una entidad por ID y no se encuentra
- Al intentar actualizar o eliminar un recurso inexistente
- En operaciones que requieren que el recurso exista previamente

**Dónde se usa:**
- En servicios, dentro de métodos como `findById()`, `update()`, `delete()`
- Después de consultas a repositorios que retornan `Optional.empty()`

**Ejemplo de uso:**
```java
// En un servicio
public Product findById(Long id) {
    return productRepository.findById(id)
        .orElseThrow(() -> new NotFoundException("Producto no encontrado con ID: " + id));
}
```

Archivo:
`exception/domain/NotFoundException.java`

```java
public class NotFoundException extends ApplicationException {

    public NotFoundException(String message) {
        super(HttpStatus.NOT_FOUND, message);
    }
}
```


## 3.2 Conflicto de estado

**Descripción:**  
Se lanza cuando existe un conflicto con el estado actual del recurso, generalmente por duplicación de datos únicos o violación de restricciones de integridad.

**Cuándo usarla:**
- Al intentar crear un recurso con un identificador único ya existente (email, username, código)
- Cuando se intenta realizar una operación que violaría una restricción de unicidad
- Al detectar conflictos de concurrencia o versiones

**Dónde se usa:**
- En servicios, dentro de métodos `create()` o `register()`
- Antes de persistir datos, validando unicidad
- En operaciones de registro de usuarios o creación de entidades con campos únicos

**Ejemplo de uso:**
```java
// En un servicio
public User register(UserDto userDto) {
    if (userRepository.existsByEmail(userDto.getEmail())) {
        throw new ConflictException("El email " + userDto.getEmail() + " ya está registrado");
    }
    return userRepository.save(new User(userDto));
}
```

Archivo:
`exception/domain/ConflictException.java`

```java
public class ConflictException extends ApplicationException {

    public ConflictException(String message) {
        super(HttpStatus.CONFLICT, message);
    }
}
```


## 3.3 Solicitud inválida (Bad Request)

**Descripción:**  
Se lanza cuando la solicitud del cliente no puede ser procesada debido a datos inválidos, malformados o que no cumplen con las expectativas del servidor. Es la excepción general para errores de validación de negocio y datos.

**Cuándo usarla:**
- Cuando los datos son técnicamente válidos pero violan reglas de negocio
- Al detectar operaciones no permitidas según el estado actual del sistema
- Cuando se incumplen condiciones del dominio (stock insuficiente, saldo negativo, edad mínima)
- Para errores de validación que no son capturados por anotaciones de Bean Validation
- Cuando la estructura de los datos es correcta pero los valores no son aceptables

**Dónde se usa:**
- En servicios, dentro de la lógica de negocio y validaciones
- Después de validaciones específicas del dominio o del sistema
- En operaciones complejas que requieren verificar múltiples condiciones
- Como alternativa general a errores de validación no cubiertos por `@Valid`

**Ejemplo de uso:**
```java
// En un servicio
public Order createOrder(OrderDto orderDto) {
    Product product = findProductById(orderDto.getProductId());
    
    if (product.getStock() < orderDto.getQuantity()) {
        throw new BadRequestException(
            "Stock insuficiente. Disponible: " + product.getStock() + 
            ", solicitado: " + orderDto.getQuantity()
        );
    }
    
    if (orderDto.getQuantity() < 1) {
        throw new BadRequestException("La cantidad debe ser al menos 1");
    }
    
    return orderRepository.save(new Order(orderDto));
}
```

Archivo:
`exception/domain/BadRequestException.java`

```java
public class BadRequestException extends ApplicationException {

    public BadRequestException(String message) {
        super(HttpStatus.BAD_REQUEST, message);
    }
}
```

Estas excepciones:

* se lanzan desde **services**
* no conocen controladores
* no construyen respuestas


# 4. Contrato de respuesta de error

## `ErrorResponse`

Archivo:
`exception/response/ErrorResponse.java`

```java
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ErrorResponse implements Serializable {

    private LocalDateTime timestamp;
    private int status;
    private String error;
    private String message;
    private String path;
    private Map<String, String> details;

    public ErrorResponse(
            HttpStatus status,
            String message,
            String path,
            Map<String, String> details
    ) {
        this.timestamp = LocalDateTime.now();
        this.status = status.value();
        this.error = status.getReasonPhrase();
        this.message = message;
        this.path = path;
        this.details = details;
    }

    public ErrorResponse(HttpStatus status, String message, String path) {
        this(status, message, path, null);
    }

    // getters
}
```

### ¿Por qué dos constructores?

La clase `ErrorResponse` tiene dos constructores que responden a dos escenarios distintos:

#### Constructor completo (con `details`)
```java
public ErrorResponse(
        HttpStatus status,
        String message,
        String path,
        Map<String, String> details
)
```

**Se usa para:**
- Errores de validación con múltiples campos inválidos
- Cuando se necesita detallar qué campos específicos fallaron y por qué
- Permite al cliente saber exactamente qué debe corregir

**Ejemplo de respuesta:**
```json
{
  "timestamp": "2025-12-26T15:12:42.301031",
  "status": 400,
  "error": "Bad Request",
  "message": "Datos de entrada inválidos",
  "path": "/api/users",
  "details": {
    "name": "El nombre es obligatorio",
    "email": "El email es obligatorio"
  }
}
```

#### Constructor simplificado (sin `details`)
```java
public ErrorResponse(HttpStatus status, String message, String path) {
    this(status, message, path, null);
}
```

**Se usa para:**
- Errores de dominio simples (recurso no encontrado, conflicto)
- Excepciones generales del sistema
- Cuando no hay campos específicos que reportar

**Ejemplo de respuesta:**
```json
{
  "timestamp": "2025-12-26T15:07:20.967935",
  "status": 404,
  "error": "Not Found",
  "message": "Usuario no encontrado",
  "path": "/api/users/10"
}
```

Note que el campo `details` no aparece cuando es `null` gracias a:
```java
@JsonInclude(JsonInclude.Include.NON_NULL)
```

Este objeto:

* define el **único formato de error**
* soporta errores simples y de validación
* no expone información interna
* es reutilizable en todo el sistema


# 5. Handler global de excepciones

## `GlobalExceptionHandler`

Archivo:
`exception/handler/GlobalExceptionHandler.java`

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ApplicationException.class)
    public ResponseEntity<ErrorResponse> handleApplicationException(
            ApplicationException ex,
            HttpServletRequest request
    ) {
        ErrorResponse response = new ErrorResponse(
                ex.getStatus(),
                ex.getMessage(),
                request.getRequestURI()
        );

        return ResponseEntity
                .status(ex.getStatus())
                .body(response);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(
            MethodArgumentNotValidException ex,
            HttpServletRequest request
    ) {
        Map<String, String> errors = new HashMap<>();

        ex.getBindingResult()
          .getFieldErrors()
          .forEach(error ->
              errors.put(error.getField(), error.getDefaultMessage())
          );

        ErrorResponse response = new ErrorResponse(
                HttpStatus.BAD_REQUEST,
                "Datos de entrada inválidos",
                request.getRequestURI(),
                errors
        );

        return ResponseEntity
                .badRequest()
                .body(response);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleUnexpectedException(
            Exception ex,
            HttpServletRequest request
    ) {
        ErrorResponse response = new ErrorResponse(
                HttpStatus.INTERNAL_SERVER_ERROR,
                "Error interno del servidor",
                request.getRequestURI()
        );

        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(response);
    }
}
```


# 6. Uso desde los servicios


Antes de aplicar el manejo global, lanzabamos una excepcion generica no controlado con 

```java
 @Override
    public UserResponseDto findOne(int id) {
        return userRepo.findById((long) id)
                .map(User::fromEntity)
                .map(UserMapper::toResponse)
                .orElseThrow(() -> new IllegalStateException("Usuario no encontrado"));
    }
```
Lo que nos daba una respuesta de error inconsistente como:

```
{
  "timestamp": "2025-12-26T20:02:02.067Z",
  "status": 500,
  "error": "Internal Server Error",
  "trace": "java.lang.IllegalStateException: Usuario no encontrado...."
}
```

Genera un `500 Internal Server Error` con un stack trace expuesto al cliente. Incluso el error no es correcto ya que el recurso no fue encontrado, por lo cual debió ser un `404 Not Found`. No seria error del servidor, sino del cliente al solicitar un recurso inexistente.

Que pudiera estar bien para desarrollo, pero no es profesional para un API REST. Ni tampoco es escalable ni mantenible y su el logging es deficiente ya que modificar un logger en cada servicio es tedioso.

Por lo cual aplicamos el manejo global de errores y excepciones, lanzando excepciones de dominio específicas como `NotFoundException`, `ConflictException` o `BadRequestException`.

Ejemplo real en un servicio:

```java
@Override
public UserResponseDto findOne(int id) {
    return userRepository.findById((long) id)
            .map(User::fromEntity)
            .map(UserMapper::toResponse)
            .orElseThrow(() ->
                new NotFoundException("Usuario no encontrado")
            );
}
```

Lo que nos da una respuesta de error consistente como:

```
{
  "error": "Not Found",
  "message": "Usuario no encontrado",
  "path": "/api/users/10",
  "status": 404,
  "timestamp": "2025-12-26T15:07:20.967935"
}
```

Aqui se genera un `404 Not Found` con un mensaje claro y sin exponer detalles internos. Dando a entender al cliente que el recurso no existe y que pide algo incorrecto.

El atributo `path` en situaciones reales es muy útil para debugging en el cliente. Pero dependiendo del caso de uso, se puede omitir si no es necesario y no mostrar información extra.

El servicio:

* **no captura**
* **no construye ResponseEntity**
* **solo expresa el error**


# 6.2. Validación automática de DTOs

## ¿Cómo funciona la validación de DTOs?

Cuando se envía una petición POST con datos mal formados:

**Request:**
```http
POST /api/users
Content-Type: application/json

{
  "name": "",
  "email": null,
  "password": "********"
}
```

El proceso automático es:

### 1. Las anotaciones de validación en el DTO

```java
    @NotBlank(message = "El nombre es obligatorio")
    private String name;
    
    @NotNull(message = "El email es obligatorio")
    @Email(message = "El email debe ser válido")
    private String email;
    // mas campos
}
```

### 2. El controlador usa `@Valid`

```java
@PostMapping
public ResponseEntity<UserResponseDto> create(
        @Valid @RequestBody UserDto userDto
) {
    UserResponseDto created = userService.create(userDto);
    return ResponseEntity.status(HttpStatus.CREATED).body(created);
}
```

Al usar `@Valid`, Spring Boot automáticamente:

1. Valida cada campo del DTO según sus anotaciones
2. Si hay errores, **NO llama al servicio**
3. Lanza una excepción: `MethodArgumentNotValidException`
4. Esta excepción es capturada por el `GlobalExceptionHandler`

### 3. El handler procesa los errores de validación

En el `GlobalExceptionHandler` existe un método específico:

```java
@ExceptionHandler(MethodArgumentNotValidException.class)
public ResponseEntity<ErrorResponse> handleValidationException(
        MethodArgumentNotValidException ex,
        HttpServletRequest request
) {
    Map<String, String> errors = new HashMap<>();

    // Extrae cada error de validación
    ex.getBindingResult()
      .getFieldErrors()
      .forEach(error ->
          errors.put(error.getField(), error.getDefaultMessage())
      );

    ErrorResponse response = new ErrorResponse(
            HttpStatus.BAD_REQUEST,
            "Datos de entrada inválidos",
            request.getRequestURI(),
            errors  // ← Aquí van los detalles campo por campo
    );

    return ResponseEntity
            .badRequest()
            .body(response);
}
```

### 4. La respuesta mejora automáticamente

**Response:**
```json
{
  "timestamp": "2025-12-26T15:12:42.301031",
  "status": 400,
  "error": "Bad Request",
  "message": "Datos de entrada inválidos",
  "path": "/api/users",
  "details": {
    "name": "El nombre es obligatorio",
    "email": "El email es obligatorio"
  }
}
```

## ¿Por qué aparece el campo `details`?

El campo `details` aparece porque:

1. **Hay múltiples errores de validación**: Los campos `name` y `email` fallaron
2. **El handler los recopila**: El método `handleValidationException` extrae cada `FieldError`
3. **Se usa el constructor completo**: Se invoca el constructor de `ErrorResponse` que acepta el parámetro `details`
4. **El cliente recibe toda la información**: Puede mostrar errores específicos por campo en su interfaz

## Flujo completo de validación

```
Request con datos inválidos
 ↓
Controller con @Valid
 ↓
Spring valida automáticamente
 ↓
¿Hay errores?
 ↓ (Sí)
MethodArgumentNotValidException
 ↓
GlobalExceptionHandler
 ↓
handleValidationException
 ↓
Extrae FieldErrors → Map<String, String>
 ↓
ErrorResponse con details
 ↓
Cliente recibe JSON estructurado
```

### Ventajas de este enfoque

**Cero código de validación en servicios**
- Los servicios asumen que los datos ya están validados
- No hay `if (name.isEmpty())` en cada método

**Respuestas consistentes**
- Todos los errores de validación usan el mismo formato
- El frontend sabe exactamente cómo interpretar errores

**Mensajes personalizados**
- Cada anotación define su propio mensaje
- No hay mensajes técnicos genéricos

**Escalable**
- Agregar nuevas validaciones solo requiere agregar anotaciones
- No hay que modificar handlers ni servicios

**Separación de responsabilidades**
- Validación estructural → anotaciones en DTOs
- Validación de negocio → servicios con excepciones de dominio
- Formato de respuesta → GlobalExceptionHandler


# 7. Flujo completo en ejecución

Ahora que se ha explicado cómo funciona la validación automática de DTOs, se puede visualizar el flujo completo del sistema de manejo de errores en dos escenarios:

## Escenario 1: Error de validación (datos mal formados)

**Request:**
```http
POST /api/users
Content-Type: application/json

{
  "name": "",
  "email": null,
  "password": "********"
}
```

**Flujo:**
```
Request HTTP con datos inválidos
 ↓
Controller (@Valid detecta errores)
 ↓
MethodArgumentNotValidException
 ↓
GlobalExceptionHandler.handleValidationException()
 ↓
Extrae cada FieldError → Map<campo, mensaje>
 ↓
ErrorResponse (constructor con details)
 ↓
Response HTTP 400
```

**Response:**
```json
{
  "timestamp": "2025-12-26T15:12:42.301031",
  "status": 400,
  "error": "Bad Request",
  "message": "Datos de entrada inválidos",
  "path": "/api/users",
  "details": {
    "name": "El nombre es obligatorio",
    "email": "El email es obligatorio"
  }
}
```

**¿Por qué sale así?**

1. **El campo `details` aparece**: Porque hay múltiples errores de validación y se usa el constructor completo de `ErrorResponse`
2. **Los mensajes son personalizados**: Provienen de las anotaciones en el DTO (`@NotBlank(message = "...")`)
3. **Status 400**: Indica que el cliente envió datos inválidos
4. **El servicio nunca se ejecutó**: La validación ocurre ANTES de llegar al servicio

## Escenario 2: Error de dominio (recurso no encontrado)

**Request:**
```http
GET /api/users/999
```

**Flujo:**
```
Request HTTP
 ↓
Controller
 ↓
Service.findOne(999)
 ↓
Repository.findById(999) → Optional.empty()
 ↓
NotFoundException("Usuario no encontrado")
 ↓
GlobalExceptionHandler.handleApplicationException()
 ↓
ErrorResponse (constructor sin details)
 ↓
Response HTTP 404
```

**Response:**
```json
{
  "timestamp": "2025-12-26T15:07:20.967935",
  "status": 404,
  "error": "Not Found",
  "message": "Usuario no encontrado",
  "path": "/api/users/999"
}
```

**¿Por qué sale así?**

1. **No hay campo `details`**: Es un error simple, no de validación de múltiples campos
2. **Status 404**: La excepción `NotFoundException` define este status
3. **Mensaje claro**: El servicio lanza la excepción con un mensaje específico
4. **Sin stack trace**: Solo información necesaria para el cliente

## Comparación de ambos escenarios

| Aspecto | Validación de DTOs | Excepción de Dominio |
|---------|-------------------|---------------------|
| **Cuándo ocurre** | Antes del servicio | Dentro del servicio |
| **Tipo de excepción** | `MethodArgumentNotValidException` | `NotFoundException`, `ConflictException`, etc. |
| **Handler que responde** | `handleValidationException()` | `handleApplicationException()` |
| **Constructor usado** | Con `details` | Sin `details` |
| **Campo details** | Presente (Map de errores) | Ausente (null) |
| **Ejemplo de status** | 400 Bad Request | 404 Not Found, 409 Conflict |

## Ventajas del flujo unificado

Este flujo es:

* **Limpio**: Los controladores y servicios no manejan errores manualmente
* **Mantenible**: Agregar nuevos tipos de error solo requiere una nueva excepción
* **Escalable**: El formato de respuesta es consistente sin importar el tipo de error
* **Reutilizable**: El mismo handler funciona para toda la aplicación
* **Profesional**: Las respuestas están estandarizadas y son predecibles para el cliente

## Código del controlador (sin manejo de errores)

Gracias a este sistema, los controladores quedan extremadamente simples:

```java
@PostMapping
public ResponseEntity<UserResponseDto> create(
        @Valid @RequestBody UserDto userDto  // ← Validación automática
) {
    UserResponseDto created = userService.create(userDto);
    return ResponseEntity.status(HttpStatus.CREATED).body(created);
    // ← Sin try/catch, sin manejo manual
}

@GetMapping("/{id}")
public ResponseEntity<UserResponseDto> findOne(@PathVariable int id) {
    return ResponseEntity.ok(userService.findOne(id));
    // ← Si no existe, el servicio lanza NotFoundException
    // ← El handler se encarga del resto
}
```

El controlador solo:
- Define rutas
- Delega al servicio
- Retorna respuestas exitosas

Todos los errores se manejan globalmente de forma automática.


# 8. Buenas prácticas reforzadas

* Un solo formato de error
* Sin `try/catch` en controladores
* Excepciones semánticas
* Separación dominio / transporte
* Validación estructurada
* Preparado para frontend real


# 9. Actividad práctica

El estudiante debe:

1. Implementar el sistema de manejo global de errores
2. Usarlas desde servicios reales de **`Productos`**
3. Probar:
   * producto inexistente
   * conflicto lógico (Crear una regla de negocio como: "No se puede crear un producto con nombre duplicado" Crear otra no nombre duplicado)
   * error de validación (enviar datos mal formados)
4. Verificar que **todas** las respuestas cumplen el mismo formato
5. Capturar evidencias desde Bruno para cada caso de prueba.

**3 Capturas en total:**
