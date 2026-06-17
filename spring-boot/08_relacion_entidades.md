# Programación y Plataformas Web

# **Spring Boot – Relaciones entre Entidades JPA: Mapeo de Asociaciones 1:N y N:N**

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg" width="95">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="95">
</div>

## **Práctica 8 (Spring Boot): Relaciones JPA, Estrategias de Carga y Mapeo Objeto-Relacional**

### **Autores**

**Pablo Torres**

📧 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

💻 GitHub: PabloT18

# **1. Introducción a las Relaciones en JPA**

En aplicaciones reales, las entidades **NO** son independientes. Existe información relacionada que debe ser mapeada correctamente entre el modelo orientado a objetos y el modelo relacional.

## **1.1. ¿Por qué son importantes las relaciones?**

* **Normalización**: Evita duplicación de datos
* **Integridad referencial**: Mantiene consistencia entre tablas
* **Consultas eficientes**: Permite JOINs optimizados
* **Dominio expresivo**: El código refleja la realidad del negocio

## **1.2. Tipos de relaciones en JPA**

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `@OneToOne` | 1 entidad → 1 entidad | Usuario ↔ Perfil |
| `@OneToMany` | 1 entidad → N entidades | Usuario → Productos |
| `@ManyToOne` | N entidades → 1 entidad | Productos → Usuario |
| `@ManyToMany` | N entidades ↔ N entidades | Productos ↔ Categorías |

## **1.3. Escenario de este tema**

Trabajaremos con un dominio de **e-commerce básico**:

### **Fase 1: Relaciones 1:N (One-to-Many)**
```
User 1 ──── N Product    (Un usuario puede crear muchos productos)
Category 1 ──── N Product (Una categoría puede tener muchos productos)
```

### **Fase 2: Relaciones N:N (Many-to-Many)**
```
Product N ──── N Category (Un producto puede tener múltiples categorías)
```

### **Evolución del dominio**

1. **Fase inicial**: Producto con una sola categoría
2. **Fase dos**: Producto con múltiples categorías (tags, clasificaciones)

# **2. Preparación: Entidades Base Actualizadas**

Antes de implementar relaciones, necesitamos actualizar nuestras entidades base.

## **2.1. Entidad UserEntity (sin relación bidireccional)**

Archivo: `users/entities/UserEntity.java`

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

    // Getters y setters (ya implementados anteriormente)
}
```

### **¿Por qué NO se agrega `@OneToMany` en UserEntity?**

**Decisión de diseño**: Mantenemos la entidad `User` simple sin conocer directamente sus productos.

**Ventajas**:
* **Menor acoplamiento**: User no depende de Product
* **Rendimiento**: Se evita carga de colecciones innecesarias
* **Simplicidad**: Menos complejidad en la entidad
* **Consultas específicas**: Se consultan productos por user_id cuando sea necesario

**Alternativa bidireccional** (no recomendada para este caso):
```java
// NO implementar aun - solo ejemplo 
@OneToMany(mappedBy = "owner", fetch = FetchType.LAZY)
private List<ProductEntity> products = new ArrayList<>();
```

## **2.2. Entidad CategoryEntity (preparada para escalarla)**

Archivo: `categories/entities/CategoryEntity.java`

```java
@Entity
@Table(name = "categories")
public class CategoryEntity extends BaseModel {

    @Column(nullable = false, unique = true, length = 120)
    private String name;

    @Column(length = 500)
    private String description;

    // Getters y setters
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}
```

**Nota**: Esta entidad se mantendrá simple inicialmente, pero evolucionará para soportar relaciones N:N más adelante.

# **3. FASE 1: Relaciones 1:N - ProductEntity con Asociaciones**

La entidad `ProductEntity` es el **propietario** de las relaciones. Aquí se define cómo se conecta con `User` y `Category`.

Archivo: `products/entities/ProductEntity.java`

```java
@Entity
@Table(name = "products")
public class ProductEntity extends BaseModel {

    @Column(nullable = false, length = 150)
    private String name;

    @Column(nullable = false)
    private Double price;

    @Column(length = 500)
    private String description;

    // ================== RELACIONES 1:N ==================

    /**
     * Relación Many-to-One con User
     * Muchos productos pertenecen a un usuario (owner/creator)
     */
    @ManyToOne(optional = false, fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private UserEntity owner;

    /**
     * Relación Many-to-One con Category  
     * Muchos productos pertenecen a una categoría
     */
    @ManyToOne(optional = false, fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id", nullable = false)
    private CategoryEntity category;

    // Constructores
    public ProductEntity() {
    }

    // Getters y setter....
}
```

## **3.1. Explicación detallada de las anotaciones**

### **@ManyToOne**
```java
@ManyToOne(optional = false, fetch = FetchType.LAZY)
```

**Parámetros**:
* **optional = false**: La relación es **obligatoria**. No puede existir un producto sin user y sin category
* **fetch = FetchType.LAZY**: La entidad relacionada se carga **bajo demanda**, no automáticamente

### **@JoinColumn**
```java
@JoinColumn(name = "user_id", nullable = false)
```

**Función**: Define la **Foreign Key** en la tabla `products`
* **name = "user_id"**: Nombre de la columna FK en PostgreSQL
* **nullable = false**: La FK no puede ser NULL (refuerza optional = false)

### **Resultado en PostgreSQL**

```sql
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    description VARCHAR(500),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted BOOLEAN DEFAULT FALSE,
    
    -- Foreign Keys generadas por JPA
    user_id BIGINT NOT NULL REFERENCES users(id),
    category_id BIGINT NOT NULL REFERENCES categories(id)
);
```

# **4. Estrategias de Carga: LAZY vs EAGER**

## **4.1. ¿Qué es el Fetch Strategy?**

Determina **cuándo** se cargan las entidades relacionadas desde la base de datos.

### **FetchType.LAZY (Carga Perezosa) - RECOMENDADO**

```java
@ManyToOne(fetch = FetchType.LAZY)
private UserEntity owner;
```

**Comportamiento**:
* La entidad `UserEntity` **NO** se carga automáticamente
* Se carga solo cuando se accede a `product.getOwner().getName()`
* Genera consulta SQL adicional en ese momento

**Ventajas**:
* **Performance inicial**: Consulta más rápida
* **Memoria eficiente**: No carga datos innecesarios
* **Escalabilidad**: Funciona bien con grandes volúmenes

### **FetchType.EAGER (Carga Inmediata) - USAR CON CUIDADO**

```java
@ManyToOne(fetch = FetchType.EAGER)
private UserEntity owner;
```

**Comportamiento**:
* `UserEntity` se carga automáticamente con `ProductEntity`
* Una sola consulta con JOIN
* Datos disponibles inmediatamente

**Desventajas**:
* **N+1 Problem**: Puede generar muchas consultas innecesarias
* **Memoria**: Carga datos que tal vez no se usen
* **Performance**: Consultas más pesadas

## **4.2. Ejemplo práctico de carga LAZY**

```java
@Service
public class ProductServiceImpl {

    public ProductResponseDto findById(Long id) {
        ProductEntity product = productRepo.findById(id)
            .orElseThrow(() -> new NotFoundException("Producto no encontrado"));

        // AQUÍ: product.owner NO está cargado aún (proxy)
        
        // Esta línea DISPARA una consulta SQL adicional
        String ownerName = product.getOwner().getName();
        
        // Hibernate ejecuta: SELECT * FROM users WHERE id = ?
        
        return toResponseDto(product);
    }
}
```

## **4.3. ¿Cuándo usar cada estrategia?**

| Escenario | Usar LAZY | Usar EAGER |
|-----------|-----------|------------|
| Relación siempre necesaria | ❌ | ✅ Considerar |
| Relación opcional en uso | ✅ SÍ | ❌ |
| Listados con muchos elementos | ✅ SÍ | ❌ |
| Operaciones batch/masivas | ✅ SÍ | ❌ |
| APIs REST (DTOs) | ✅ SÍ | ❌ |

**Recomendación general**: Usar **LAZY por defecto** y optimizar casos específicos con consultas personalizadas.

# **5. Repositorios con Consultas Relacionales**

Los repositorios deben incluir consultas que aprovechen las relaciones definidas.

## **5.1. UserRepository (sin cambios)**

Archivo: `users/repositories/UserRepository.java`

```java
@Repository
public interface UserRepository extends JpaRepository<UserEntity, Long> {

    Optional<UserEntity> findByEmail(String email);
}
```

## **5.2. CategoryRepository**

Archivo: `categories/repositories/CategoryRepository.java`

```java
@Repository
public interface CategoryRepository extends JpaRepository<CategoryEntity, Long> {

    /**
     * Verifica si ya existe una categoría con ese nombre
     * Útil para validaciones de unicidad
     */
    boolean existsByName(String name);

    /**
     * Busca categoría por nombre (case insensitive)
     */
    Optional<CategoryEntity> findByNameIgnoreCase(String name);
}
```

## **5.3. ProductRepository - Consultas con Relaciones**

Archivo: `products/repositories/ProductRepository.java`

```java
@Repository
public interface ProductRepository extends JpaRepository<ProductEntity, Long> {

    /**
     * Encuentra todos los productos de un usuario específico
     * Spring Data JPA genera: SELECT * FROM products WHERE user_id = ?
     */
    List<ProductEntity> findByOwnerId(Long userId);

    /**
     * Encuentra todos los productos de una categoría específica
     * Spring Data JPA genera: SELECT * FROM products WHERE category_id = ?
     */
    List<ProductEntity> findByCategoryId(Long categoryId);

    /**
     * Encuentra productos por nombre de usuario
     * Genera JOIN automáticamente: 
     * SELECT p.* FROM products p JOIN users u ON p.user_id = u.id WHERE u.name = ?
     */
    List<ProductEntity> findByOwnerName(String ownerName);

    /**
     * Encuentra productos por nombre de categoría
     * Genera JOIN automáticamente:
     * SELECT p.* FROM products p JOIN categories c ON p.category_id = c.id WHERE c.name = ?
     */
    List<ProductEntity> findByCategoryName(String categoryName);

    /**
     * Encuentra productos con precio mayor a X de una categoría específica
     * Consulta con múltiples condiciones
     * Genera:
     * SELECT p.* FROM products p WHERE p.category_id = ? AND p.price > ?
     */
    List<ProductEntity> findByCategoryIdAndPriceGreaterThan(Long categoryId, Double price);
}
```

### **Ventajas de Spring Data JPA Query Methods**

* **Automático**: No se escribe SQL manualmente
* **Type-safe**: Verificación en tiempo de compilación
* **Legible**: El nombre del método describe la consulta
* **Optimizado**: Hibernate genera SQL eficiente

# **6. DTOs Actualizados para Relaciones**

Los DTOs deben incluir información de las entidades relacionadas.

## **6.1. CreateProductDto**

Archivo: `products/dtos/CreateProductDto.java`

```java
public class CreateProductDto {

    @NotBlank(message = "El nombre es obligatorio")
    @Size(min = 3, max = 150, message = "El nombre debe tener entre 3 y 150 caracteres")
    public String name;

    @NotNull(message = "El precio es obligatorio")
    @DecimalMin(value = "0.0", inclusive = false, message = "El precio debe ser mayor a 0")
    public Double price;

    @Size(max = 500, message = "La descripción no puede superar 500 caracteres")
    public String description;

    // ============== RELACIONES ==============

    @NotNull(message = "El ID del usuario es obligatorio")
    public Long userId;

    @NotNull(message = "El ID de la categoría es obligatorio")
    public Long categoryId;
}
```

## **6.2. ProductResponseDto - Estructura Anidada vs Plana**



### **Opción 1: Estructura Anidada (RECOMENDADA)**

En esta opción se pueden crear Dtos especificos para los modelos relacionadas, o se peude usar los DTOS de cada modelo especifico, 
es decir, `UserResponseDto` y `CategoryResponseDto`, pero para simplicidad se crean Dtos internos simples como `UserSummaryDto` y `CategorySummaryDto`.

Archivo: `products/dtos/ProductResponseDto.java`

```java
public class ProductResponseDto {

    public Long id;
    public String name;
    public Double price;
    public String description;

    // ============== OBJETOS ANIDADOS ==============
    
    public UserSummaryDto user;
    public CategoryResponseDto category;

    // ============== AUDITORÍA ==============
    
    public LocalDateTime createdAt;
    public LocalDateTime updatedAt;

    // ============== DTOs INTERNOS ==============
    
    public static class UserSummaryDto {
        public Long id;
        public String name;
        public String email;
    }

    public static class CategoryResponseDto {
        public Long id;
        public String name;
        public String description;
    }
}
```

**Respuesta JSON resultante:**
```json
{
    "id": 1,
    "name": "Laptop Gaming",
    "price": 1200.00,
    "description": "Laptop de alto rendimiento",
    "user": {
        "id": 1,
        "name": "Juan Pérez",
        "email": "juan@email.com"
    },
    "category": {
        "id": 2,
        "name": "Electrónicos",
        "description": "Dispositivos electrónicos"
    },
    "createdAt": "2024-01-15T10:30:00",
    "updatedAt": "2024-01-15T10:30:00"
}
```

### **Opción 2: Estructura Plana (alternativa)**

```java
public class ProductResponseDto {

    public Long id;
    public String name;
    public Double price;
    public String description;

    // ============== INFORMACIÓN PLANA ==============
    
    public Long userId;
    public String userName;
    public String userEmail;
    
    public Long categoryId;
    public String categoryName;
    public String categoryDescription;

    public LocalDateTime createdAt;
    public LocalDateTime updatedAt;
}
```

**Respuesta JSON resultante:**
```json
{
    "id": 1,
    "name": "Laptop Gaming",
    "price": 1200.00,
    "description": "Laptop de alto rendimiento",
    "userId": 1,
    "userName": "Juan Pérez",
    "userEmail": "juan@email.com",
    "categoryId": 2,
    "categoryName": "Electrónicos",
    "categoryDescription": "Dispositivos electrónicos",
    "createdAt": "2024-01-15T10:30:00",
    "updatedAt": "2024-01-15T10:30:00"
}
```

### **Comparación de enfoques**

| Aspecto | Estructura Anidada | Estructura Plana |
|---------|-------------------|------------------|
| **Semántica** | ✅ Clara y expresiva | ⚠️ Confusa con muchos campos |
| **Legibilidad** | ✅ Fácil de entender | ❌ Difícil con muchas relaciones |
| **Frontend** | ✅ `product.user.name` | ❌ `product.userName` |
| **Reutilización** | ✅ DTOs internos reutilizables | ❌ Duplicación |
| **Escalabilidad** | ✅ Fácil agregar campos | ⚠️ Contamina DTO principal |
| **Tipado** | ✅ Fuertemente tipado | ⚠️ Propenso a errores |

### **¿Cuándo usar cada enfoque?**

**Usar estructura ANIDADA cuando:**
* Las relaciones son **complejas** o tienen múltiples campos
* El frontend necesita **acceso frecuente** a datos relacionados
* Se busca **claridad semántica** en la API
* Hay **múltiples niveles** de relaciones

**Usar estructura PLANA cuando:**
* Las relaciones son **simples** (solo ID + nombre)
* Se requiere **máxima performance** (menos objetos)
* La **compatibilidad** con sistemas legacy es importante

### **Recomendación: Estructura Anidada**

Para este tema usaremos la **estructura anidada** porque:
* Es más **expresiva** del dominio
* Facilita el trabajo del **frontend**
* Es una **mejor práctica** en APIs modernas
* Prepara para **futuras extensiones**

## **6.3. UpdateProductDto**

Archivo: `products/dtos/UpdateProductDto.java`

```java
public class UpdateProductDto {

    @NotBlank(message = "El nombre es obligatorio")
    @Size(min = 3, max = 150)
    public String name;

    @NotNull(message = "El precio es obligatorio")
    @DecimalMin(value = "0.0", inclusive = false)
    public Double price;

    @Size(max = 500)
    public String description;

    // ============== ACTUALIZACIÓN DE RELACIONES ==============

    @NotNull(message = "El ID de la categoría es obligatorio")
    public Long categoryId;

    // Nota: No se permite cambiar el owner de un producto una vez creado
    // Si fuera necesario, sería una operación de negocio especial
}
```

# **7. Modelo de Dominio Product con Factory Methods**

El modelo de dominio se mantiene limpio, sin conocer JPA directamente.

Archivo: `products/models/Product.java`

```java
public class Product {

    private Long id;
    private String name;
    private Double price;
    private String description;

    // Constructores
    public Product() {
    }

    public Product(String name, Double price, String description) {
        this.validateBusinessRules(name, price, description);
        this.name = name;
        this.price = price;
        this.description = description;
    }

    private void validateBusinessRules(String name, Double price, String description) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("El nombre del producto es obligatorio");
        }
        if (price == null || price <= 0) {
            throw new IllegalArgumentException("El precio debe ser mayor a 0");
        }
        if (description != null && description.length() > 500) {
            throw new IllegalArgumentException("La descripción no puede superar 500 caracteres");
        }
    }

    // ==================== FACTORY METHODS ====================

    /**
     * Crea un Product desde un DTO de creación
     */
    public static Product fromDto(CreateProductDto dto) {
        return new Product(dto.name, dto.price, dto.description);
    }

    /**
     * Crea un Product desde una entidad persistente
     */
    public static Product fromEntity(ProductEntity entity) {
        Product product = new Product(
            entity.getName(), 
            entity.getPrice(), 
            entity.getDescription()
        );
        product.id = entity.getId();
        return product;
    }

    // ==================== CONVERSION METHODS ====================

    /**
     * Convierte este Product a una entidad persistente
     * REQUIERE las entidades relacionadas como parámetros
     */
    public ProductEntity toEntity(UserEntity owner, CategoryEntity category) {
        ProductEntity entity = new ProductEntity();
        
        if (this.id != null && this.id > 0) {
            entity.setId(this.id);
        }
        
        entity.setName(this.name);
        entity.setPrice(this.price);
        entity.setDescription(this.description);
        
        // Asignar relaciones
        entity.setOwner(owner);
        entity.setCategory(category);
        
        return entity;
    }

    /**
     * Actualiza los campos modificables de este Product
     */
    public Product update(UpdateProductDto dto) {
        this.validateBusinessRules(dto.name, dto.price, dto.description);
        this.name = dto.name;
        this.price = dto.price;
        this.description = dto.description;
        return this;
    }

    // Getters y setters
    public Long getId() { return id; }
    public String getName() { return name; }
    public Double getPrice() { return price; }
    public String getDescription() { return description; }

    public void setId(Long id) { this.id = id; }
    public void setName(String name) { this.name = name; }
    public void setPrice(Double price) { this.price = price; }
    public void setDescription(String description) { this.description = description; }
}
```

### **¿Por qué el dominio NO conoce las entidades relacionadas?**

* **Separación de responsabilidades**: Product se enfoca en sus reglas de negocio
* **Testing**: Es fácil probar Product sin dependencias JPA
* **Flexibilidad**: Product puede usarse en contextos que no requieren persistencia
* **Claridad**: El servicio es responsable de manejar las relaciones
# **8. Servicio ProductServiceImpl - Orquestación de Relaciones**

El servicio es responsable de validar y gestionar las relaciones entre entidades.

Archivo: `products/services/ProductServiceImpl.java`

ProductServiceImpl conoce todos los repositorios necesarios para validar y gestionar las relaciones.
La clase `ProductServiceImpl` es la que orquestiona la creación, actualización y consulta de productos con sus relaciones, por eso 
no debe tener los otros servicios inyectados, sino solo los repositorios.

Ya que un servicio que depender de otro servicio puede generar:
* acoplamiento horizontal entre servicios

* dependencia circular potencial

* dificultad para testear

* propagación de lógica que no le corresponde al caso de uso actual

En clean architecture, los servicios deben ser lo más independientes posibles entre sí y no llamarse entre estos.


```java
@Service
public class ProductServiceImpl implements ProductService {

    private final ProductRepository productRepo;
    private final UserRepository userRepo;
    private final CategoryRepository categoryRepo;

    public ProductServiceImpl(
            ProductRepository productRepo,
            UserRepository userRepo,
            CategoryRepository categoryRepo
    ) {
        this.productRepo = productRepo;
        this.userRepo = userRepo;
        this.categoryRepo = categoryRepo;
    }
```


## Creación de un Producto con relaciones

Para crear un producto, se deben validar las entidades relacionadas (usuario y categoría) antes de persistir.
Si estos no existen, se lanza una excepción `NotFoundException`.



  ```java
    @Override
    public ProductResponseDto create(CreateProductDto dto) {
        
        // 1. VALIDAR EXISTENCIA DE RELACIONES
        UserEntity owner = userRepo.findById(dto.userId)
                .orElseThrow(() -> new NotFoundException("Usuario no encontrado con ID: " + dto.userId));

        CategoryEntity category = categoryRepo.findById(dto.categoryId)
                .orElseThrow(() -> new NotFoundException("Categoría no encontrada con ID: " + dto.categoryId));


        // Regla: nombre único
        if (productRepo.findByName(dto.name).isPresent()) {
            throw new IllegalStateException("El nombre del producto ya está registrado");
        }

        // 2. CREAR MODELO DE DOMINIO
        Product product = Product.fromDto(dto);

        // 3. CONVERTIR A ENTIDAD CON RELACIONES
        ProductEntity entity = product.toEntity(owner, category);

        // 4. PERSISTIR
        ProductEntity saved = productRepo.save(entity);

        // 5. CONVERTIR A DTO DE RESPUESTA
        return toResponseDto(saved);
    }

```

## Métodos de consulta, actualización y eliminación

`.map(this::toResponseDto)` Para cada instancial de ProductEntity obtenida del repositorio, se llama al método `toResponseDto` para convertirla en un `ProductResponseDto`.

```java

    @Override
    public List<ProductResponseDto> findAll() {
        return productRepo.findAll()
                .stream()
                .map(this::toResponseDto)
                .toList();
    }
```

Si se peude realizamos un mapeo directo entre Entidad -> DTO, esto se puede aplicar  
* Operaciones de solo lectura (como findAll, findById)
* No hay lógica de negocio que aplicar
* Performance crítica (menos objetos intermedios)
* Consultas simples sin validacione

Ventajas:

Más eficiente en memoria
Menos objetos temporales
Código más directo para consultas

Caso contrario se puede realizar la forma que se trabajó


```java

    @Override
    public List<ProductResponseDto> findAll() {
        return productRepo.findAll()
                .stream()
                .map(Product::fromEntity)        // ProductEntity → Product
                .map(Product::toResponseDto)     // Product → ProductResponseDto  
                .toList();
    }
```

El mapeo por cada calse se puede implementar cuadno:

* Operaciones que modifican estado (create, update)
* Hay reglas de negocio que aplicar
* Necesitas validaciones de dominio
* Consistencia arquitectural es prioritaria

Ventajas:

Mantiene separación de capas
Permite aplicar reglas de negocio
Código más consistente y predecible
Facilita testing del dominio

```java

    @Override
    public ProductResponseDto findById(Long id) {
        return productRepo.findById(id)
                .map(this::toResponseDto)
                .orElseThrow(() -> new NotFoundException("Producto no encontrado con ID: " + id));
    }

    @Override
    public List<ProductResponseDto> findByUserId(Long userId) {
        
        // Validar que el usuario existe
        if (!userRepo.existsById(userId)) {
            throw new NotFoundException("Usuario no encontrado con ID: " + userId);
        }

        return productRepo.findByOwnerId(userId)
                .stream()
                .map(this::toResponseDto)
                .toList();
    }

    @Override
    public List<ProductResponseDto> findByCategoryId(Long categoryId) {
        
        // Validar que la categoría existe
        if (!categoryRepo.existsById(categoryId)) {
            throw new NotFoundException("Categoría no encontrada con ID: " + categoryId);
        }

        return productRepo.findByCategoryId(categoryId)
                .stream()
                .map(this::toResponseDto)
                .toList();
    }

    @Override
    public ProductResponseDto update(Long id, UpdateProductDto dto) {
        
        // 1. BUSCAR PRODUCTO EXISTENTE
        ProductEntity existing = productRepo.findById(id)
                .orElseThrow(() -> new NotFoundException("Producto no encontrado con ID: " + id));

        // 2. VALIDAR NUEVA CATEGORÍA (si cambió)
        CategoryEntity newCategory = categoryRepo.findById(dto.categoryId)
                .orElseThrow(() -> new NotFoundException("Categoría no encontrada con ID: " + dto.categoryId));

        // 3. ACTUALIZAR USANDO DOMINIO
        Product product = Product.fromEntity(existing);
        product.update(dto);

        // 4. CONVERTIR A ENTIDAD MANTENIENDO OWNER ORIGINAL
        ProductEntity updated = product.toEntity(existing.getOwner(), newCategory);
        updated.setId(id); // Asegurar que mantiene el ID

        // 5. PERSISTIR Y RESPONDER
        ProductEntity saved = productRepo.save(updated);
        return toResponseDto(saved);
    }

    @Override
    public void delete(Long id) {
        
        ProductEntity product = productRepo.findById(id)
                .orElseThrow(() -> new NotFoundException("Producto no encontrado con ID: " + id));

        // Eliminación física (también se puede implementar lógica)
        productRepo.delete(product);
    }

```

## MÉTODO HELPER 

Tipo mapper, para convertir entidad a DTO con relaciones cargadas

```java

    /**
     * Convierte ProductEntity a ProductResponseDto
     * Usa estructura anidada para mejor organización semántica
     */
    private ProductResponseDto toResponseDto(ProductEntity entity) {
        ProductResponseDto dto = new ProductResponseDto();
        
        // Campos básicos del producto
        dto.id = entity.getId();
        dto.name = entity.getName();
        dto.price = entity.getPrice();
        dto.description = entity.getDescription();
        
        // Crear objeto User anidado (se carga LAZY)
        ProductResponseDto.UserSummaryDto userDto = new ProductResponseDto.UserSummaryDto();
        userDto.id = entity.getOwner().getId();
        userDto.name = entity.getOwner().getName();
        userDto.email = entity.getOwner().getEmail();
        dto.user = userDto;
        
        // Crear objeto Category anidado (se carga LAZY)
        CategoryResponseDto categoryDto = new CategoryResponseDto();
        categoryDto.id = entity.getCategory().getId();
        categoryDto.name = entity.getCategory().getName();
        categoryDto.description = entity.getCategory().getDescription();
        dto.category = categoryDto;
        
        // Auditoría
        dto.createdAt = entity.getCreatedAt();
        dto.updatedAt = entity.getUpdatedAt();
        
        return dto;
    }
}
```

### **Aspectos clave del servicio**

1. **Validación proactiva**: Se valida que las entidades relacionadas existan antes de crear/actualizar
2. **Manejo de errores**: Se lanzan excepciones específicas que serán capturadas por el GlobalExceptionHandler
3. **Carga LAZY controlada**: En `toResponseDto()` se accede a las propiedades relacionadas, provocando las consultas adicionales necesarias
4. **Separación de responsabilidades**: El servicio orquesta, el dominio valida reglas de negocio, el repositorio persiste

# **9. Controlador ProductController**

Archivo: `products/controllers/ProductController.java`

Actualizado para manejar las relaciones en las operaciones CRUD. Quitamos otros endpoints que no son necesarios para este tema, o que se vieron en temas anteriores.

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {

    private final ProductService productService;

    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    @PostMapping
    public ResponseEntity<ProductResponseDto> create(@Valid @RequestBody CreateProductDto dto) {
        ProductResponseDto created = productService.create(dto);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @GetMapping
    public ResponseEntity<List<ProductResponseDto>> findAll() {
        List<ProductResponseDto> products = productService.findAll();
        return ResponseEntity.ok(products);
    }

    @GetMapping("/{id}")
    public ResponseEntity<ProductResponseDto> findById(@PathVariable Long id) {
        ProductResponseDto product = productService.findById(id);
        return ResponseEntity.ok(product);
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<List<ProductResponseDto>> findByUserId(@PathVariable Long userId) {
        List<ProductResponseDto> products = productService.findByUserId(userId);
        return ResponseEntity.ok(products);
    }

    @GetMapping("/category/{categoryId}")
    public ResponseEntity<List<ProductResponseDto>> findByCategoryId(@PathVariable Long categoryId) {
        List<ProductResponseDto> products = productService.findByCategoryId(categoryId);
        return ResponseEntity.ok(products);
    }

    @PutMapping("/{id}")
    public ResponseEntity<ProductResponseDto> update(
            @PathVariable Long id,
            @Valid @RequestBody UpdateProductDto dto
    ) {
        ProductResponseDto updated = productService.update(id, dto);
        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        productService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
```

# **10. FASE 2: Evolución a Relaciones Many-to-Many (N:N)**

### **¿Cuándo necesitamos relaciones N:N?**

**Escenario**: Un producto puede pertenecer a múltiples categorías simultáneamente.

**Ejemplos**:
* Laptop → ["Electrónicos", "Oficina", "Gaming"]
* Manual de Laptio → ["Libros", "Oficina", "Electrónicos"]
* Teclado → ["Electrónicos", "Gaming"] 

### **Evolución del esquema**

```
ANTES (1:N):
Product N ──── 1 Category

DESPUÉS (N:N):
Product N ──── N Category
```

## **10.1. Nueva entidad ProductEntity con relación N:N**

```java
@Entity
@Table(name = "products")
public class ProductEntity extends BaseModel {

    @Column(nullable = false, length = 150)
    private String name;

    @Column(nullable = false)
    private Double price;

    @Column(length = 500)
    private String description;

    // ============== RELACIÓN 1:N (se mantiene) ==============
    
    @ManyToOne(optional = false, fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private UserEntity owner;

    // ============== NUEVA RELACIÓN N:N ==============
    
    /**
     * Relación Many-to-Many con Category
     * Un producto puede tener múltiples categorías
     * Una categoría puede estar en múltiples productos
     */
    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(
        name = "product_categories",                    // Tabla intermedia
        joinColumns = @JoinColumn(name = "product_id"), // FK hacia products
        inverseJoinColumns = @JoinColumn(name = "category_id") // FK hacia categories
    )
    private Set<CategoryEntity> categories = new HashSet<>();

    // Constructores
    public ProductEntity() {
    }

    // Getters y setters
    public Set<CategoryEntity> getCategories() {
        return categories;
    }

    public void setCategories(Set<CategoryEntity> categories) {
        this.categories = categories != null ? categories : new HashSet<>();
    }
```

Para manejar la relación N:N de manera más sencilla, se agregan métodos de conveniencia:
que deberan actualizar la colección de categorías asociadas al producto.



```java
    // ============== MÉTODOS DE CONVENIENCIA ==============
  /**
 * Agrega una categoría al producto y sincroniza la relación bidireccional
 */
public void addCategory(CategoryEntity category) {
    this.categories.add(category);
}

/**
 * Remueve una categoría del producto y sincroniza la relación bidireccional
 */
public void removeCategory(CategoryEntity category) {
    this.categories.remove(category);
}

/**
 * Limpia todas las categorías y sincroniza las relaciones
 */
public void clearCategories() {
  
    this.categories.clear();
}
    // ... resto de getters y setters
}
```

## **10.2. Explicación de @ManyToMany**

### **@ManyToMany**
```java
@ManyToMany(fetch = FetchType.LAZY)
```
* Configura una relación bidireccional N:N
* `fetch = LAZY`: Las categorías se cargan bajo demanda

### **@JoinTable**
```java
@JoinTable(
    name = "product_categories",
    joinColumns = @JoinColumn(name = "product_id"),
    inverseJoinColumns = @JoinColumn(name = "category_id")
)
```

**Función**: Define la **tabla intermedia** que almacena la relación

**Resultado en PostgreSQL**:
```sql
CREATE TABLE product_categories (
    product_id BIGINT NOT NULL REFERENCES products(id),
    category_id BIGINT NOT NULL REFERENCES categories(id),
    PRIMARY KEY (product_id, category_id)
);
```

### **¿Por qué Set<CategoryEntity> y no List<CategoryEntity>?**

* **Set**: No permite duplicados, ideal para relaciones N:N
* **List**: Permite duplicados, puede causar problemas de consistencia
* **HashSet**: Implementación eficiente para búsquedas y operaciones de conjunto

## **10.3. CategoryEntity actualizada (lado inverso)**

```java
@Entity
@Table(name = "categories")
public class CategoryEntity extends BaseModel {

    @Column(nullable = false, unique = true, length = 120)
    private String name;

    @Column(length = 500)
    private String description;

    // ============== RELACIÓN BIDIRECCIONAL N:N ==============
    
    /**
     * Relación inversa con Product
     * mappedBy = "categories" hace referencia al atributo en ProductEntity
     */
    @ManyToMany(mappedBy = "categories", fetch = FetchType.LAZY)
    private Set<ProductEntity> products = new HashSet<>();

    // Constructores y getters/setters
    
    public Set<ProductEntity> getProducts() {
        return products;
    }

    public void setProducts(Set<ProductEntity> products) {
        this.products = products != null ? products : new HashSet<>();
    }

    // ============== MÉTODOS DE CONVENIENCIA ==============
    
    public void addProduct(ProductEntity product) {
        this.products.add(product);    }

    public void removeProduct(ProductEntity product) {
        this.products.remove(product);

    }
}
```

### **Parámetro mappedBy**

```java
@ManyToMany(mappedBy = "categories")
```

* **mappedBy = "categories"**: Indica que esta es la relación "inversa"
* La tabla intermedia se define solo en `ProductEntity`
* `CategoryEntity` no genera tabla adicional
* Mantiene sincronización bidireccional.



## **10.4. DTOs actualizados para relación N:N**

### **CreateProductDto con múltiples categorías**

```java
public class CreateProductDto {

    // Campos básicos
    // ============== RELACIONES ==============

    /// campo relacion USER se mantiene igual

    @NotNull(message = "Debe especificar al menos una categoría")
    @Size(min = 1, message = "El producto debe tener al menos una categoría")
    public Set<Long> categoryIds; // Múltiples categorías
}
```

### **ProductResponseDto con lista de categorías (N:N)**

Actualizamos el DTO de respuesta para incluir una lista de categorías.

```java
public class ProductResponseDto {

    // Campos básicos
    // ============== OBJETOS ANIDADOS ==============
    // campo relacion USER se mantiene igual

    // ============== CATEGORÍAS (N:N) - Lista de objetos ==============
    public List<CategoryResponseDto> categories;

 
}
```

**Respuesta JSON con múltiples categorías:**
```json
{
    "id": 1,
    "name": "Laptop Gaming",
    "price": 1200.00,
    "description": "Laptop de alto rendimiento",
    "user": {
        "id": 1,
        "name": "Juan Pérez", 
        "email": "juan@email.com"
    },
    "categories": [
        {
            "id": 2,
            "name": "Electrónicos",
            "description": "Dispositivos electrónicos"
        },
        {
            "id": 5,
            "name": "Gaming",
            "description": "Productos para gamers"
        },
        {
            "id": 8,
            "name": "Oficina",
            "description": "Equipos de oficina"
        }
    ],
    "createdAt": "2024-01-15T10:30:00",
    "updatedAt": "2024-01-15T10:30:00"
}
```


## **10.5. ProductRepository actualizado para N:N**

Modficamos el repositorio para consultas basadas en categorías múltiples.

Elimanar los métodos antiguos que asumen relación 1:N.


```java
@Repository
public interface ProductRepository extends JpaRepository<ProductEntity, Long> {

    // otros métodos... 

    /**
     * Encuentra productos que tienen UNA categoría específica
     * Útil para filtros de categoría
     */
    List<ProductEntity> findByCategoriesId(Long categoryId);

    /**
     * Encuentra productos que tienen una categoría con nombre específico
     */
    List<ProductEntity> findByCategoriesName(String categoryName);

    /**
     * Consulta personalizada: productos con TODAS las categorías especificadas
     */
    @Query("SELECT p FROM ProductEntity p " +
           "WHERE SIZE(p.categories) >= :categoryCount " +
           "AND :categoryCount = " +
           "(SELECT COUNT(c) FROM p.categories c WHERE c.id IN :categoryIds)")
    List<ProductEntity> findByAllCategories(@Param("categoryIds") List<Long> categoryIds,
                                          @Param("categoryCount") long categoryCount);
}
```

## **10.6. Servicio actualizado para manejar N:N**

> **NOTA:** Deberan actualizar los demás métodos del servicio y controlador para manejar la relación N:N según sea necesario.


```java
@Service
public class ProductServiceImpl implements ProductService {

    // ... repositorios inyectados

    @Override
    public ProductResponseDto create(CreateProductDto dto) {
        
        // 1. VALIDAR USER
        UserEntity owner = userRepo.findById(dto.userId)
                .orElseThrow(() -> new NotFoundException("Usuario no encontrado"));

        // 2. VALIDAR Y OBTENER CATEGORÍAS
        Set<CategoryEntity> categories = validateAndGetCategories(dto.categoryIds);

        // 3. CREAR DOMINIO
        Product product = Product.fromDto(dto);

        // 4. CREAR ENTIDAD CON RELACIONES N:N
        ProductEntity entity = product.toEntity(owner);
        entity.setCategories(categories);

        // 5. PERSISTIR
        ProductEntity saved = productRepo.save(entity);

        return toResponseDto(saved);
    }

    @Override
    public ProductResponseDto update(Long id, UpdateProductDto dto) {
        
        ProductEntity existing = productRepo.findById(id)
                .orElseThrow(() -> new NotFoundException("Producto no encontrado"));

        // Validar nuevas categorías
        Set<CategoryEntity> newCategories = validateAndGetCategories(dto.categoryIds);

        // Actualizar usando dominio
        Product product = Product.fromEntity(existing);
        product.update(dto);

      // 3. ACTUALIZAR USANDO Instancia de entidad
        existing.setDescription(dto.description != null ? dto.description : existing.getDescription());
        existing.setName(dto.name != null ? dto.name : existing.getName());
        existing.setPrice(dto.price != null ? dto.price : existing.getPrice());
        
        // IMPORTANTE: Limpiar categorías existentes y asignar nuevas
        existing.clearCategories();
        existing.setCategories(newCategories);

        ProductEntity saved = productRepo.save(existing);
        return toResponseDto(saved);
    }

    // ============== MÉTODOS HELPER ==============

      /**
     * Convierte ProductEntity a DTO incluyendo categorías (N:N)
     * Usa estructura anidada para mejor semántica
     */
    private ProductResponseDto toResponseDto(ProductEntity entity) {
        ProductResponseDto dto = new ProductResponseDto();
        
        // Campos básicos
        dto.id = entity.getId();
        dto.name = entity.getName();
        dto.price = entity.getPrice();
        dto.description = entity.getDescription();
        
        // Crear objeto User anidado
        ProductResponseDto.UserSummaryDto userDto = new ProductResponseDto.UserSummaryDto();
        userDto.id = entity.getOwner().getId();
        userDto.name = entity.getOwner().getName();
        userDto.email = entity.getOwner().getEmail();
        dto.user = userDto;
        
        // Convertir Set<CategoryEntity> a List<CategorySummaryDto>
        dto.categories = entity.getCategories().stream()
                .map(this::toCategorySummary)
                .sorted((c1, c2) -> c1.name.compareTo(c2.name)) // Ordenar por nombre
                .toList();
        
        dto.createdAt = entity.getCreatedAt();
        dto.updatedAt = entity.getUpdatedAt();
        
        return dto;
    }

    private ProductResponseDto.CategorySummaryDto toCategorySummary(CategoryEntity category) {
        ProductResponseDto.CategorySummaryDto summary = new ProductResponseDto.CategorySummaryDto();
        summary.id = category.getId();
        summary.name = category.getName();
        summary.description = category.getDescription();
        return summary;
    }
}
```

### Creamos un validador de categorias

Para todas las categorías recibidas en el DTO pueder ser un servicio aparte si se desea reutilizar en otros casos de uso.

```java
    // ============== MÉTODOS HELPER ==============

private Set<CategoryEntity> validateAndGetCategories(Set<Long> categoryIds) {
    Set<CategoryEntity> categories = new HashSet<>();
    
    for (Long categoryId : categoryIds) {
        CategoryEntity category = categoryRepo.findById(categoryId)
                .orElseThrow(() -> new NotFoundException("Categoría no encontrada: " + categoryId));
        categories.add(category);
    }
    
    return categories;
}

```

> **NOTA:** Deberan actualizar los demás métodos del servicio y controlador para manejar la relación N:N según sea necesario.
>
> **NOTA** : Recuerden actualizar los DTOs, repositorios y controladores para reflejar la nueva relación N:N. El metodo `toResponseDto` deberia ser acutalizado para mapear la colección de categorías.


# **11. Flujo de Consultas SQL Generadas**

## **11.1. Crear producto con múltiples categorías**

```java
// Al ejecutar productService.create(dto)
```

**SQL generado por Hibernate**:

```sql
-- 1. Insertar producto
INSERT INTO products (name, price, description, user_id, created_at, deleted) 
VALUES ('Laptop Gaming', 1200.00, 'Alta performance', 1, NOW(), false);

-- 2. Insertar relaciones en tabla intermedia
INSERT INTO product_categories (product_id, category_id) VALUES (1, 2); -- Electrónicos
INSERT INTO product_categories (product_id, category_id) VALUES (1, 5); -- Gaming  
INSERT INTO product_categories (product_id, category_id) VALUES (1, 8); -- Oficina
```

## **11.2. Consultar producto con categorías**

```java
// Al ejecutar productService.findById(1L)
```

**SQL generado**:

```sql
-- 1. Consulta principal (LAZY loading)
SELECT p.* FROM products p WHERE p.id = 1;

-- 2. Consulta de categorías (cuando se accede a getCategories())
SELECT c.*, pc.product_id 
FROM categories c 
INNER JOIN product_categories pc ON c.id = pc.category_id 
WHERE pc.product_id = 1;
```

# **12. Comparación: 1:N vs N:N**

| Aspecto | Relación 1:N | Relación N:N |
|---------|-------------|-------------|
| **Tabla intermedia** | ❌ No necesaria | ✅ Requerida |
| **Flexibilidad** | ⚠️ Limitada | ✅ Alta |
| **Complejidad** | ✅ Simple | ⚠️ Media |
| **Performance** | ✅ Mejor | ⚠️ Más consultas |
| **Uso de memoria** | ✅ Menos | ⚠️ Más (colecciones) |
| **Casos de uso** | Relaciones fijas | Clasificaciones, tags |

## **12.1. ¿Cuándo usar cada tipo?**

### **Usar 1:N cuando:**
* La relación es **naturalmente jerárquica**
* Un elemento pertenece a **una sola categoría padre**
* La estructura es **estable** y no cambiará frecuentemente

### **Usar N:N cuando:**
* Necesitas **clasificación múltiple**
* Los elementos pueden tener **múltiples etiquetas**
* Requieres **flexibilidad** en la categorización

# **13. Actividad Práctica Completa**

El estudiante debe implementar **ambos enfoques** para entender las diferencias.

## **13.1. PARTE A: Implementar relación 1:N (básica)**

1. **Crear CategoryEntity básica**
2. **Actualizar ProductEntity con @ManyToOne**
3. **Implementar ProductService con validación de relaciones**
4. **Crear endpoints**:
   - `POST /api/products` (con userId y categoryId)
   - `GET /api/products/user/{userId}`
   - `GET /api/products/category/{categoryId}`
5. **Probar con datos reales en PostgreSQL**

## **13.2. PARTE B: Evolucionar a N:N (dos)**

1. **Actualizar ProductEntity con @ManyToMany**
2. **Actualizar CategoryEntity con relación bidireccional**
3. **Modificar DTOs para múltiples categorías**
4. **Actualizar ProductService para manejar Set<CategoryEntity>**
5. **Probar creación de productos con múltiples categorías**

## **13.3. PARTE C: Consultas avanzadas**

1. **Implementar endpoints adicionales**:

   - `GET /api/categories/{id}/products/count` (contar productos por categoría)
2. **Agregar consultas personalizadas con @Query**
3. **Implementar filtros complejos**



# **14. Resultados y Evidencias Requeridas**

## **14.1. Evidencias de implementación**
1. **Captura de ProductEntity.java** (con ambas versiones: 1:N y N:N)
2. **Captura de ProductServiceImpl.java** (métodos create y update)

## **14.2. Evidencias de funcionamiento**
1. **Producto creado con una categoría** (versión 1:N)
2. **Producto creado con múltiples categorías** (versión N:N)
3. **Consulta SQL en consola** mostrando tabla intermedia `product_categories`
4. **Respuesta JSON** de un producto con múltiples categorías

## **14.3. Evidencias de base de datos**
1. **CAputra  del consumo de** /api/categories/{id}/products/count

## **14.4. Datos para revisión**

**Crear los siguientes productos de prueba**:

1. **Laptop Gaming** → Categorías: ["Electrónicos", "Gaming", "Oficina"]
2. **Mouse Inalámbrico** → Categorías: ["Electrónicos", "Oficina"]
3. **Monitor 4K** → Categorías: ["Electrónicos", "Gaming", "Diseño"]
4. **Teclado Mecánico** → Categorías: ["Gaming", "Oficina"]
5. **Libro Java** → Categorías: ["Libros", "Programación", "Educación"]
