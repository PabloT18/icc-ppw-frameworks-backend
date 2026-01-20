# Programación y Plataformas Web

# **Spring Boot – Request Parameters en Consultas Relacionadas: Contexto Semántico y Filtrado**

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg" width="95">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="95">
</div>

## **Práctica 9 (Spring Boot): Request Parameters, Consultas Relacionadas y Optimización**

### **Autores**

**Pablo Torres**

📧 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

💻 GitHub: PabloT18

# **1. Introducción a Request Parameters en Consultas Relacionadas**

En el tema anterior implementamos **relaciones entre entidades** usando JPA. Ahora, en aplicaciones reales, necesitamos **consultar y filtrar** datos relacionados de manera eficiente.

Los principales retos son:

* **¿Cómo diseñar endpoints que reflejen la semántica del dominio?**
* **¿Cuál es la diferencia entre navegación de relaciones y consultas explícitas?**
* **¿Cómo implementar filtros dinámicos con @RequestParam?**
* **¿Cómo mantener la separación de responsabilidades en consultas relacionadas?**

## **1.1. Contexto semántico en Spring Boot**

El **contexto semántico** define desde qué perspectiva se accede a un recurso relacionado en REST.

### **Principio fundamental**

**El endpoint debe reflejar la relación lógica del dominio**, no la estructura técnica de la base de datos.

### **Ejemplo práctico**

**Obtener productos de un usuario específico:**

```
✅ CORRECTO: /users/{id}/products
❌ INCORRECTO: /products?userId={id}
❌ INCORRECTO: /products/user/{id}
```

**¿Por qué `/users/{id}/products` es superior?**
* Los productos **pertenecen** al usuario
* El usuario es el **contexto principal**
* Se consulta una **subcolección** del usuario
* La relación es **clara e intuitiva**

## **1.2. Request Parameters para filtrado**

Los **@RequestParam** permiten filtrar las consultas sin cambiar la semántica del endpoint.

### **Estructura básica**

```java
@GetMapping("/users/{id}/products")
public ResponseEntity<List<ProductResponseDto>> getProducts(
    @PathVariable Long id,
    @RequestParam(required = false) String name,
    @RequestParam(required = false) Double minPrice,
    @RequestParam(required = false) Double maxPrice,
    @RequestParam(required = false) Long categoryId
) {
    // Implementación
}
```

### **Ejemplos de uso**

```
// Todos los productos del usuario
GET /api/users/123/products

// Productos que contengan "laptop"
GET /api/users/123/products?name=laptop

// Productos en rango de precios
GET /api/users/123/products?minPrice=500&maxPrice=1500

// Combinación de filtros
GET /api/users/123/products?name=gaming&minPrice=800&categoryId=2
```

# **2. Navegación vs Consulta Explícita en Spring Boot**

## **2.1. Navegación de relaciones (problemática)**

**Concepto**: Acceder a datos relacionados navegando el grafo de objetos.

```java
// ❌ PROBLEMÁTICO - Navegación
@Override
public List<ProductResponseDto> getProductsByUserId(Long userId) {
    UserEntity user = userRepository.findById(userId)
        .orElseThrow(() -> new NotFoundException("User not found"));
    
    // Navegación problemática
    List<ProductEntity> products = user.getProducts(); // ← EVITAR
    
    return products.stream()
        .map(this::toResponseDto)
        .collect(Collectors.toList());
}
```

**Problemas de este enfoque**:
* **LazyInitializationException**: Si la sesión Hibernate está cerrada
* **Carga EAGER**: Consume memoria innecesariamente
* **Sin control de consulta**: No se pueden aplicar filtros eficientemente
* **N+1 Problem**: Consultas múltiples ocultas
* **No escala**: Con miles de productos es inviable

## **2.2. Consulta explícita (recomendada)**

**Concepto**: Usar el repositorio correspondiente para consultas directas.

```java
// ✅ RECOMENDADO - Consulta explícita
@Override
public List<ProductResponseDto> getProductsByUserId(Long userId) {
    // 1. Validar que el usuario existe
    if (!userRepository.existsById(userId)) {
        throw new NotFoundException("Usuario no encontrado con ID: " + userId);
    }
    
    // 2. Consulta explícita al repositorio correcto
    List<ProductEntity> products = productRepository.findByOwnerId(userId);
    
    // 3. Mapear a DTOs
    return products.stream()
        .map(this::toResponseDto)
        .collect(Collectors.toList());
}
```

**Ventajas de este enfoque**:
* **Control total**: Se especifica exactamente qué traer
* **Filtros eficientes**: Se aplican a nivel de base de datos
* **Performance predecible**: Una consulta, resultado conocido
* **Escalable**: Funciona con cualquier volumen de datos
* **Mantenible**: Lógica clara y explícita

### **Comparación práctica**

| Aspecto | Navegación | Consulta Explícita |
|---------|------------|-------------------|
| **Performance** | ⚠️ Impredecible | ✅ Controlada |
| **Escalabilidad** | ❌ Limitada | ✅ Excelente |
| **Filtros** | ❌ En memoria | ✅ En BD |
| **Mantenimiento** | ⚠️ Dependencias ocultas | ✅ Lógica explícita |
| **Testing** | ❌ Complejo | ✅ Directo |

# **3. Principio de Responsabilidad en Spring Boot**

## **3.1. Regla fundamental**

**El repositorio correcto es el del agregado consultado, independientemente del contexto del endpoint.**

## **3.2. Patrón de implementación**

```
@Controller
UserController.getProducts(userId, filters)
        ↓
@Service  
UserService.getProductsByUserId(userId, filters)
        ↓
@Repository
ProductRepository.findByOwnerIdWithFilters(userId, filters) ← Repositorio correcto
```

**¿Por qué ProductRepository y no UserRepository?**
* Los **datos consultados son productos**
* Product es el **agregado raíz** de los datos retornados
* ProductRepository tiene **conocimiento especializado** sobre consultas de productos
* Permite **optimizaciones específicas** (índices, joins, etc.)

# **4. Actualización de Entidades para Consultas Relacionadas**

## **4.1. UserEntity con relación bidireccional (solo para modelo)**

Archivo: `users/entities/UserEntity.java`

```java
@Entity
@Table(name = "users")
public class UserEntity extends BaseModel {



    // ================== RELACIÓN BIDIRECCIONAL ==================

    /**
     * Relación One-to-Many con Products
     * IMPORTANTE: Esta relación existe solo para consistencia del modelo
     * NO debe usarse para consultas desde el servicio
     */
    @OneToMany(mappedBy = "owner", fetch = FetchType.LAZY)
    private Set<ProductEntity> products = new HashSet<>();

    // Constructores
    

    // ============== GETTERS Y SETTERS ==============


}
```

### **¿Por qué agregar la relación si no la vamos a usar?**

**Razones**:
* **Consistencia del modelo**: Refleja la relación real en el dominio
* **Documentación**: Otros desarrolladores entienden la relación
* **Herramientas ORM**: Algunos frameworks requieren relaciones bidireccionales
* **Flexibilidad futura**: Si eventualmente se necesita navegar (con cuidado)

**IMPORTANTE**: La relación existe a nivel de modelo, pero **NO debe usarse como mecanismo de consulta** desde los servicios.

# **5. Implementación de Request Parameters**

## **5.1. UserController - Endpoints con contexto semántico**

Archivo: `users/controllers/UserController.java`

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    // ============== OTROS ENDPOINTS EXISTENTES ==============

    // ============== ENDPOINT BÁSICO: PRODUCTOS DE USUARIO ==============

    /**
     * Obtiene todos los productos de un usuario específico
     * Ejemplo: GET /api/users/123/products
     */
    @GetMapping("/{id}/products")
    public ResponseEntity<List<ProductResponseDto>> getProducts(
            @PathVariable Long id) {
        
        List<ProductResponseDto> products = userService.getProductsByUserId(id);
        return ResponseEntity.ok(products);
    }

    // ============== ENDPOINT AVANZADO: PRODUCTOS CON FILTROS ==============

    /**
     * Obtiene productos de un usuario con filtros opcionales
     * Ejemplo: GET /api/users/5/products-v2?name=laptop&minPrice=500&maxPrice=2000&categoryId=3
     */
    
    @GetMapping("/{id}/products-v2")
    public ResponseEntity<List<ProductResponseDto>> getProductsWithFilters(
            @PathVariable Long id,
            @RequestParam(required = false) String name,
            @RequestParam(required = false) Double minPrice,
            @RequestParam(required = false) Double maxPrice,
            @RequestParam(required = false) Long categoryId) {
        
        List<ProductResponseDto> products = userService.getProductsByUserIdWithFilters(
            id, name, minPrice, maxPrice, categoryId);
        
        return ResponseEntity.ok(products);
    }

    

}
```

### **Aspectos clave del controlador**

1. **Contexto semántico claro**: Los endpoints están bajo `/users/{id}/` porque el contexto es el usuario
2. **Request parameters opcionales**: Todos los filtros son `required = false`
3. **Separación de responsabilidades**: El controlador solo expone endpoints, delega al servicio
4. **Convenciones REST**: Se mantiene la semántica REST correcta

## **5.2. Validación de Request Parameters**

Para validaciones más robustas, se puede usar un DTO de filtros:

Archivo: `users/dtos/ProductFilterDto.java`

```java
import javax.validation.constraints.*;

public class ProductFilterDto {

    @Size(min = 2, max = 100, message = "El nombre debe tener entre 2 y 100 caracteres")
    private String name;

    @DecimalMin(value = "0.0", inclusive = true, message = "El precio mínimo debe ser mayor o igual a 0")
    private Double minPrice;

    @DecimalMin(value = "0.0", inclusive = true, message = "El precio máximo debe ser mayor o igual a 0")
    private Double maxPrice;

    @Positive(message = "El ID de categoría debe ser positivo")
    private Long categoryId;

    // Constructores
    public ProductFilterDto() {
    }

    // Getters y setters
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Double getMinPrice() {
        return minPrice;
    }

    public void setMinPrice(Double minPrice) {
        this.minPrice = minPrice;
    }

    public Double getMaxPrice() {
        return maxPrice;
    }

    public void setMaxPrice(Double maxPrice) {
        this.maxPrice = maxPrice;
    }

    public Long getCategoryId() {
        return categoryId;
    }

    public void setCategoryId(Long categoryId) {
        this.categoryId = categoryId;
    }

    // ============== VALIDACIONES DE NEGOCIO ==============

    /**
     * Valida que maxPrice sea mayor o igual a minPrice
     */
    public boolean isValidPriceRange() {
        if (minPrice != null && maxPrice != null) {
            return maxPrice >= minPrice;
        }
        return true;
    }
}
```

### **Controlador alternativo con DTO de filtros**

```java
@GetMapping("/{id}/products-v3")
public ResponseEntity<List<ProductResponseDto>> getProductsWithFiltersDto(
        @PathVariable Long id,
        @Valid @ModelAttribute ProductFilterDto filters) {
    
    // Validación adicional de negocio
    if (!filters.isValidPriceRange()) {
        throw new BadRequestException("El precio máximo debe ser mayor o igual al precio mínimo");
    }
    
    List<ProductResponseDto> products = userService.getProductsByUserIdWithFilters(
        id, filters.getName(), filters.getMinPrice(), 
        filters.getMaxPrice(), filters.getCategoryId());
    
    return ResponseEntity.ok(products);
}
```

# **6. Implementación del UserService**

## **6.1. Actualización del UserService con consultas relacionadas**

Archivo: `users/services/UserService.java`

```java
import java.util.List;

public interface UserService {

    // ============== MÉTODOS BÁSICOS EXISTENTES ==============
    
    UserResponseDto create(CreateUserDto createUserDto);
    List<UserResponseDto> findAll();
    UserResponseDto findById(Long id);
    UserResponseDto update(Long id, UpdateUserDto updateUserDto);
    void delete(Long id);

    // ============== NUEVOS MÉTODOS PARA CONSULTAS RELACIONADAS ==============

    /**
     * Obtiene todos los productos de un usuario específico
     * @param userId ID del usuario
     * @return Lista de productos del usuario
     */
    List<ProductResponseDto> getProductsByUserId(Long userId);

    /**
     * Obtiene productos de un usuario aplicando filtros opcionales
     * @param userId ID del usuario
     * @param name Filtro por nombre (opcional)
     * @param minPrice Precio mínimo (opcional)
     * @param maxPrice Precio máximo (opcional)
     * @param categoryId ID de categoría (opcional)
     * @return Lista de productos filtrados
     */
    List<ProductResponseDto> getProductsByUserIdWithFilters(
        Long userId,
        String name,
        Double minPrice,
        Double maxPrice,
        Long categoryId
    );
}
```

## **6.2. Implementación del UserServiceImpl**

Archivo: `users/services/UserServiceImpl.java`

```java
@Service
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final ProductRepository productRepository; // ← Inyección del repositorio correcto

    public UserServiceImpl(UserRepository userRepository, ProductRepository productRepository) {
        this.userRepository = userRepository;
        this.productRepository = productRepository;
    }

    // ============== MÉTODOS BÁSICOS EXISTENTES ==============
  
    // ============== NUEVOS MÉTODOS PARA CONSULTAS RELACIONADAS ==============

    @Override
    public List<ProductResponseDto> getProductsByUserId(Long userId) {
        // 1. Validar que el usuario existe
        if (!userRepository.existsById(userId)) {
            throw new NotFoundException("Usuario no encontrado con ID: " + userId);
        }
        
        // 2. Consulta explícita al repositorio correcto
        List<ProductEntity> products = productRepository.findByOwnerId(userId);
        
        // 3. Mapear a DTOs
        return products.stream()
            .map(this::toProductResponseDto)
            .collect(Collectors.toList());
    }

    @Override
    public List<ProductResponseDto> getProductsByUserIdWithFilters(
            Long userId,
            String name,
            Double minPrice,
            Double maxPrice,
            Long categoryId) {
        
        // 1. Validar que el usuario existe
        if (!userRepository.existsById(userId)) {
            throw new NotFoundException("Usuario no encontrado con ID: " + userId);
        }
        
        // 2. Validaciones de filtros
        if (minPrice != null && minPrice < 0) {
            throw new BadRequestException("El precio mínimo no puede ser negativo");
        }
        
        if (maxPrice != null && maxPrice < 0) {
            throw new BadRequestException("El precio máximo no puede ser negativo");
        }
        
        if (minPrice != null && maxPrice != null && maxPrice < minPrice) {
            throw new BadRequestException("El precio máximo debe ser mayor o igual al precio mínimo");
        }
        
        // 3. Consulta con filtros al repositorio correcto
        List<ProductEntity> products = productRepository.findByOwnerIdWithFilters(
            userId, name, minPrice, maxPrice, categoryId);
        
        // 4. Mapear a DTOs
        return products.stream()
            .map(this::toProductResponseDto)
            .collect(Collectors.toList());
    }

    // ============== MÉTODO HELPER ==============

    /**
     * Convierte ProductEntity a ProductResponseDto
     * NOTA: Este método podría estar en un mapper separado para mejor organización
     */
    private ProductResponseDto toProductResponseDto(ProductEntity product) {
        ProductResponseDto dto = new ProductResponseDto();
        
        dto.id = product.getId();
        dto.name = product.getName();
        dto.price = product.getPrice();
        dto.description = product.getDescription();
        dto.createdAt = product.getCreatedAt();
        dto.updatedAt = product.getUpdatedAt();
        
        // Información del usuario (owner)
        dto.user = new ProductResponseDto.UserSummaryDto();
        dto.user.id = product.getOwner().getId();
        dto.user.name = product.getOwner().getName();
        dto.user.email = product.getOwner().getEmail();
        
        List<CategoryResponseDto> categoryDtos = new ArrayList<>();
        for (CategoryEntity categoryEntity : entity.getCategories()) {
            CategoryResponseDto categoryDto = new CategoryResponseDto();
            categoryDto.id = categoryEntity.getId();
            categoryDto.name = categoryEntity.getName();
            categoryDtos.add(categoryDto);
        }
        dto.categories = categoryDtos;
        
        return dto;
    }
}
```

### **Aspectos clave del servicio**

1. **Inyección correcta**: Se inyecta `ProductRepository` porque los datos consultados son productos
2. **Validación proactiva**: Se valida que el usuario exista antes de consultar
3. **Consulta explícita**: Se usa `productRepository.findByOwnerId()` en lugar de navegar relaciones
4. **Validaciones de negocio**: Se validan los filtros antes de aplicarlos
5. **Separación de responsabilidades**: El servicio orquesta, el repositorio consulta

# **7. Actualización del ProductRepository**

## **7.1. ProductRepository con consultas especializadas**

Archivo: `products/repositories/ProductRepository.java`

```java
@Repository
public interface ProductRepository extends JpaRepository<ProductEntity, Long> {

    // ============== CONSULTAS BÁSICAS DE RELACIONES (ya implementadas) ==============
    
    List<ProductEntity> findByOwnerId(Long userId);
    List<ProductEntity> findByCategoryId(Long categoryId);
    List<ProductEntity> findByOwnerName(String ownerName);
    List<ProductEntity> findByCategoryName(String categoryName);
    List<ProductEntity> findByCategoryIdAndPriceGreaterThan(Long categoryId, Double price);

    // ============== NUEVA CONSULTA CON FILTROS DINÁMICOS ==============

    /**
     * Encuentra productos de un usuario con filtros opcionales
     * Usa @Query personalizada para manejar filtros dinámicos
     * NOTA: categoryId filtra por la relación Many-to-Many con categories
     */
    @Query("SELECT DISTINCT p FROM ProductEntity p " +
           "LEFT JOIN p.categories c " +
           "WHERE p.owner.id = :userId " +
           "AND (COALESCE(:name, '') = '' OR LOWER(p.name) LIKE LOWER(CONCAT('%', :name, '%'))) " +
           "AND (:minPrice IS NULL OR p.price >= :minPrice) " +
           "AND (:maxPrice IS NULL OR p.price <= :maxPrice) " +
           "AND (:categoryId IS NULL OR c.id = :categoryId)")
    List<ProductEntity> findByOwnerIdWithFilters(
        @Param("userId") Long userId,
        @Param("name") String name,
        @Param("minPrice") Double minPrice,
        @Param("maxPrice") Double maxPrice,
        @Param("categoryId") Long categoryId
    );

    // ============== ALTERNATIVA CON SPECIFICATION (AVANZADA) ==============

    /**
     * Para casos más complejos, se puede usar Specification
     * Requiere implementar JpaSpecificationExecutor<ProductEntity>
     */
    // Esta implementación se puede agregar si se necesita más flexibilidad
}
```

### **Explicación de la consulta @Query**

```sql
-- SQL generado aproximadamente:
SELECT DISTINCT p.* FROM products p 
JOIN users u ON p.user_id = u.id 
LEFT JOIN product_categories pc ON p.id = pc.product_id
LEFT JOIN categories c ON pc.category_id = c.id
WHERE p.user_id = ? 
  AND (COALESCE(?, '') = '' OR LOWER(p.name) LIKE LOWER('%' || ? || '%'))
  AND (? IS NULL OR p.price >= ?)
  AND (? IS NULL OR p.price <= ?)
  AND (? IS NULL OR c.id = ?)
```

**Ventajas de este enfoque**:
* **Filtros opcionales**: Si un parámetro es `null` o vacío, no se aplica el filtro
* **COALESCE para strings**: Maneja tanto valores `NULL` como strings vacíos correctamente
* **Performance**: Filtros aplicados en base de datos, no en memoria
* **Flexibilidad**: Se pueden combinar filtros de forma dinámica
* **Búsqueda parcial**: `LIKE` permite buscar por nombre parcial
* **Case-insensitive**: `LOWER()` hace la búsqueda insensible a mayúsculas
* **DISTINCT necesario**: Evita duplicados cuando un producto tiene múltiples categorías

## **7.2. Alternativa avanzada con Specification**

Para casos más complejos, se puede usar `Specification`:

```java
@Repository
public interface ProductRepository extends JpaRepository<ProductEntity, Long>, 
                                           JpaSpecificationExecutor<ProductEntity> {
    // Métodos básicos...
}
```

```java
// Clase helper para Specifications
public class ProductSpecifications {

    public static Specification<ProductEntity> belongsToUser(Long userId) {
        return (root, query, criteriaBuilder) -> 
            criteriaBuilder.equal(root.get("owner").get("id"), userId);
    }

    public static Specification<ProductEntity> nameContains(String name) {
        return (root, query, criteriaBuilder) -> {
            if (name == null || name.trim().isEmpty()) {
                return null;
            }
            return criteriaBuilder.like(
                criteriaBuilder.lower(root.get("name")),
                "%" + name.toLowerCase() + "%"
            );
        };
    }

    public static Specification<ProductEntity> priceGreaterThanOrEqual(Double minPrice) {
        return (root, query, criteriaBuilder) -> {
            if (minPrice == null) {
                return null;
            }
            return criteriaBuilder.greaterThanOrEqualTo(root.get("price"), minPrice);
        };
    }

    public static Specification<ProductEntity> priceLessThanOrEqual(Double maxPrice) {
        return (root, query, criteriaBuilder) -> {
            if (maxPrice == null) {
                return null;
            }
            return criteriaBuilder.lessThanOrEqualTo(root.get("price"), maxPrice);
        };
    }

    public static Specification<ProductEntity> hasCategory(Long categoryId) {
        return (root, query, criteriaBuilder) -> {
            if (categoryId == null) {
                return null;
            }
            // JOIN con la colección categories (relación Many-to-Many)
            Join<ProductEntity, CategoryEntity> categoryJoin = root.join("categories");
            return criteriaBuilder.equal(categoryJoin.get("id"), categoryId);
        };
    }
}
```

### **Uso con Specification en el servicio**

```java
@Override
public List<ProductResponseDto> getProductsByUserIdWithFilters(
        Long userId, String name, Double minPrice, Double maxPrice, Long categoryId) {
    
    // Construir Specification dinámicamente
    Specification<ProductEntity> spec = Specification.where(
        ProductSpecifications.belongsToUser(userId))
        .and(ProductSpecifications.nameContains(name))
        .and(ProductSpecifications.priceGreaterThanOrEqual(minPrice))
        .and(ProductSpecifications.priceLessThanOrEqual(maxPrice))
        .and(ProductSpecifications.hasCategory(categoryId));
    
    // Ejecutar consulta con Specification
    List<ProductEntity> products = productRepository.findAll(spec);
    
    return products.stream()
        .map(this::toProductResponseDto)
        .collect(Collectors.toList());
}
```


# **8. Actividad Práctica Completa**

## **8.1. Implementación requerida**

El estudiante debe implementar:

1. **Actualizar UserEntity** con relación `@OneToMany` hacia productos
2. **Implementar endpoints** en `UserController`:
   - `GET /api/users/{id}/products` (básico)
   - `GET /api/users/{id}/products-v2` (con filtros)
3. **Implementar métodos** en `UserService`:
   - `getProductsByUserId(Long userId)`
   - `getProductsByUserIdWithFilters(userId, name, minPrice, maxPrice, categoryId)`
4. **Crear consulta personalizada** en `ProductRepository`:
   - `findByOwnerIdWithFilters()` usando `@Query`
5. **Escribir tests** unitarios e integración

## **8.2. Casos de prueba específicos**

**Probar los siguientes casos**:

```bash
# 1. Productos de usuario existente
GET /api/users/1/products

# 2. Productos con filtro de nombre
GET /api/users/1/products-v2?name=laptop

# 3. Productos en rango de precio
GET /api/users/1/products-v2?minPrice=500&maxPrice=1500

# 4. Productos por categoría
GET /api/users/1/products-v2?categoryId=2

# 5. Filtros combinados
GET /api/users/1/products-v2?name=gaming&minPrice=800&categoryId=2

# 6. Usuario inexistente (debe retornar 404)
GET /api/users/999/products

# 7. Rango de precios inválido (debe retornar 400)
GET /api/users/1/products-v2?minPrice=1500&maxPrice=500
```

## **8.3. Verificaciones técnicas**

1. **SQL generado**: Verificar en logs que se generen consultas eficientes
2. **Lazy loading**: Confirmar que NO se use `user.getProducts()`
3. **Validaciones**: Probar casos de error (usuario inexistente, filtros inválidos)
4. **Performance**: Medir tiempos de respuesta con datasets grandes

# **9. Resultados y Evidencias Requeridas**

## **9.1. Evidencias de implementación**
1. **Captura de UserEntity.java** con relación `@OneToMany` agregada
2. **Captura de UserController.java** con ambos endpoints implementados
3. **Captura de UserServiceImpl.java** con métodos de consulta relacionada
4. **Captura de ProductRepository.java** con consulta `@Query` personalizada

## **9.2. Evidencias de funcionamiento**
1. **Request básico**: `GET /api/users/1/products` con respuesta exitosa
2. **Request con filtros**: `GET /api/users/1/products-v2?name=laptop&minPrice=500` con productos filtrados
3. **Request combinado**: `GET /api/users/1/products-v2?name=gaming&categoryId=2` mostrando múltiples filtros
4. **Error handling**: `GET /api/users/999/products` mostrando error 404

## **9.3. Evidencias técnicas**
1. **SQL queries**: Captura de logs mostrando SQL generado por la consulta con filtros
2. **Tests unitarios**: Capturas de tests pasando para ambos métodos del servicio
3. **Validation**: Captura de error 400 con filtros inválidos (ej: minPrice > maxPrice)

## **9.4. Datos para revisión**

**Usar los productos creados en el tema anterior**:
- Usuario 1 con productos: "Laptop Gaming", "Mouse Inalámbrico", "Monitor 4K"
- Usuario 2 con productos: "Teclado Mecánico", "Libro Java"
- Categorías: "Electrónicos", "Gaming", "Oficina", "Libros"

**Consultas de prueba**:
1. Todos los productos del usuario 1
2. Productos del usuario 1 que contengan "gaming"
3. Productos del usuario 1 entre $500 y $1500
4. Productos del usuario 1 de categoría "Electrónicos"
5. Combinación: productos "gaming" + precio > $800 + categoría "Gaming"

# **10. Conclusiones**

Esta implementación demuestra:

* **Contexto semántico correcto**: `/users/{id}/products` refleja la relación del dominio
* **Separación de responsabilidades**: UserController → UserService → ProductRepository
* **Consultas explícitas**: Uso directo de `productRepository.findByOwnerId()` 
* **Filtrado eficiente**: Request parameters aplicados en base de datos
* **Escalabilidad**: Solución que funciona con grandes volúmenes de datos
* **Mantenibilidad**: Código claro, testeable y extensible

