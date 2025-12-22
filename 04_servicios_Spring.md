

# Programación y Plataformas Web

# Frameworks Backend: Spring Boot – Servicios, Lógica de Negocio e Inyección de Dependencias

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg" width="100" alt="Spring Boot Logo">
</div>


# Práctica 4 (Spring Boot): Controladores + Servicios + Lógica de Negocio

### Autores

**Juan Alvarez - David Villa**

---

# 1. Introducción

En la práctica anterior (Práctica 3) se implementó un **CRUD REST completo** colocando toda la lógica dentro del controlador:

* creación de usuarios
* búsqueda
* actualización
* eliminación
* manejo del listado en memoria

Este enfoque funciona para aprender los endpoints, pero **no escala** en proyectos reales.

En esta práctica se introduce:

* servicios (`@Service`)
* inyección de dependencias
* separación de responsabilidades (SRP)
* traslado de la lógica del controlador al servicio
* arquitectura MVCS aplicada correctamente

El módulo de trabajo sigue siendo **users/**.
En la parte práctica se replica todo para **products/**.


# 2. Estructura del módulo con servicios

Carpeta objetivo:

```
src/main/java/ec/edu/ups/icc/fundamentos01/users/
```

La estructura ahora incluye:

```
users/
 ├── controllers/
 ├── dtos/
 ├── entities/
 ├── mappers/
 ├── services/
 │     ├── UserService.java
 │     └── UserServiceImpl.java
```

En este tema:

* el controlador queda reducido a **enrutar solicitudes y llamar al servicio**
* la lógica de negocio se mueve a **UserServiceImpl**
* la lista en memoria ahora vive dentro del **servicio**


# 3. Definición del Servicio (Interfaz)

Archivo:
`services/UserService.java`

Su función es declarar **qué operaciones ofrece el módulo**, sin implementar nada aún.

```java

public interface UserService {

    List<UserResponseDto> findAll();

    Object findOne(int id);

    UserResponseDto create(CreateUserDto dto);

    Object update(int id, UpdateUserDto dto);

    Object partialUpdate(int id, PartialUpdateUserDto dto);

    Object delete(int id);
}
```


# 4. Implementación del Servicio

Archivo:
`services/UserServiceImpl.java`

Aquí se mueve toda la lógica antes ubicada en el controlador:

```java

@Service
public class UserServiceImpl implements UserService {

    private List<User> users = new ArrayList<>();
    private int currentId = 1;

    @Override
    public List<UserResponseDto> findAll() {
        return users.stream().map(UserMapper::toResponse).toList();
    }

    @Override
    public Object findOne(int id) {
        return users.stream()
                .filter(u -> u.getId() == id)
                .findFirst()
                .map(UserMapper::toResponse)
                .orElseGet(() -> new Object() { public String error = "User not found"; });
    }

    @Override
    public UserResponseDto create(CreateUserDto dto) {
        User user = UserMapper.toEntity(currentId++, dto.name, dto.email);
        users.add(user);
        return UserMapper.toResponse(user);
    }

    @Override
    public Object update(int id, UpdateUserDto dto) {
        User user = users.stream().filter(u -> u.getId() == id).findFirst().orElse(null);
        if (user == null) return new Object() { public String error = "User not found"; };

        user.setName(dto.name);
        user.setEmail(dto.email);

        return UserMapper.toResponse(user);
    }

    @Override
    public Object partialUpdate(int id, PartialUpdateUserDto dto) {
        User user = users.stream().filter(u -> u.getId() == id).findFirst().orElse(null);
        if (user == null) return new Object() { public String error = "User not found"; };

        if (dto.name != null) user.setName(dto.name);
        if (dto.email != null) user.setEmail(dto.email);

        return UserMapper.toResponse(user);
    }

    @Override
    public Object delete(int id) {
        boolean removed = users.removeIf(u -> u.getId() == id);
        if (!removed) return new Object() { public String error = "User not found"; };

        return new Object() { public String message = "Deleted successfully"; };
    }
}
```


# 5. Inyección del Servicio en el Controlador

Archivo:
`controllers/UsersController.java`

El controlador ahora queda limpio:

```java
//.....
public class UsersController {

    private final UserService service;

    public UsersController(UserService service) {
        this.service = service;
    }

   // TODO: actualizar endpoints que llaman a service
}
```


# 6. ¿Por qué se implementa así?

Separar controlador → servicio cumple estos objetivos:

### Mantener el controlador pequeño

El controlador solo enruta solicitudes y devuelve respuestas.

### Reutilizar lógica

Si otro controlador necesitara lógica de usuarios, solo depende del servicio.

### Facilitar pruebas unitarias

El servicio se puede probar sin levantar el servidor.

### Preparar el camino para una base de datos real

Pronto se reemplazará:

```
List<User> users
```

por:

```
UserRepository (Spring Data JPA)
```

y el controlador seguirá funcionando igual.


# 7. Flujo completo después de aplicar servicios

```
Cliente
  ↓
Controlador (recibe DTO)
  ↓ llama →
Servicio (reglas, validaciones, lógica)
  ↓ usa →
Entidad + Mapper
  ↓
Controlador (retorna DTO de respuesta)
  ↓
Cliente
```

Esto refleja el patrón MVCS aplicado correctamente.


# 8. Endpoints disponibles

| Método | Ruta             | Descripción                |
| ------ | ---------------- | -------------------------- |
| GET    | `/api/users`     | Lista usuarios             |
| GET    | `/api/users/:id` | Obtiene usuario            |
| POST   | `/api/users`     | Crea usuario               |
| PUT    | `/api/users/:id` | Reemplaza usuario completo |
| PATCH  | `/api/users/:id` | Actualiza parcialmente     |
| DELETE | `/api/users/:id` | Elimina usuario            |


# 9. Actividad práctica

Los estudiantes deben replicar toda la estructura anterior para el módulo:

```
products/
```

Creando:

```
controllers/
dtos/
entities/
mappers/
services/
    ProductService.java
    ProductServiceImpl.java
```

Y deben implementar **los mismos 6 endpoints REST**, trasladando la lógica del controlador al servicio.


# 10. Resultados y evidencias

Cada estudiante debe entregar:

### 2. Captura del `constructor`  archivo

![alt text](nest/p67/alvarez_villa/assets/Productoscontroller.java.jpeg)

### 3. Captura completa del archivo

![alt text](nest/p67/alvarez_villa/assets/Producto1.jpeg)

![alt text](nest/p67/alvarez_villa/assets/Producto2.jpeg)


### 4. Explicación breve

**Por qué se usa un servicio**
- Se utiliza un servicio para separar la lógica de negocio del controlador. El servicio es el encargado de realizar las operaciones principales del sistema, como crear, buscar, actualizar o eliminar datos. De esta manera, el controlador no se encarga de cómo se procesan los datos, sino únicamente de recibir las solicitudes y delegarlas al servicio correspondiente. Esta separación mejora la organización del código y facilita su mantenimiento.

**Qué ventajas aporta MVCS**

La arquitectura MVC(S) permite dividir la aplicación en capas con responsabilidades claras:

- Modelo: representa los datos y la lógica relacionada.

- Vista: se encarga de la presentación de la información.

- Controlador: gestiona las peticiones del cliente.

- Servicio (S): contiene la lógica de negocio.

Asi reduce el acoplamiento entre componentes, mejora la escalabilidad del sistema y facilita la reutilización del código. Además, hace que el proyecto sea más ordenado y comprensible, especialmente en aplicaciones backend como las desarrolladas con Spring Boot.

**Por qué el controlador ahora está más limpio**

- El controlador está más limpio porque ya no contiene lógica de negocio ni manejo directo de datos. Su función principal es recibir las solicitudes HTTP, llamar al servicio correspondiente y devolver la respuesta. Al delegar la lógica al servicio, el código del controlador se vuelve más simple, legible y fácil de mantener, cumpliendo con el principio de responsabilidad única.

