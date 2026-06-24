# Programación y Plataformas Web

# Frameworks Backend: NestJS – Control Global de Errores y Excepciones

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nestjs/nestjs-original.svg" width="95">
</div>

---

# Práctica 7 (NestJS): Manejo Global de Errores y Excepciones

### Autores

**Pablo Torres**

[ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: PabloT18

---

# 1. Introducción

En las prácticas anteriores se implementó:

* controladores
* servicios
* DTOs con validación
* modelos de dominio
* entidades persistentes
* mappers
* repositorios TypeORM
* conexión a PostgreSQL
* eliminado lógico mediante `deleted`

Hasta este punto, la API ya puede recibir datos, validarlos, procesarlos y guardarlos en base de datos.

Sin embargo, todavía existe un problema importante: los errores no se manejan con un formato propio y centralizado.

NestJS ya maneja errores automáticamente, pero sus respuestas pueden variar dependiendo del tipo de excepción.

Actualmente pueden existir errores como:

```ts
throw new NotFoundException('User not found');
```

o respuestas generadas directamente por NestJS como:

```json
{
  "message": "User not found",
  "error": "Not Found",
  "statusCode": 404
}
```

Este enfoque funciona, pero no define un contrato propio de error para toda la aplicación.

Un backend no debe manejar errores de forma distinta en cada controlador o servicio.

En esta práctica se implementa un sistema global de manejo de errores usando:

* excepciones propias de la aplicación
* excepciones de dominio
* una interfaz única de error
* un filtro global de excepciones
* `ExceptionFilter`
* `ValidationPipe`

El objetivo es que todos los errores de la API tengan un formato uniforme y que los servicios solo expresen el error, sin construir respuestas HTTP manualmente.

---

# 2. Problema actual

Antes de esta práctica, cuando un usuario no existía, el servicio podía tener algo como:

```ts
async findOne(id: number): Promise<UserResponseDto> {
  const entity = await this.userRepository.findOne({
    where: {
      id,
      deleted: false,
    },
  });

  if (!entity) {
    throw new NotFoundException('User not found');
  }

  const model = UserMapper.toModelFromEntity(entity);

  return UserMapper.toResponse(model);
}
```

Esto genera una excepción de NestJS.

El problema es que la respuesta no necesariamente tiene el mismo formato que se desea para todos los errores del sistema.

El cliente podría recibir una respuesta como:

```json
{
  "message": "User not found",
  "error": "Not Found",
  "statusCode": 404
}
```

Aunque el código HTTP es correcto, el formato no coincide con el contrato usado en el backend.

Se busca que todos los errores tengan una estructura como:

```json
{
  "timestamp": "2025-12-26T15:07:20.967Z",
  "status": 404,
  "error": "Not Found",
  "message": "User not found",
  "path": "/api/users/999"
}
```

---

# 3. Flujo después de aplicar manejo global de errores

El flujo será:

```txt
Cliente
  ↓
UsersController
  ↓
UsersService
  ↓
lanza NotFoundException / ConflictException / BadRequestException
  ↓
AllExceptionsFilter
  ↓
ErrorResponse
  ↓
Cliente
```

El servicio ya no construye respuestas de error.

El controlador ya no usa `try/catch`.

El filtro global se encarga de convertir excepciones en respuestas HTTP.

---

# 4. Estructura del paquete de excepciones

Se creará una estructura global para errores dentro de:

```txt
src/core/exceptions/
```

Estructura recomendada:

```txt
core/
└── exceptions/
    ├── base/
    │   └── application.exception.ts
    │
    ├── domain/
    │   ├── not-found.exception.ts
    │   ├── conflict.exception.ts
    │   └── bad-request.exception.ts
    │
    ├── filters/
    │   └── all-exceptions.filter.ts
    │
    └── interfaces/
        └── error-response.interface.ts
```

Esta estructura permite separar:

```txt
base       → excepción raíz de la aplicación
domain     → errores del negocio
filters    → conversión global de excepciones a HTTP
interfaces → formato único de respuesta de error
```

---

# 5. Excepción base de la aplicación

Archivo:

```txt
core/exceptions/base/application.exception.ts
```

Código:

```ts
/*
 * Excepción base de la aplicación.
 *
 * Todas las excepciones propias del sistema deben extender de esta clase.
 * Permite asociar cada error con un HttpStatus específico.
 */
export abstract class ApplicationException extends HttpException {
  constructor(message: string, status: HttpStatus) {
    super(message, status);
  }
}
```

---

## 5.1. Explicación

`ApplicationException` es la clase padre de las excepciones propias del sistema.

Permite que cada error tenga asociado un estado HTTP.

Ejemplo:

```txt
NotFoundException   → 404 Not Found
ConflictException   → 409 Conflict
BadRequestException → 400 Bad Request
```

Esto evita lanzar excepciones genéricas o depender directamente de las excepciones nativas en cada servicio.

---

# 6. Excepciones de dominio

Las excepciones de dominio representan errores propios de la lógica de negocio.

No construyen respuestas HTTP.

Solo expresan qué error ocurrió.

---

## 6.1. NotFoundException

Se utiliza cuando un recurso no existe o está eliminado lógicamente.

Archivo:

```txt
core/exceptions/domain/not-found.exception.ts
```

Código:

```ts
/*
 * Excepción usada cuando un recurso no existe
 * o no está disponible para la operación solicitada.
 */
export class NotFoundException extends ApplicationException {
  constructor(message: string) {
    super(message, HttpStatus.NOT_FOUND);
  }
}
```

### Cuándo usarla

Usar `NotFoundException` cuando:

* se busca un usuario inexistente
* se intenta actualizar un producto inexistente
* se intenta eliminar un registro ya eliminado
* el recurso existe en base de datos pero tiene `deleted = true`

Ejemplo:

```ts
throw new NotFoundException('User not found');
```

---

## 6.2. ConflictException

Se utiliza cuando existe un conflicto con el estado actual del sistema.

Archivo:

```txt
core/exceptions/domain/conflict.exception.ts
```

Código:

```ts
/*
 * Excepción usada cuando existe un conflicto
 * con el estado actual del recurso.
 */
export class ConflictException extends ApplicationException {
  constructor(message: string) {
    super(message, HttpStatus.CONFLICT);
  }
}
```

### Cuándo usarla

Usar `ConflictException` cuando:

* se intenta crear un usuario con email duplicado
* se intenta crear un producto con nombre duplicado
* se viola una regla de unicidad
* existe un conflicto lógico con datos ya registrados

Ejemplo:

```ts
throw new ConflictException('Email already registered');
```

---

## 6.3. BadRequestException

Se utiliza cuando la solicitud tiene datos que no pueden procesarse por reglas de negocio.

Archivo:

```txt
core/exceptions/domain/bad-request.exception.ts
```

Código:

```ts
/*
 * Excepción usada cuando la solicitud es inválida
 * según reglas de negocio.
 */
export class BadRequestException extends ApplicationException {
  constructor(message: string) {
    super(message, HttpStatus.BAD_REQUEST);
  }
}
```

### Cuándo usarla

Usar `BadRequestException` cuando:

* los datos son válidos sintácticamente, pero inválidos para el negocio
* se intenta realizar una operación no permitida
* se incumple una regla que no puede validarse solo con decoradores

Ejemplo:

```ts
throw new BadRequestException('Stock insufficient');
```

---

# 7. Contrato único de respuesta de error

Archivo:

```txt
core/exceptions/interfaces/error-response.interface.ts
```

Código:

```ts
/*
 * Interfaz estándar para devolver errores al cliente.
 *
 * Define un formato único para errores de dominio,
 * errores de validación y errores inesperados.
 */
export interface ErrorResponse {
  timestamp: string;
  status: number;
  error: string;
  message: string;
  path: string;
  details?: Record<string, string>;
}
```

---

## 7.1. Explicación de campos

| Campo       | Función                       |
| ----------- | ----------------------------- |
| `timestamp` | Fecha y hora del error        |
| `status`    | Código HTTP                   |
| `error`     | Nombre del error HTTP         |
| `message`   | Mensaje general del error     |
| `path`      | Ruta donde ocurrió el error   |
| `details`   | Errores específicos por campo |

---

## 7.2. Uso de `details`

El campo `details` se usa principalmente para errores de validación.

Ejemplo:

```json
{
  "timestamp": "2025-12-26T15:12:42.301Z",
  "status": 400,
  "error": "Bad Request",
  "message": "Datos de entrada inválidos",
  "path": "/api/users",
  "details": {
    "name": "El nombre es obligatorio",
    "email": "Debe ingresar un email válido"
  }
}
```

Cuando no existen detalles, el campo no aparece porque es opcional:

```ts
details?: Record<string, string>;
```

---

# 8. Filtro global de excepciones

Archivo:

```txt
core/exceptions/filters/all-exceptions.filter.ts
```

Código:

```ts
/*
 * Filtro global de excepciones.
 *
 * Captura las excepciones lanzadas desde cualquier controlador o servicio
 * y las convierte en una respuesta HTTP uniforme.
 */
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost): void {
    const ctx = host.switchToHttp();

    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let message = 'Error interno del servidor';
    let error = 'Internal Server Error';
    let details: Record<string, string> | undefined;

    if (exception instanceof HttpException) {
      status = exception.getStatus();

      const exceptionResponse = exception.getResponse();

      if (
        typeof exceptionResponse === 'object' &&
        exceptionResponse !== null &&
        'message' in exceptionResponse
      ) {
        const body = exceptionResponse as {
          message?: string | string[];
          error?: string;
          statusCode?: number;
        };

        if (Array.isArray(body.message)) {
          message = 'Datos de entrada inválidos';
          details = this.extractValidationErrors(body.message);
        } else {
          message = body.message ?? exception.message;
        }

        error = body.error ?? this.getErrorName(status);
      } else {
        message = exception.message;
        error = this.getErrorName(status);
      }
    }

    const errorResponse: ErrorResponse = {
      timestamp: new Date().toISOString(),
      status,
      error,
      message,
      path: request.url,
      ...(details && { details }),
    };

    response.status(status).json(errorResponse);
  }

  /*
   * Convierte los mensajes de validación en un objeto details.
   *
   * Cada campo queda asociado con su mensaje de error.
   */
  private extractValidationErrors(messages: string[]): Record<string, string> {
    const errors: Record<string, string> = {};

    messages.forEach((message) => {
      const field = this.extractFieldFromMessage(message);
      errors[field] = message;
    });

    return errors;
  }

  /*
   * Extrae un nombre de campo aproximado desde el mensaje.
   *
   * En esta práctica se usa el primer texto antes del espacio.
   * Luego se puede mejorar con exceptionFactory en ValidationPipe.
   */
  private extractFieldFromMessage(message: string): string {
    return message.split(' ')[0];
  }

  /*
   * Obtiene el nombre estándar del error HTTP.
   */
  private getErrorName(status: number): string {
    return HttpStatus[status] ?? 'Internal Server Error';
  }
}
```

---

# 9. Registrar el filtro global

El filtro debe registrarse en `main.ts`.

Archivo:

```txt
src/main.ts
```

Código:

```ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.setGlobalPrefix('api');

  app.useGlobalFilters(new AllExceptionsFilter());

  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    }),
  );

  await app.listen(3000);
}
bootstrap();
```

---

## 9.1. Explicación

`app.useGlobalFilters()` registra el filtro para toda la aplicación.

A partir de ese momento, cualquier excepción lanzada desde controladores o servicios será procesada por `AllExceptionsFilter`.

`ValidationPipe` sigue validando los DTOs.

Si ocurre un error de validación, NestJS lanza una excepción HTTP de tipo `400 Bad Request`.

El filtro global la captura y la transforma al formato estándar.

---

# 10. Reemplazo de errores en UsersService

En la práctica anterior se podía usar:

```ts
throw new NotFoundException('User not found');
```

pero importando desde:

```ts
@nestjs/common
```

Ahora se usará la excepción propia:

```ts
import { NotFoundException } from '../../core/exceptions/domain/not-found.exception';
import { ConflictException } from '../../core/exceptions/domain/conflict.exception';
import { BadRequestException } from '../../core/exceptions/domain/bad-request.exception';
```

---

## 10.1. findOne con NotFoundException

Antes:

```ts
async findOne(id: number): Promise<UserResponseDto> {
  const entity = await this.userRepository.findOne({
    where: {
      id,
      deleted: false,
    },
  });

  if (!entity) {
    throw new NotFoundException('User not found');
  }

  const model = UserMapper.toModelFromEntity(entity);

  return UserMapper.toResponse(model);
}
```

Ahora se mantiene la lógica, pero usando la excepción propia:

```ts
/*
 * Busca un usuario activo por id.
 *
 * Si no existe o está eliminado, lanza NotFoundException.
 */
async findOne(id: number): Promise<UserResponseDto> {
  const entity = await this.userRepository.findOne({
    where: {
      id,
      deleted: false,
    },
  });

  if (!entity) {
    throw new NotFoundException('User not found');
  }

  const model = UserMapper.toModelFromEntity(entity);

  return UserMapper.toResponse(model);
}
```

---

## 10.2. create con ConflictException

Antes se podía tener:

```ts
if (exists) {
  throw new BadRequestException('Email already registered');
}
```

Ahora:

```ts
/*
 * Crea un nuevo usuario.
 *
 * Valida que el email no esté registrado.
 * Si ya existe, lanza ConflictException.
 */
async create(dto: CreateUserDto): Promise<UserResponseDto> {
  const exists = await this.userRepository.exist({
    where: {
      email: dto.email,
      deleted: false,
    },
  });

  if (exists) {
    throw new ConflictException('Email already registered');
  }

  const model = UserMapper.toModelFromDto(dto);

  const entity = UserMapper.toEntityFromModel(model);

  const savedEntity = await this.userRepository.save(entity);

  const savedModel = UserMapper.toModelFromEntity(savedEntity);

  return UserMapper.toResponse(savedModel);
}
```

---

## 10.3. update con NotFoundException

```ts
/*
 * Actualiza completamente un usuario activo.
 *
 * Si no existe o está eliminado, lanza NotFoundException.
 */
async update(id: number, dto: UpdateUserDto): Promise<UserResponseDto> {
  const entity = await this.userRepository.findOne({
    where: {
      id,
      deleted: false,
    },
  });

  if (!entity) {
    throw new NotFoundException('User not found');
  }

  entity.name = dto.name;
  entity.email = dto.email;

  const savedEntity = await this.userRepository.save(entity);

  const model = UserMapper.toModelFromEntity(savedEntity);

  return UserMapper.toResponse(model);
}
```

---

## 10.4. partialUpdate con NotFoundException

```ts
/*
 * Actualiza parcialmente un usuario activo.
 *
 * Si no existe o está eliminado, lanza NotFoundException.
 */
async partialUpdate(
  id: number,
  dto: PartialUpdateUserDto,
): Promise<UserResponseDto> {
  const entity = await this.userRepository.findOne({
    where: {
      id,
      deleted: false,
    },
  });

  if (!entity) {
    throw new NotFoundException('User not found');
  }

  if (dto.name !== undefined) {
    entity.name = dto.name;
  }

  if (dto.email !== undefined) {
    entity.email = dto.email;
  }

  const savedEntity = await this.userRepository.save(entity);

  const model = UserMapper.toModelFromEntity(savedEntity);

  return UserMapper.toResponse(model);
}
```

---

## 10.5. delete con NotFoundException

```ts
/*
 * Elimina lógicamente un usuario por id.
 *
 * Si no existe o ya está eliminado, lanza NotFoundException.
 */
async delete(id: number): Promise<void> {
  const entity = await this.userRepository.findOne({
    where: {
      id,
      deleted: false,
    },
  });

  if (!entity) {
    throw new NotFoundException('User not found');
  }

  entity.deleted = true;

  await this.userRepository.save(entity);
}
```

---

# 11. Validación automática de DTOs

En la práctica anterior ya se configuró `ValidationPipe`.

Ejemplo:

```ts
@Post()
create(@Body() dto: CreateUserDto): Promise<UserResponseDto> {
  return this.service.create(dto);
}
```

Cuando se envía una petición inválida:

```json
{
  "name": "",
  "email": "correo-invalido",
  "password": "123"
}
```

NestJS lanza automáticamente una excepción HTTP de validación.

Esta excepción es capturada por:

```ts
AllExceptionsFilter
```

y devuelve una respuesta uniforme.

---

## 11.1. Respuesta de validación esperada

```json
{
  "timestamp": "2025-12-26T15:12:42.301Z",
  "status": 400,
  "error": "Bad Request",
  "message": "Datos de entrada inválidos",
  "path": "/api/users",
  "details": {
    "El": "El nombre es obligatorio",
    "Debe": "Debe ingresar un email válido",
    "La": "La contraseña debe tener al menos 8 caracteres"
  }
}
```

En esta práctica, el campo usado como clave en `details` sale del primer texto del mensaje.

Más adelante se puede mejorar este comportamiento usando `exceptionFactory` en `ValidationPipe`.

---

# 12. Flujo completo en ejecución

## Escenario 1: Error de validación

Request:

```http
POST /api/users
Content-Type: application/json

{
  "name": "",
  "email": "correo-invalido",
  "password": "123"
}
```

Flujo:

```txt
Request HTTP con datos inválidos
 ↓
Controller
 ↓
ValidationPipe
 ↓
BadRequestException de NestJS
 ↓
AllExceptionsFilter
 ↓
Extrae errores de campos
 ↓
ErrorResponse con details
 ↓
Response HTTP 400
```

---

## Escenario 2: Recurso no encontrado

Request:

```http
GET /api/users/999
```

Flujo:

```txt
Request HTTP
 ↓
Controller
 ↓
Service.findOne(999)
 ↓
Repository.findOne({ id: 999, deleted: false })
 ↓
NotFoundException("User not found")
 ↓
AllExceptionsFilter
 ↓
ErrorResponse sin details
 ↓
Response HTTP 404
```

Respuesta:

```json
{
  "timestamp": "2025-12-26T15:07:20.967Z",
  "status": 404,
  "error": "Not Found",
  "message": "User not found",
  "path": "/api/users/999"
}
```

---

## Escenario 3: Conflicto por email duplicado

Request:

```http
POST /api/users
Content-Type: application/json

{
  "name": "Juan Pérez",
  "email": "juan@ups.edu.ec",
  "password": "12345678"
}
```

Si el email ya existe, el servicio lanza:

```ts
throw new ConflictException('Email already registered');
```

Respuesta:

```json
{
  "timestamp": "2025-12-26T15:07:20.967Z",
  "status": 409,
  "error": "Conflict",
  "message": "Email already registered",
  "path": "/api/users"
}
```

---

# 13. Comparación de escenarios

| Aspecto             | Validación de DTOs            | Excepción de dominio                                                    |
| ------------------- | ----------------------------- | ----------------------------------------------------------------------- |
| Cuándo ocurre       | Antes del servicio            | Dentro del servicio                                                     |
| Excepción           | BadRequestException de NestJS | `NotFoundException`, `ConflictException`, `BadRequestException` propias |
| Handler             | `AllExceptionsFilter`         | `AllExceptionsFilter`                                                   |
| Código HTTP         | 400                           | 400, 404, 409                                                           |
| Campo `details`     | Sí                            | No                                                                      |
| Servicio se ejecuta | No                            | Sí                                                                      |

---

# 14. Pruebas sugeridas en Postman / Bruno

## Usuario inexistente

Método:

```txt
GET
```

Ruta:

```txt
/api/users/999
```

Resultado esperado:

```txt
404 Not Found
```

---

## Usuario con datos inválidos

Método:

```txt
POST
```

Ruta:

```txt
/api/users
```

Body:

```json
{
  "name": "",
  "email": "correo-invalido",
  "password": "123"
}
```

Resultado esperado:

```txt
400 Bad Request
```

---

## Usuario con email repetido

Método:

```txt
POST
```

Ruta:

```txt
/api/users
```

Body:

```json
{
  "name": "Juan Repetido",
  "email": "juan@ups.edu.ec",
  "password": "12345678"
}
```

Resultado esperado:

```txt
409 Conflict
```

---

## Eliminar usuario inexistente

Método:

```txt
DELETE
```

Ruta:

```txt
/api/users/999
```

Resultado esperado:

```txt
404 Not Found
```

---

# 15. Buenas prácticas reforzadas

Con esta práctica se refuerza:

* un solo formato de error
* sin `try/catch` en controladores
* servicios sin construir respuestas HTTP
* excepciones semánticas
* separación entre lógica de negocio y respuesta HTTP
* validación estructurada
* errores útiles para frontend
* no exposición de stack trace al cliente

---

# 16. Actividad práctica

Se debe implementar el sistema global de errores en el módulo:

```txt
products/
```

---

## 16.1. Reemplazar errores genéricos

Cambiar en `ProductsService`:

```ts
throw new Error(...)
```

o excepciones nativas de NestJS importadas desde:

```ts
@nestjs/common
```

por:

```ts
throw new NotFoundException(...)
throw new ConflictException(...)
throw new BadRequestException(...)
```

desde:

```txt
core/exceptions/domain/
```

---

## 16.2. Validar producto inexistente

En métodos como:

```txt
findOne()
update()
partialUpdate()
delete()
```

si el producto no existe o tiene `deleted = true`, lanzar:

```ts
throw new NotFoundException('Product not found');
```

---

## 16.3. Validar conflicto lógico

Agregar una regla de negocio:

```txt
No se puede crear un producto con nombre duplicado.
```

Para eso, el servicio puede usar:

```ts
this.productRepository.findOne({
  where: {
    name: dto.name,
    deleted: false,
  },
});
```

Si ya existe un producto activo con el mismo nombre:

```ts
throw new ConflictException('Product name already registered');
```

---

## 16.4. Validar error de datos

Enviar datos inválidos desde Bruno o Postman:

```json
{
  "name": "",
  "price": -5,
  "stock": -1
}
```

Debe responder con:

```txt
400 Bad Request
```

y el formato estándar de `ErrorResponse`.

---

## 16.5. Verificar eliminado lógico

Después de eliminar un producto:

```txt
DELETE /api/products/{id}
```

Probar nuevamente:

```txt
GET /api/products/{id}
```

Debe responder:

```txt
404 Not Found
```

---

# 17. Resultados y evidencias

En la nueva entrada del README, se debe agregar:

## Captura de error por producto inexistente

Ejemplo:

```txt
GET /api/products/999
```

Debe evidenciar respuesta:

```txt
404 Not Found
```

---

## Captura de error por producto duplicado

Ejemplo:

```txt
POST /api/products
```

con un nombre ya registrado.

Debe evidenciar respuesta:

```txt
409 Conflict
```

---

## Captura de error por validación de DTO

Ejemplo:

```json
{
  "name": "",
  "price": -5,
  "stock": -1
}
```

Debe evidenciar respuesta:

```txt
400 Bad Request
```

con campo `details`.

---

## Explicación breve

El estudiante debe explicar:

```txt
¿Cómo el AllExceptionsFilter centraliza los errores de validación, negocio y errores inesperados?
```
