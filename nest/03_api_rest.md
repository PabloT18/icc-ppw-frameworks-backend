# Programación y Plataformas Web

# Frameworks Backend: NestJS – API REST y CRUD Inicial sin Servicios

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nestjs/nestjs-original.svg" width="110" alt="Nest Logo"/>
</div>

---

# Práctica 3 (NestJS): Construcción de una API REST usando controladores, DTOs, modelos y mappers

### Autores

**Pablo Torres**

[ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: PabloT18

---

# 1. Introducción

En esta práctica se construye un **CRUD REST completo** usando únicamente:

* controladores (`@Controller`)
* modelos
* DTOs de entrada y salida
* mappers para transformar datos
* almacenamiento en memoria con `UserModel[]`

Aún **no se utiliza**:

* servicios (`@Injectable`)
* repositorios
* base de datos

El objetivo de esta práctica es comprender:

* cómo se estructuran endpoints REST en NestJS
* cómo se reciben datos con DTOs
* cómo se retorna información segura con DTOs de respuesta
* cómo implementar CRUD desde el controlador antes de aplicar MVCS completo

---

# 2. Estructura que se usará

Dentro de:

```txt
src/users/
```

solo se usarán estas carpetas en este tema:

```txt
src/users/
├── controllers/
│   └── users.controller.ts
│
├── dtos/
│   ├── create-user.dto.ts
│   ├── update-user.dto.ts
│   ├── partial-update-user.dto.ts
│   └── user-response.dto.ts
│
├── models/
│   └── user.model.ts
│
├── mappers/
│   └── user.mapper.ts
│
└── users.module.ts
```

Recordatorio:

```txt
DTO = lo que entra o sale por la API
Model = lo que usa la lógica de negocio
Mapper = lo que convierte entre DTO y Model
Controller = lo que expone endpoints

En esta práctica todavía no se usa:
Service
Repository
Entity
Base de datos
```

---

# 3. Modelo de dominio

Aquí se define el modelo interno del usuario, incluyendo campos que **no se enviarán al cliente**.

Archivo:

`models/user.model.ts`

```ts
/*
 * Modelo de dominio del recurso users.
 *
 * Representa al usuario dentro de la lógica de negocio.
 * No es una entidad de base de datos y no debe tener decoradores de ORM.
 */
export class UserModel {
  id: number;
  name: string;
  email: string;
  createdAt: Date;
  password: string;
  passwordHash: string;

  // Constructor vacío

  // Constructor lleno
}
```

---

# 4. DTOs de entrada (para recibir datos)

Los DTOs controlan **qué datos acepta la API**.

Dependiendo del endpoint, y de si es creación o actualización, se usan distintos DTOs.

No suelen ser idénticos al modelo, ni tampoco se usan siempre todos los campos. Una mejor práctica es definir DTOs específicos por acción, aplicando el **principio de responsabilidad única**.

---

## 4.1. DTO para crear usuario

Archivo:

`dtos/create-user.dto.ts`

```ts
/*
 * DTO utilizado para recibir los datos necesarios
 * para crear un nuevo usuario desde una petición HTTP.
 *
 * No incluye id porque el backend lo genera.
 * No incluye createdAt porque el backend asigna la fecha de creación.
 */
export class CreateUserDto {
  name: string;
  email: string;
  password: string;
}
```

---

## 4.2. DTO para actualizar completamente (PUT)

Archivo:

`dtos/update-user.dto.ts`

```ts
/*
 * DTO utilizado para recibir los datos necesarios
 * para actualizar completamente un usuario existente.
 *
 * No incluye id porque el id llega por la URL.
 * No incluye createdAt porque la fecha de creación no debe modificarse.
 */
export class UpdateUserDto {
  name: string;
  email: string;
}
```

---

## 4.3. DTO para actualización parcial (PATCH)

Archivo:

`dtos/partial-update-user.dto.ts`

```ts
/*
 * DTO utilizado para recibir los datos que se desean
 * actualizar parcialmente en un usuario existente.
 *
 * Los campos pueden venir indefinidos cuando no se desean actualizar.
 * No incluye createdAt porque la fecha de creación no debe modificarse.
 */
export class PartialUpdateUserDto {
  name?: string;
  email?: string;
}
```

> **El ID no se coloca en el DTO** porque viene en la ruta del endpoint.

---

# 5. DTO de salida (Response DTO)

Este DTO define **qué datos se devuelven al cliente**.

Archivo:

`dtos/user-response.dto.ts`

```ts
/*
 * DTO utilizado para devolver al cliente los datos públicos
 * de un usuario como respuesta de la API.
 *
 * No incluye password.
 * No incluye passwordHash.
 */
export class UserResponseDto {
  id: number;
  name: string;
  email: string;
}
```

> No se expone: `password`, `createdAt` ni ningún dato interno.

---

# 6. Mapper User ↔ DTO

Archivo:

`mappers/user.mapper.ts`

```ts
/*
 * Clase encargada de convertir objetos entre DTOs y modelos.
 *
 * En esta práctica se usa para separar los datos que llegan desde la API
 * de los datos que maneja internamente la aplicación.
 *
 * El mapper evita que el controlador copie manualmente los campos
 * entre CreateUserDto, UserModel y UserResponseDto.
 */
export class UserMapper {
  /*
   * Convierte un CreateUserDto en un UserModel.
   *
   * Se usa cuando llega una petición POST para crear un usuario.
   * El DTO contiene los datos enviados por el cliente.
   * El modelo representa el usuario dentro de la aplicación.
   *
   * En este método también se asigna createdAt porque la fecha de creación
   * debe generarla el backend y no el cliente.
   */
  static toModel(dto: CreateUserDto): UserModel {
    const model = new UserModel();

    model.name = dto.name;
    model.email = dto.email;
    model.password = dto.password;

    model.passwordHash = 'HASH_' + dto.password;
    model.createdAt = new Date();

    return model;
  }

  /*
   * Convierte un UserModel en un UserResponseDto.
   *
   * Se usa para construir la respuesta que se devuelve al cliente.
   * El DTO de respuesta solo debe contener datos seguros.
   *
   * No se copia password ni passwordHash porque esos datos
   * no deben exponerse en la respuesta de la API.
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

# 7. Controlador con CRUD completo

Archivo:

`controllers/users.controller.ts`

Clase controladora donde se implementan todos los endpoints REST.

Se empieza creando solo un arreglo que simula la base de datos en memoria.

```ts
/*
 * Controlador REST encargado de exponer los endpoints HTTP
 * para la gestión de usuarios.
 */
@Controller('users')
export class UsersController {
  private users: UserModel[] = [];
  private currentId = 1;
```

---

## GET Users

Este endpoint devuelve la lista de usuarios mapeados a DTOs de respuesta.

```ts
  @Get()
  findAll(): UserResponseDto[] {
    // Programación tradicional iterativa para mapear cada UserModel a UserResponseDto
    const dtos: UserResponseDto[] = [];

    for (const user of this.users) {
      dtos.push(UserMapper.toResponse(user));
    }

    return dtos;

    // Programación funcional para mapear cada UserModel a UserResponseDto
    return this.users.map((user) => UserMapper.toResponse(user));
  }
```

---

## GET User por ID

Aquí se obtiene un usuario por su ID. Se busca en el arreglo y, si no se encuentra, se devuelve un mensaje de error.

Si se quisiera un mejor rendimiento podrían usar:

* búsqueda binaria si el arreglo está ordenado por ID
* `Map<number, UserModel>` en lugar de un `UserModel[]`

Con un `Map`, la búsqueda por ID sería O(1) en promedio, pero con mayor costo en complejidad espacial.

```ts
  @Get(':id')
  findOne(@Param('id') id: string): object {
    const numericId = Number(id);

    // Programación tradicional iterativa
    // Búsqueda lineal
    for (const user of this.users) {
      if (user.id === numericId) {
        return UserMapper.toResponse(user);
      }
    }

    return {
      error: 'User not found',
    };

    // Programación funcional
    // Búsqueda lineal
    const user = this.users.find((item) => item.id === numericId);

    if (!user) {
      return {
        error: 'User not found',
      };
    }

    return UserMapper.toResponse(user);
  }
```

---

## POST

Este endpoint crea un nuevo usuario a partir del DTO de creación.

Usa los atributos de `CreateUserDto` para crear el modelo `UserModel`, asigna un ID único y lo agrega al arreglo en memoria.

Finalmente, devuelve el DTO de respuesta del usuario creado.

* El ID debería ser secuencial o generado por la base de datos en un entorno real.

```ts
  @Post()
  create(@Body() dto: CreateUserDto): UserResponseDto {
    const user = UserMapper.toModel(dto);

    user.id = this.currentId;
    this.currentId++;

    this.users.push(user);

    return UserMapper.toResponse(user);
  }
```

---

## PUT

Endpoint `PUT` para reemplazar completamente un usuario existente.

Busca el usuario por ID. Si no lo encuentra, devuelve un error.

Si lo encuentra, actualiza todos los campos con los del DTO de actualización y devuelve el DTO de respuesta actualizado.

```ts
  @Put(':id')
  update(@Param('id') id: string, @Body() dto: UpdateUserDto): object {
    const numericId = Number(id);

    // Programación tradicional iterativa
    for (const user of this.users) {
      if (user.id === numericId) {
        user.name = dto.name;
        user.email = dto.email;

        return UserMapper.toResponse(user);
      }
    }

    return {
      error: 'UserModel not found',
    };

    // Programación funcional
    const user = this.users.find((item) => item.id === numericId);

    if (!user) {
      return {
        error: 'UserModel not found',
      };
    }

    user.name = dto.name;
    user.email = dto.email;

    return UserMapper.toResponse(user);
  }
```

---

## PATCH

Endpoint `PATCH` para actualizar parcialmente un usuario existente.

Busca el usuario por ID. Si no lo encuentra, devuelve un error.

Si lo encuentra, actualiza solo los campos proporcionados en el DTO de actualización parcial y devuelve el DTO de respuesta actualizado.

```ts
  @Patch(':id')
  partialUpdate(
    @Param('id') id: string,
    @Body() dto: PartialUpdateUserDto,
  ): object {
    const numericId = Number(id);

    // Programación tradicional iterativa
    for (const user of this.users) {
      // ESTE ES EL CAMBIO pero debería estar en un método aparte para evitar
      // duplicación de código y mejorar mantenibilidad con separación de
      // responsabilidades.
      if (user.id === numericId) {
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
      error: 'UserModel not found',
    };

    // Programación funcional
    // Búsqueda lineal del usuario por id
    const user = this.users.find((item) => item.id === numericId);

    if (!user) {
      return {
        error: 'UserModel not found',
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
```

---

## DELETE

Endpoint `DELETE` para eliminar un usuario por ID.

Busca el usuario en el arreglo y lo elimina si existe. Si no lo encuentra, devuelve un mensaje de error.

```ts
  @Delete(':id')
  delete(@Param('id') id: string): object {
    const numericId = Number(id);

    // Programación funcional
    const exists = this.users.some((item) => item.id === numericId);

    if (!exists) {
      return {
        error: 'User not found',
      };
    }

    this.users = this.users.filter((item) => item.id !== numericId);

    return {
      message: 'Deleted successfully',
    };
  }
}
```

---

# 8. Endpoints disponibles

| Método | Ruta             | Descripción                |
| ------ | ---------------- | -------------------------- |
| GET    | `/api/users`     | Lista usuarios             |
| GET    | `/api/users/:id` | Obtiene usuario            |
| POST   | `/api/users`     | Crea usuario               |
| PUT    | `/api/users/:id` | Reemplaza usuario completo |
| PATCH  | `/api/users/:id` | Actualiza parcialmente     |
| DELETE | `/api/users/:id` | Elimina usuario            |

---

# 9. Actividad práctica

En esta práctica se debe:

### 1. Corrección del POST `/api/users` para que el ID se genere automáticamente y no se reciba desde el cliente. El ID debe ser único para cada usuario creado.

### 2. Replicar toda la estructura para el recurso de productos.

Los campos del producto deben ser:

```ts
id: number;
name: string;
price: number;
stock: number;
createdAt: Date;
```

### 3. Implementar los 6 endpoints REST para productos

Con funcionamiento idéntico al de usuarios.

---

# 10. Resultados y evidencias

En la nueva entrada del README, se debe agregar:

### 1. Captura de consumo de endpoints de Products desde Postman.

Incluyendo:

* GET /api/products con 3 productos creados
* GET /api/products/:id con un producto existente
* DELETE /api/products/:id eliminando un producto existente
* DELETE /api/products/:id eliminando un producto que no existe

### 2. Todo lo adicional que indique el formato de entrega.
