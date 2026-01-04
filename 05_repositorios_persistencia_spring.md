

# Programación y Plataformas Web

# **Spring Boot – Persistencia con JPA, Entidades, Repositorios y Conexión a Base de Datos**

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg" width="95">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="95">
</div>

## **Práctica 5 (Spring Boot): Persistencia real con PostgreSQL, Entidades JPA y Repositorios**

### **Autores**

**Juan Alvarez - David Villa**



---

# **1. Instalación y Preparación del Entorno (Dependencias y Configuración)**

Para utilizar una base de datos real con Spring Boot se necesitan:

1. **Dependencia JPA (Hibernate)**
2. **Driver PostgreSQL**
3. **Conexión en `application.yml`**
4. **Base de datos en ejecución (Docker recomendado, tema 05-B)**

## **1.1. Dependencias necesarias en `build.gradle`**

Agregar las siguientes líneas en la sección de dependencias: 

```kotlin
dependencies {
    // ... Dependencias existentes ...
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    runtimeOnly("org.postgresql:postgresql")
}
```


## **1.2. Configuración de conexión en `application.yml`**

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/devdb
    username: ups
    password: ups123
  jpa:
    hibernate:
      ddl-auto: update
    properties:
      hibernate:
        format_sql: true
        dialect: org.hibernate.dialect.PostgreSQLDialect

server:
  port: 8080
```

### **Explicación de cada propiedad**

#### **spring.datasource** – Configuración de la fuente de datos

```yaml
url: jdbc:postgresql://localhost:5432/devdb
```
* **url**: Cadena de conexión JDBC que especifica:
  * `jdbc:postgresql://` → Protocolo JDBC para PostgreSQL
  * `localhost:5432` → Host y puerto donde se ejecuta PostgreSQL (5432 es el puerto por defecto)
  * `devdb` → Nombre de la base de datos a la que se conectará la aplicación

```yaml
username: ups
password: ups123
```
* **username**: Usuario de PostgreSQL que tiene permisos sobre la base de datos
* **password**: Contraseña del usuario especificado

#### **spring.jpa.hibernate** – Configuración de Hibernate

```yaml
ddl-auto: update
```
* **ddl-auto**: Define cómo Hibernate gestiona el esquema de la base de datos al iniciar la aplicación
* Valores posibles:
  * `update` → **Actualiza** las tablas existentes (agrega columnas nuevas, pero NO elimina columnas existentes). Recomendado para desarrollo.
  * `create` → Crea el esquema desde cero cada vez (destruye datos previos)
  * `create-drop` → Crea al iniciar y elimina al cerrar la aplicación
  * `validate` → Solo valida que el esquema coincida con las entidades (no modifica la BD)
  * `none` → No realiza ninguna acción automática

#### **spring.jpa.properties.hibernate** – Propiedades avanzadas

```yaml
format_sql: true
```
* **format_sql**: Formatea el SQL generado por Hibernate en los logs para que sea legible
* Útil para debugging y aprendizaje
* En producción suele establecerse en `false`

```yaml
dialect: org.hibernate.dialect.PostgreSQLDialect
```
* **dialect**: Indica a Hibernate qué dialecto SQL utilizar
* PostgreSQL tiene funciones y sintaxis específicas diferentes a MySQL, Oracle, etc.
* Hibernate genera SQL optimizado para PostgreSQL
* Spring Boot lo detecta automáticamente, pero es buena práctica especificarlo

#### **server.port** – Configuración del servidor

```yaml
port: 8080
```
* **port**: Puerto donde se ejecutará la aplicación Spring Boot
* Por defecto es 8080
* Se puede cambiar a cualquier puerto disponible (ej: 9000, 3000)

### **¿Por qué es importante esta configuración?**

1. **Conexión automática**: Spring Boot lee este archivo al iniciar y establece la conexión con PostgreSQL
2. **Desarrollo ágil**: Con `ddl-auto: update`, las tablas se crean/actualizan automáticamente según las entidades
3. **Debugging facilitado**: `format_sql: true` permite ver exactamente qué SQL ejecuta Hibernate
4. **Portabilidad**: Cambiar de base de datos solo requiere modificar estas propiedades
5. **Centralización**: Todas las configuraciones de conexión en un solo lugar

### **Ubicación del archivo**

Este archivo debe estar en:

```
src/main/resources/application.yml
```

Spring Boot lo detecta automáticamente al iniciar la aplicación.


## **1.3. Requisitos previos**

La base debe existir antes de iniciar Spring:

```
Base: devdb
Usuario: ups
Contraseña: ups123
```

Creada mediante Docker según:

* [`docs/05_b_instalacion_postgres_docker.md`](../../../docs/05_b_instalacion_postgres_docker.md)




# **2. Modelo vs Entidad Persistente: Diferencias**

Hasta el tema anterior se trabajó con:

### Un **modelo User** sin anotaciones, usado solo en memoria.

Ese modelo **no sirve para persistencia** porque:

* no posee anotaciones JPA
* no representa una tabla
* no tiene ID gestionado por BD
* no funciona con Hibernate
* no debe usarse como entidad pública ni de dominio

Por lo tanto, en este tema se crea **por primera vez una entidad real User**.

Además, para mantener separación de capas se utilizará un:

### Mapper / Factory / Builder

para convertir:

```
DTO → Modelo de dominio → Entidad persistente
Entidad persistente → DTO
```

Este patrón permite independencia total entre dominio y base de datos.


# **3. Superclase de Auditoría (BaseModel)**

Todas las entidades deben tener:

* id autogenerado
* fechas de creación / actualización
* marca lógica de eliminado

Se implementa este patrón mediante `@MappedSuperclass`.

Archivo:
`src/core/entities/BaseModel.java`

![
    
](../../../docs/assets/06_repositorios_bd-05.png)
```java
@MappedSuperclass
public abstract class BaseModel {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    private boolean deleted;

    @PrePersist
    protected void onCreate() {
        this.deleted = false;
        this.createdAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        this.updatedAt = LocalDateTime.now();
    }

    // Getters y Setters
}


```

Esta superclase:

* no genera tabla propia
* es heredada por todas las entidades persistentes
* ofrece auditoría automática
* unifica estructura del sistema


# **4. ORM (JPA + Hibernate): Creación de la entidad persistente User**

Archivo:
`entities/UserEntity.java`

```java
@Entity
@Table(name = "users")
public class UserEntity extends BaseModel {

    @Column(nullable = false, length = 150)
    private String name;

    @Column(nullable = false, unique = true, length = 150)
    private String email;

    @Column(nullable = false)
    private String password;
}
```

Explicación de anotaciones:

| Anotación                    | Función                                     |
| ---------------------------- | ------------------------------------------- |
| `@Entity`                    | La clase es una tabla de BD                 |
| `@Table`                     | Define el nombre de la tabla                |
| `@Column`                    | Configura columnas, nulabilidad, longitudes |
| `@Id` (heredado)             | PK de la tabla                              |
| `@GeneratedValue`            | Autoincremento                              |
| `@PrePersist` / `@PreUpdate` | Hooks automáticos de auditoría              |


# **5. Repositorios**

Los repositorios reemplazan completamente las listas en memoria.

### **Repositorio de usuarios**

Archivo:
`repositories/UserRepository.java`

```java
@Repository
public interface UserRepository extends JpaRepository<UserEntity, Long> {

    Optional<UserEntity> findByEmail(String email);
}
```

### **¿Por qué se usa `JpaRepository<UserEntity, Long>`?**

La interfaz `JpaRepository` utiliza **genéricos** para especificar dos tipos:

```java
JpaRepository<T, ID>
```

Donde:
* **T** → Tipo de la entidad que el repositorio gestionará
* **ID** → Tipo del identificador (Primary Key) de esa entidad

#### **En nuestro caso: `JpaRepository<UserEntity, Long>`**

```java
JpaRepository<UserEntity, Long>
          ↑            ↑
       Entidad    Tipo del ID
```

**1. UserEntity (primer genérico)**
* Indica que este repositorio trabajará con la entidad `UserEntity`
* Todos los métodos automáticos operarán sobre esta entidad
* Spring Data JPA genera el SQL específico para la tabla `users`
* Los métodos devolverán `UserEntity` o colecciones de `UserEntity`

**2. Long (segundo genérico)**
* Especifica que el tipo del ID de `UserEntity` es `Long`
* En `BaseModel` se definió: `private Long id;`
* Los métodos que buscan por ID (`findById`, `deleteById`) esperarán un `Long`
* Si el ID fuera `Integer`, `String` o `UUID`, se especificaría ese tipo

### **Métodos automáticos proporcionados por JpaRepository**

Al extender `JpaRepository`, Spring Data JPA proporciona automáticamente:

#### **Métodos CRUD básicos**
```java
// Guardar
UserEntity save(UserEntity entity)
List<UserEntity> saveAll(Iterable<UserEntity> entities)

// Buscar
Optional<UserEntity> findById(Long id)
List<UserEntity> findAll()
boolean existsById(Long id)
long count()

// Eliminar
void deleteById(Long id)
void delete(UserEntity entity)
void deleteAll()
```

#### **Métodos con paginación y ordenamiento**
```java
Page<UserEntity> findAll(Pageable pageable)
List<UserEntity> findAll(Sort sort)
```

#### **Métodos personalizados por convención**
```java
// Spring genera automáticamente el SQL basándose en el nombre del método
Optional<UserEntity> findByEmail(String email)
// Genera: SELECT * FROM users WHERE email = ?

List<UserEntity> findByNameContaining(String name)
// Genera: SELECT * FROM users WHERE name LIKE %?%

Optional<UserEntity> findByEmailAndName(String email, String name)
// Genera: SELECT * FROM users WHERE email = ? AND name = ?
```

### **¿Cómo funciona la magia de Spring Data JPA?**

1. **En tiempo de ejecución**, Spring detecta la interfaz `UserRepository`
2. Spring Data JPA **genera automáticamente una implementación** de esa interfaz
3. Los métodos como `findByEmail` se traducen a SQL usando:
   * El nombre del método (`findBy...`)
   * Los atributos de la entidad (`email`)
   * Los parámetros del método (`String email`)
4. Hibernate ejecuta el SQL contra PostgreSQL
5. Los resultados se mapean automáticamente a objetos `UserEntity`

### **Ventajas de usar JpaRepository**

* **Sin código repetitivo**: No se escriben consultas básicas
* **Type-safe**: El compilador verifica que los tipos sean correctos
* **Consistencia**: Todos los repositorios siguen el mismo patrón
* **Productividad**: Se enfoca en lógica de negocio, no en SQL básico
* **Mantenibilidad**: Spring gestiona las implementaciones
* **Testing**: Fácil de mockear en pruebas unitarias

Hibernate genera el SQL automáticamente.


# **6. Transformaciones: Patrón Factory Method en la Clase de Dominio**

Los servicios NO deben devolver entidades directamente.

### **¿Qué patrón usar para las conversiones?**

En temas anteriores se usó un **Mapper** separado. Ahora se introduce el **Factory Method Pattern** directamente en la clase de dominio `User`.

Este patrón permite que la clase `User` sea responsable de:
* Crear instancias desde DTOs
* Crear instancias desde Entidades JPA
* Convertirse a Entidad persistente
* Convertirse a DTO de respuesta

### **Ventajas del Factory Method en la clase de dominio**

* **Encapsulación**: La lógica de conversión está donde pertenece
* **Cohesión**: La clase conoce cómo construirse desde diferentes fuentes
* **Menos clases**: No se necesita un Mapper separado
* **Claridad**: `User.fromDto()` es más explícito que `UserMapper.toEntity()`

### **Implementación del patrón**

Archivo:
`models/User.java`

```java
public class User {

     /// Variables de instancia

    /// Constructores 

    // Getters y Setters

    // ==================== FACTORY METHODS ====================

    /**
     * Crea un User desde un DTO de creación
     * @param dto DTO con datos del formulario
     * @return instancia de User para lógica de negocio
     */
    //public static User fromDto(CreateUserDto dto) {
      

    /**
     * Crea un User desde una entidad persistente
     * @param entity Entidad recuperada de la BD
     * @return instancia de User para lógica de negocio
     */
    public static User fromEntity(UserEntity entity) {
        return new User(
            entity.getId().intValue(),
            entity.getName(),
            entity.getEmail(),
            entity.getPassword()
        );
    }

    // ==================== CONVERSION METHODS ====================

    /**
     * Convierte este User a una entidad persistente
     * @return UserEntity lista para guardar en BD
     */
    public UserEntity toEntity() {
        UserEntity entity = new UserEntity();
        if (this.id > 0) {
            entity.setId((long) this.id);
        }
        entity.setName(this.name);
        entity.setEmail(this.email);
        entity.setPassword(this.password);
        return entity;
    }

    /**
     * Convierte este User a un DTO de respuesta
     * @return DTO sin información sensible
     */
    /// public UserResponseDto toResponseDto() {
        
}
```

### **Flujo de conversión con Factory Methods**

```
1. Cliente → CreateUserDto
   ↓
2. User.fromDto(dto) → User (dominio)
   ↓
3. user.toEntity() → UserEntity
   ↓
4. repository.save(entity) → BD
   ↓
5. User.fromEntity(entity) → User
   ↓
6. user.toResponseDto() → UserResponseDto
   ↓
7. Cliente
```

### **Uso en el servicio**

```java
@Service
public class UserServiceImpl implements UserService {

    private final UserRepository repo;

    public UserServiceImpl(UserRepository repo) {
        this.repo = repo;
    }

    @Override
    public UserResponseDto create(CreateUserDto dto) {
        // 1. DTO → User (dominio)
        User user = User.fromDto(dto);
        
        // 2. User → UserEntity
        UserEntity entity = user.toEntity();
        
        // 3. Guardar en BD
        UserEntity saved = repo.save(entity);
        
        // 4. UserEntity → User → DTO
        return User.fromEntity(saved).toResponseDto();
    }
}
```

### **¿Cuándo usar Factory Methods vs Mapper separado?**

| Situación | Usar Factory Methods | Usar Mapper separado |
|-----------|---------------------|----------------------|
| Conversiones simples | ✅ Sí | ❌ Excesivo |
| Lógica de conversión compleja | ❌ No, clase muy grande | ✅ Sí |
| Múltiples formatos de entrada/salida | ❌ Dificulta la clase | ✅ Sí |
| Aplicación empresarial grande | ⚠️ Evaluar | ✅ Sí, mejor separación |

Para este tema se usa **Factory Methods** por claridad didáctica. En temas avanzados se puede migrar a Mappers separados o usar librerías como **MapStruct**.


# **7. Integración del Repositorio en el Servicio**

El servicio deja de usar:

```java
//Elimnar
private List<User> users = new ArrayList<>();
private int currentId = 1;
```

Y empieza a usar:

```java
private final UserRepository userRepository
```

Archivo:
`services/UserServiceImpl.java`

```java
@Service
public class UserServiceImpl implements UserService {
  
    private final UserRepository userRepo;

    public UserServiceImpl(UserRepository userRepo) {
        this.userRepo = userRepo;
    }

    // Actualizar código de los métodos para usar userRepo
    // 
    @Override
    public List<UserResponseDto> findAll() {

        // 1. El repositorio devuelve entidades JPA (UserEntity)
        return userRepo.findAll()
            .stream()

            // 2. Cada UserEntity se transforma en un modelo de dominio User
            //    Aquí se desacopla la capa de persistencia de la lógica de negocio
            .map(User::fromEntity)

            // 3. El modelo de dominio se convierte en DTO de respuesta
            //    Solo se exponen los campos permitidos por la API
            .map(UserMapper::toResponse)

            // 4. Se recopila el resultado final como una lista de DTOs
            .toList();
    }

    //Forma iterativa tradicional
     @Override
    public List<UserResponseDto> findAll() {

        // Lista final que se devolverá al controlador
        List<UserResponseDto> response = new ArrayList<>();

        // 1. Obtener todas las entidades desde la base de datos
        List<UserEntity> entities = userRepo.findAll();

        // 2. Iterar sobre cada entidad
        for (UserEntity entity : entities) {

            // 3. Convertir la entidad en modelo de dominio
            User user = User.fromEntity(entity);

            // 4. Convertir el modelo de dominio en DTO de respuesta
            UserResponseDto dto = UserMapper.toResponse(user);

            // 5. Agregar el DTO a la lista de resultados
            response.add(dto);
        }

        // 6. Retornar la lista final de DTOs
        return response;
    }



    @Override
    public UserResponseDto findOne(int id) {
        return userRepo.findById((long) id)
                .map(User::fromEntity)
                .map(UserMapper::toResponse)
                .orElseThrow(() -> new IllegalStateException("Usuario no encontrado"));
    }



 @Override
    public UserResponseDto create(CreateUserDto dto) {
        return Optional.of(dto)
                .map(UserMapper::fromCreateDto)
                .map(User::toEntity)
                .map(userRepo::save)
                .map(User::fromEntity)
                .map(UserMapper::toResponse)

                .orElseThrow(() -> new IllegalStateException("Error al crear el usuario"));
    }




}
```


El metodo `update()` puede ser:

```java
   @Override
    public UserResponseDto update(int id, UpdateUserDto dto) {
        Optional<UserEntity> userEntity= userRepo.findById((long) id);
       if(!userEntity.isPresent()){
        throw new IllegalStateException("Usuario no encontrado");
       }      
       userEntity.get().setName(dto.name);
         userEntity.get().setEmail(dto.email);

        userRepo.save(userEntity.get());

        User responseDto = User.fromEntity(userEntity.get());
        UserResponseDto dtoResponse = UserMapper.toResponse(responseDto);
        return dtoResponse;
    }
```

o su forma funcional 

```java
@Override
public UserResponseDto update(int id, UpdateUserDto dto) {

    return userRepo.findById((long) id)
        // Entity → Domain
        .map(User::fromEntity)

        // Aplicar cambios permitidos en el dominio
        .map(user -> user.update(dto))

        // Domain → Entity
        .map(User::toEntity)

        // Persistencia
        .map(userRepo::save)

        // Entity → Domain
        .map(User::fromEntity)

        // Domain → DTO
        .map(UserMapper::toResponse)

        // Error controlado si no existe
        .orElseThrow(() -> new IllegalStateException("Usuario no encontrado"));
}

```

Para hay que crear el metodo `update()` en la clase de dominio `User`:

```java
public User update(UpdateUserDto dto) {
    this.name = dto.name;
    this.email = dto.email;    
    this.password = dto.password;
    return this;
}
```

Siendo esta la mejor ya que :


* Mantiene un flujo coherente en todo el servicio.
* El service no toca JPA directamente.
* La lógica de actualización queda en el modelo de dominio.
* Es consistente con create y findAll.
* Facilita agregar reglas de negocio sin romper capas.


 El metodo `partialUpdate()` puede ser, su metodo funcional:

```java 
@Override
public UserResponseDto partialUpdate(int id, PartialUpdateUserDto dto) {

    return userRepo.findById((long) id)
        // Entity → Domain
        .map(User::fromEntity)

        // Aplicar solo los cambios presentes
        .map(user -> user.partialUpdate(dto))

        // Domain → Entity
        .map(User::toEntity)

        // Persistencia
        .map(userRepo::save)

        // Entity → Domain
        .map(User::fromEntity)

        // Domain → DTO
        .map(UserMapper::toResponse)

        // Error si no existe
        .orElseThrow(() -> new IllegalStateException("Usuario no encontrado"));
}
```

Para hay que crear el metodo `partialUpdate()` en la clase de dominio `User`:

```java
public User partialUpdate(PartialUpdateUserDto dto) {
    if (dto.name != null) {
        this.name = dto.name;
    }
    if (dto.email != null) {
        this.email = dto.email;
    }
    if (dto.password != null) {
        this.password = dto.password;
    }
    return this;
}
```

El metodo `delete()` puede ser:

```java
   @Override
    public void delete(int id) {
          // Verifica existencia y elimina
        userRepo.findById((long) id)
        .ifPresentOrElse(
            userRepo::delete,
            () -> {
                throw new IllegalStateException("Usuario no encontrado");
            }
        );
    }
```


### La recomendación es usar **Streams** para mayor concisión.

Por qué es la mejor opción: 
* Expresa mejor el flujo de transformación de datos
* Reduce código accidental
* Es más fácil de mantener
* Es el estilo esperado en Java moderno (8+)
* No introduce penalización de rendimiento en este caso

 ### Cuándo usar la versión iterativa

Usa for solo si necesitas:

* lógica condicional compleja
* manejo explícito de errores por elemento
* depuración paso a paso
* mutar varias colecciones en un mismo bucle 


# **8. Flujo completo con base de datos real**

```
Cliente
 ↓
Controlador  → recibe DTO
 ↓
Servicio     → valida, mapea, usa repositorio
 ↓
Repositorio  → CRUD
 ↓
Base de Datos PostgreSQL
 ↓
Repositorio
 ↓
Servicio → mapea a DTO
 ↓
Controlador
 ↓
Cliente
```


## Al ejecutar la aplicación Spring Boot:

Se ber ver en consola la salida de la conexión a PostgreSQL:

![alt text](../../../docs/assets/07_repositorios_bd-05.png)



## Salida esperada de consola cuando ejecutamos los endpoints:

### Crear usuario (POST /users)

![alt text](../../../docs/assets/08_repositorios_bd-05.png)

### Listar usuarios (GET /users) con Id

![alt text](../../../docs/assets/09_repositorios_bd-05.png)


> Estas salidas las peude ver ya que en application.yml se habilitó `format_sql: true` 


# **9. Actividad práctica**

El estudiante debe replicar toda la arquitectura aprendida, pero ahora en el módulo:

```
products/
```

Debe implementar:

### **9.1 Extender de BaseModel**

### **9.2 Crear entidad persistente ProductEntity**

Ejemplo sugerido:

```
name, description, price, stock
```

### **9.3 Crear ProductRepository**

Extender `JpaRepository`.

### **9.4 Implementar ProductService + ProductServiceImpl**

Usando repositorio, no listas en memoria.

### **9.5 Actualizar ProductController**

Para usar el servicio con persistencia real.

### **9.6 Probar el CRUD completo con PostgreSQL**

* POST create product
* GET list products
* GET product by id
* PUT update
* DELETE remove
* Validación en BD mediante DBeaver o VSCode PostgreSQL

### Datos para revisión
 
  **Ingresar 5 productos mediante API REST**


# **10. Resultados y evidencias**

## 1. Caputra de `ProductosEntity.java`

![alt text](<nest/p67/alvarez_villa/assets/05 spring 1.jpeg>)
![alt text](<nest/p67/alvarez_villa/assets/05 spring 2.jpeg>)

## 2. Caputra de `ProductosRepository.java`

![alt text](<nest/p67/alvarez_villa/assets/05 spirng 3.jpeg>)

## 3. Capturas de los 5 productos creados en PostgreSQL (DBeaver, VSCode, etc) Sentencia SQL

![alt text](<nest/p67/alvarez_villa/assets/05 spirng 4.jpeg>)
