# Programación y Plataformas Web

# Frameworks Backend: NestJS – Servicios, Lógica de Negocio e Inyección de Dependencias

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nestjs/nestjs-original.svg" width="110" alt="Nest Logo">
</div>

---

# Práctica 4 (NestJS): Controladores + Servicios + Lógica de Negocio

### Autores

**Pablo Torres**

[ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: PabloT18

---

# 1. Introducción

En la práctica anterior se implementó un CRUD REST completo colocando toda la lógica dentro del controlador.

El controlador realizaba varias tareas al mismo tiempo:

* recibía peticiones HTTP
* almacenaba usuarios en memoria
* buscaba usuarios por ID
* creaba nuevos usuarios
* actualizaba usuarios
* eliminaba usuarios
* convertía modelos a DTOs de respuesta

Este enfoque sirve para comprender cómo funcionan los endpoints REST, pero no es adecuado para una aplicación más organizada.

En esta práctica se introduce el uso de servicios mediante `@Injectable()`.

El objetivo es mover la lógica del controlador hacia una clase de servicio, de manera que el controlador quede responsable únicamente de recibir la petición HTTP y delegar la operación.

En esta práctica se trabajará con:

* controladores
* DTOs
* modelos
* mappers
* servicios
* almacenamiento en memoria con `UserModel[]`

Todavía no se utiliza:

* repositorios
* entidades de base de datos
* base de datos

---

# 2. Flujo después de aplicar servicios

Ahora el flujo será:

```txt
Cliente
  ↓
UsersController
  ↓
UsersService
  ↓
UserModel[]
  ↓
UserMapper
  ↓
UserResponseDto
  ↓
Cliente
```

El controlador ya no manejará directamente el arreglo de usuarios.

El arreglo en memoria se moverá al servicio.

---

## 2.1. Responsabilidad de cada clase

| Clase                  | Responsabilidad                                |
| ---------------------- | ---------------------------------------------- |
| `UsersController`      | Recibir peticiones HTTP y llamar al servicio   |
| `UsersService`         | Implementar la lógica de negocio               |
| `UserModel`            | Representar el usuario dentro de la aplicación |
| `UserMapper`           | Convertir entre DTOs y modelos                 |
| `CreateUserDto`        | Recibir datos para crear usuario               |
| `UpdateUserDto`        | Recibir datos para actualización completa      |
| `PartialUpdateUserDto` | Recibir datos para actualización parcial       |
| `UserResponseDto`      | Devolver datos seguros al cliente              |
| `ErrorResponseDto`     | Devolver mensajes de error                     |

---

# 3. Creación del servicio

Dentro de la carpeta correspondiente se creará el archivo:

```txt
users.service.ts
```

---

## UsersService

Archivo `users.service.ts`:

```ts
/*
 * Servicio encargado de implementar las operaciones disponibles
 * para la gestión de usuarios.
 *
 * En esta clase se mueve la lógica que antes estaba dentro del controlador.
 *
 * En esta práctica todavía no se usa repository ni base de datos.
 * Por eso se mantiene un arreglo en memoria dentro del servicio.
 */
@Injectable()
export class UsersService {

  private users: UserModel[] = [];
  private currentId = 1;

  /*
   * Retorna todos los usuarios registrados en memoria.
   *
   * Convierte cada UserModel a UserResponseDto para no exponer
   * datos internos como password o passwordHash.
   */
  findAll(): UserResponseDto[] {

    // Programación tradicional iterativa
    /*
    const dtos: UserResponseDto[] = [];

    for (const user of this.users) {
      dtos.push(UserMapper.toResponse(user));
    }

    return dtos;
    */

    // Programación funcional
    return this.users.map((user) => UserMapper.toResponse(user));
  }

  /*
   * Busca un usuario por id.
   *
   * Si el usuario existe, devuelve UserResponseDto.
   * Si no existe, devuelve ErrorResponseDto.
   */
  findOne(id: number): object {

    // Programación tradicional iterativa
    /*
    for (const user of this.users) {
      if (user.id === id) {
        return UserMapper.toResponse(user);
      }
    }

    return {
      error: 'User not found',
    };
    */

    // Programación funcional
    const user = this.users.find((item) => item.id === id);

    if (!user) {
      return {
        error: 'User not found',
      };
    }

    return UserMapper.toResponse(user);
  }

  /*
   * Crea un nuevo usuario.
   *
   * Recibe un CreateUserDto, lo convierte a UserModel,
   * asigna un id generado en memoria y devuelve UserResponseDto.
   */
  create(dto: CreateUserDto): UserResponseDto {

    const user = UserMapper.toModel(dto);

    user.id = this.currentId;
    this.currentId++;

    this.users.push(user);

    return UserMapper.toResponse(user);
  }

  /*
   * Actualiza completamente un usuario existente.
   *
   * En PUT se reemplazan los campos editables enviados en el DTO.
   * No se modifica el id ni createdAt.
   */
  update(id: number, dto: UpdateUserDto): object {

    // Programación tradicional iterativa
    /*
    for (const user of this.users) {
      if (user.id === id) {
        user.name = dto.name;
        user.email = dto.email;

        return UserMapper.toResponse(user);
      }
    }

    return {
      error: 'User not found',
    };
    */

    // Programación funcional
    const user = this.users.find((item) => item.id === id);

    if (!user) {
      return {
        error: 'User not found',
      };
    }

    user.name = dto.name;
    user.email = dto.email;

    return UserMapper.toResponse(user);
  }

  /*
   * Actualiza parcialmente un usuario existente.
   *
   * En PATCH solo se actualizan los campos que llegan en el DTO.
   * Los campos indefinidos se ignoran.
   */
  partialUpdate(id: number, dto: PartialUpdateUserDto): object {

    // Programación tradicional iterativa
    /*
    for (const user of this.users) {
      if (user.id === id) {

        if (dto.name !== undefined) {
          user.name = dto.name;
        }

        if (dto.email !== undefined) {
          user.email = dto.email;
        }

        return UserMapper.toResponse(user);
      }
    }

    return {
      error: 'User not found',
    };
    */

    // Programación funcional
    const user = this.users.find((item) => item.id === id);

    if (!user) {
      return {
        error: 'User not found',
      };
    }

    if (dto.name !== undefined) {
      user.name = dto.name;
    }

    if (dto.email !== undefined) {
      user.email = dto.email;
    }

    return UserMapper.toResponse(user);
  }

  /*
   * Elimina un usuario por id.
   *
   * Si el usuario existe, se elimina del arreglo en memoria.
   * Si no existe, se devuelve un DTO de error.
   */
  delete(id: number): object {

    const exists = this.users.some((item) => item.id === id);

    if (!exists) {
      return {
        error: 'User not found',
      };
    }

    this.users = this.users.filter((item) => item.id !== id);

    return {
      message: 'Deleted successfully',
    };
  }
}
```

---

### Explicación de UsersService

`UsersService` es la clase que implementa la lógica del módulo de usuarios.

Se marca con:

```ts
@Injectable()
```

Este decorador le indica a NestJS que esta clase debe ser registrada como un proveedor.

Cuando una clase tiene `@Injectable()`, NestJS puede crear una instancia automáticamente y entregarla a otras clases mediante inyección de dependencias.

En esta práctica, el arreglo:

```ts
private users: UserModel[] = [];
```

ya no vive en el controlador.

Ahora vive en el servicio.

Esto permite que el controlador quede más limpio.

---

# 4. Actualizar UsersController

Archivo `users.controller.ts`:

```ts
/*
 * Controlador REST encargado de exponer los endpoints HTTP
 * para la gestión de usuarios.
 *
 * En esta práctica el controlador ya no contiene la lógica del CRUD.
 * Solo recibe la petición y delega la operación al servicio.
 */
@Controller('users')
export class UsersController {

  private readonly service: UsersService;

  /*
   * Inyección de dependencias por constructor.
   *
   * NestJS busca una instancia de UsersService,
   * la crea porque está registrada como provider,
   * y la inyecta automáticamente en el controlador.
   */
  constructor(service: UsersService) {
    this.service = service;
  }

  /*
   * Endpoint para listar todos los usuarios.
   *
   * GET /users
   */
  @Get()
  findAll(): UserResponseDto[] {
    return this.service.findAll();
  }

  /*
   * Endpoint para buscar un usuario por id.
   *
   * GET /users/:id
   */
  @Get(':id')
  findOne(@Param('id') id: string): object {
    return this.service.findOne(Number(id));
  }

  /*
   * Endpoint para crear un nuevo usuario.
   *
   * POST /users
   */
  @Post()
  create(@Body() dto: CreateUserDto): UserResponseDto {
    return this.service.create(dto);
  }

  /*
   * Endpoint para actualizar completamente un usuario.
   *
   * PUT /users/:id
   */
  @Put(':id')
  update(
    @Param('id') id: string,
    @Body() dto: UpdateUserDto,
  ): object {
    return this.service.update(Number(id), dto);
  }

  /*
   * Endpoint para actualizar parcialmente un usuario.
   *
   * PATCH /users/:id
   */
  @Patch(':id')
  partialUpdate(
    @Param('id') id: string,
    @Body() dto: PartialUpdateUserDto,
  ): object {
    return this.service.partialUpdate(Number(id), dto);
  }

  /*
   * Endpoint para eliminar un usuario.
   *
   * DELETE /users/:id
   */
  @Delete(':id')
  delete(@Param('id') id: string): object {
    return this.service.delete(Number(id));
  }
}
```

---

## Explicación del controlador actualizado

El controlador ya no tiene:

```ts
private users: UserModel[] = [];
private currentId = 1;
```

Tampoco contiene directamente la lógica de búsqueda, creación, actualización o eliminación.

Ahora solo tiene una dependencia:

```ts
private readonly service: UsersService;
```

Esta dependencia se recibe por constructor:

```ts
constructor(service: UsersService) {
  this.service = service;
}
```

Esto se conoce como inyección de dependencias por constructor.

NestJS detecta que el controlador necesita un `UsersService`.

Luego busca una clase registrada como provider dentro del módulo.

Encuentra:

```ts
@Injectable()
export class UsersService
```

Entonces crea una instancia de `UsersService` y la inyecta en el controlador.

---

# 5. Inyección de dependencias

La inyección de dependencias permite que una clase no cree manualmente los objetos que necesita.

En lugar de hacer esto:

```ts
private service = new UsersService();
```

NestJS se encarga de crear e inyectar el objeto:

```ts
private readonly service: UsersService;

constructor(service: UsersService) {
  this.service = service;
}
```

Esto mejora la organización del código y facilita futuras pruebas.

---

## Implementación de un servicio y su inyección

Se usa un servicio porque permite separar:

```txt
qué recibe el controlador
```

de:

```txt
cómo se ejecuta la lógica
```

El controlador llama:

```ts
return this.service.findOne(Number(id));
```

El servicio define cómo se busca el usuario:

```ts
const user = this.users.find((item) => item.id === id);

if (!user) {
  return {
    error: 'User not found',
  };
}

return UserMapper.toResponse(user);
```

Esto permite que más adelante se pueda cambiar la implementación interna sin modificar el controlador.

---

# 6. Pruebas sugeridas en Postman / Bruno

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

# 7. Actividad práctica

## 1. Replicar la estructura implementada en `users/` para el recurso `products/`.

---

# 8. Resultados y evidencias

En la nueva entrada del README, se debe agregar:

## Captura completa de ProductsService

Debe evidenciarse:

* uso de `@Injectable()`
* arreglo en memoria
* generación de ID
* uso del mapper
* métodos CRUD implementados

---

## Captura de ProductsController

Debe evidenciarse:

* inyección de `ProductsService`
* endpoints llamando al servicio
* ausencia de lógica CRUD dentro del controlador

---

## Explicación breve

```txt
¿Cómo se inyecta el servicio en el controlador?
```
