# Programación y Plataformas Web

# **Spring Boot – Roles y @PreAuthorize**

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg" width="95">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="95">
</div>

## **Práctica 12 (Spring Boot): Protección de Endpoints con Roles**

### **Autores**

**Pablo Torres**

 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: PabloT18


# **Introducción**

En la práctica anterior implementamos autenticación completa con JWT. Con `.anyRequest().authenticated()` en SecurityConfig, **todos los endpoints ya requieren token válido** (excepto los públicos como `/auth/**`).

Ahora vamos a implementar **protección por roles** usando:

- **@PreAuthorize con roles**: hasRole(), hasAnyRole()
- **Roles específicos**: ROLE_USER, ROLE_ADMIN, ROLE_MODERATOR
- **@AuthenticationPrincipal**: Acceder al usuario autenticado
- **Dos enfoques**: Configuración global vs. anotaciones por método

**Prerequisitos**:
- Haber completado la Práctica 11 (JWT + Login)
- Tener usuarios registrados con diferentes roles
- SecurityConfig con @EnableMethodSecurity configurado


# **1. Dos Enfoques para Protección por Roles**

## **1.1. Enfoque 1: Configuración Global (SecurityConfig)**

Proteger rutas completas por patrón de URL:

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        .csrf(AbstractHttpConfigurer::disable)
        .exceptionHandling(exception -> exception
            .authenticationEntryPoint(unauthorizedHandler)
        )
        .sessionManagement(session -> session
            .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
        )
        .authorizeHttpRequests(auth -> auth
            // Endpoints públicos
            .requestMatchers("/auth/**").permitAll()
            .requestMatchers("/status/**").permitAll()
            
            // Endpoints por rol
            .requestMatchers("/api/admin/**").hasRole("ADMIN")
            .requestMatchers("/api/moderator/**").hasAnyRole("ADMIN", "MODERATOR")
            
            // Resto requiere autenticación
            .anyRequest().authenticated()
        )
        .addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class);
    
    return http.build();
}
```

**Ventajas**:
- Centralizado: Toda la configuración en un lugar
- Primera línea de defensa: Bloquea antes de llegar al controlador
- Ideal para proteger rutas administrativas completas

**Desventajas**:
-  Menos granular: Protege por patrón de URL, no por método específico
-  No permite expresiones complejas

## **1.2. Enfoque 2: Anotaciones por Método (@PreAuthorize)**

Proteger métodos individuales con expresiones:

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")  // Solo ADMIN puede eliminar
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        productService.delete(id);
        return ResponseEntity.noContent().build();
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'MODERATOR')")  // ADMIN o MODERATOR
    public ResponseEntity<ProductResponseDto> update(@PathVariable Long id) {
        // ...
    }
}
```

**Ventajas**:
- Granular: Control por método específico
- Expresiones complejas: Permite SpEL avanzado
- Visible: La seguridad está junto al código

**Desventajas**:
-  Distribuido: Seguridad esparcida por múltiples controladores
-  Segunda línea: Se ejecuta después del filtro (más tarde en el flujo)

## **1.3. Mejor Práctica: COMBINAR AMBOS**

```java
// SecurityConfig - Protección básica por rutas
.authorizeHttpRequests(auth -> auth
    .requestMatchers("/auth/**").permitAll()
    .requestMatchers("/api/admin/**").hasRole("ADMIN")  // ← Primera barrera
    .anyRequest().authenticated()
)

// Controlador - Validación granular adicional
@DeleteMapping("/{id}")
@PreAuthorize("hasRole('ADMIN')")  // ← Segunda barrera + control fino
public ResponseEntity<Void> adminDelete(@PathVariable Long id) {
    productService.adminDelete(id);
    return ResponseEntity.noContent().build();
}
```


# **2. ProductController con Protección por Roles**

# **2. ProductController con Protección por Roles**

Archivo: `products/controllers/ProductController.java`

```java
// imports packages y clases....

public class ProductController {


    // ============== ENDPOINTS DE CREACIÓN ==============

    /**
     * Crear producto
     * POST /api/products
     * 
     * Nota: Requiere autenticación por .anyRequest().authenticated()
     * Se asigna al usuario actual como owner en el servicio
     */
    @PostMapping
    public ResponseEntity<ProductResponseDto> create(@Valid @RequestBody CreateProductDto dto) {
        ProductResponseDto created = productService.create(dto);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    // ============== ENDPOINTS DE CONSULTA ==============

    /**
     * Listar TODOS los productos (sin paginación) - SOLO ADMIN
     * GET /api/products
     * 
     * Este endpoint muestra información sensible de todos los usuarios
     * Por eso está protegido con @PreAuthorize
     */
    @GetMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<List<ProductResponseDto>> findAll() {
        List<ProductResponseDto> products = productService.findAll();
        return ResponseEntity.ok(products);
    }

    /**
     * Listar productos con paginación básica
     * GET /api/products/paginated?page=0&size=10&sort=name,asc
     * 
     * Nota: Requiere autenticación por .anyRequest().authenticated()
     */
    @GetMapping("/paginated")
    public ResponseEntity<Page<ProductResponseDto>> findAllPaginado(
            @RequestParam(value = "page", defaultValue = "0") int page,
            @RequestParam(value = "size", defaultValue = "10") int size,
            @RequestParam(value = "sort", defaultValue = "id") String[] sort) {

        Page<ProductResponseDto> products = productService.findAllPaginado(page, size, sort);
        return ResponseEntity.ok(products);
    }

    /**
     * Listar productos usando Slice para mejor performance
     * GET /api/products/slice?page=0&size=10&sort=createdAt,desc
     * 
     * Nota: Requiere autenticación por .anyRequest().authenticated()
     */
    @GetMapping("/slice")
    public ResponseEntity<Slice<ProductResponseDto>> findAllSlice(
            @RequestParam(value = "page", defaultValue = "0") int page,
            @RequestParam(value = "size", defaultValue = "10") int size,
            @RequestParam(value = "sort", defaultValue = "id") String[] sort) {

        Slice<ProductResponseDto> products = productService.findAllSlice(page, size, sort);
        return ResponseEntity.ok(products);
    }

    /**
     * Listar productos con filtros opcionales y paginación
     * GET /api/products/search?name=laptop&minPrice=500&page=0&size=5
     * 
     * Nota: Requiere autenticación por .anyRequest().authenticated()
     */
    @GetMapping("/search")
    public ResponseEntity<Page<ProductResponseDto>> findWithFilters(
            @RequestParam(value = "name", required = false) String name,
            @RequestParam(value = "minPrice", required = false) Double minPrice,
            @RequestParam(value = "maxPrice", required = false) Double maxPrice,
            @RequestParam(value = "categoryId", required = false) Long categoryId,
            @RequestParam(value = "page", defaultValue = "0") int page,
            @RequestParam(value = "size", defaultValue = "10") int size,
            @RequestParam(value = "sort", defaultValue = "id") String[] sort) {

        Page<ProductResponseDto> products = productService.findWithFilters(
                name, minPrice, maxPrice, categoryId, page, size, sort);

        return ResponseEntity.ok(products);
    }

    /**
     * Obtener producto por ID
     * GET /api/products/{id}
     * 
     * Nota: Requiere autenticación por .anyRequest().authenticated()
     */
    @GetMapping("/{id}")
    public ResponseEntity<ProductResponseDto> findById(@PathVariable("id") String id) {
        ProductResponseDto product = productService.findById(Long.parseLong(id));
        return ResponseEntity.ok(product);
    }

    /**
     * Productos de un usuario específico con filtros opcionales y paginación
     * GET /api/products/user/1?name=laptop&page=0&size=5&sort=price,desc
     * 
     * Nota: Requiere autenticación por .anyRequest().authenticated()
     */
    @GetMapping("/user/{userId}")
    public ResponseEntity<Page<ProductResponseDto>> findByUserId(
            @PathVariable("userId") Long userId,
            @RequestParam(value = "name", required = false) String name,
            @RequestParam(value = "minPrice", required = false) Double minPrice,
            @RequestParam(value = "maxPrice", required = false) Double maxPrice,
            @RequestParam(value = "categoryId", required = false) Long categoryId,
            @RequestParam(value = "page", defaultValue = "0") int page,
            @RequestParam(value = "size", defaultValue = "10") int size,
            @RequestParam(value = "sort", defaultValue = "id") String[] sort) {

        Page<ProductResponseDto> products = productService.findByUserIdWithFilters(
                userId, name, minPrice, maxPrice, categoryId, page, size, sort);

        return ResponseEntity.ok(products);
    }

    /**
     * Productos por categoría
     * GET /api/products/category/{categoryId}
     * 
     * Nota: Requiere autenticación por .anyRequest().authenticated()
     */
    @GetMapping("/category/{categoryId}")
    public ResponseEntity<List<ProductResponseDto>> findByCategoryId(
            @PathVariable("categoryId") Long categoryId) {
        List<ProductResponseDto> products = productService.findByCategoryId(categoryId);
        return ResponseEntity.ok(products);
    }

    // ============== ENDPOINTS DE MODIFICACIÓN ==============

    /**
     * Actualizar producto
     * PUT /api/products/{id}
     * 
     * Nota: NO tiene @PreAuthorize aquí porque la validación de ownership
     * se hace EN EL SERVICIO (ver Práctica 13)
     * 
     * El servicio valida:
     * - Si eres USER → Solo puedes actualizar TUS productos
     * - Si eres ADMIN o MODERATOR → Puedes actualizar CUALQUIER producto
     */
    @PutMapping("/{id}")
    public ResponseEntity<ProductResponseDto> update(
            @PathVariable("id") Long id,
            @Valid @RequestBody UpdateProductDto dto) {
        ProductResponseDto updated = productService.update(id, dto);
        return ResponseEntity.ok(updated);
    }

    /**
     * Eliminar producto
     * DELETE /api/products/{id}
     * 
     * Nota: NO tiene @PreAuthorize aquí porque la validación de ownership
     * se hace EN EL SERVICIO (ver Práctica 13)
     * 
     * El servicio valida:
     * - Si eres USER → Solo puedes eliminar TUS productos
     * - Si eres ADMIN o MODERATOR → Puedes eliminar CUALQUIER producto
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable("id") Long id) {
        productService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
```

## **2.1. ¿Por qué update() y delete() NO tienen @PreAuthorize?**

Porque la validación de ownership se hace **EN EL SERVICIO**, no en el controlador:

```java
// NO necesitamos esto en el controlador:
@DeleteMapping("/{id}")
@PreAuthorize("hasRole('ADMIN') or @productService.isOwner(#id, authentication.principal.id)")
public ResponseEntity<Void> delete(@PathVariable Long id) { ... }

// En su lugar, validamos en el servicio (Práctica 13):
@Service
public class ProductService {
    public void delete(Long id) {
        ProductEntity product = findProductOrThrow(id);
        validateOwnership(product);  // ← Aquí se valida
        productRepository.delete(product);
    }
    
    private void validateOwnership(ProductEntity product) {
        UserDetailsImpl currentUser = getCurrentUser();
        
        // ADMIN o MODERATOR pueden todo
        if (hasAnyRole(currentUser, "ADMIN", "MODERATOR")) {
            return;
        }
        
        // USER solo sus propios productos
        if (!product.getOwner().getId().equals(currentUser.getId())) {
            throw new AccessDeniedException("No puedes modificar productos ajenos");
        }
    }
}
```

**Ventajas de validar en el servicio**:
- Mismo método para todos (no necesitas `/admin` separado)
- Lógica de negocio centralizada
- Más fácil de testear
- Reutilizable desde otros lugares

### **¿Cómo funciona @PreAuthorize en findAll()?**

**@PreAuthorize("hasRole('ADMIN')")** evalúa la expresión **ANTES** de ejecutar el método:

```java
@GetMapping
@PreAuthorize("hasRole('ADMIN')")  // ← Se evalúa ANTES del método
public ResponseEntity<List<ProductResponseDto>> findAll() {
    // Solo llega aquí si el usuario tiene ROLE_ADMIN
    List<ProductResponseDto> products = productService.findAll();
    return ResponseEntity.ok(products);
}
```

**Flujo de validación**:
```
Request: GET /api/products
Header: Authorization: Bearer <token-con-ROLE_USER>
        ↓
1. JwtAuthenticationFilter valida token 2. SecurityContext se establece con usuario 3. .anyRequest().authenticated() pasa 4. @PreAuthorize("hasRole('ADMIN')") evalúa    → Usuario tiene ROLE_USER
   → NO tiene ROLE_ADMIN
   → Expresión = false
5. Spring Security lanza AccessDeniedException
6. → 403 Forbidden
   
¡El método NUNCA se ejecuta!
```


# **3. Expresiones de @PreAuthorize**

## **3.1. Expresiones Básicas por Rol**

| Expresión | Descripción | Ejemplo de uso |
|-----------|-------------|----------------|
| `hasRole('ADMIN')` | Usuario tiene rol ADMIN | Eliminar recursos |
| `hasAnyRole('ADMIN', 'MODERATOR')` | Tiene al menos uno de los roles | Moderar contenido |
| `hasRole('ADMIN') and hasRole('MODERATOR')` | Tiene ambos roles | Permisos combinados |

**Ejemplos**:

```java
// Solo ADMIN
@PreAuthorize("hasRole('ADMIN')")
public void deleteUser(Long id) { ... }

// ADMIN o MODERATOR
@PreAuthorize("hasAnyRole('ADMIN', 'MODERATOR')")
public void moderateContent(Long id) { ... }

// Combinación con AND
@PreAuthorize("hasRole('ADMIN') and hasRole('SUPERUSER')")
public void criticalOperation() { ... }
```

## **3.2. Diferencia entre hasRole() y hasAuthority()**

```java
// hasRole() - Añade prefijo "ROLE_" automáticamente
@PreAuthorize("hasRole('ADMIN')")
// Busca: "ROLE_ADMIN" en authorities

// hasAuthority() - Busca el nombre exacto
@PreAuthorize("hasAuthority('ROLE_ADMIN')")
// Busca: "ROLE_ADMIN" en authorities

//  INCORRECTO - No encuentra nada
@PreAuthorize("hasAuthority('ADMIN')")
// Busca: "ADMIN" → NO existe (tenemos "ROLE_ADMIN")
```

**Recomendación**: Usa `hasRole()` por simplicidad y consistencia.

## **3.3. @AuthenticationPrincipal**

Inyecta el usuario autenticado en el método:

```java
@PostMapping
public ResponseEntity<ProductResponseDto> create(
        @Valid @RequestBody CreateProductDto dto,
        @AuthenticationPrincipal UserDetailsImpl currentUser) {
    
    // Acceso directo al usuario autenticado
    Long userId = currentUser.getId();
    String email = currentUser.getEmail();
    String name = currentUser.getName();
    Collection<? extends GrantedAuthority> roles = currentUser.getAuthorities();
    
    // Usar en lógica de negocio
    ProductResponseDto product = productService.create(dto, userId);
    return ResponseEntity.status(HttpStatus.CREATED).body(product);
}
```

**¿Cuándo usar @AuthenticationPrincipal?**
- Crear recursos asociados al usuario actual
- Filtrar resultados por usuario
- Auditoría (quién modificó qué)
- Pasar contexto al servicio


# **4. Flujo Completo de Validación por Roles**

```
Request: DELETE /api/products/5/admin
Header: Authorization: Bearer <token>
        ↓
┌─────────────────────────────────────────┐
│ 1. JwtAuthenticationFilter              │
│    - Extrae token del header            │
│    - Valida con JwtUtil                 │
│    - Carga usuario con roles            │
│    - Establece SecurityContext          │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ 2. SecurityConfig                       │
│    .anyRequest().authenticated()        │
│    Usuario autenticado → Continúa    │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ 3. @PreAuthorize("hasRole('ADMIN')")   │
│    - Extrae authorities del usuario     │
│    - Busca "ROLE_ADMIN"                 │
│    - Tiene → Ejecuta método          │
│    -  NO tiene → 403 Forbidden        │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ 4. Método del controlador               │
│    adminDelete(5)                       │
│    → productService.adminDelete(5)      │
└─────────────────────────────────────────┘
        ↓
 Response 204 No Content
```


# **5. Ejemplos de Peticiones**

# **5. Ejemplos de Peticiones**

## **5.1. Usuario con ROLE_USER**

```http
# Crear producto (permitido)
POST http://localhost:8080/api/products
Authorization: Bearer <token-ROLE_USER>
Body: {"name": "Laptop", "price": 999}
→ 201 Created

# Ver productos paginados (permitido)
GET http://localhost:8080/api/products/paginated?page=0&size=10
Authorization: Bearer <token-ROLE_USER>
→ 200 OK

# Buscar productos (permitido)
GET http://localhost:8080/api/products/search?name=laptop
Authorization: Bearer <token-ROLE_USER>
→ 200 OK

# Actualizar propio producto (permitido, ver Práctica 13)
PUT http://localhost:8080/api/products/1
Authorization: Bearer <token-ROLE_USER-owner>
Body: {"name": "Updated"}
→ 200 OK

# Actualizar producto ajeno (DENEGADO en servicio)
PUT http://localhost:8080/api/products/2
Authorization: Bearer <token-ROLE_USER>
Body: {"name": "Updated"}
→ 403 Forbidden
{
  "status": 403,
  "error": "Forbidden",
  "message": "No puedes modificar productos ajenos"
}

# Intentar listar TODOS los productos (DENEGADO)
GET http://localhost:8080/api/products
Authorization: Bearer <token-ROLE_USER>
→ 403 Forbidden
{
  "status": 403,
  "error": "Forbidden",
  "message": "Access Denied"
}
```

## **5.2. Usuario con ROLE_ADMIN**

```http
# Listar TODOS los productos (permitido)
GET http://localhost:8080/api/products
Authorization: Bearer <token-ROLE_ADMIN>
→ 200 OK
[
  { "id": 1, "name": "Laptop", "owner": {...} },
  { "id": 2, "name": "Mouse", "owner": {...} },
  ...
]

# Actualizar cualquier producto (permitido)
PUT http://localhost:8080/api/products/1
Authorization: Bearer <token-ROLE_ADMIN>
Body: {"name": "Updated by admin"}
→ 200 OK

# Eliminar cualquier producto (permitido)
DELETE http://localhost:8080/api/products/2
Authorization: Bearer <token-ROLE_ADMIN>
→ 204 No Content
```

## **5.3. Usuario con ROLE_MODERATOR**

```http
# Actualizar cualquier producto (permitido, si así lo defines en servicio)
PUT http://localhost:8080/api/products/1
Authorization: Bearer <token-ROLE_MODERATOR>
Body: {"name": "Updated by moderator"}
→ 200 OK

# Eliminar cualquier producto (permitido, si así lo defines en servicio)
DELETE http://localhost:8080/api/products/2
Authorization: Bearer <token-ROLE_MODERATOR>
→ 204 No Content

# Intentar listar TODOS los productos (DENEGADO)
GET http://localhost:8080/api/products
Authorization: Bearer <token-ROLE_MODERATOR>
→ 403 Forbidden
```

## **5.4. Sin Token**

```http
# Cualquier endpoint protegido
GET http://localhost:8080/api/products/paginated
→ 401 Unauthorized
{
  "status": 401,
  "error": "Unauthorized",
  "message": "Token de autenticación inválido o no proporcionado"
}
```


# **6. Configuración Necesaria**

## **6.1. @EnableMethodSecurity en SecurityConfig**

Para que @PreAuthorize funcione, debes tener:

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity(prePostEnabled = true)  // ← IMPORTANTE
public class SecurityConfig {
    // ...
}
```

**¿Qué hace @EnableMethodSecurity?**
- Habilita anotaciones de seguridad en métodos
- Permite usar @PreAuthorize, @PostAuthorize, @Secured
- Evalúa expresiones SpEL antes de ejecutar métodos
- Integra con SecurityContext de Spring Security

**Sin esta anotación**:
```java
@PreAuthorize("hasRole('ADMIN')")
public void delete() { }
// ← Se ignora, el método se ejecuta sin validar
```

## **6.2. Tabla Comparativa de Protección**

| Endpoint | Método | Protección | Quién puede acceder |
|----------|--------|------------|---------------------|
| `POST /api/products` | create() | `.anyRequest().authenticated()` | Cualquier usuario autenticado |
| `GET /api/products` | findAll() | `@PreAuthorize("hasRole('ADMIN')")` | Solo ADMIN |
| `GET /api/products/paginated` | findAllPaginado() | `.anyRequest().authenticated()` | Cualquier usuario autenticado |
| `GET /api/products/slice` | findAllSlice() | `.anyRequest().authenticated()` | Cualquier usuario autenticado |
| `GET /api/products/search` | findWithFilters() | `.anyRequest().authenticated()` | Cualquier usuario autenticado |
| `GET /api/products/{id}` | findById() | `.anyRequest().authenticated()` | Cualquier usuario autenticado |
| `GET /api/products/user/{userId}` | findByUserId() | `.anyRequest().authenticated()` | Cualquier usuario autenticado |
| `GET /api/products/category/{categoryId}` | findByCategoryId() | `.anyRequest().authenticated()` | Cualquier usuario autenticado |
| `PUT /api/products/{id}` | update() | Ownership en servicio | Propietario, ADMIN o MODERATOR (ver Práctica 13) |
| `DELETE /api/products/{id}` | delete() | Ownership en servicio | Propietario, ADMIN o MODERATOR (ver Práctica 13) |

**Nota importante**: Los métodos `update()` y `delete()` **NO tienen @PreAuthorize en el controlador** porque la validación de ownership (propietario vs ADMIN/MODERATOR) se hace **dentro del servicio** en la Práctica 13.



# **7. Manejo de Excepciones de Autorización**

## **7.1. Problema: Error 500 en lugar de 403**

Cuando un usuario sin el rol adecuado intenta acceder a un endpoint protegido con `@PreAuthorize`, Spring Security lanza una excepción de autorización. Si no la manejas correctamente, tu API devuelve **500 Internal Server Error** en lugar del esperado **403 Forbidden**.

**Ejemplo del problema**:

```http
# Usuario con ROLE_USER intenta acceder a endpoint de ADMIN
GET http://localhost:8080/api/products
Authorization: Bearer <token-ROLE_USER>

# Respuesta INCORRECTA (sin manejador):
→ 500 Internal Server Error
{
  "status": 500,
  "error": "Internal Server Error",
  "message": "Error interno del servidor"
}

# Respuesta CORRECTA (con manejador):
→ 403 Forbidden
{
  "status": 403,
  "error": "Forbidden",
  "message": "No tienes permisos para acceder a este recurso"
}
```

## **7.2. Solución: Agregar Manejadores en GlobalExceptionHandler**

Spring Security lanza diferentes excepciones según la versión y el contexto. Debes manejar todas:

Archivo: `shared/exception/GlobalExceptionHandler.java`

```java
package com.p67.iccppwbackend.shared.exception;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.ConstraintViolation;
import jakarta.validation.ConstraintViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.authorization.AuthorizationDeniedException;
import org.springframework.security.core.AuthenticationException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

    // ============== EXCEPCIONES DE NEGOCIO ==============

    @ExceptionHandler(ApplicationException.class)
    public ResponseEntity<ErrorResponse> handleApplicationException(
            ApplicationException ex,
            HttpServletRequest request) {
        ErrorResponse response = new ErrorResponse(
                ex.getStatus(),
                ex.getMessage(),
                request.getRequestURI());

        return ResponseEntity
                .status(ex.getStatus())
                .body(response);
    }

    // ============== EXCEPCIONES DE VALIDACIÓN ==============

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(
            MethodArgumentNotValidException ex,
            HttpServletRequest request) {
        Map<String, String> errors = new HashMap<>();

        ex.getBindingResult()
                .getFieldErrors()
                .forEach(error -> errors.put(error.getField(), error.getDefaultMessage()));

        ErrorResponse response = new ErrorResponse(
                HttpStatus.BAD_REQUEST,
                "Datos de entrada inválidos",
                request.getRequestURI(),
                errors);

        return ResponseEntity
                .badRequest()
                .body(response);
    }

    // ============== EXCEPCIONES DE SEGURIDAD ==============

    /**
     * Maneja AuthorizationDeniedException (Spring Security 6.x)
     * Se lanza cuando un usuario autenticado no tiene los permisos necesarios
     * 
     * Contexto: Ocurre cuando @PreAuthorize evalúa a false
     * Ejemplo: Usuario con ROLE_USER intenta acceder a endpoint con hasRole('ADMIN')
     */
    @ExceptionHandler(AuthorizationDeniedException.class)
    public ResponseEntity<ErrorResponse> handleAuthorizationDeniedException(
            AuthorizationDeniedException ex,
            HttpServletRequest request) {
        ErrorResponse response = new ErrorResponse(
                HttpStatus.FORBIDDEN,
                "No tienes permisos para acceder a este recurso",
                request.getRequestURI());

        return ResponseEntity
                .status(HttpStatus.FORBIDDEN)
                .body(response);
    }

    /**
     * Maneja AccessDeniedException (Spring Security legacy)
     * Fallback para versiones anteriores de Spring Security o casos específicos
     * 
     * Contexto: Excepción estándar de acceso denegado
     * También se lanza desde código personalizado de validación de ownership
     */
    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<ErrorResponse> handleAccessDeniedException(
            AccessDeniedException ex,
            HttpServletRequest request) {
        ErrorResponse response = new ErrorResponse(
                HttpStatus.FORBIDDEN,
                "Acceso denegado. No tienes los permisos necesarios",
                request.getRequestURI());

        return ResponseEntity
                .status(HttpStatus.FORBIDDEN)
                .body(response);
    }

    /**
     * Maneja AuthenticationException
     * Se lanza cuando hay problemas con la autenticación
     * 
     * Contexto: Problemas con credenciales, tokens inválidos, sesión expirada
     * Nota: JwtAuthenticationFilter ya maneja la mayoría de casos de tokens inválidos
     */
    @ExceptionHandler(AuthenticationException.class)
    public ResponseEntity<ErrorResponse> handleAuthenticationException(
            AuthenticationException ex,
            HttpServletRequest request) {
        ErrorResponse response = new ErrorResponse(
                HttpStatus.UNAUTHORIZED,
                "Credenciales inválidas o sesión expirada",
                request.getRequestURI());

        return ResponseEntity
                .status(HttpStatus.UNAUTHORIZED)
                .body(response);
    }

    // ============== EXCEPCIONES GENERALES ==============

    /**
     * Maneja cualquier excepción no capturada por otros manejadores
     * Debe ser el último manejador (más genérico)
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleUnexpectedException(
            Exception ex,
            HttpServletRequest request) {
        ErrorResponse response = new ErrorResponse(
                HttpStatus.INTERNAL_SERVER_ERROR,
                "Error interno del servidor",
                request.getRequestURI());

        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(response);
    }
}
```

## **7.3. Diferencias entre las Excepciones de Seguridad**

| Excepción | Cuándo se lanza | Código HTTP | Contexto |
|-----------|-----------------|-------------|----------|
| `AuthorizationDeniedException` | @PreAuthorize evalúa a false (Spring Security 6.x) | 403 | Usuario autenticado sin permisos |
| `AccessDeniedException` | Validación de autorización fallida (legacy/custom) | 403 | Usuario autenticado sin permisos |
| `AuthenticationException` | Token inválido, credenciales incorrectas | 401 | Usuario no autenticado |

## **7.4. Flujo de Manejo de Excepciones**

```
Request: GET /api/products
Header: Authorization: Bearer <token-ROLE_USER>
        ↓
1. JwtAuthenticationFilter valida token → OK
2. SecurityContext se establece con usuario
3. @PreAuthorize("hasRole('ADMIN')") evalúa
   → Usuario tiene ROLE_USER
   → NO tiene ROLE_ADMIN
   → Lanza AuthorizationDeniedException
        ↓
4. GlobalExceptionHandler captura excepción
   → Método: handleAuthorizationDeniedException()
   → Crea ErrorResponse con status 403
   → Devuelve ResponseEntity<ErrorResponse>
        ↓
Response: 403 Forbidden
{
  "status": 403,
  "error": "Forbidden",
  "message": "No tienes permisos para acceder a este recurso",
  "path": "/api/products"
}
```

## **7.5. ¿Por qué necesitas AMBOS manejadores?**

```java
// Spring Security 6.x (nueva excepción)
@ExceptionHandler(AuthorizationDeniedException.class)
// Lanzada por @PreAuthorize, @PostAuthorize

// Spring Security legacy (excepción tradicional)
@ExceptionHandler(AccessDeniedException.class)
// Lanzada por código personalizado o configuraciones antiguas
// También útil si lanzas manualmente desde servicios
```

**Ejemplo de uso personalizado**:

```java
@Service
public class ProductService {
    public void delete(Long id) {
        ProductEntity product = findProductOrThrow(id);
        
        if (!isOwner(product)) {
            // Lanza AccessDeniedException manualmente
            throw new AccessDeniedException("No puedes eliminar productos ajenos");
        }
        
        productRepository.delete(product);
    }
}
```

## **7.6. Pruebas de Validación**

Después de agregar los manejadores, verifica:

```http
# 1. Usuario sin rol ADMIN intenta acceder a endpoint protegido
GET http://localhost:8080/api/products
Authorization: Bearer <token-ROLE_USER>
→ Debe devolver 403 (NO 500)
{
  "status": 403,
  "message": "No tienes permisos para acceder a este recurso"
}

# 2. Usuario sin token intenta acceder a endpoint protegido
GET http://localhost:8080/api/products
→ Debe devolver 401
{
  "status": 401,
  "message": "Token de autenticación inválido o no proporcionado"
}

# 3. Usuario ADMIN accede correctamente
GET http://localhost:8080/api/products
Authorization: Bearer <token-ROLE_ADMIN>
→ Debe devolver 200 con lista de productos

# 4. Token expirado o inválido
GET http://localhost:8080/api/products
Authorization: Bearer invalid-token
→ Debe devolver 401
```

## **7.7. Orden de Importancia de los Manejadores**

1. **Manejadores específicos primero**: `@ExceptionHandler(AuthorizationDeniedException.class)`
2. **Manejadores genéricos al final**: `@ExceptionHandler(Exception.class)`

Spring busca el manejador más específico que coincida con la excepción. Si no hay manejadores para `AuthorizationDeniedException`, cae en `Exception.class` y devuelve 500.


# **8. Actividad Práctica**

**Objetivo**: Implementar protección por roles en tu API y manejar correctamente las excepciones de autorización.

**Pasos**:

1. **Agregar @EnableMethodSecurity** en SecurityConfig (si no lo tienes)
   
2. **Agregar manejadores de excepciones de seguridad** en GlobalExceptionHandler:
   - `AuthorizationDeniedException` → 403
   - `AccessDeniedException` → 403
   - `AuthenticationException` → 401

3. **Agregar @PreAuthorize a findAll()** en ProductController:
   ```java
   @GetMapping
   @PreAuthorize("hasRole('ADMIN')")
   public ResponseEntity<List<ProductResponseDto>> findAll() { ... }
   ```

4. **Usar el usuario ADMIN** en tu base de datos:

    Este se genera en el script inicial o puedes asignarlo manualmente:
   ```sql
   -- Asignar ROLE_ADMIN a un usuario existente
   INSERT INTO user_roles (user_id, role_id) 
   VALUES (1, (SELECT id FROM roles WHERE name = 'ROLE_ADMIN'));
   ```

5. **Probar con Postman**:
   - Login con usuario normal (ROLE_USER)
   - Intentar `GET /api/products` → Debe dar **403 Forbidden** (NO 500)
   - Login con usuario ADMIN
   - Intentar `GET /api/products` → Debe funcionar (200)
   - Probar `GET /api/products/paginated` con ambos usuarios → Ambos funcionan
   - Intentar sin token → Debe dar **401 Unauthorized**

6. **Verificar diferencia de endpoints**:
   - `/api/products` → Solo ADMIN (lista completa sin paginación)
   - `/api/products/paginated` → Cualquier usuario autenticado
   - `/api/products/search` → Cualquier usuario autenticado

**Resultado esperado**:
- ADMIN puede acceder a `/api/products` (200 con lista completa)
- USER no puede acceder a `/api/products` (403 Forbidden, NO 500)
- USER puede acceder a `/api/products/paginated` y otros endpoints (200)
- Sin token → 401 Unauthorized en cualquier endpoint protegido
- UPDATE y DELETE funcionan para todos (ownership en servicio, Práctica 13)


# **9. Próximos Pasos**

En la **Práctica 13** implementaremos:
- Validación de ownership en servicios
- Método `validateOwnership()` 
- Diferencia entre validación por rol y por ownership
- ADMIN puede saltarse validación de ownership
- Mejores prácticas de autorización contextual

**Relación entre archivos**:
- **Archivo 11**: Token válido → 401 si falla
- **Archivo 12**: Rol correcto → 403 si falla
- **Archivo 13**: Propietario del recurso → 403 si falla

