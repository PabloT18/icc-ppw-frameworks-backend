# Programación y Plataformas Web

## Frameworks Backend: NestJS – API REST y CRUD Inicial

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nestjs/nestjs-original.svg" width="110" alt="Nest Logo"/>
</div>

---

# Práctica 3 (NestJS): Construcción de una API REST usando controladores, DTOs, modelos y mappers

### Autores

**Pablo Torres**
📧 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)
💻 GitHub: PabloT18

---

# 1. Introducción

En esta práctica se desarrolla un **CRUD REST completo** utilizando únicamente:

* controladores
* modelos
* DTOs
* mappers
* un arreglo en memoria como almacenamiento temporal

Aún **no** se utilizan:

* servicios (van en el tema 05)
* pipes de validación (tema 06)
* base de datos (tema 07)

El objetivo de este tema es comprender:

* cómo se estructuran los endpoints REST dentro de NestJS
* cómo se reciben datos mediante DTOs
* cómo se devuelve información usando DTOs de respuesta
* cómo un controlador puede administrar un CRUD básico antes de usar servicios

El módulo de ejemplo será **users/**.
En la parte práctica se replica todo para **products/**.

---

# 2. Estructura que se utilizará

Dentro de:

```
src/users/
```

se deben tener únicamente estas carpetas para este tema:

```
users/
 ├── controllers/
 ├── dtos/
 ├── entities/
 ├── mappers/
 └── users.module.ts   (ya creado en el tema anterior)
```

---

# 3. Modelo de dominio (Entidad sin base de datos)

En:

`src/users/entities/user.entity.ts`

Aquí se define la estructura interna del usuario, incluyendo campos que **no** se enviarán al cliente.

```ts
export class User {
  id: number;
  name: string;
  email: string;
  password: string; // campo interno, no se expone
  createdAt: Date;

  constructor(id: number, name: string, email: string, password: string) {
    this.id = id;
    this.name = name;
    this.email = email;
    this.password = password; 
    this.createdAt = new Date();
  }
}
```

---

# 4. DTOs de entrada (Request DTOs)

Los DTOs controlan **qué se recibe** desde el cliente.

---

## 4.1. DTO para crear un usuario

`src/users/dtos/create-user.dto.ts`

```ts
export class CreateUserDto {
  name: string;
  email: string;
}
```

---

## 4.2. DTO para actualizar completamente (PUT)

`src/users/dtos/update-user.dto.ts`

```ts
export class UpdateUserDto {
  name: string;
  email: string;
}
```

---

## 4.3. DTO para actualización parcial (PATCH)

`src/users/dtos/partial-update-user.dto.ts`

```ts
export class PartialUpdateUserDto {
  name?: string;
  email?: string;
}
```

---

# 5. DTO de salida (Response DTO)

Este DTO controla **qué campos se devuelven al cliente**.

`src/users/dtos/user-response.dto.ts`

```ts
export class UserResponseDto {
  id: number;
  name: string;
  email: string;
}
```

Note que este DTO **no** incluye `createdAt`.

---

# 6. Mapper para transformar Entidad ↔ DTO

En:

`src/users/mappers/user.mapper.ts`

Aquí se define la conversión entre:

* DTO → Entidad
* Entidad → DTO

```ts
export class UserMapper {
  static toEntity(id: number, dto: any) {
    return new User(id, dto.name, dto.email);
  }

  static toResponse(entity: User) {
    return {
      id: entity.id,
      name: entity.name,
      email: entity.email,
    };
  }
}
```

---

# 7. Controlador con CRUD completo

Ahora se construyen los endpoints REST.

Archivo:

`src/users/controllers/users.controller.ts`

```ts
import { Controller, Get, Post, Put, Patch, Delete, Param, Body } from '@nestjs/common';

@Controller('api/users')
export class UsersController {
  private users = [];
  private currentId = 1;

  @Get()
  findAll() {
    return this.users.map(u => UserMapper.toResponse(u));
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    const user = this.users.find(u => u.id === Number(id));
    if (!user) return { error: 'User not found' };

    return UserMapper.toResponse(user);
  }

  @Post()
  create(@Body() dto: CreateUserDto) {
    const entity = UserMapper.toEntity(this.currentId++, dto);
    this.users.push(entity);
    return UserMapper.toResponse(entity);
  }

c

  @Patch(':id')
  partialUpdate(@Param('id') id: string, @Body() dto: PartialUpdateUserDto) {
    const user = this.users.find(u => u.id === Number(id));
    if (!user) return { error: 'User not found' };

    if (dto.name !== undefined) user.name = dto.name;
    if (dto.email !== undefined) user.email = dto.email;

    return UserMapper.toResponse(user);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    const exists = this.users.some(u => u.id === Number(id));
    if (!exists) return { error: 'User not found' };

    this.users = this.users.filter(u => u.id !== Number(id));
    return { message: 'Deleted successfully' };
  }
}
```

---

# 8. Endpoints disponibles

| Método | Ruta             | Descripción                |
| ------ | ---------------- | -------------------------- |
| GET    | `/api/users`     | Lista usuarios             |
| GET    | `/api/users/:id` | Obtiene un usuario         |
| POST   | `/api/users`     | Crea usuario               |
| PUT    | `/api/users/:id` | Reemplaza usuario completo |
| PATCH  | `/api/users/:id` | Actualiza parcialmente     |
| DELETE | `/api/users/:id` | Elimina usuario            |

---

# 9. Actividad práctica

En esta práctica se:

1. Construye el CRUD completo para `users/`
2. Se verifica que el controlador funciona sin servicios ni base de datos
3. Se replica toda la estructura para el dominio:

```
products/
```

El módulo `products/` debe contener:

```
products/
 ├── controllers/
 ├── dtos/
 ├── entities/
 ├── mappers/
 └── products.module.ts
```

Y su controlador debe incluir **los mismos endpoints REST** que `users/`.

---

# 10. Resultados y evidencias

Cada estudiante debe agregar en su archivo:

### ✔ 1. Captura del consumo de cada endpoint de Products:

* GET /api/products
* GET /api/products/:id
* POST /api/products
* PUT /api/products/:id
* PATCH /api/products/:id
* DELETE /api/products/:id

![alt text](assets/imageF03.png)

![alt text](assets/imageF03-2.png)

![alt text](assets/imageF03-3.png)

![alt text](assets/imageF03-4.png)

![alt text](assets/imageF03-5.png)


### ✔ 2. Captura del archivo `products.controller.ts`

![alt text](assets/imageF03-6.png)

### ✔ 3. Explicación breve

Debe incluir:

* por qué se usa DTO de entrada y DTO de salida

En nuestro controlador se usan DTOs para controlar qué datos entran y cuáles salen de la API.

-> DTO de entrada (CreateUserDto)

    Se usa en @Body() para recibir datos del cliente.

    Define exactamente qué campos puede enviar el usuario (por ejemplo: name, email).

    Evita que el cliente envíe propiedades que no deberían modificarse, como id u otros campos internos.

    Facilita validaciones y reglas de negocio antes de crear o actualizar la entidad.

-> DTO de salida (Response DTO)

    Se genera con UserMapper.toResponseDto(user).

    Permite controlar la respuesta que se envía al cliente.

    Evita exponer datos internos o sensibles de la entidad.

* por qué la entidad no debe devolverse a la API

La entidad User representa el modelo interno del dominio, no el contrato de la API.

-> No devolver la entidad directamente es importante porque:

    Seguridad: la entidad puede tener campos sensibles o técnicos que no deben exponerse.

    Desacoplamiento: si cambia la entidad (base de datos, relaciones, campos internos), la API no se rompe.

    Control de la respuesta: puedes cambiar el formato del JSON sin modificar la entidad.

    Buenas prácticas de arquitectura: la entidad pertenece a la capa de dominio, no a la capa de presentación.

* cómo funciona el mapper

El mapper es el encargado de transformar datos entre capas.

En nuestro proyecto, UserMapper cumple tres funciones clave:

1. DTO → Entidad

  const entity: User = UserMapper.toEntity(this.currentId++, dto);

    Convierte los datos recibidos (CreateUserDto) en una entidad User.

    Asigna campos internos como id.

    Centraliza la lógica de creación del objeto de dominio.

2. Entidad → DTO de salida

  UserMapper.toResponseDto(user);

    Convierte la entidad en un objeto listo para la API.

    Filtra y da formato a los datos que se enviarán al cliente.

    Separación de responsabilidades

    El controlador no sabe cómo se construye la entidad ni cómo se arma la respuesta.

    El mapper se encarga de esa transformación, haciendo el código más limpio y mantenible.
