# Programación y Plataformas Web

# Frameworks Backend: Spring Boot – Request Parameters, Consultas Relacionadas y Filtrado

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg" width="95">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="95">
</div>

---

# Práctica 9 (Spring Boot): Request Parameters, Consultas Relacionadas y Filtrado con JPA

### Autores

**Pablo Torres**

[ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: PabloT18

---

# 1. Introducción

En la práctica anterior se implementaron relaciones entre entidades usando JPA.

El producto quedó relacionado con:

```txt
UserEntity
CategoryEntity
```

mediante relaciones:

```java
@ManyToOne
@JoinColumn
```

Esto permitió que cada producto tenga:

* un usuario propietario
* una categoría asociada

En esta práctica se trabajará sobre esas relaciones, pero desde el punto de vista de las consultas.

El objetivo es aprender a consultar datos relacionados usando:

* endpoints semánticos
* `@PathVariable`
* `@RequestParam`
* `@ModelAttribute`
* consultas derivadas en repositorios
* consultas personalizadas con `@Query`
* validación de filtros
* manejo global de errores

En esta práctica no se cambia el modelo relacional.

Todavía se mantiene:

```txt
User 1 ──── N Product
Category 1 ──── N Product
```

Todavía no se implementa:

* `@ManyToMany`
* tabla intermedia
* productos con múltiples categorías

Eso se trabajará en una práctica posterior.

---

# 2. Problema actual

En la práctica anterior se agregaron endpoints como:

```txt
GET /api/products/user/{userId}
GET /api/products/category/{categoryId}
```

Estos endpoints funcionan, pero no expresan completamente el contexto del dominio.

Cuando se desea consultar los productos de un usuario, el usuario es el contexto principal.

Una ruta más semántica sería:

```txt
GET /api/users/{id}/products
```

Cuando se desea consultar los productos de una categoría, la categoría es el contexto principal.

Una ruta más semántica sería:

```txt
GET /api/categories/{id}/products
```

Además, en una API real no basta con listar todo.

También se necesitan filtros como:

```txt
name
minPrice
maxPrice
categoryId
userId
```

Ejemplos:

```txt
GET /api/users/1/products?name=laptop
GET /api/users/1/products?minPrice=500&maxPrice=1500
GET /api/users/1/products?categoryId=2
GET /api/categories/2/products?name=gaming
```

---

# 3. Flujo después de aplicar filtros

El flujo será:

```txt
Cliente
  ↓
UsersController / CategoriesController
  ↓
ProductFilterByUserDto
  ↓
ProductService
  ↓
ProductServiceImpl
  ↓
ProductRepository
  ↓
PostgreSQL
  ↓
ProductEntity
  ↓
ProductResponseDto
  ↓
Cliente
```

El controlador define el contexto de la consulta.

El servicio valida el contexto y los filtros.

El repositorio ejecuta la consulta sobre productos.

---

## 3.1. Responsabilidad de cada clase

| Clase                  | Responsabilidad                                        |
| ---------------------- | ------------------------------------------------------ |
| `UsersController`      | Exponer endpoint semántico `/users/{id}/products`      |
| `CategoriesController` | Exponer endpoint semántico `/categories/{id}/products` |
| `ProductFilterByUserDto`     | Recibir filtros opcionales por query params            |
| `ProductService`       | Definir operaciones de consulta filtrada               |
| `ProductServiceImpl`   | Validar contexto y delegar al repositorio              |
| `ProductRepository`    | Ejecutar consultas relacionales con filtros            |
| `ProductResponseDto`   | Devolver producto con relaciones anidadas              |
| `NotFoundException`    | Reportar usuario, categoría o producto inexistente     |
| `BadRequestException`  | Reportar filtros inválidos                             |

---

# 4. Contexto semántico en endpoints REST

El contexto semántico indica desde qué recurso se consulta la información.

---

## 4.1. Productos desde el contexto de usuario

Ruta recomendada:

```txt
GET /api/users/{id}/products
```

Significa:

```txt
Obtener los productos del usuario con id indicado.
```

Ejemplo:

```txt
GET /api/users/1/products
```

Con filtros:

```txt
GET /api/users/1/products?name=laptop&minPrice=500&maxPrice=1500&categoryId=2
```

---

## 4.2. Productos desde el contexto de categoría

Ruta recomendada:

```txt
GET /api/categories/{id}/products
```

Significa:

```txt
Obtener los productos de la categoría con id indicado.
```

Ejemplo:

```txt
GET /api/categories/2/products
```

Con filtros:

```txt
GET /api/categories/2/products?name=gaming&minPrice=100
```

---

## 4.3. Diferencia con endpoints técnicos

Endpoint técnico:

```txt
GET /api/products/user/1
```

Endpoint semántico:

```txt
GET /api/users/1/products
```

Ambos pueden funcionar, pero el segundo expresa mejor la relación del dominio.

La ruta indica que:

```txt
products
```

es una subcolección consultada desde:

```txt
users/{id}
```

---

# 5. Navegación de relaciones vs consulta explícita

En JPA existen dos formas de obtener datos relacionados.

---

## 5.1. Navegación de relaciones

La navegación consiste en acceder a una colección desde la entidad padre.

Ejemplo:

```java
UserEntity user = userRepository.findById(userId)
        .orElseThrow(() -> new NotFoundException("User not found"));

Set<ProductEntity> products = user.getProducts();
```

Este enfoque no se usará en esta práctica.

No se recomienda para este caso porque:

* obliga a agregar una colección en `UserEntity`
* puede generar problemas de carga perezosa
* puede producir consultas innecesarias
* dificulta aplicar filtros a nivel de base de datos
* puede cargar demasiados registros en memoria

---

## 5.2. Consulta explícita

La consulta explícita usa el repositorio del recurso que se desea obtener.

Si se van a consultar productos, se usa:

```java
ProductRepository
```

Ejemplo:

```java
List<ProductEntity> products = productRepository.findByOwner_IdAndDeletedFalse(userId);
```

Este enfoque es el recomendado en esta práctica porque:

* consulta directamente la tabla `products`
* permite aplicar filtros en base de datos
* evita recorrer colecciones en memoria
* mantiene control sobre el SQL generado
* escala mejor con muchos registros

---

# 6. No modificar UserEntity con OneToMany

En la práctica anterior `UserEntity` se mantuvo simple.

No se agregó:

```java
@OneToMany(mappedBy = "owner")
private Set<ProductEntity> products;
```

En esta práctica se mantiene esa decisión.

La relación se consulta desde `ProductRepository`.

Esto evita acoplar `UserEntity` con una colección de productos que no siempre se necesita.

La relación real ya existe en la base de datos mediante:

```java
@ManyToOne
@JoinColumn(name = "user_id")
private UserEntity owner;
```

dentro de `ProductEntity`.

---

# 7. DTO para filtros de productos

Se creará un DTO para recibir filtros opcionales desde query params.

Archivo:

```txt
products/dtos/ProductFilterByUserDto.java
```

Código:

```java
/*
 * DTO utilizado para recibir filtros opcionales
 * en consultas de productos.
 *
 * Sus campos llegan desde query params.
 * Ejemplo:
 * /api/users/1/products?name=laptop&minPrice=500&maxPrice=1500&categoryId=2
 */
public class ProductFilterByUserDto {

    @Size(min = 2, max = 150, message = "El nombre debe tener entre 2 y 150 caracteres")
    private String name;

    @DecimalMin(value = "0.0", inclusive = true, message = "El precio mínimo no puede ser negativo")
    private Double minPrice;

    @DecimalMin(value = "0.0", inclusive = true, message = "El precio máximo no puede ser negativo")
    private Double maxPrice;

    @Min(value = 1, message = "El ID de categoría debe ser mayor a 0")
    private Long categoryId;



    /*
     * Valida que el rango de precios sea coherente.
     *
     * Si ambos valores existen, maxPrice debe ser mayor o igual a minPrice.
     */
    public boolean hasValidPriceRange() {
        if (minPrice != null && maxPrice != null) {
            return maxPrice >= minPrice;
        }

        return true;
    }

    /*
     * Retorna true si el filtro name viene vacío.
     */
    public boolean hasEmptyName() {
        return name == null || name.isBlank();
    }

    // Constructor vacío

    // Constructor lleno

    // Getters y setters
}
```

---

# 8. Validación de `@ModelAttribute`

Para recibir filtros desde query params se puede usar:

```java
@ModelAttribute
```

Ejemplo:

```java
@GetMapping("/{id}/products")
public List<ProductResponseDto> findProductsByUser(
        @PathVariable Long id,
        @Valid @ModelAttribute ProductFilterByUserDto filters
) {
    return productService.findByUserIdWithFilters(id, filters);
}
```

Esto permite que Spring construya el DTO usando los query params.

Ejemplo:

```txt
GET /api/users/1/products?name=laptop&minPrice=500
```

Spring asigna:

```txt
filters.name = "laptop"
filters.minPrice = 500
```

---

# 9. Actualización del handler global para filtros

En prácticas anteriores se manejó:

```java
MethodArgumentNotValidException
```

Ese error ocurre principalmente cuando falla `@Valid` sobre un `@RequestBody`.

Cuando se valida un DTO recibido con `@ModelAttribute`, Spring puede lanzar:

```java
BindException
```

Por eso se debe agregar un handler adicional.

Archivo:

```txt
core/exceptions/handler/GlobalExceptionHandler.java
```

Agregar:

```java
/*
 * Maneja errores de validación en query params
 * recibidos mediante @ModelAttribute.
 */
@ExceptionHandler(BindException.class)
public ResponseEntity<ErrorResponse> handleBindException(
        BindException ex,
        HttpServletRequest request
) {
    Map<String, String> errors = new HashMap<>();

    ex.getBindingResult()
            .getFieldErrors()
            .forEach(error ->
                    errors.put(error.getField(), error.getDefaultMessage())
            );

    ErrorResponse response = new ErrorResponse(
            HttpStatus.BAD_REQUEST,
            "Parámetros de consulta inválidos",
            request.getRequestURI(),
            errors
    );

    return ResponseEntity
            .badRequest()
            .body(response);
}
```

Con esto, los errores en filtros también mantienen el formato estándar.

Ejemplo de respuesta:

```json
{
  "timestamp": "2026-01-15T10:30:00",
  "status": 400,
  "error": "Bad Request",
  "message": "Parámetros de consulta inválidos",
  "path": "/api/users/1/products",
  "details": {
    "minPrice": "El precio mínimo no puede ser negativo"
  }
}
```

---

# 10. Actualización de ProductRepository

El repositorio de productos debe incluir consultas con filtros dinámicos.

Archivo:

```txt
products/repositories/ProductRepository.java
```

Código:

```java
/*
 * Repositorio encargado de gestionar la persistencia
 * de productos usando Spring Data JPA.
 *
 * Incluye consultas relacionales y filtros opcionales.
 */
@Repository
public interface ProductRepository extends JpaRepository<ProductEntity, Long> {

    /// Otros métodos existentes ...

    /*
     * Busca productos activos de un usuario aplicando filtros opcionales.
     *
     * Si un filtro llega como null, no se aplica.
     */
    @Query("""
            SELECT p
            FROM ProductEntity p
            WHERE p.deleted = false
              AND p.owner.id = :userId
              AND p.owner.deleted = false
              AND (COALESCE(:name, '') = '' OR LOWER(p.name) LIKE LOWER(CONCAT('%', COALESCE(:name, ''), '%')))
              AND (:minPrice IS NULL OR p.price >= :minPrice)
              AND (:maxPrice IS NULL OR p.price <= :maxPrice)
              AND (:categoryId IS NULL OR p.category.id = :categoryId)
              AND (:categoryId IS NULL OR p.category.deleted = false)
            """)
    List<ProductEntity> findByOwnerIdWithFilters(
            @Param("userId") Long userId,
            @Param("name") String name,
            @Param("minPrice") Double minPrice,
            @Param("maxPrice") Double maxPrice,
            @Param("categoryId") Long categoryId
    );

    /*
     * Busca productos activos de una categoría aplicando filtros opcionales.
     *
     * Si un filtro llega como null, no se aplica.
     */
    @Query("""
            SELECT p
            FROM ProductEntity p
            WHERE p.deleted = false
              AND p.category.id = :categoryId
              AND p.category.deleted = false
              AND (COALESCE(:name, '') = '' OR LOWER(p.name) LIKE LOWER(CONCAT('%', COALESCE(:name, ''), '%')))
              AND (:minPrice IS NULL OR p.price >= :minPrice)
              AND (:maxPrice IS NULL OR p.price <= :maxPrice)
              AND (:userId IS NULL OR p.owner.id = :userId)
              AND (:userId IS NULL OR p.owner.deleted = false)
            """)
    List<ProductEntity> findByCategoryIdWithFilters(
            @Param("categoryId") Long categoryId,
            @Param("name") String name,
            @Param("minPrice") Double minPrice,
            @Param("maxPrice") Double maxPrice,
            @Param("userId") Long userId
    );
}
```

---

## 10.1. Explicación de la consulta

Esta parte:

```java
(:name IS NULL OR LOWER(p.name) LIKE LOWER(CONCAT('%', :name, '%')))
```

significa:

```txt
Si name es null, no se filtra por nombre.
Si name tiene valor, se busca coincidencia parcial sin importar mayúsculas o minúsculas.
```

Esta parte:

```java
(:minPrice IS NULL OR p.price >= :minPrice)
```

significa:

```txt
Si minPrice es null, no se filtra por precio mínimo.
Si minPrice tiene valor, se buscan productos con precio mayor o igual.
```

Esta parte:

```java
(:categoryId IS NULL OR p.category.id = :categoryId)
```

significa:

```txt
Si categoryId es null, no se filtra por categoría.
Si categoryId tiene valor, se buscan productos de esa categoría.
```

---

# 11. Actualización de ProductService

## 11.1. ProductService

Archivo:

```txt
products/services/ProductService.java
```

Agregar métodos:

```java
/*
 * Servicio que define las operaciones disponibles
 * para la gestión de productos.
 */
public interface ProductService {

  
    // Otros métodos existentes ...
  
    List<ProductResponseDto> findByUserIdWithFilters(
            Long userId,
            ProductFilterByUserDto filters
    );

    List<ProductResponseDto> findByCategoryIdWithFilters(
            Long categoryId,
            ProductFilterByUserDto filters
    );

 
}
```

---

# 12. Actualización de ProductServiceImpl

Archivo:

```txt
products/services/ProductServiceImpl.java
```

La clase ya debe tener inyectados:

```java
private final ProductRepository productRepository;

private final UserRepository userRepository;

private final CategoryRepository categoryRepository;
```

---

## 12.1. Consulta de productos por usuario con filtros

```java
/*
 * Retorna productos activos de un usuario aplicando filtros opcionales.
 *
 * Primero valida que el usuario exista y no esté eliminado.
 * Luego valida el rango de precios.
 * Finalmente consulta los productos desde ProductRepository.
 */
@Override
public List<ProductResponseDto> findByUserIdWithFilters(
        Long userId,
        ProductFilterByUserDto filters
) {
    if (!userRepository.existsByIdAndDeletedFalse(userId)) {
        throw new NotFoundException("User not found");
    }

    validateFilters(filters);

    String name = normalizeName(filters.getName());

    return productRepository.findByOwnerIdWithFilters(
                    userId,
                    name,
                    filters.getMinPrice(),
                    filters.getMaxPrice(),
                    filters.getCategoryId()
            )
            .stream()
           .map(ProductMapper::toModelFromEntity)
                .map(ProductMapper::toResponse)
            .toList();
}
```

---

## 12.2. Consulta de productos por categoría con filtros

```java
/*
 * Retorna productos activos de una categoría aplicando filtros opcionales.
 *
 * Primero valida que la categoría exista y no esté eliminada.
 * Luego valida el rango de precios.
 * Finalmente consulta los productos desde ProductRepository.
 */
@Override
public List<ProductResponseDto> findByCategoryIdWithFilters(
        Long categoryId,
        ProductFilterByCategoryDto filters
) {
    if (!categoryRepository.existsByIdAndDeletedFalse(categoryId)) {
        throw new NotFoundException("Category not found");
    }

    validateFilters(filters);

    String name = normalizeName(filters.getName());

    return productRepository.findByCategoryIdWithFilters(
                    categoryId,
                    name,
                    filters.getMinPrice(),
                    filters.getMaxPrice(),
                    filters.getUserId()
            )
            .stream()
           .map(ProductMapper::toModelFromEntity)
                .map(ProductMapper::toResponse)
            .toList();
}
```

---

## 12.3. Método helper para validar filtros

```java
/*
 * Valida reglas de negocio relacionadas con filtros.
 */
private void validateUserFilters(ProductFilterByUserDto filters) {

    if (filters == null) {
        return;
    }

    if (!filters.hasValidPriceRange()) {
        throw new BadRequestException("El precio máximo debe ser mayor o igual al precio mínimo");
    }

    if (filters.getCategoryId() != null &&
            !categoryRepository.existsByIdAndDeletedFalse(filters.getCategoryId())) {
        throw new NotFoundException("Category not found");
    }


}
```

---

## 12.4. Método helper para normalizar nombre

```java
/*
 * Convierte un texto vacío en null.
 *
 * Esto permite que el repositorio ignore el filtro por nombre
 * cuando el query param llega vacío.
 */
private String normalizeName(String name) {

    if (name == null || name.isBlank()) {
        return null;
    }

    return name.trim();
}
```

---


# 13. Actualización de UsersController

Se agrega un endpoint semántico para consultar productos de un usuario.

Archivo:

```txt
users/controllers/UserProductsController.java
```

Código:

```java
/*
 * Controlador REST encargado de exponer consultas relacionadas
 * entre usuarios y productos.
 *
 * La ruta pertenece al contexto semántico de usuarios:
 * /users/{id}/products
 *
 * Sin embargo, la lógica se delega a ProductService
 * porque el recurso consultado es products.
 */
@RestController
@RequestMapping("/users")
public class UserProductsController {

    private final ProductService productService;

    public UserProductsController(

            ProductService productService
    ) {
        this.productService = productService;
    }


    /*
     * Endpoint para consultar productos de un usuario.
     *
     * GET /api/users/{id}/products
     * GET /api/users/{id}/products?name=laptop
     * GET /api/users/{id}/products?minPrice=500&maxPrice=1500
     * GET /api/users/{id}/products?categoryId=2
     */
    @GetMapping("/{id}/products")
    public List<ProductResponseDto> findProductsByUser(
            @PathVariable Long id,
            @Valid @ModelAttribute ProductFilterByUserDto filters
    ) {
        return productService.findByUserIdWithFilters(id, filters);
    }
}
```

---

## 13.1. Explicación

El endpoint final será:

```txt
GET /api/users/{id}/products
```

El controlador está bajo:

```java
@RequestMapping("/users")
```

porque el context-path global ya es:

```txt
/api
```

Por eso no se debe colocar:

```java
@RequestMapping("/api/users")
```

---

# 14. Actualización de CategoriesController

Se agrega un endpoint semántico para consultar productos de una categoría.

Archivo:

```txt
categories/controllers/CategoriesController.java
```

Código:

```java
/*
 * Controlador REST encargado de exponer los endpoints HTTP
 * para la gestión de categorías.
 *
 * También expone consultas semánticas relacionadas con productos
 * desde el contexto de una categoría.
 */
@RestController
@RequestMapping("/categories")
public class CategoriesController {

    private final CategoryService service;

    private final ProductService productService;

    public CategoriesController(
            CategoryService service,
            ProductService productService
    ) {
        this.service = service;
        this.productService = productService;
    }

    // Endpoints existentes de categorías

    /*
     * Endpoint para consultar productos de una categoría.
     *
     * GET /api/categories/{id}/products
     * GET /api/categories/{id}/products?name=gaming
     * GET /api/categories/{id}/products?minPrice=100
     * GET /api/categories/{id}/products?userId=1
     */
    @GetMapping("/{id}/products")
    public List<ProductResponseDto> findProductsByCategory(
            @PathVariable Long id,
            @Valid @ModelAttribute ProductFilterByUserDto filters
    ) {
        return productService.findByCategoryIdWithFilters(id, filters);
    }
}
```

---

# 15. Endpoints disponibles

## Productos por usuario

| Método | Ruta                                                             | Descripción                   |
| ------ | ---------------------------------------------------------------- | ----------------------------- |
| GET    | `/api/users/{id}/products`                                       | Lista productos de un usuario |
| GET    | `/api/users/{id}/products?name=laptop`                           | Filtra por nombre             |
| GET    | `/api/users/{id}/products?minPrice=500`                          | Filtra por precio mínimo      |
| GET    | `/api/users/{id}/products?maxPrice=1500`                         | Filtra por precio máximo      |
| GET    | `/api/users/{id}/products?categoryId=2`                          | Filtra por categoría          |
| GET    | `/api/users/{id}/products?name=gaming&minPrice=800&categoryId=2` | Combina filtros               |

## Productos por categoría

| Método | Ruta                                                 | Descripción                      |
| ------ | ---------------------------------------------------- | -------------------------------- |
| GET    | `/api/categories/{id}/products`                      | Lista productos de una categoría |
| GET    | `/api/categories/{id}/products?name=laptop`          | Filtra por nombre                |
| GET    | `/api/categories/{id}/products?minPrice=100`         | Filtra por precio mínimo         |
| GET    | `/api/categories/{id}/products?maxPrice=900`         | Filtra por precio máximo         |
| GET    | `/api/categories/{id}/products?userId=1`             | Filtra por usuario               |
| GET    | `/api/categories/{id}/products?name=gaming&userId=1` | Combina filtros                  |

---

# 16. Pruebas sugeridas en Postman / Bruno

## Productos de un usuario

Método:

```txt
GET
```

Ruta:

```txt
/api/users/1/products
```

Resultado esperado:

```txt
Lista de productos activos del usuario 1
```

---

## Productos de un usuario filtrados por nombre

Método:

```txt
GET
```

Ruta:

```txt
/api/users/1/products?name=laptop
```

Resultado esperado:

```txt
Productos del usuario 1 cuyo nombre contenga laptop
```

---

## Productos de un usuario filtrados por rango de precio

Método:

```txt
GET
```

Ruta:

```txt
/api/users/1/products?minPrice=500&maxPrice=1500
```

Resultado esperado:

```txt
Productos del usuario 1 con precio entre 500 y 1500
```

---

## Productos de un usuario filtrados por categoría

Método:

```txt
GET
```

Ruta:

```txt
/api/users/1/products?categoryId=2
```

Resultado esperado:

```txt
Productos del usuario 1 pertenecientes a la categoría 2
```

---

## Productos de una categoría

Método:

```txt
GET
```

Ruta:

```txt
/api/categories/1/products
```

Resultado esperado:

```txt
Productos activos de la categoría 1
```

---

## Productos de una categoría filtrados por usuario

Método:

```txt
GET
```

Ruta:

```txt
/api/categories/1/products?userId=1
```

Resultado esperado:

```txt
Productos de la categoría 1 creados por el usuario 1
```

---

## Error por usuario inexistente

Método:

```txt
GET
```

Ruta:

```txt
/api/users/999/products
```

Resultado esperado:

```txt
404 Not Found
```

---

## Error por categoría inexistente

Método:

```txt
GET
```

Ruta:

```txt
/api/categories/999/products
```

Resultado esperado:

```txt
404 Not Found
```

---

## Error por rango inválido

Método:

```txt
GET
```

Ruta:

```txt
/api/users/1/products?minPrice=1500&maxPrice=500
```

Resultado esperado:

```txt
400 Bad Request
```

Mensaje esperado:

```txt
El precio máximo debe ser mayor o igual al precio mínimo
```

---

## Error por parámetro inválido

Método:

```txt
GET
```

Ruta:

```txt
/api/users/1/products?minPrice=-5
```

Resultado esperado:

```txt
400 Bad Request
```

con campo `details`.

---

# 17. SQL esperado

Al consultar productos de un usuario con filtros, Hibernate generará una consulta similar a:

```sql
SELECT 
    p.*
FROM products p
INNER JOIN users u ON p.user_id = u.id
INNER JOIN categories c ON p.category_id = c.id
WHERE p.deleted = false
  AND u.id = ?
  AND u.deleted = false
  AND (? IS NULL OR LOWER(p.name) LIKE LOWER(CONCAT('%', ?, '%')))
  AND (? IS NULL OR p.price >= ?)
  AND (? IS NULL OR p.price <= ?)
  AND (? IS NULL OR c.id = ?);
```

Al consultar productos de una categoría con filtros:

```sql
SELECT 
    p.*
FROM products p
INNER JOIN users u ON p.user_id = u.id
INNER JOIN categories c ON p.category_id = c.id
WHERE p.deleted = false
  AND c.id = ?
  AND c.deleted = false
  AND (? IS NULL OR LOWER(p.name) LIKE LOWER(CONCAT('%', ?, '%')))
  AND (? IS NULL OR p.price >= ?)
  AND (? IS NULL OR p.price <= ?)
  AND (? IS NULL OR u.id = ?);
```

---

# 18. Verificación en PostgreSQL

Entrar a PostgreSQL:

```bash
docker exec -it postgres-dev psql -U ups -d devdb
```

Consultar productos con usuario y categoría:

```sql
SELECT 
    p.id,
    p.name,
    p.price,
    p.stock,
    p.user_id,
    u.name AS user_name,
    p.category_id,
    c.name AS category_name
FROM products p
INNER JOIN users u ON p.user_id = u.id
INNER JOIN categories c ON p.category_id = c.id
WHERE p.deleted = false;
```

Consultar productos de un usuario:

```sql
SELECT 
    p.id,
    p.name,
    p.price,
    p.stock
FROM products p
WHERE p.user_id = 1
  AND p.deleted = false;
```

Consultar productos de una categoría:

```sql
SELECT 
    p.id,
    p.name,
    p.price,
    p.stock
FROM products p
WHERE p.category_id = 1
  AND p.deleted = false;
```

---

# 19. Actividad práctica

Se debe implementar consultas relacionadas con filtros usando request parameters.

---

## 19.1. Crear `ProductFilterByUserDto`

Crear:

```txt
products/dtos/ProductFilterByUserDto.java
```

Debe incluir:

```txt
name
minPrice
maxPrice
categoryId
userId
```

con validaciones.

---

## 19.2. Actualizar `GlobalExceptionHandler`

Agregar manejo de:

```java
BindException
```

para validar correctamente errores de `@ModelAttribute`.

---

## 19.3. Actualizar `ProductRepository`

Agregar:

```txt
findByOwnerIdWithFilters
findByCategoryIdWithFilters
```

usando `@Query`.

---

## 19.4. Actualizar `ProductService`

Agregar métodos:

```txt
findByUserIdWithFilters
findByCategoryIdWithFilters
```

---

## 19.5. Actualizar `UsersController`

Agregar endpoint:

```txt
GET /api/users/{id}/products
```

con filtros opcionales.

---

## 19.6. Actualizar `CategoriesController`

Agregar endpoint:

```txt
GET /api/categories/{id}/products
```

con filtros opcionales.

---

## 19.7. Probar filtros combinados

Probar:

```txt
GET /api/users/1/products?name=laptop
GET /api/users/1/products?minPrice=500&maxPrice=1500
GET /api/users/1/products?categoryId=2
GET /api/users/1/products?name=gaming&minPrice=800&categoryId=2
GET /api/categories/1/products?userId=1
```

---

# 20. Resultados y evidencias

En la nueva entrada del README, se debe agregar:

## Captura de `ProductFilterByUserDto.java`

Debe evidenciar:

* validaciones de `name`
* validaciones de `minPrice`
* validaciones de `maxPrice`
* validaciones de `categoryId`
* validaciones de `userId`
* método `hasValidPriceRange`

---

## Captura de `ProductRepository.java`

Debe evidenciar:

* consulta `findByOwnerIdWithFilters`
* consulta `findByCategoryIdWithFilters`
* uso de `@Query`
* filtros opcionales

---

## Captura de `UsersController.java`

Debe evidenciar el endpoint:

```txt
GET /api/users/{id}/products
```

---

## Captura de `CategoriesController.java`

Debe evidenciar el endpoint:

```txt
GET /api/categories/{id}/products
```

---

## Captura de consulta con filtros por usuario

Ejemplo:

```txt
GET /api/users/1/products?name=laptop&minPrice=500
```

---

## Captura de consulta con filtros por categoría

Ejemplo:

```txt
GET /api/categories/1/products?userId=1
```

---

## Captura de error por rango inválido

Ejemplo:

```txt
GET /api/users/1/products?minPrice=1500&maxPrice=500
```

Debe responder:

```txt
400 Bad Request
```

---

## Captura de SQL en consola o PostgreSQL

Debe evidenciar que la consulta se realiza sobre productos relacionados con usuario y categoría.

---

## Explicación breve

El estudiante debe explicar:

```txt
¿Por qué se usa ProductRepository para consultar productos aunque el endpoint esté dentro del contexto /users/{id}/products?
```
