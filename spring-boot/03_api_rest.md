# Programación y Plataformas Web

# Frameworks Backend: Spring Boot – API REST y CRUD Inicial sin Servicios

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg" width="100" alt="Spring Boot Logo">
</div>

---

# Práctica 3 (Spring Boot): Construcción de una API REST usando controladores, DTOs, modelos y mappers

### Autores

**Pablo Torres**

 📧 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

 💻 GitHub: PabloT18

---

# 1. Introducción

En esta práctica se construye un **CRUD REST completo** usando únicamente:

* controladores (`@RestController`)
* modelos (entidades sin BD)
* DTOs de entrada y salida
* mappers para transformar datos
* almacenamiento en memoria con `List<User>`

Aún **no se utiliza**:

* servicios (`@Service`)
* repositorios JPA
* base de datos

El objetivo de esta práctica es comprender:

* cómo se estructuran endpoints REST en Spring Boot
* cómo se reciben datos con DTOs
* cómo se retorna información segura con DTOs de respuesta
* cómo implementar CRUD desde el controlador antes de aplicar MVCS completo

El módulo de ejemplo será **users/**.
En la parte práctica cada estudiante deberá replicarlo para **products/**.

---

# 2. Estructura que se usará

Dentro de:

```
src/main/java/ec/edu/ups/icc/fundamentos01/users/
```

solo se usarán estas carpetas en este tema:

```
users/
 ├── controllers/
 ├── dtos/
 ├── entities/
 ├── mappers/
```

> **No se crean servicios todavía.**
> Se mantienen las clases simples para aprender la API REST base.

---

# 3. Modelo de dominio (Entidad sin base de datos)

Archivo:

`src/.../users/entities/User.java`

Aquí se define el modelo interno del usuario, incluyendo campos que **no se enviarán al cliente**:

```java
package ec.edu.ups.icc.fundamentos01.users.entities;

public class User {

    private int id;
    private String name;
    private String email;
    private String password; // no se expone en la API
    private String createdAt;

    public User(int id, String name, String email, String password) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.password = password;
        this.createdAt = java.time.LocalDateTime.now().toString();
    }

    // getters y setters
}
```

---

# 4. DTOs de entrada (para recibir datos)

Los DTOs controlan **qué datos acepta la API**. Dependiendo del endpoint, y de si es creación o actualización, se usan distintos DTOs. No suelen ser idénticos a la entidad, ni tampoco se usan siempre todos los campos o de uno para cada acción pero siempre es la mejor practica definir DTOs específicos por **principio de responsabilidad única**. 

---

## 4.1. DTO para crear usuario

Archivo:
`dtos/CreateUserDto.java`

```java
package ec.edu.ups.icc.fundamentos01.users.dtos;

public class CreateUserDto {
    public String name;
    public String email;
}
```

---

## 4.2. DTO para actualizar completamente (PUT)

Archivo:
`dtos/UpdateUserDto.java`

```java
package ec.edu.ups.icc.fundamentos01.users.dtos;

public class UpdateUserDto {
    public String name;
    public String email;
}
```

---

## 4.3. DTO para actualización parcial (PATCH)

Archivo:
`dtos/PartialUpdateUserDto.java`

```java
package ec.edu.ups.icc.fundamentos01.users.dtos;

public class PartialUpdateUserDto {
    public String name;
    public String email;
}
```

> Igual que en NestJS, **el ID no se coloca en el DTO** porque viene en la ruta del endpoint.

---

# 5. DTO de salida (Response DTO)

Este DTO define **qué datos se devuelven al cliente**.

Archivo:
`dtos/UserResponseDto.java`

```java
package ec.edu.ups.icc.fundamentos01.users.dtos;

public class UserResponseDto {
    public int id;
    public String name;
    public String email;
}
```

> No se expone: `password`, `createdAt` ni ningún dato interno.

---

# 6. Mapper User ↔ DTO

Archivo:
`mappers/UserMapper.java`

```java
package ec.edu.ups.icc.fundamentos01.users.mappers;

import ec.edu.ups.icc.fundamentos01.users.entities.User;
import ec.edu.ups.icc.fundamentos01.users.dtos.UserResponseDto;

public class UserMapper {

    public static User toEntity(int id, String name, String email) {
        return new User(id, name, email, "secret");
    }

    public static UserResponseDto toResponse(User user) {
        UserResponseDto dto = new UserResponseDto();
        dto.id = user.getId();
        dto.name = user.getName();
        dto.email = user.getEmail();
        return dto;
    }
}
```

---

# 7. Controlador con CRUD completo

Archivo:
`controllers/UsersController.java`


Clase controladora donde se implementan todos los endpoints REST:
Se empieza creado solo un Lista que simula la base de datos en memoria.
```java
package ec.edu.ups.icc.fundamentos01.users.controllers;

@RestController
@RequestMapping("/api/users")
public class UsersController {

    private List<User> users = new ArrayList<>();
    private int currentId = 1;
```


## GET Users
Este endpoint devuelve la lista de usuarios mapeados a DTOs de respuesta.
```java
    @GetMapping
    public List<UserResponseDto> findAll() {

        // Programación tradicional iterativa para mapear cada User a UserResponseDto
        List<UserResponseDto> dtos = new ArrayList<>();
        for (User user : users) {
            dtos.add(UserMapper.toResponse(user));
        }
        return dtos;

        // Programación funcional para mapear cada User a UserResponseDto
        return users.stream()
                .map(UserMapper::toResponse)
                .toList();
    }
```

## GET User por ID
Aqui se obtiene un usuario por su ID. buscamos en la lista y si no se encuentra devolvemos un mensaje de error.

Si quieren un mejor rendimiento podrían usar:
* Busqueda binaria si la lista está ordenada por ID. Pedir al repositorio la consulta ordenada por ID o un valor especifico.

* `Map<Integer, User>` en lugar de una `List<User>`. con un HashMap la búsqueda por ID sería O(1) en promedio. Mas costo en complejidad espacial.

```java
    @GetMapping("/{id}")
    public Object findOne(@PathVariable int id) {

      // Programación tradicional iterativa para mapear cada User a UserResponseDto
      // Busqueda Lineal
        for (User user : users) {
            if (user.getId() == id) {
                return UserMapper.toResponse(user);
            }
        }
        return new Object() {
            public String error = "User not found";
        };

      // Programación funcional para mapear cada User a UserResponseDto
      // Busqueda Lineal
        return users.stream()
                .filter(u -> u.getId() == id)
                .findFirst()
                .map(UserMapper::toResponse)
                .orElseGet(() -> new Object() {
                    public String error = "User not found";
                });
    }
```

## POST
Este endpoint crea un nuevo usuario a partir del DTO de creación. Usa los atributos de `CreateUserDto` para crear la entidad `User`, asigna un ID único y lo agrega a la lista en memoria. Finalmente, devuelve el DTO de respuesta del usuario creado.

* El ID deberia ser secuencial o generado por la base de datos en un entorno real.
```java
    @PostMapping
    public UserResponseDto create(@RequestBody CreateUserDto dto) {
        User user = UserMapper.toEntity(currentId++, dto.name, dto.email);
        users.add(user);
        return UserMapper.toResponse(user);
    }
```


## PUT
Endpoint `PUT` para reemplazar completamente un usuario existente. Busca el usuario por ID, si no lo encuentra devuelve un error. Si lo encuentra, actualiza todos los campos con los del DTO de actualización y devuelve el DTO de respuesta actualizado.
```java
    @PutMapping("/{id}")
    public Object update(@PathVariable int id, @RequestBody UpdateUserDto dto) {

        // Programacion tradicional iterativa
        for (User user : users) {
            if (user.getId() == id) {
                user.setName(dto.name);
                user.setEmail(dto.email);
                return UserMapper.toResponse(user);
            }
        }
        return new Object() { 
            public String error = "User not found"; 
        };
      
        // Programacion funcional
        User user = users.stream().filter(u -> u.getId() == id).findFirst().orElse(null);
        if (user == null) return new Object() { public String error = "User not found"; };

        user.setName(dto.name);
        user.setEmail(dto.email);

        return UserMapper.toResponse(user);
    }
```
## PATCH
Endpoint `PATCH` para actualizar parcialmente un usuario existente. Busca el usuario por ID, si no lo encuentra devuelve un error. Si lo encuentra, actualiza solo los campos proporcionados en el DTO de actualización parcial y devuelve el DTO de respuesta actualizado.
```java

    @PatchMapping("/{id}")
    public Object partialUpdate(@PathVariable int id, @RequestBody PartialUpdateUserDto dto) {

      // Programacion tradicional iterativa
        for (User user : users) {
          // ESTE ES EL CAMBIO pero deberia estar en un metodo aparte para evitar duplicacion de codigo y mejorar mantenibilidad con separacion de responsabilidades.
            if (user.getId() == id) {
                if (dto.name != null) user.setName(dto.name);
                if (dto.email != null) user.setEmail(dto.email);
                return UserMapper.toResponse(user);
            }
        }
        return new Object() { 
            public String error = "User not found"; 
        };
// Programacion funcional
        User user = users.stream().filter(u -> u.getId() == id).findFirst().orElse(null);
        if (user == null) return new Object() { public String error = "User not found"; };

        if (dto.name != null) user.setName(dto.name);
        if (dto.email != null) user.setEmail(dto.email);

        return UserMapper.toResponse(user);
    }
```

## DELETE
// Endpoint `DELETE` para eliminar un usuario por ID. Busca el usuario en la lista y lo elimina si existe. Si no lo encuentra, devuelve un mensaje de error.
```java

    @DeleteMapping("/{id}")
    public Object delete(@PathVariable int id) {
      // Programacion tradicional iterativa
        Iterator<User> iterator = users.iterator();
        while (iterator.hasNext()) {
            User user = iterator.next();
            if (user.getId() == id) {
                iterator.remove();
                return new Object() { public String message = "Deleted successfully"; };
            }
        }
        return new Object() { public String error = "User not found"; };
      // Programacion funcional
        boolean exists = users.removeIf(u -> u.getId() == id);
        if (!exists) return new Object() { public String error = "User not found"; };

        return new Object() { public String message = "Deleted successfully"; };
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

Los estudiantes deben:

### 1. Replicar toda la estructura para el módulo:

```
products/
```

Con las carpetas:

```
controllers/
dtos/
entities/
mappers/
```

### 2. Implementar los 6 endpoints REST para productos

Con funcionamiento idéntico al de usuarios.

---

# 10. Resultados y evidencias

Cada estudiante debe entregar:

### 1. Captura de consumo de endpoints de Products desde Postman.

Incluyendo:

* GET /api/products
* GET /api/products/:id
* POST /api/products
* PUT /api/products/:id
* PATCH /api/products/:id
* DELETE /api/products/:id

### 2. Captura del archivo

`products.controller.java`

Mostrando toda la estructura.

### 3. Explicación breve

Incluyendo:

* por qué existen DTOs distintos para entrada y salida
* por qué la entidad nunca se devuelve al cliente
* cómo funciona el mapper
