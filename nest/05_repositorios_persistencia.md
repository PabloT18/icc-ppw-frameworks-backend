# Programación y Plataformas Web

# Frameworks Backend: NestJS – Persistencia con TypeORM, Entidades, Repositorios y Base de Datos

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nestjs/nestjs-original.svg" width="110" alt="Nest Logo">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="95">
</div>

---

# Práctica 5 (NestJS): Persistencia real con PostgreSQL, Entidades TypeORM y Repositorios

### Autores

**Pablo Torres**

[ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: PabloT18

---

# 1. Introducción

En la práctica anterior se organizó el CRUD REST usando servicios.

La lógica dejó de estar directamente dentro del controlador y se movió a `UsersService`.

Hasta ese momento, los datos todavía se almacenaban en memoria usando:

```ts
private users: UserModel[] = [];
private currentId = 1;
```

Ese enfoque sirve para practicar el flujo de una API REST, pero tiene una limitación importante: los datos se pierden cada vez que se reinicia la aplicación.

En esta práctica se reemplaza el arreglo en memoria por una base de datos real usando:

* PostgreSQL
* TypeORM
* entidades TypeORM
* repositorios
* conexión mediante `TypeOrmModule`

A partir de esta práctica ya no se utilizará:

* arreglo en memoria dentro del servicio
* generación manual de ID con `currentId`

---

# 2. Flujo después de aplicar repositorios y base de datos

Ahora el flujo será:

```txt
Cliente
  ↓
UsersController
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

El servicio ya no manejará directamente un arreglo en memoria.

La persistencia se delega al repositorio.

El repositorio se comunica con PostgreSQL mediante TypeORM.

---

## 2.1. Responsabilidad de cada clase

| Clase                    | Responsabilidad                                        |
| ------------------------ | ------------------------------------------------------ |
| `UsersController`        | Recibir peticiones HTTP y llamar al servicio           |
| `UsersService`           | Implementar la lógica de negocio y usar el repositorio |
| `Repository<UserEntity>` | Ejecutar operaciones de persistencia                   |
| `UserEntity`             | Representar la tabla en la base de datos               |
| `UserModel`              | Representar el usuario dentro de la aplicación         |
| `UserMapper`             | Convertir entre DTOs, modelos y entidades              |
| `CreateUserDto`          | Recibir datos para crear usuario                       |
| `UpdateUserDto`          | Recibir datos para actualización completa              |
| `PartialUpdateUserDto`   | Recibir datos para actualización parcial               |
| `UserResponseDto`        | Devolver datos seguros al cliente                      |
| `ErrorResponseDto`       | Devolver mensajes de error                             |

---

# 3. Instalación y configuración de dependencias

Para trabajar con PostgreSQL desde NestJS se necesitan tres dependencias principales:

* `@nestjs/typeorm`
* `typeorm`
* `pg`

---

## 3.1. Dependencias necesarias

Ejecutar en la raíz del proyecto:

```bash
pnpm install @nestjs/typeorm typeorm pg
```

`@nestjs/typeorm` permite integrar TypeORM con NestJS.

`typeorm` permite trabajar con entidades, repositorios y consultas.

`pg` permite que la aplicación se conecte al motor PostgreSQL.

---

# 4. Configuración de conexión en `app.module.ts`

Archivo:

```txt
src/app.module.ts
```

Configuración:

```ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';

import { UsersModule } from './users/users.module';
import { ProductsModule } from './products/products.module';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: 'localhost',
      port: 5432,
      username: 'ups',
      password: 'ups123',
      database: 'devdb-nest',
      entities: [__dirname + '/**/*.entity{.ts,.js}'],
      synchronize: true,
      logging: true,
    }),
    UsersModule,
    ProductsModule,
  ],
})
export class AppModule {}
```

---

## 4.1. Explicación de cada propiedad

### Propiedades de conexión

```ts
type: 'postgres'
```

Indica que TypeORM se conectará a PostgreSQL.

```ts
host: 'localhost'
port: 5432
```

Indica el servidor y puerto donde se ejecuta PostgreSQL.

```ts
username: 'ups'
password: 'ups123'
database: 'devdb-nest'
```

Estos valores corresponden al usuario, contraseña y base de datos configurados en el contenedor Docker.

Para NestJS se usará la base:

```txt
devdb-nest
```

---

### Propiedades de TypeORM

```ts
entities: [__dirname + '/**/*.entity{.ts,.js}']
```

Indica dónde TypeORM buscará las entidades.

Busca todos los archivos que terminen en:

```txt
.entity.ts
.entity.js
```

---

```ts
synchronize: true
```

Permite que TypeORM cree o actualice las tablas automáticamente según las entidades.

Para esta práctica se usará:

```ts
synchronize: true
```

porque permite crear las tablas durante el desarrollo.

En producción no se recomienda usar `synchronize: true`.

---

```ts
logging: true
```

Permite ver las consultas SQL generadas por TypeORM en consola.

Esto es útil para aprendizaje y depuración.

---

# 5. Base de datos PostgreSQL mediante Docker

Esta práctica utiliza la base de datos levantada mediante Docker en la guía complementaria `05-B`.

Los datos de conexión para NestJS son:

| Parámetro     | Valor        |
| ------------- | ------------ |
| Host          | `localhost`  |
| Puerto        | `5432`       |
| Usuario       | `ups`        |
| Contraseña    | `ups123`     |
| Base de datos | `devdb-nest` |

Para verificar que el contenedor está activo:

```bash
docker ps
```

Debe aparecer el contenedor:

```txt
postgres-dev
```

Si está detenido, iniciarlo con:

```bash
docker start postgres-dev
```

Si la base `devdb-nest` no existe, crearla con:

```bash
docker exec -it postgres-dev psql -U ups -d postgres -c "CREATE DATABASE \"devdb-nest\";"
```

---

# 6. Modelo vs Entidad persistente

Hasta la práctica anterior se trabajó con:

```txt
UserModel
```

Ese modelo representa los datos internos de la aplicación.

Pero para guardar datos en PostgreSQL se necesita una entidad TypeORM:

```txt
UserEntity
```

---

## 6.1. Diferencia entre Model y Entity

| Elemento          | Función                                                    |
| ----------------- | ---------------------------------------------------------- |
| `UserModel`       | Representa el usuario dentro de la lógica de la aplicación |
| `UserEntity`      | Representa cómo se guarda el usuario en la base de datos   |
| `UserResponseDto` | Representa lo que se devuelve al cliente                   |
| `CreateUserDto`   | Representa lo que el cliente envía para crear un usuario   |

---

## 6.2. Por qué no usar directamente la entidad como respuesta

No se debe devolver directamente `UserEntity` al cliente porque:

* representa la estructura de la base de datos
* puede tener campos internos
* puede exponer información sensible
* acopla la API a la persistencia
* dificulta cambios futuros en la base de datos

Por eso se mantiene el flujo:

```txt
Entity → Model → ResponseDto
```

---

# 7. Superclase de auditoría `BaseEntity`

Todas las entidades pueden compartir campos comunes como:

* id
* fecha de creación
* fecha de actualización
* eliminado lógico

Para eso se crea una clase base.

Archivo:

```txt
src/core/entities/base.entity.ts
```

Código:

```ts
/*
 * Superclase base para entidades TypeORM.
 *
 * Contiene campos comunes de persistencia como id,
 * createdAt, updatedAt y deleted.
 *
 * No representa por sí sola una tabla de negocio.
 * Sus atributos se heredan en las entidades hijas.
 */
export abstract class BaseEntity {

  @PrimaryGeneratedColumn('increment')
  id: number;

  @CreateDateColumn({ type: 'timestamp' })
  createdAt: Date;

  @UpdateDateColumn({ type: 'timestamp' })
  updatedAt: Date;

  @Column({ default: false })
  deleted: boolean;
}
```

---

## 7.1. Explicación de decoradores

| Decorador                 | Función                                            |
| ------------------------- | -------------------------------------------------- |
| `@PrimaryGeneratedColumn` | Marca el identificador principal autogenerado      |
| `@CreateDateColumn`       | Asigna automáticamente la fecha de creación        |
| `@UpdateDateColumn`       | Actualiza automáticamente la fecha de modificación |
| `@Column`                 | Define una columna normal en la tabla              |

---

# 8. Creación de la entidad persistente UserEntity

Archivo:

```txt
users/entities/user.entity.ts
```

Código:

```ts
/*
 * Entidad TypeORM del recurso users.
 *
 * Representa la tabla users en PostgreSQL.
 * Esta clase sí pertenece a la capa de persistencia.
 */
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

---

## 8.1. Explicación de decoradores

| Decorador          | Función                                         |
| ------------------ | ----------------------------------------------- |
| `@Entity('users')` | Indica que la clase representa la tabla `users` |
| `@Column`          | Configura propiedades de las columnas           |
| `nullable: false`  | Indica que la columna no permite valores nulos  |
| `unique: true`     | Indica que el correo no se puede repetir        |
| `length: 150`      | Define la longitud máxima de la columna         |

---

# 9. Actualización del modelo UserModel

El modelo se mantiene como clase de dominio.

Archivo:

```txt
users/models/user.model.ts
```

Código:

```ts
/*
 * Modelo de dominio del recurso users.
 *
 * Representa al usuario dentro de la lógica de negocio.
 * No es una entidad de base de datos y no debe tener decoradores de TypeORM.
 */
export class UserModel {

  id: number;

  name: string;

  email: string;

  createdAt: Date;

  updatedAt: Date;

  deleted: boolean;

  password: string;

  passwordHash: string;
}
```

---

# 10. Registro del repositorio en el módulo

En NestJS con TypeORM no se crea una interfaz de repositorio como en Spring Data JPA.

TypeORM proporciona un repositorio genérico:

```txt
Repository<UserEntity>
```

Para poder inyectarlo en el servicio, primero se registra la entidad en el módulo.

Archivo:

```txt
users/users.module.ts
```

Código:

```ts
/*
 * Módulo del recurso users.
 *
 * Registra el controlador, el servicio y la entidad que usará TypeORM.
 */
@Module({
  imports: [
    TypeOrmModule.forFeature([UserEntity]),
  ],
  controllers: [UsersController],
  providers: [UsersService],
})
export class UsersModule {}
```

---

## 10.1. Explicación de `TypeOrmModule.forFeature`

```ts
TypeOrmModule.forFeature([UserEntity])
```

Permite que NestJS registre el repositorio de `UserEntity` dentro del módulo.

A partir de eso, se puede inyectar:

```ts
Repository<UserEntity>
```

dentro de `UsersService`.

---

## 10.2. Métodos automáticos de Repository

TypeORM proporciona métodos como:

```ts
save(entity)
find()
findOne(options)
delete(id)
remove(entity)
count()
exist(options)
```

Por eso ya no se necesita crear manualmente un arreglo ni recorrerlo para hacer operaciones básicas.

---

# 11. Actualización del UserMapper

Hasta la práctica anterior, el mapper convertía:

```txt
CreateUserDto → UserModel
UserModel → UserResponseDto
```

Ahora también debe convertir:

```txt
UserModel → UserEntity
UserEntity → UserModel
```

Archivo:

```txt
users/mappers/user.mapper.ts
```

Cambian algunos nombres de métodos para reflejar mejor su función.

Código:

```ts
/*
 * Clase encargada de convertir objetos entre DTOs, modelos y entidades.
 *
 * En esta práctica se agrega la conversión hacia UserEntity
 * porque ya se trabaja con persistencia real en PostgreSQL.
 */
export class UserMapper {

  /*
   * Convierte un CreateUserDto en UserModel.
   *
   * El DTO contiene los datos recibidos desde la API.
   * El modelo representa el usuario dentro de la lógica de la aplicación.
   */
  static toModelFromDto(dto: CreateUserDto): UserModel {
    const model = new UserModel();

    model.name = dto.name;
    model.email = dto.email;
    model.password = dto.password;
    model.passwordHash = 'HASH_' + dto.password;

    return model;
  }

  /*
   * Convierte una entidad TypeORM en UserModel.
   *
   * Se usa cuando el repositorio devuelve datos desde PostgreSQL.
   */
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

  /*
   * Convierte un UserModel en UserEntity.
   *
   * Se usa antes de guardar datos en la base de datos.
   */
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

  /*
   * Convierte un UserModel en UserResponseDto.
   *
   * No se expone password ni passwordHash.
   */
  static toResponse(model: UserModel): UserResponseDto {
    const response = new UserResponseDto();

    response.id = model.id;
    response.name = model.name;
    response.email = model.email;

    return response;
  }
}
```

---

# 12. Actualización de UsersService

En NestJS no se usa una interfaz obligatoria para el servicio en esta práctica.

El servicio mantiene las mismas operaciones, pero ahora los métodos son asíncronos porque acceden a la base de datos.

En esta práctica, cuando no exista un registro, se lanzará un error simple con `NotFoundException`.

El manejo centralizado de errores se trabajará posteriormente.

---

# 13. Actualización de UsersService

La implementación del servicio ya no usa arreglo en memoria. Se debe eliminar:

```ts
private users: UserModel[] = [];
private currentId = 1;
```

Ahora usa:

```ts
private readonly userRepository: Repository<UserEntity>;
```

Archivo:

```txt
users/services/users.service.ts
```

Código:

```ts
/*
 * Servicio de usuarios.
 *
 * En esta clase se reemplaza el arreglo en memoria por Repository<UserEntity>.
 * El repositorio se encarga de comunicarse con PostgreSQL mediante TypeORM.
 */
@Injectable()
export class UsersService {

  constructor(
    @InjectRepository(UserEntity)
    private readonly userRepository: Repository<UserEntity>,
  ) {}

}
```

En el constructor se inyecta el repositorio para poder usarlo en los métodos del servicio.

Ahora cada método del servicio debe usar el repositorio para realizar las operaciones de persistencia, en lugar de manipular un arreglo en memoria.

```ts
/*
 * Retorna todos los usuarios almacenados en PostgreSQL.
 *
 * El repositorio devuelve entidades.
 * El mapper convierte entidades a modelos.
 * Luego convierte modelos a DTOs de respuesta.
 */
async findAll(): Promise<UserResponseDto[]> {
  return this.userRepository.find({
    where: {
      deleted: false,
    },
  })
    .then((entities) =>
      entities
        .map(UserMapper.toModelFromEntity)
        .map(UserMapper.toResponse),
    );
}

/*
 * Busca un usuario por id.
 *
 * Si no existe, lanza un error simple.
 * El manejo formal de errores se implementará después.
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

/*
 * Crea un nuevo usuario.
 *
 * Convierte DTO a Model.
 * Convierte Model a Entity.
 * Guarda Entity en PostgreSQL.
 * Convierte Entity guardada a Model.
 * Devuelve Response DTO.
 */
async create(dto: CreateUserDto): Promise<UserResponseDto> {
  const model = UserMapper.toModelFromDto(dto);

  const entity = UserMapper.toEntityFromModel(model);

  const savedEntity = await this.userRepository.save(entity);

  const savedModel = UserMapper.toModelFromEntity(savedEntity);

  return UserMapper.toResponse(savedModel);
}

/*
 * Actualiza completamente un usuario.
 *
 * Busca la entidad existente.
 * Actualiza los campos editables.
 * Guarda los cambios.
 * Devuelve DTO de respuesta.
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

/*
 * Actualiza parcialmente un usuario.
 *
 * Solo actualiza los campos enviados en el DTO.
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

/*
 * Elimina lógicamente un usuario por id.
 *
 * Primero verifica que exista.
 * Luego marca la entidad como eliminada usando deleted = true.
 * No elimina físicamente el registro de la base de datos.
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

# 14. Actualización de UsersController

El controlador casi no cambia.

La diferencia es que ahora el servicio ya no usa un arreglo en memoria, sino un repositorio conectado a PostgreSQL.

Como los métodos del servicio son asíncronos, el controlador puede retornar directamente las promesas.

Archivo:

```txt
users/controllers/users.controller.ts
```

Código:

```ts
/*
 * Controlador REST encargado de exponer los endpoints HTTP
 * para la gestión de usuarios.
 *
 * El controlador sigue delegando las operaciones al servicio.
 */
@Controller('users')
export class UsersController {

  constructor(private readonly service: UsersService) {}

  @Get()
  findAll(): Promise<UserResponseDto[]> {
    return this.service.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string): Promise<UserResponseDto> {
    return this.service.findOne(Number(id));
  }

  @Post()
  create(@Body() dto: CreateUserDto): Promise<UserResponseDto> {
    return this.service.create(dto);
  }

  @Put(':id')
  update(
    @Param('id') id: string,
    @Body() dto: UpdateUserDto,
  ): Promise<UserResponseDto> {
    return this.service.update(Number(id), dto);
  }

  @Patch(':id')
  partialUpdate(
    @Param('id') id: string,
    @Body() dto: PartialUpdateUserDto,
  ): Promise<UserResponseDto> {
    return this.service.partialUpdate(Number(id), dto);
  }

  @Delete(':id')
  delete(@Param('id') id: string): Promise<void> {
    return this.service.delete(Number(id));
  }
}
```

---

# 15. ¿Qué cambió respecto a la práctica anterior?

Antes:

```ts
private users: UserModel[] = [];
private currentId = 1;
```

Ahora:

```ts
@InjectRepository(UserEntity)
private readonly userRepository: Repository<UserEntity>
```

Antes el ID se asignaba manualmente:

```ts
user.id = this.currentId;
this.currentId++;
```

Ahora lo genera PostgreSQL:

```ts
@PrimaryGeneratedColumn('increment')
id: number;
```

Antes los datos se perdían al reiniciar.

Ahora los datos permanecen guardados en PostgreSQL.

---

# 16. Verificación en PostgreSQL

Para verificar las tablas desde el contenedor:

```bash
docker exec -it postgres-dev psql -U ups -d devdb-nest
```

Dentro de `psql`:

```sql
\dt
```

Para consultar usuarios:

```sql
SELECT * FROM users;
```

Para salir:

```sql
\q
```

También se puede verificar desde:

* DBeaver
* DataGrip
* TablePlus
* VS Code PostgreSQL

---

# 17. Pruebas sugeridas en Postman / Bruno

## Crear usuario

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
  "password": "123456"
}
```

---

## Listar usuarios

Método:

```txt
GET
```

Ruta:

```txt
/api/users
```

---

## Buscar usuario por ID

Método:

```txt
GET
```

Ruta:

```txt
/api/users/1
```

---

## Actualizar usuario completo

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
  "email": "juan.actualizado@ups.edu.ec"
}
```

---

## Actualizar usuario parcialmente

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
  "email": "nuevo.correo@ups.edu.ec"
}
```

---

## Eliminar usuario

Método:

```txt
DELETE
```

Ruta:

```txt
/api/users/1
```

---

# 18. Salida esperada en consola

Al ejecutar la aplicación, debe verse que NestJS se conecta a PostgreSQL mediante TypeORM.

También se podrán observar consultas SQL si está habilitado:

```ts
logging: true
```

Ejemplo conceptual:

```sql
SELECT
  "UserEntity"."id" AS "UserEntity_id",
  "UserEntity"."createdAt" AS "UserEntity_createdAt",
  "UserEntity"."updatedAt" AS "UserEntity_updatedAt",
  "UserEntity"."deleted" AS "UserEntity_deleted",
  "UserEntity"."name" AS "UserEntity_name",
  "UserEntity"."email" AS "UserEntity_email",
  "UserEntity"."passwordHash" AS "UserEntity_passwordHash"
FROM
  "users" "UserEntity"
WHERE
  "UserEntity"."deleted" = false
```

---

# 19. Actividad práctica

Se debe replicar toda la arquitectura aprendida, pero ahora en el módulo:

```txt
products/
```

Debe implementar:

### 19.1 Crear `ProductEntity`

La entidad debe extender de `BaseEntity`.

---

### 19.2 Registrar la entidad en `ProductsModule`

Debe usar:

```ts
TypeOrmModule.forFeature([ProductEntity])
```

---

### 19.3 Actualizar `ProductMapper`

Debe permitir conversiones entre:

```txt
CreateProductDto → ProductModel
ProductModel → ProductEntity
ProductEntity → ProductModel
ProductModel → ProductResponseDto
```

---

### 19.4 Actualizar `ProductsService`

El servicio debe usar repositorio, no arreglo en memoria.

Debe implementar:

```txt
findAll()
findOne()
create()
update()
partialUpdate()
delete()
```

---

### 19.5 Actualizar `ProductsController`

El controlador debe seguir delegando al servicio.

No debe contener lógica de persistencia.

---

### 19.6 Probar el CRUD completo con PostgreSQL

Probar:

* POST create product
* GET list products
* GET product by id
* PUT update product
* PATCH partial update product
* DELETE remove product

### Datos para revisión

Ingresar 5 productos mediante API REST.

---

# 20. Resultados y evidencias

En la nueva entrada del README, se debe agregar:

---

## Captura de 5 productos creados en PostgreSQL

Puede ser desde:

* DBeaver
* VS Code PostgreSQL
* terminal con `psql`

Consulta sugerida:

```sql
SELECT * FROM products;
```

## Explicar brevemente el flujo de datos desde la API REST hasta PostgreSQL y viceversa, destacando el uso de BaseEntity.
