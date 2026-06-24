# Programación y Plataformas Web

# Frameworks Backend: Control Centralizado de Errores y Excepciones

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="80" alt="Java Logo">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="80" alt="TS Logo">
</div>

## Práctica 7: Control Centralizado de Errores, Excepciones y Respuestas Uniformes

### Autores

**Pablo Torres**

[ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: [PabloT18](https://github.com/PabloT18)

---

# Introducción

En los temas anteriores se trabajó con una arquitectura backend organizada mediante:

* controladores
* servicios
* DTOs
* modelos
* entidades
* mappers
* repositorios
* validaciones
* base de datos

Hasta este punto, la aplicación ya puede recibir datos, validarlos, transformarlos y almacenarlos.

Sin embargo, en una API real no todas las operaciones terminan correctamente.

Pueden ocurrir situaciones como:

* datos inválidos en una petición
* recursos inexistentes
* reglas de negocio incumplidas
* duplicidad de información
* errores de base de datos
* fallos inesperados del servidor

Si cada controlador o servicio maneja estos errores de forma diferente, la API se vuelve inconsistente y difícil de mantener.

Por eso se utiliza un **control centralizado de errores**, cuyo objetivo es capturar las excepciones del sistema y transformarlas en respuestas uniformes para el cliente.

---

# 1. Problema inicial

Una forma incorrecta de manejar errores es hacerlo directamente en cada controlador o servicio.

Ejemplo conceptual:

```txt
Controller
  - recibe petición
  - llama servicio
  - usa try/catch
  - arma mensaje de error
  - devuelve respuesta
```

Si esto se repite en muchos endpoints, aparecen problemas:

* duplicación de código
* respuestas diferentes para errores similares
* mensajes poco claros
* errores técnicos expuestos al cliente
* controladores demasiado grandes
* dificultad para mantener la API

Ejemplo de respuestas inconsistentes:

```json
{
  "error": "Usuario no encontrado"
}
```

En otro endpoint:

```json
{
  "message": "No existe el producto",
  "code": 404
}
```

En otro endpoint:

```json
{
  "status": "fail",
  "reason": "email already exists"
}
```

Aunque los tres son errores, cada uno tiene una estructura distinta.

Esto complica el consumo de la API desde el frontend.

---

# 2. Qué es un error en backend

Un error en backend es una situación que impide completar correctamente una operación.

No todos los errores tienen la misma causa.

Algunos errores son provocados por datos incorrectos enviados por el cliente.

Otros errores ocurren porque se incumple una regla del negocio.

Otros errores indican fallos técnicos del sistema.

Ejemplos:

```txt
El email tiene formato inválido.
El usuario no existe.
El correo ya está registrado.
La base de datos no responde.
El servidor falló inesperadamente.
```

Un backend profesional debe controlar estos casos y responder de forma clara.

---

# 3. Error y excepción

## 3.1 Error

El error es la situación no válida que ocurre dentro del sistema.

Ejemplo:

```txt
El usuario solicitado no existe.
```

## 3.2 Excepción

La excepción es el mecanismo técnico usado para interrumpir el flujo normal y comunicar que ocurrió un problema.

Ejemplo conceptual:

```txt
throw UserNotFoundException
```

La diferencia es:

| Concepto  | Significado                               |
| --------- | ----------------------------------------- |
| Error     | Situación no válida                       |
| Excepción | Mecanismo técnico para comunicar el error |

---

# 4. Tipos de errores en una API backend

## 4.1 Errores de validación

Son errores producidos porque los datos enviados por el cliente no cumplen el formato esperado.

Ejemplos:

```txt
El nombre es obligatorio.
El email no tiene formato válido.
La contraseña tiene menos de 8 caracteres.
El precio debe ser mayor que cero.
```

Estos errores normalmente se detectan en los DTOs.

Ejemplo:

```json
{
  "name": "",
  "email": "correo-invalido",
  "password": "123"
}
```

---

## 4.2 Errores de negocio

Son errores producidos cuando la petición tiene formato correcto, pero incumple una regla del sistema.

Ejemplos:

```txt
El correo ya está registrado.
El usuario está bloqueado.
No existe stock suficiente.
El estudiante ya está matriculado en el curso.
La orden ya fue pagada y no puede modificarse.
```

Estos errores normalmente se detectan en el servicio.

---

## 4.3 Errores de persistencia

Son errores relacionados con la base de datos o con restricciones de almacenamiento.

Ejemplos:

```txt
Clave única duplicada.
Relación inexistente.
Error de conexión con la base de datos.
Restricción de campo no nulo.
Error al guardar una entidad.
```

Estos errores pueden originarse en el repositorio, el ORM o la base de datos.

---

## 4.4 Errores técnicos

Son errores inesperados del sistema.

Ejemplos:

```txt
Servicio externo no disponible.
Error de red.
Archivo no encontrado.
Variable de entorno ausente.
Error no controlado del servidor.
```

Estos errores no deberían exponerse directamente al cliente.

---

# 5. Ubicación de los errores por capa

Cada capa puede producir errores diferentes.

| Capa       | Tipo de error frecuente | Ejemplo                 |
| ---------- | ----------------------- | ----------------------- |
| DTO        | Validación de formato   | Email inválido          |
| Controller | Parámetros incorrectos  | ID no numérico          |
| Service    | Regla de negocio        | Email ya registrado     |
| Mapper     | Conversión inválida     | Campo requerido ausente |
| Repository | Persistencia            | Error al consultar      |
| Database   | Restricción             | Clave única duplicada   |

Flujo conceptual:

```txt
Request JSON
  ↓
DTO
  ↓ error de validación
Controller
  ↓ error de parámetro
Service
  ↓ error de negocio
Repository
  ↓ error de persistencia
Database
  ↓ restricción de datos
```

El objetivo del control centralizado es que, sin importar dónde ocurra el error, la respuesta final tenga una estructura uniforme.

---

# 6. Respuesta uniforme de error

Una API backend debe responder los errores usando un formato común.

Ejemplo recomendado:

```json
{
  "timestamp": "2026-06-23T10:30:00Z",
  "statusCode": 404,
  "error": "Not Found",
  "message": "Usuario no encontrado",
  "path": "/api/v1/users/10"
}
```

Campos recomendados:

| Campo        | Descripción                        |
| ------------ | ---------------------------------- |
| `timestamp`  | Fecha y hora del error             |
| `statusCode` | Código HTTP asociado               |
| `error`      | Nombre general del error           |
| `message`    | Mensaje entendible para el cliente |
| `path`       | Ruta donde ocurrió el error        |

Para errores de validación, puede agregarse un campo `errors`.

Ejemplo:

```json
{
  "timestamp": "2026-06-23T10:30:00Z",
  "statusCode": 400,
  "error": "Bad Request",
  "message": "Error de validación",
  "path": "/api/v1/users",
  "errors": [
    {
      "field": "email",
      "message": "El correo debe tener un formato válido"
    },
    {
      "field": "password",
      "message": "La contraseña debe tener mínimo 8 caracteres"
    }
  ]
}
```

---

# 7. Por qué centralizar errores

Centralizar errores significa tener un componente global encargado de capturar excepciones y construir respuestas.

Sin control centralizado:

```txt
Controller A -> maneja error de una forma
Controller B -> maneja error de otra forma
Controller C -> no maneja error
```

Con control centralizado:

```txt
Controller
  ↓
Service
  ↓
Exception
  ↓
Global Error Handler
  ↓
Respuesta uniforme
```

Ventajas:

* evita duplicación de `try/catch`
* mantiene controladores limpios
* mantiene servicios enfocados en negocio
* unifica la estructura de errores
* facilita el consumo desde frontend
* mejora el mantenimiento
* reduce errores no controlados

---

# 8. Excepciones personalizadas

## 8.1 Qué son

Una excepción personalizada representa un error específico de la aplicación.

No todos los errores deberían lanzarse como errores genéricos.

Ejemplo no recomendado:

```txt
RuntimeException
Exception
Error
```

Ejemplo recomendado:

```txt
UserNotFoundException
EmailAlreadyExistsException
BusinessRuleException
ResourceNotFoundException
```

Las excepciones personalizadas permiten expresar mejor qué ocurrió.

---

## 8.2 Ejemplos de excepciones por caso

| Caso                        | Excepción conceptual           |
| --------------------------- | ------------------------------ |
| Usuario no encontrado       | `UserNotFoundException`        |
| Correo duplicado            | `EmailAlreadyExistsException`  |
| Producto sin stock          | `InsufficientStockException`   |
| Operación no permitida      | `OperationNotAllowedException` |
| Recurso inexistente         | `ResourceNotFoundException`    |
| Regla de negocio incumplida | `BusinessRuleException`        |

---

## 8.3 Dónde se lanzan las excepciones

Las excepciones deben lanzarse en la capa donde se detecta el problema.

Ejemplo:

```txt
DTO -> detecta formato inválido
Service -> lanza error de negocio
Repository -> propaga error de persistencia
Database -> genera error de restricción
```

Caso de usuario no encontrado:

```txt
Controller
  ↓
Service
  ↓ busca usuario
  ↓ no existe
  ↓ lanza UserNotFoundException
Global Handler
  ↓
Response 404
```

Caso de correo duplicado:

```txt
Controller
  ↓
Service
  ↓ verifica email
  ↓ email existe
  ↓ lanza EmailAlreadyExistsException
Global Handler
  ↓
Response 409
```

---

# 9. Códigos de estado asociados a errores

Aunque los códigos HTTP ya se revisaron anteriormente, en control de errores es necesario relacionarlos con el tipo de excepción.

| Código | Caso común                        | Ejemplo                     |
| ------ | --------------------------------- | --------------------------- |
| 400    | Error de validación               | DTO inválido                |
| 401    | Falta autenticación               | Token ausente               |
| 403    | Sin permisos                      | Usuario sin rol requerido   |
| 404    | Recurso no encontrado             | Usuario inexistente         |
| 409    | Conflicto de negocio              | Email duplicado             |
| 422    | Datos válidos pero no procesables | Regla específica incumplida |
| 500    | Error inesperado                  | Fallo interno               |

El objetivo no es memorizar códigos, sino asociar cada tipo de error con una respuesta coherente.

---

# 10. Validación y errores

Las validaciones del tema anterior generan errores controlados.

## 10.1 Validación de formato

Ubicación:

```txt
DTO
```

Ejemplo:

```txt
email inválido
password muy corto
campo obligatorio ausente
```

Respuesta esperada:

```txt
400 Bad Request
```

---

## 10.2 Validación de negocio

Ubicación:

```txt
Service
```

Ejemplo:

```txt
email ya registrado
usuario bloqueado
stock insuficiente
```

Respuesta esperada:

```txt
409 Conflict
```

o según el caso:

```txt
422 Unprocessable Entity
```

---

## 10.3 Validación de persistencia

Ubicación:

```txt
Entity / Repository / Database
```

Ejemplo:

```txt
clave única duplicada
relación inexistente
campo no nulo
```

Respuesta esperada:

```txt
409 Conflict
```

o:

```txt
500 Internal Server Error
```

según si el error era esperado o inesperado.

---

# 11. Errores seguros para el cliente

El cliente debe recibir mensajes claros, pero no información interna del servidor.

No recomendado:

```json
{
  "message": "org.postgresql.util.PSQLException: duplicate key value violates unique constraint users_email_key"
}
```

Recomendado:

```json
{
  "statusCode": 409,
  "error": "Conflict",
  "message": "El correo ya se encuentra registrado",
  "path": "/api/v1/users"
}
```

No se debe exponer:

* stacktrace
* nombres internos de tablas
* consultas SQL
* rutas internas del servidor
* nombres de variables de entorno
* detalles de infraestructura
* tokens
* contraseñas
* claves privadas

---

# 12. Logging de errores

El logging permite registrar información útil para diagnóstico.

No todo error debe tratarse igual.

| Tipo de error      | Nivel sugerido            | Motivo                            |
| ------------------ | ------------------------- | --------------------------------- |
| Validación         | Bajo o informativo        | Es parte normal del uso de la API |
| Negocio            | Informativo o advertencia | Indica una regla incumplida       |
| Persistencia       | Error                     | Puede afectar la operación        |
| Técnico inesperado | Error crítico             | Requiere revisión                 |

El cliente recibe una respuesta controlada.

El servidor registra los detalles técnicos necesarios.

Ejemplo conceptual:

```txt
Cliente recibe:
"El correo ya se encuentra registrado"

Servidor registra:
Detalle técnico, endpoint, fecha, usuario, stacktrace si aplica
```

---


# 13. Estructura recomendada de archivos

El control de errores puede organizarse en una carpeta común porque aplica a toda la aplicación.

No pertenece a un único recurso como `users`, `products` u `orders`.

## 13.1 Estructura conceptual

```txt
src/
├── common/
│   ├── errors/
│   │   ├── GlobalErrorHandler
│   │   ├── ErrorResponse
│   │   ├── ValidationErrorResponse
│   │   └── exceptions/
│   │       ├── ResourceNotFoundException
│   │       ├── BusinessRuleException
│   │       └── ConflictException
│   │
│   └── logging/
│       └── Logger
│
└── users/
    ├── controller/
    ├── service/
    ├── repository/
    ├── dto/
    ├── model/
    ├── entity/
    └── mapper/
```

---

## 13.2 Qué va en `common/errors`

En `common/errors` se ubican componentes reutilizables para toda la API.

| Archivo                     | Responsabilidad                            |
| --------------------------- | ------------------------------------------ |
| `GlobalErrorHandler`        | Captura excepciones y construye respuestas |
| `ErrorResponse`             | Define el formato general de error         |
| `ValidationErrorResponse`   | Define errores por campo                   |
| `ResourceNotFoundException` | Representa recurso inexistente             |
| `BusinessRuleException`     | Representa reglas de negocio incumplidas   |
| `ConflictException`         | Representa conflictos del sistema          |

---

## 13.3 Excepciones específicas por módulo

Algunas excepciones pueden vivir dentro del módulo cuando pertenecen solo a ese recurso.

Ejemplo:

```txt
users/
└── exceptions/
    ├── UserNotFoundException
    └── EmailAlreadyExistsException
```

Uso recomendado:

```txt
common/errors/exceptions
  -> excepciones generales reutilizables

users/exceptions
  -> excepciones específicas del módulo users
```

---

# 15. Estructura recomendada en Spring Boot

```txt
src/main/java/ec/edu/ups/app/
├── common/
│   └── errors/
│       ├── GlobalExceptionHandler.java
│       ├── ErrorResponse.java
│       ├── ValidationErrorResponse.java
│       └── exceptions/
│           ├── ResourceNotFoundException.java
│           ├── BusinessRuleException.java
│           └── ConflictException.java
│
└── users/
    ├── controller/
    ├── service/
    ├── repository/
    ├── dto/
    ├── model/
    ├── entity/
    ├── mapper/
    └── exception/
        ├── UserNotFoundException.java
        └── EmailAlreadyExistsException.java
```

Notas:

* `GlobalExceptionHandler` centraliza las respuestas de error.
* `ErrorResponse` define el contrato de error.
* Las excepciones generales pueden ir en `common`.
* Las excepciones específicas pueden ir dentro del módulo.
* El servicio lanza excepciones.
* El handler global construye la respuesta HTTP.

---

# 16. Estructura recomendada en NestJS

```txt
src/
├── common/
│   └── errors/
│       ├── filters/
│       │   └── global-exception.filter.ts
│       ├── responses/
│       │   ├── error-response.ts
│       │   └── validation-error-response.ts
│       └── exceptions/
│           ├── resource-not-found.exception.ts
│           ├── business-rule.exception.ts
│           └── conflict.exception.ts
│
└── users/
    ├── controllers/
    ├── services/
    ├── repositories/
    ├── dto/
    ├── models/
    ├── entities/
    ├── mappers/
    └── exceptions/
        ├── user-not-found.exception.ts
        └── email-already-exists.exception.ts
```

Notas:

* El filtro global captura excepciones.
* Las respuestas de error se normalizan en un solo lugar.
* Las excepciones generales viven en `common`.
* Las excepciones específicas pueden vivir dentro del módulo.
* El servicio lanza excepciones.
* El filtro global devuelve la respuesta HTTP.

---

# 17. Cuándo crear una excepción personalizada

## 17.1 Crear excepción personalizada cuando

El error representa una situación importante del negocio o del dominio.

Ejemplos:

```txt
UserNotFoundException
EmailAlreadyExistsException
InsufficientStockException
OrderAlreadyPaidException
StudentAlreadyEnrolledException
```

Razón:

```txt
El código expresa claramente qué problema ocurrió.
```

---

## 17.2 No crear excepción personalizada cuando

El error es demasiado genérico o no aporta significado.

Ejemplo no necesario:

```txt
NameIsEmptyException
InvalidEmailFormatException
PasswordTooShortException
```

Esos casos deberían manejarse como errores de validación del DTO.

---

## 17.3 Regla práctica

```txt
Formato incorrecto -> DTO validation
Regla de negocio incumplida -> custom exception
Recurso inexistente -> not found exception
Conflicto de datos -> conflict exception
Fallo inesperado -> error técnico controlado
```

---

# 18. Ejemplo conceptual con users

## 18.1 Caso: usuario no encontrado

Petición:

```txt
GET /api/v1/users/10
```

Flujo:

```txt
UserController
  ↓
UserService
  ↓
buscar usuario por id
  ↓
no existe
  ↓
lanza UserNotFoundException
  ↓
Global Error Handler
  ↓
404 Not Found
```

Respuesta:

```json
{
  "timestamp": "2026-06-23T10:30:00Z",
  "statusCode": 404,
  "error": "Not Found",
  "message": "Usuario no encontrado",
  "path": "/api/v1/users/10"
}
```

---

## 18.2 Caso: email duplicado

Petición:

```txt
POST /api/v1/users
```

Entrada:

```json
{
  "name": "Ana",
  "email": "ana@example.com",
  "password": "12345678"
}
```

Flujo:

```txt
CreateUserDto
  ↓
UserController
  ↓
UserService
  ↓
verificar si email existe
  ↓
email ya registrado
  ↓
lanza EmailAlreadyExistsException
  ↓
Global Error Handler
  ↓
409 Conflict
```

Respuesta:

```json
{
  "timestamp": "2026-06-23T10:30:00Z",
  "statusCode": 409,
  "error": "Conflict",
  "message": "El correo ya se encuentra registrado",
  "path": "/api/v1/users"
}
```

---

## 18.3 Caso: datos inválidos

Petición:

```txt
POST /api/v1/users
```

Entrada:

```json
{
  "name": "",
  "email": "correo-invalido",
  "password": "123"
}
```

Flujo:

```txt
CreateUserDto
  ↓
validación de formato
  ↓
error de validación
  ↓
Global Error Handler
  ↓
400 Bad Request
```

Respuesta:

```json
{
  "timestamp": "2026-06-23T10:30:00Z",
  "statusCode": 400,
  "error": "Bad Request",
  "message": "Error de validación",
  "path": "/api/v1/users",
  "errors": [
    {
      "field": "name",
      "message": "El nombre es obligatorio"
    },
    {
      "field": "email",
      "message": "El correo debe tener un formato válido"
    },
    {
      "field": "password",
      "message": "La contraseña debe tener mínimo 8 caracteres"
    }
  ]
}
```

---

# 19. Errores comunes

## 19.1 Usar try/catch en todos los controladores

Problema:

```txt
Cada controlador maneja errores manualmente.
```

Consecuencia:

```txt
Código duplicado y respuestas inconsistentes.
```

Corrección:

```txt
Usar un manejador global de excepciones.
```

---

## 19.2 Devolver errores técnicos al cliente

Problema:

```txt
Se devuelve SQL, stacktrace o nombres internos de clases.
```

Consecuencia:

```txt
Se expone información sensible del servidor.
```

Corrección:

```txt
Mostrar mensaje controlado al cliente y registrar detalle técnico en logs.
```

---

## 19.3 Lanzar excepciones genéricas para todo

Problema:

```txt
throw Exception
throw RuntimeException
```

Consecuencia:

```txt
No se entiende qué regla falló.
```

Corrección:

```txt
Usar excepciones con significado.
```

---

## 19.4 Mezclar validación de DTO con validación de negocio

Problema:

```txt
El DTO verifica si el correo ya existe.
```

Consecuencia:

```txt
El DTO depende de la base de datos o del servicio.
```

Corrección:

```txt
DTO valida formato.
Service valida reglas de negocio.
```

---

## 19.5 Construir respuestas de error en el servicio

Problema:

```txt
El servicio devuelve objetos HTTP de error.
```

Consecuencia:

```txt
La lógica de negocio queda acoplada al transporte HTTP.
```

Corrección:

```txt
El servicio lanza excepciones.
El handler global construye la respuesta HTTP.
```

---

# 20 Aplicación directa en los siguientes módulos

Estos conceptos se aplicarán directamente en:

* [`spring-boot/07_control_errores.md`](../spring-boot/07_control_errores.md)
* [`nest/07_control_errores.md`](../nest/07_control_errores.md)
