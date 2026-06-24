# Programación y Plataformas Web

# Frameworks Backend: NestJS – DTOs, Validación y Reglas de Entrada

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nestjs/nestjs-original.svg" width="110">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="110">
</div>

---

# Práctica 6 (NestJS): Validación de DTOs y Control de Datos de Entrada

### Autores

**Pablo Torres**

[ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: PabloT18

---

# 1. Introducción

En las prácticas anteriores se implementó:

* controladores
* servicios
* modelos
* entidades persistentes
* mappers
* repositorios TypeORM
* conexión a PostgreSQL

Hasta este punto, la API ya puede recibir datos, procesarlos y guardarlos en base de datos.

Sin embargo, todavía falta un componente esencial: validar correctamente los datos que entran al sistema.

Sin validación, la API podría recibir:

* nombres vacíos
* correos inválidos
* contraseñas débiles
* precios negativos
* stock negativo
* campos obligatorios incompletos

En esta práctica se introduce la validación de DTOs usando `class-validator` y `class-transformer`.

El objetivo es validar los datos antes de que lleguen al servicio y antes de que se guarden en PostgreSQL.

En esta práctica se trabajará con:

* DTOs con decoradores de validación
* `ValidationPipe` en NestJS
* reglas básicas de entrada
* validaciones en servicios
* validaciones reforzadas por base de datos

Todavía no se implementa:

* manejo centralizado de errores personalizado
* filtros globales de excepciones
* respuestas de error propias del sistema

Eso se trabajará en una práctica posterior.

---

# 2. Flujo después de aplicar validación

Ahora el flujo será:

```txt
Cliente
  ↓
UsersController
  ↓
ValidationPipe
  ↓
CreateUserDto / UpdateUserDto / PartialUpdateUserDto
  ↓
UsersService
  ↓
Repository<UserEntity>
  ↓
PostgreSQL
  ↓
UserEntity
  ↓
UserMapper
  ↓
UserModel
  ↓
UserResponseDto
  ↓
Cliente
```

La validación ocurre antes de ejecutar la lógica del servicio.

Si los datos no cumplen las reglas del DTO, NestJS detiene la petición y devuelve un error `400 Bad Request`.

---

# 3. Instalación y configuración de dependencias

NestJS utiliza `class-validator` y `class-transformer` para validar DTOs.

---

## 3.1. Dependencias necesarias

Ejecutar en la raíz del proyecto:

```bash
pnpm add class-validator class-transformer
```

Estas dependencias permiten usar decoradores como:

```ts
@IsNotEmpty()
@IsEmail()
@MinLength()
@MaxLength()
@IsOptional()
@IsNumber()
@Min()
```

---

# 4. Diseño de DTOs con validación

Los DTOs se validan antes de llegar al servicio.

Esto evita que datos incorrectos entren a la lógica de negocio.

---

## 4.1. CreateUserDto

Archivo:

```txt
users/dtos/create-user.dto.ts
```

Código:

```ts
/*
 * DTO utilizado para recibir los datos necesarios
 * para crear un nuevo usuario desde una petición HTTP.
 *
 * No incluye id porque el backend lo genera.
 * No incluye createdAt porque el backend asigna la fecha de creación.
 */
export class CreateUserDto {

  @IsNotEmpty({ message: 'El nombre es obligatorio' })
  @MinLength(3, { message: 'El nombre debe tener al menos 3 caracteres' })
  @MaxLength(150, { message: 'El nombre no debe superar los 150 caracteres' })
  name: string;

  @IsNotEmpty({ message: 'El email es obligatorio' })
  @IsEmail({}, { message: 'Debe ingresar un email válido' })
  @MaxLength(150, { message: 'El email no debe superar los 150 caracteres' })
  email: string;

  @IsNotEmpty({ message: 'La contraseña es obligatoria' })
  @MinLength(8, { message: 'La contraseña debe tener al menos 8 caracteres' })
  password: string;
}
```

---

## 4.2. UpdateUserDto

Archivo:

```txt
users/dtos/update-user.dto.ts
```

Código:

```ts
/*
 * DTO utilizado para recibir los datos necesarios
 * para actualizar completamente un usuario existente.
 *
 * No incluye id porque el id llega por la URL.
 * No incluye createdAt porque la fecha de creación no debe modificarse.
 */
export class UpdateUserDto {

  @IsNotEmpty({ message: 'El nombre es obligatorio' })
  @MinLength(3, { message: 'El nombre debe tener al menos 3 caracteres' })
  @MaxLength(150, { message: 'El nombre no debe superar los 150 caracteres' })
  name: string;

  @IsNotEmpty({ message: 'El email es obligatorio' })
  @IsEmail({}, { message: 'Debe ingresar un email válido' })
  @MaxLength(150, { message: 'El email no debe superar los 150 caracteres' })
  email: string;
}
```

---

## 4.3. PartialUpdateUserDto

Archivo:

```txt
users/dtos/partial-update-user.dto.ts
```

Código:

```ts
/*
 * DTO utilizado para recibir los datos que se desean
 * actualizar parcialmente en un usuario existente.
 *
 * Los campos pueden venir indefinidos cuando no se desean actualizar.
 * Solo se validan los campos enviados.
 */
export class PartialUpdateUserDto {

  @IsOptional()
  @MinLength(3, { message: 'El nombre debe tener al menos 3 caracteres' })
  @MaxLength(150, { message: 'El nombre no debe superar los 150 caracteres' })
  name?: string;

  @IsOptional()
  @IsEmail({}, { message: 'Debe ingresar un email válido' })
  @MaxLength(150, { message: 'El email no debe superar los 150 caracteres' })
  email?: string;
}
```

---

# 5. Activar validación en NestJS

Para que NestJS valide los DTOs, se debe configurar `ValidationPipe`.

Archivo:

```txt
src/main.ts
```

Código:

```ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.setGlobalPrefix('api');

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

## 5.1. ¿Qué hace `ValidationPipe`?

`ValidationPipe` indica que los objetos recibidos deben evaluarse con los decoradores de `class-validator`.

Ejemplo:

```ts
@Post()
create(@Body() dto: CreateUserDto) {
  return this.service.create(dto);
}
```

Si el cliente envía un nombre vacío, un email inválido o una contraseña corta, NestJS detiene la ejecución antes de entrar al servicio.

---

## 5.2. Propiedades usadas en `ValidationPipe`

| Propiedad                    | Función                                                      |
| ---------------------------- | ------------------------------------------------------------ |
| `whitelist: true`            | Elimina propiedades que no estén definidas en el DTO         |
| `forbidNonWhitelisted: true` | Devuelve error si el cliente envía campos extra              |
| `transform: true`            | Permite transformar valores recibidos según el tipo esperado |

---

# 6. Ejemplo de petición inválida

Endpoint:

```txt
POST /api/users
```

Body inválido:

```json
{
  "name": "",
  "email": "correo-invalido",
  "password": "123"
}
```

El DTO tiene estas reglas:

```ts
@IsNotEmpty()
@IsEmail()
@MinLength()
@MaxLength()
```

Por tanto, la petición no debe llegar al servicio.

---

## 6.1. Respuesta generada por NestJS

En esta práctica todavía no se implementa un filtro global personalizado.

Por eso NestJS puede devolver una respuesta parecida a:

```json
{
  "message": [
    "El nombre es obligatorio",
    "Debe ingresar un email válido",
    "La contraseña debe tener al menos 8 caracteres"
  ],
  "error": "Bad Request",
  "statusCode": 400
}
```

El manejo personalizado de errores se trabajará después.

> Respuesta HTTP: `400 Bad Request`.

---

# 7. Validación en el servicio

Los DTOs validan reglas de formato.

El servicio puede validar reglas de negocio.

Ejemplos de reglas de negocio:

* no registrar dos usuarios con el mismo email
* no actualizar un usuario eliminado
* no buscar registros eliminados lógicamente

---

## 7.1. Validar email duplicado

Como el repositorio permite consultar por condiciones, se puede validar antes de guardar.

Archivo:

```txt
users/services/users.service.ts
```

Método `create` actualizado:

```ts
/*
 * Crea un nuevo usuario.
 *
 * Valida que el email no esté registrado.
 * Convierte DTO a Model.
 * Convierte Model a Entity.
 * Guarda Entity en PostgreSQL.
 * Convierte Entity guardada a Model.
 * Devuelve Response DTO.
 */
async create(dto: CreateUserDto): Promise<UserResponseDto> {

  const exists = await this.userRepository.exist({
    where: {
      email: dto.email,
      deleted: false,
    },
  });

  if (exists) {
    throw new BadRequestException('Email already registered');
  }

  // Resto del método...
}
```

---

# 8. Validación en la entidad y base de datos

La validación del DTO protege la entrada desde la API.

La base de datos también refuerza reglas mediante la entidad TypeORM.

Ejemplo:

```ts
@Entity('users')
export class UserEntity extends BaseEntity {

  @Column({ type: 'varchar', length: 150, nullable: false })
  name: string;

  @Column({ type: 'varchar', length: 150, unique: true, nullable: false })
  email: string;

  @Column({ type: 'varchar', nullable: false })
  passwordHash: string;
}
```

Estas restricciones generan reglas en PostgreSQL:

```txt
name no puede ser null
email no puede ser null
email debe ser único
passwordHash no puede ser null
```

---

# 9. Métodos de conversión con Mapper

Hasta este punto, la conversión entre capas se mantiene con `UserMapper`.

El mapper se encarga de convertir:

```txt
CreateUserDto → UserModel
UserModel → UserEntity
UserEntity → UserModel
UserModel → UserResponseDto
```

Ejemplo:

```ts
export class UserMapper {

  static toModelFromDto(dto: CreateUserDto): UserModel {
    const model = new UserModel();

    model.name = dto.name;
    model.email = dto.email;
    model.password = dto.password;
    model.passwordHash = 'HASH_' + dto.password;

    return model;
  }

  static toModelFromEntity(entity: UserEntity): UserModel {
    const model = new UserModel();

    model.id = entity.id;
    model.name = entity.name;
    model.email = entity.email;
    model.passwordHash = entity.passwordHash;
    model.createdAt = entity.createdAt;
    model.updatedAt = entity.updatedAt;
    model.deleted = entity.deleted;

    return model;
  }

  static toEntityFromModel(model: UserModel): UserEntity {
    const entity = new UserEntity();

    if (model.id !== undefined && model.id !== null) {
      entity.id = model.id;
    }

    entity.name = model.name;
    entity.email = model.email;
    entity.passwordHash = model.passwordHash;

    return entity;
  }

  static toResponse(model: UserModel): UserResponseDto {
    const response = new UserResponseDto();

    response.id = model.id;
    response.name = model.name;
    response.email = model.email;

    return response;
  }
}
```

> En esta práctica se mantiene el uso de `UserMapper`. Aunque estos métodos crean objetos nuevos, su responsabilidad principal es transformar datos entre capas, no aplicar Builder ni Factory Method.

---

# 10. Pruebas sugeridas en Postman / Bruno

## Crear usuario inválido

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

## Crear usuario válido

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
  "name": "Juan Pérez",
  "email": "juan@ups.edu.ec",
  "password": "12345678"
}
```

Resultado esperado:

```txt
Usuario creado correctamente
```

---

## Crear usuario con email repetido

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
Error por email ya registrado
```

---

## Actualizar usuario con email inválido

Método:

```txt
PUT
```

Ruta:

```txt
/api/users/1
```

Body:

```json
{
  "name": "Juan Actualizado",
  "email": "correo-invalido"
}
```

Resultado esperado:

```txt
400 Bad Request
```

---

## Actualizar parcialmente con nombre inválido

Método:

```txt
PATCH
```

Ruta:

```txt
/api/users/1
```

Body:

```json
{
  "name": "A"
}
```

Resultado esperado:

```txt
400 Bad Request
```

---

# 11. Actividad práctica

Se debe implementar validación en el módulo:

```txt
products/
```

---

## 11.1. Actualizar DTOs con validación

Aplicar validaciones a:

```txt
CreateProductDto
UpdateProductDto
PartialUpdateProductDto
```

Reglas mínimas:

| Campo   | Regla                             |
| ------- | --------------------------------- |
| `name`  | obligatorio, mínimo 3, máximo 150 |
| `price` | obligatorio, mínimo 0             |
| `stock` | obligatorio, mínimo 0             |

---

## 11.2. Validaciones para CreateProductDto

Ejemplo:

```ts
export class CreateProductDto {

  @IsNotEmpty({ message: 'El nombre es obligatorio' })
  @MinLength(3, { message: 'El nombre debe tener al menos 3 caracteres' })
  @MaxLength(150, { message: 'El nombre no debe superar los 150 caracteres' })
  name: string;

  @IsNotEmpty({ message: 'El precio es obligatorio' })
  @Type(() => Number)
  @IsNumber({}, { message: 'El precio debe ser numérico' })
  @Min(0, { message: 'El precio no puede ser negativo' })
  price: number;

  @IsNotEmpty({ message: 'El stock es obligatorio' })
  @Type(() => Number)
  @IsNumber({}, { message: 'El stock debe ser numérico' })
  @Min(0, { message: 'El stock no puede ser negativo' })
  stock: number;
}
```

---

## 11.3. Validaciones para UpdateProductDto

```ts
export class UpdateProductDto {

  @IsNotEmpty({ message: 'El nombre es obligatorio' })
  @MinLength(3, { message: 'El nombre debe tener al menos 3 caracteres' })
  @MaxLength(150, { message: 'El nombre no debe superar los 150 caracteres' })
  name: string;

  @IsNotEmpty({ message: 'El precio es obligatorio' })
  @Type(() => Number)
  @IsNumber({}, { message: 'El precio debe ser numérico' })
  @Min(0, { message: 'El precio no puede ser negativo' })
  price: number;

  @IsNotEmpty({ message: 'El stock es obligatorio' })
  @Type(() => Number)
  @IsNumber({}, { message: 'El stock debe ser numérico' })
  @Min(0, { message: 'El stock no puede ser negativo' })
  stock: number;
}
```

---

## 11.4. Validaciones para PartialUpdateProductDto

```ts
export class PartialUpdateProductDto {

  @IsOptional()
  @MinLength(3, { message: 'El nombre debe tener al menos 3 caracteres' })
  @MaxLength(150, { message: 'El nombre no debe superar los 150 caracteres' })
  name?: string;

  @IsOptional()
  @Type(() => Number)
  @IsNumber({}, { message: 'El precio debe ser numérico' })
  @Min(0, { message: 'El precio no puede ser negativo' })
  price?: number;

  @IsOptional()
  @Type(() => Number)
  @IsNumber({}, { message: 'El stock debe ser numérico' })
  @Min(0, { message: 'El stock no puede ser negativo' })
  stock?: number;
}
```

---

## 11.5. Activar validación en ProductsController

Si el `ValidationPipe` está configurado globalmente en `main.ts`, no se necesita agregar decoradores extra en cada método.

Solo se deben recibir los DTOs correctamente:

```ts
@Post()
create(@Body() dto: CreateProductDto) {
  return this.service.create(dto);
}
```

```ts
@Put(':id')
update(
  @Param('id') id: string,
  @Body() dto: UpdateProductDto,
) {
  return this.service.update(Number(id), dto);
}
```

```ts
@Patch(':id')
partialUpdate(
  @Param('id') id: string,
  @Body() dto: PartialUpdateProductDto,
) {
  return this.service.partialUpdate(Number(id), dto);
}
```

---

## 11.6. Validar reglas de negocio en ProductsService

Validar:

* no actualizar productos eliminados
* no devolver productos eliminados en `findAll`
* no eliminar dos veces el mismo producto

El `delete` debe mantenerse como eliminado lógico:

```ts
entity.deleted = true;
await this.productRepository.save(entity);
```

---

## 11.7. Validar casos erróneos desde Postman / Bruno

Probar:

* `price: -5`
* `stock: -1`
* `name: ""`
* `name: "A"`

---

# 12. Resultados y evidencias

En la nueva entrada del README, se debe agregar:

## Captura de respuesta de error al enviar un POST inválido

Ejemplo:

```json
{
  "name": "",
  "price": -5,
  "stock": -1
}
```

---

## Captura de CRUD de productos validado correctamente

Debe evidenciarse:

* error al crear producto con precio negativo
* error al actualizar producto eliminado
* `findAll` no devuelve productos eliminados
