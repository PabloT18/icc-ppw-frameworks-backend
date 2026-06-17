# Programación y Plataformas Web

# **Spring Boot – Resumen: Seguridad Completa (JWT + Roles + Ownership)**

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg" width="95">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="95">
</div>

## **Resumen Integrado: Prácticas 11, 12 y 13**

### **Autores**

**Pablo Torres**

📧 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

💻 GitHub: PabloT18

---

# **Índice**

1. [Visión General de las 3 Prácticas](#visión-general)
2. [Práctica 11: Autenticación con JWT](#práctica-11)
3. [Práctica 12: Autorización por Roles](#práctica-12)
4. [Práctica 13: Validación de Ownership](#práctica-13)
5. [Integración Completa: Flujo de Seguridad](#integración-completa)
6. [Checklist de Implementación](#checklist)

---

# **Visión General de las 3 Prácticas**

| Práctica | Propósito | Validación | HTTP Code | Lugar |
|----------|-----------|------------|-----------|-------|
| **11 - JWT** | ¿Quién eres? | Token válido | 401 Unauthorized | JwtAuthenticationFilter |
| **12 - Roles** | ¿Qué puedes hacer? | Rol necesario | 403 Forbidden | @PreAuthorize / SecurityConfig |
| **13 - Ownership** | ¿Es tuyo? | Dueño del recurso | 403 Forbidden | Servicio (validateOwnership) |

**Flujo de validación**:
```
Request → [1. ¿Token válido?] → [2. ¿Rol correcto?] → [3. ¿Es dueño?] → Ejecutar
             401 si falla           403 si falla          403 si falla      
```

---

# **Práctica 11: Autenticación con JWT**

## **Objetivo**: 
Validar que el usuario esté autenticado con un token JWT válido.

## **Archivos y Clases Principales**

### **1. JwtUtil**  `security/jwt/JwtUtil.java`
**Responsabilidad**: Crear y validar tokens JWT

**Métodos clave**:
- `generateToken(UserDetailsImpl)` → Crear token con email y roles
- `validateToken(String)` → Verificar si token es válido
- `extractUsername(String)` → Extraer email del token

**Anotaciones**:
- `@Component` → Bean de Spring
- `@Value("${jwt.secret}")` → Leer configuración de application.yml

---

### **2. JwtAuthenticationFilter**  `security/jwt/JwtAuthenticationFilter.java`
**Responsabilidad**: Interceptar TODAS las peticiones y validar token JWT

**Flujo**:
1. Extraer token del header `Authorization: Bearer <token>`
2. Validar token con `JwtUtil`
3. Cargar usuario completo con roles
4. Establecer `Authentication` en `SecurityContext`
5. Continuar con siguiente filtro

**Anotaciones**:
- `@Component` → Bean de Spring
- Extiende `OncePerRequestFilter` → Se ejecuta una vez por request

---

### **3. UserDetailsServiceImpl**  `security/services/UserDetailsServiceImpl.java`
**Responsabilidad**: Cargar usuario desde BD con roles

**Método clave**:
- `loadUserByUsername(String email)` → Busca usuario en BD y retorna `UserDetailsImpl` con roles

**Anotaciones**:
- `@Service` → Bean de servicio
- Implementa `UserDetailsService` (interfaz de Spring Security)

---

### **4. UserDetailsImpl**  `security/services/UserDetailsImpl.java`
**Responsabilidad**: Representar usuario autenticado con roles

**Campos**:
- `id`, `email`, `password`
- `authorities` (roles como `ROLE_ADMIN`, `ROLE_USER`)

**Anotaciones**:
- Implementa `UserDetails` (interfaz de Spring Security)

---

### **5. SecurityConfig**  `security/config/SecurityConfig.java`
**Responsabilidad**: Configurar seguridad de la aplicación

**Configuraciones clave**:
- `.csrf(csrf -> csrf.disable())` → Deshabilitar CSRF (API REST)
- `.sessionCreationPolicy(STATELESS)` → Sin sesiones (JWT es stateless)
- `.requestMatchers("/auth/**").permitAll()` → Rutas públicas
- `.anyRequest().authenticated()` → Todo lo demás requiere token
- `.addFilterBefore(jwtAuthenticationFilter, ...)` → Agregar filtro JWT

**Anotaciones**:
- `@Configuration` → Clase de configuración
- `@EnableWebSecurity` → Habilitar seguridad web
- `@EnableMethodSecurity(prePostEnabled = true)` → Habilitar `@PreAuthorize`
- `@Bean` → Definir beans (SecurityFilterChain, PasswordEncoder)

---

### **6. AuthController**  `auth/controllers/AuthController.java`
**Responsabilidad**: Endpoints de autenticación

**Endpoints**:
- `POST /auth/register` → Registrar usuario
- `POST /auth/login` → Login y obtener token

**Anotaciones**:
- `@RestController` → Controlador REST
- `@RequestMapping("/auth")` → Prefijo de rutas
- `@PostMapping` → Mapear método POST
- `@Valid` → Validar DTO
- `@RequestBody` → Leer JSON del body

---

### **7. AuthService**  `auth/services/AuthService.java`
**Responsabilidad**: Lógica de autenticación

**Métodos clave**:
- `register(RegisterDto)` → Crear usuario, encriptar contraseña, generar token
- `login(LoginDto)` → Validar credenciales, generar token

**Usa**:
- `PasswordEncoder.encode()` → Encriptar contraseña
- `AuthenticationManager.authenticate()` → Validar credenciales
- `JwtUtil.generateToken()` → Crear token

---

## **Configuración en application.yml**
```yaml
jwt:
  secret: tu-secreto-super-seguro-de-al-menos-256-bits
  expiration: 86400000  # 24 horas
```

---

# **Práctica 12: Autorización por Roles**

## **Objetivo**: 
Validar que el usuario tenga el rol necesario para acceder a un recurso.

## **Clases y Componentes Principales**

### **1. SecurityConfig - Habilitar @PreAuthorize**
 `security/config/SecurityConfig.java`

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity(prePostEnabled = true)  // ← CRÍTICO para @PreAuthorize
public class SecurityConfig {
    // ... resto de configuración
}
```

**Anotación clave**:
- `@EnableMethodSecurity(prePostEnabled = true)` → Sin esto, @PreAuthorize se ignora


### **2. ProductController - Protección por Roles**
 `products/controllers/ProductController.java`

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {
    
    @Autowired
    private ProductService productService;
    
    // SOLO ADMIN puede listar TODOS los productos sin paginación
    @GetMapping
    @PreAuthorize("hasRole('ADMIN')")  // ← Valida rol ANTES de ejecutar
    public ResponseEntity<List<ProductResponseDto>> findAll() {
        List<ProductResponseDto> products = productService.findAll();
        return ResponseEntity.ok(products);
    }
    
    // Cualquier usuario autenticado puede crear productos
    @PostMapping
    public ResponseEntity<ProductResponseDto> create(
            @Valid @RequestBody CreateProductDto dto,
            @AuthenticationPrincipal UserDetailsImpl currentUser) {  // ← Usuario del JWT
        
        ProductResponseDto product = productService.create(dto, currentUser);
        return ResponseEntity.status(HttpStatus.CREATED).body(product);
    }
    
    // Cualquier usuario autenticado puede ver paginados
    @GetMapping("/paginated")
    public ResponseEntity<Page<ProductResponseDto>> findAllPaginado(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id,asc") String[] sort) {
        
        Page<ProductResponseDto> products = productService.findAllPaginado(page, size, sort);
        return ResponseEntity.ok(products);
    }
}
```

**Anotaciones clave**:
- `@PreAuthorize("hasRole('ADMIN')")` → Valida rol ADMIN antes de ejecutar
- `@AuthenticationPrincipal UserDetailsImpl currentUser` → Inyecta usuario autenticado del JWT


### **3. Expresiones de @PreAuthorize**

| Expresión | Descripción |
|-----------|-------------|
| `hasRole('ADMIN')` | Usuario tiene rol ADMIN (busca "ROLE_ADMIN") |
| `hasAnyRole('ADMIN', 'MODERATOR')` | Tiene al menos uno de los roles |
| `hasAuthority('ROLE_ADMIN')` | Busca el nombre exacto "ROLE_ADMIN" |
| `hasRole('ADMIN') and hasRole('MODERATOR')` | Tiene ambos roles |
| `hasRole('ADMIN') or @productService.isOwner(#id, principal.id)` | Rol O dueño |

**Diferencia importante**:
```java
// hasRole() - Añade prefijo "ROLE_" automáticamente
@PreAuthorize("hasRole('ADMIN')")        // Busca: "ROLE_ADMIN"

// hasAuthority() - Busca el nombre exacto
@PreAuthorize("hasAuthority('ROLE_ADMIN')")  // Busca: "ROLE_ADMIN"

//  INCORRECTO
@PreAuthorize("hasAuthority('ADMIN')")   // Busca: "ADMIN" (no existe)
```
Archivos y Clases Principales**

### **1. SecurityConfig**  `security/config/SecurityConfig.java`
**Responsabilidad**: Habilitar validación de roles en métodos

**Configuración crítica**:
- `@EnableMethodSecurity(prePostEnabled = true)` → **SIN ESTO `@PreAuthorize` NO FUNCIONA**

---

### **2. ProductController**  `products/controllers/ProductController.java`
**Responsabilidad**: Proteger endpoints por rol

**Anotaciones de protección**:
- `@PreAuthorize("hasRole('ADMIN')")` → Solo ADMIN puede ejecutar el método
- `@PreAuthorize("hasAnyRole('ADMIN', 'MODERATOR')")` → ADMIN o MODERATOR
- `@AuthenticationPrincipal UserDetailsImpl currentUser` → Inyectar usuario autenticado

**Ejemplo**:
```java
@GetMapping                              // GET /api/products
@PreAuthorize("hasRole('ADMIN')")       // Solo ADMIN
public ResponseEntity<List<...>> findAll() { }

@PostMapping                             // POST /api/products
public ResponseEntity<...> create(
    @AuthenticationPrincipal UserDetailsImpl currentUser) { }  // Cualquier autenticado
```

---

### **3. Expresiones de @PreAuthorize**

| Expresión | Qué hace |
|-----------|----------|
| `hasRole('ADMIN')` | Busca "ROLE_ADMIN" (añade prefijo automático) |
| `hasAnyRole('ADMIN', 'MODERATOR')` | Tiene al menos uno de los roles |
| `hasAuthority('ROLE_ADMIN')` | Busca exactamente "ROLE_ADMIN" |
| `hasRole('ADMIN') and hasRole('MOD')` | Tiene ambos roles |

** Diferencia crítica**:
- `hasRole('ADMIN')` → Busca `ROLE_ADMIN` 
- `hasAuthority('ADMIN')` → Busca `ADMIN`  (no existe)

---

### **4. GlobalExceptionHandler**  `shared/exception/GlobalExceptionHandler.java`
**Responsabilidad**: Convertir excepciones de seguridad a respuestas JSON

**Manejadores clave**:

| Excepción | Cuándo se lanza | HTTP | Handler |
|-----------|-----------------|------|---------|
| `AuthorizationDeniedException` | @PreAuthorize evalúa a false (Spring 6.x) | 403 | `@ExceptionHandler(AuthorizationDeniedException.class)` |
| `AccessDeniedException` | Código personalizado (validateOwnership) | 403 | `@ExceptionHandler(AccessDeniedException.class)` |
| `AuthenticationException` | Token inválido/expirado | 401 | `@ExceptionHandler(AuthenticationException.class)` |

**Anotaciones**:
- `@RestControllerAdvice` → Manejo global de excepciones
- `@ExceptionHandler(TipoExcepcion.class)` → Captura excepción específica

**¿Por qué 2 manejadores de 403?**
- Uno para Spring Security automático (`@PreAuthorize`)
- Otro para validaciones manuales en servicios
        if (dto.getPrice() != null) {
            product.setPrice(dto.getPrice());
        }
        // ... más actualizaciones
        
        // 4. Guardar y devolver
        ProductEntity updated = productRepository.save(product);
        return productMapper.toDto(updated);
    }
    
    /**
     * Eliminar producto con validación de ownership
     */
    @Transactional
    public void delete(Long id, UserDetailsImpl currentUser) {
        // 1. Buscar producto
        ProductEntity product = productRepository.findById(id)
            .orElseThrow(() -> new ApplicationException(
     Archivos y Clases Principales**

### **1. ProductController**  `products/controllers/ProductController.java`
**Responsabilidad**: Extraer usuario del JWT y pasarlo al servicio

**Cambio clave**:
```java
// Agregar parámetro en métodos update() y delete()
@PutMapping("/{id}")
public ResponseEntity<...> update(
    @PathVariable Long id,
    @Valid @RequestBody UpdateProductDto dto,
    @AuthenticationPrincipal UserDetailsImpl currentUser) {  // ← Extraer usuario aquí
    
    productService.update(id, dto, currentUser);  // ← Pasar al servicio
}
```

**Anotaciones**:
- `@AuthenticationPrincipal UserDetailsImpl currentUser` → Inyecta usuario del JWT
- `@PathVariable` → Lee parámetro de URL
- `@Valid @RequestBody` → Lee y valida JSON

**Ventajas de este enfoque**:
-  Más testeable (no usa `SecurityContextHolder`)
-  Explícito (se ve qué métodos necesitan usuario)
-  Menos acoplado (servicio no depende de Spring Security)

---

### **2. ProductService**  `products/services/ProductService.java`
**Responsabilidad**: Validar ownership antes de modificar/eliminar

**Métodos clave**:

**`update(Long id, UpdateProductDto dto, UserDetailsImpl currentUser)`**
- Buscar producto
- **Validar ownership** ← Aquí se valida
- Actualizar producto
- Guardar

**`delete(Long id, UserDetailsImpl currentUser)`**
- Buscar producto
- **Validar ownership** ← Aquí se valida
- Eliminar

**`validateOwnership(ProductEntity product, UserDetailsImpl currentUser)`**
- Si ADMIN o MODERATOR → `return` (pasa validación) 
- Si dueño → `return` (pasa validación) 
- Si no → `throw AccessDeniedException` 

**`hasAnyRole(UserDetailsImpl user, String... roles)`**
- Verificar si usuario tiene alguno de los roles especificados

**Anotaciones**:
- `@Service` → Bean de servicio
- `@Transactional` → Transacción BD (rollback automático si falla)

---

### **3. ProductEntity**  `products/entities/ProductEntity.java`
**Responsabilidad**: Representar producto con relación al usuario dueño

**Campo clave**:
```java
@ManyToOne(fetch = FetchType.LAZY)
@JoinColumn(name = "owner_id", nullable = false)
private UserEntity owner;  // ← Usuario que creó el producto
```

**Anotaciones**:
- `@Entity` → Mapea a tabla BD
- `@ManyToOne` → Muchos productos pertenecen a un usuario
- `@JoinColumn(name = "owner_id")` → Columna FK

** Requisito**: Agregar columna `owner_id` en tabla `products`
```bash 
                       ↓
Response: 403 Forbidden
{
  "status": 403,
  "error": "Forbidden",
  "message": "No puedes modificar productos ajenos",
  "path": "/api/products/1"
}
```

## **Escenario 3: Usuario USER intenta listar TODOS los productos**

```
Request: GET /api/products
Header: Authorization: Bearer <token-Usuario-B>

┌────────────────────────────────────────────────────────┐
│ 1. JwtAuthenticationFilter                             │
│    Resultado:  Usuario B autenticado (ROLE_USER)      │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│ 2. SecurityConfig                                      │
│    Resultado:  Usuario autenticado                    │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│ 3. @PreAuthorize("hasRole('ADMIN')")                   │
│    - Busca "ROLE_ADMIN" en authorities                 │
│    - Usuario B tiene "ROLE_USER"                       │
│    - Expresión evalúa a false                          │
│    →  throw AuthorizationDeniedException              │
│    ¡El método findAll() NUNCA se ejecuta!              │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│ 4. GlobalExceptionHandler                              │
│    - Captura AuthorizationDeniedException              │
│    - handleAuthorizationDeniedException()              │
│    - Devuelve ErrorResponse                            │
└────────────────────────────────────────────────────────┘
                        ↓
Response: 403 Forbidden
{
  "status": 403,
  "error": "Forbidden",
  "message": "No tienes permisos para acceder a este recurso",
  "path": "/api/products"
}
```

## **Escenario 4: ADMIN actualiza cualquier producto**

```
Request: PUT /api/products/1
Header: Authorization: Bearer <token-ADMIN>
Body: {"name": "Updated by Admin"}

┌────────────────────────────────────────────────────────┐
│ 1. JwtAuthenticationFilter                             │
│    Resultado:  Usuario ADMIN autenticado              │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│ 2. SecurityConfig                                      │
│    Resultado:  Usuario autenticado                    │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│ 3. ProductController.update()                          │
│    - @AuthenticationPrincipal inyecta Usuario ADMIN    │
│    - Llama: productService.update(1, dto, ADMIN)       │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│ 4. ProductService.update()                             │
│    - Busca Producto #1 → owner_id = Usuario A          │
│    - validateOwnership(producto, ADMIN)                │
│      • ¿Tiene ROLE_ADMIN? SÍ                           │
│      →  return (pasa validación automáticamente)      │
│    - Actualiza producto                                │
│    - Guarda en BD                                      │
└────────────────────────────────────────────────────────┘
                        ↓
Response: 200 OK
{
  "id": 1,
  "name": "Updated by Admin",
  "owner": {
    "id": 1,
    "name": "Usuario A"  ← Owner NO cambia
  }
}
```

---

# **Checklist de Implementación**

## **Práctica 11: Autenticación JWT**

### **Configuración**
- [ ] Agregar dependencia `io.jsonwebtoken:jjwt-api` en `pom.xml`
- [ ] Configurar `jwt.secret` y `jwt.expiration` en `application.yml`
- [ ] Crear tabla `users` y `roles` en BD
- [ ] Relación Many-to-Many entre `users` y `roles`

### **Clases a Crear/Modificar**
- [ ] `JwtUtil.java` - Generar y validar tokens
  - Métodos: `generateToken()`, `validateToken()`, `extractUsername()`
  - Anotación: `@Component`
  
- [ ] `JwtAuthenticationFilter.java` - Filtro de validación
  - Extender: `OncePerRequestFilter`
  - Método: `doFilterInternal()`
  - Anotación: `@Component`
  
- [ ] `UserDetailsServiceImpl.java` - Cargar usuario
  - Implementar: `UserDetailsService`
  - Método: `loadUserByUsername()`
  - Anotación: `@Service`
  
- [ ] `UserDetailsImpl.java` - Usuario con roles
  - Implementar: `UserDetails`
  - Constructor con: `id`, `email`, `password`, `authorities`
  
- [ ] `SecurityConfig.java` - Configuración de seguridad
  - Anotaciones: `@Configuration`, `@EnableWebSecurity`, `@EnableMethodSecurity`
  - Bean: `SecurityFilterChain`
  - Agregar: `addFilterBefore(jwtAuthenticationFilter, ...)`
  
- [ ] `AuthController.java` - Endpoints de autenticación
  - Rutas: `POST /auth/register`, `POST /auth/login`
  - Anotaciones: `@RestController`, `@RequestMapping("/auth")`
  
- [ ] `AuthService.java` - Lógica de autenticación
  - Métodos: `register()`, `login()`
  - Usar: `PasswordEncoder.encode()`, `AuthenticationManager.authenticate()`

### **Probar**
- [ ] POST `/auth/register` → 201 Created con token
- [ ] POST `/auth/login` → 200 OK con token
- [ ] GET `/api/products` sin token → 401 Unauthorized
- [ ] GET `/api/products` con token válido → 200 OK
- [ ] GET `/api/products` con token inválido → 401 Unauthorized

---

## **Práctica 12: Autorización por Roles**

### **Configuración**
- [ ] Verificar `@EnableMethodSecurity(prePostEnabled = true)` en SecurityConfig
- [ ] Crear usuarios con diferentes roles en BD:
  - `ROLE_USER`, `ROLE_ADMIN`, `ROLE_MODERATOR`

### **Clases a Crear/Modificar**
- [ ] `ProductController.java` - Agregar @PreAuthorize
  - `@PreAuthorize("hasRole('ADMIN')")` en `findAll()`
  - `@AuthenticationPrincipal UserDetailsImpl` en `create()`
  
- [ ] `GlobalExceptionHandler.java` - Manejo de excepciones de seguridad
  - `@ExceptionHandler(AuthorizationDeniedException.class)` → 403
  - `@ExceptionHandler(AccessDeniedException.class)` → 403
  - `@ExceptionHandler(AuthenticationException.class)` → 401
  - Anotación: `@RestControllerAdvice`

### **Probar**
- [ ] Usuario USER accede a `/api/products/paginated` → 200 OK 
- [ ] Usuario USER accede a `/api/products` → 403 Forbidden 
- [ ] Usuario ADMIN accede a `/api/products` → 200 OK 
- [ ] Usuario sin token → 401 Unauthorized 
- [ ] Verificar que devuelve 403 (NO 500) cuando falla autorización

---

## **Práctica 13: Validación de Ownership**

### **Configuración**
- [ ] Agregar columna `owner_id` en tabla `products` (FK a `users`)
- [ ] Relación `@ManyToOne` en `ProductEntity`

### **Clases a Crear/Modificar**
- [ ] `ProductController.java` - Pasar usuario al servicio
  - `@AuthenticationPrincipal UserDetailsImpl currentUser` en `update()`
  - `@AuthenticationPrincipal UserDetailsImpl currentUser` en `delete()`
  - Pasar `currentUser` al servicio: `productService.update(id, dto, currentUser)`
  
- [ ] `ProductService.java` - Validación de ownership
  - Agregar parámetro `UserDetailsImpl currentUser` en `update()` y `delete()`
  - Método: `validateOwnership(ProductEntity product, UserDetailsImpl currentUser)`
  - Método: `hasAnyRole(UserDetailsImpl user, String... roles)`
  - Lógica:
    - ADMIN/MODERATOR → `return` (pasa validación)
    - Dueño → `return` (pasa validación)
    - Otros → `throw AccessDeniedException`
  
- [ ] `ProductEntity.java` - Relación con usuario
  - Campo: `@ManyToOne private UserEntity owner;`
  - `@JoinColumn(name = "owner_id")`

### **Probar**
- [ ] Usuario A actualiza su producto (#1) → 200 OK 
- [ ] Usuario B actualiza producto de A (#1) → 403 Forbidden 
- [ ] Usuario A actualiza producto de B (#2) → 403 Forbidden 
- [ ] ADMIN actualiza cualquier producto → 200 OK 
- [ ] MODERATOR actualiza cualquier producto → 200 OK 
- [ ] Usuario A elimina su producto → 204 No Content 
- [ ] Usuario B elimina producto de A → 403 Forbidden 

---

# **Tabla de Decisión Rápida**

| Situación | ¿Dónde validar? | ¿Cómo? | HTTP |
|-----------|-----------------|--------|------|
| ¿Tiene token válido? | JwtAuthenticationFilter | `jwtUtil.validateToken()` | 401 |
| ¿Endpoint solo ADMIN? | Controlador | `@PreAuthorize("hasRole('ADMIN')")` | 403 |
| ¿Es dueño del recurso? | Servicio | `validateOwnership(product, user)` | 403 |
| ¿ADMIN puede modificar todo? | Servicio | `if (hasAnyRole(user, "ROLE_ADMIN"))` |  |

---

# **Preguntas Frecuentes**

## **¿Cuándo usar @PreAuthorize vs validateOwnership?**

**Usa @PreAuthorize cuando**:
- La protección es por **ROL** (ADMIN, USER, etc.)
- La regla es **estática** (no depende de datos de BD)
- Ejemplo: "Solo ADMIN puede listar todos los productos"

**Usa validateOwnership cuando**:
- La protección depende del **dueño del recurso**
- La regla es **dinámica** (depende de datos de BD)
- Ejemplo: "Solo el dueño puede modificar su producto"

## **¿Por qué pasar usuario al servicio en lugar de usar SecurityContextHolder?**

**Ventajas de pasar como parámetro**:
-  Más testeable (no depende de estado global)
-  Más explícito (se ve qué métodos necesitan usuario)
-  Menos acoplado (servicio independiente de Spring Security)

## **¿Dónde va la lógica de negocio?**

- **Controlador**: Mapeo de rutas, validación de entrada, extracción de usuario
- **Servicio**: Lógica de negocio, validación de ownership, operaciones de BD
- **GlobalExceptionHandler**: Manejo de excepciones, conversión a ErrorResponse

## **¿Cuál es el orden de validación?**

1. **Token válido** (JwtAuthenticationFilter) → 401 si falla
2. **Rol necesario** (@PreAuthorize) → 403 si falla
3. **Dueño del recurso** (validateOwnership en servicio) → 403 si falla
4. **Ejecutar operación** → 200/204 si todo OK

---

# **Resumen Final**

 **Práctica 11** = ¿QUIÉN ERES? → Token JWT válido → 401 si falla
 **Práctica 12** = ¿QUÉ PUEDES HACER? → Rol correcto → 403 si falla
 **Práctica 13** = ¿ES TUYO? → Dueño del recurso → 403 si falla

**Las 3 prácticas se COMBINAN** para crear un sistema de seguridad completo:
- JWT valida identidad
- Roles controlan acceso general
- Ownership controla acceso específico a recursos

**Cada capa es independiente pero se complementan**:
- Puedes tener JWT sin ownership
- Puedes tener roles sin ownership
- Pero **ownership NECESITA** JWT y puede combinarse con roles

**ADMIN y MODERATOR** son especiales:
- Pasan validación de ownership automáticamente
- Pueden modificar/eliminar recursos de otros usuarios


---

# **Tabla Resumen de Clases Implementadas**

## **Práctica 11: Autenticación JWT**

| Clase | Ubicación | Responsabilidad | Anotaciones clave | Métodos/Campos principales |
|-------|-----------|-----------------|-------------------|---------------------------|
| **JwtUtil** | `security/jwt/` | Crear y validar tokens JWT | `@Component`, `@Value` | `generateToken()`, `validateToken()`, `extractUsername()` |
| **JwtAuthenticationFilter** | `security/jwt/` | Interceptar requests y validar token | `@Component`, `OncePerRequestFilter` | `doFilterInternal()` - Valida token y establece SecurityContext |
| **UserDetailsServiceImpl** | `security/services/` | Cargar usuario desde BD con roles | `@Service`, `UserDetailsService` | `loadUserByUsername()` - Busca usuario y retorna UserDetailsImpl |
| **UserDetailsImpl** | `security/services/` | Representar usuario autenticado | `UserDetails` | `id`, `email`, `password`, `authorities` |
| **SecurityConfig** | `security/config/` | Configurar seguridad de la app | `@Configuration`, `@EnableWebSecurity`, `@EnableMethodSecurity` | `filterChain()` - Configura filtros, rutas públicas, sin sesiones |
| **AuthController** | `auth/controllers/` | Endpoints de login y registro | `@RestController`, `@RequestMapping` | `register()`, `login()` - Retornan token JWT |
| **AuthService** | `auth/services/` | Lógica de autenticación | `@Service` | `register()` - Crear usuario, `login()` - Validar y generar token |
| **UserEntity** | `users/entities/` | Entidad de usuario en BD | `@Entity`, `@ManyToMany` | `id`, `email`, `password`, `roles` |
| **RoleEntity** | `users/entities/` | Entidad de rol en BD | `@Entity` | `id`, `name` (ROLE_ADMIN, ROLE_USER, etc.) |

---

## **Práctica 12: Autorización por Roles**

| Clase | Ubicación | Responsabilidad | Anotaciones clave | Métodos/Campos principales |
|-------|-----------|-----------------|-------------------|---------------------------|
| **SecurityConfig** | `security/config/` | Habilitar validación de roles | `@EnableMethodSecurity(prePostEnabled = true)` | **Crítico**: Sin esto @PreAuthorize no funciona |
| **ProductController** | `products/controllers/` | Proteger endpoints por rol | `@RestController`, `@PreAuthorize`, `@AuthenticationPrincipal` | `findAll()` - Solo ADMIN, `create()` - Cualquier autenticado |
| **GlobalExceptionHandler** | `shared/exception/` | Convertir excepciones a JSON | `@RestControllerAdvice`, `@ExceptionHandler` | `handleAuthorizationDeniedException()` - 403, `handleAuthenticationException()` - 401 |

**Expresiones @PreAuthorize usadas**:
- `hasRole('ADMIN')` → Solo ADMIN
- `hasAnyRole('ADMIN', 'MODERATOR')` → ADMIN o MODERATOR
- `hasAuthority('ROLE_ADMIN')` → Busca exactamente "ROLE_ADMIN"

---

## **Práctica 13: Validación de Ownership**

| Clase | Ubicación | Responsabilidad | Anotaciones clave | Métodos/Campos principales |
|-------|-----------|-----------------|-------------------|---------------------------|
| **ProductController** | `products/controllers/` | Extraer usuario y pasar al servicio | `@AuthenticationPrincipal` | `update(id, dto, currentUser)`, `delete(id, currentUser)` |
| **ProductService** | `products/services/` | Validar ownership antes de modificar | `@Service`, `@Transactional` | `validateOwnership()` - Verifica dueño/ADMIN/MOD, `hasAnyRole()` |
| **ProductEntity** | `products/entities/` | Producto con relación al dueño | `@Entity`, `@ManyToOne`, `@JoinColumn` | `owner` - Usuario que creó el producto |

**Flujo de validación en validateOwnership()**:
1. ¿Es ADMIN? →  Pasa
2. ¿Es MODERATOR? →  Pasa
3. ¿Es dueño? →  Pasa
4. No cumple ninguno →  `throw AccessDeniedException`

---

## **Componentes Compartidos por las 3 Prácticas**

| Componente | Usado en | Propósito |
|------------|----------|-----------|
| **SecurityContext** | JWT, Roles, Ownership | Almacena Authentication del usuario actual |
| **Authentication** | JWT, Roles, Ownership | Objeto con usuario autenticado y sus roles |
| **UserDetailsImpl** | JWT, Roles, Ownership | Usuario con `id`, `email`, `authorities` |
| **PasswordEncoder** | JWT | Encriptar contraseñas con BCrypt |
| **@Transactional** | Ownership | Transacciones BD con rollback automático |

---

## **Orden de Ejecución de Validaciones**

| Paso | Validación | Clase/Componente | Excepción si falla | HTTP |
|------|------------|------------------|-------------------|------|
| 1 | ¿Token válido? | JwtAuthenticationFilter | `AuthenticationException` | 401 |
| 2 | ¿Rol correcto? | @PreAuthorize en Controlador | `AuthorizationDeniedException` | 403 |
| 3 | ¿Es dueño? | validateOwnership en Servicio | `AccessDeniedException` | 403 |
| 4 | Ejecutar operación | Servicio | - | 200/204 |

---

## **Configuración Requerida**

| Archivo | Configuración | Propósito |
|---------|---------------|-----------|
| **application.yml** | `jwt.secret`, `jwt.expiration` | Secreto y tiempo de expiración del token |
| **pom.xml** | `io.jsonwebtoken:jjwt-api` | Librería para trabajar con JWT |
| **Base de Datos** | Tablas: `users`, `roles`, `user_roles`, `products` | Almacenar usuarios, roles y productos con owner |
| **SecurityConfig** | `@EnableMethodSecurity(prePostEnabled = true)` | Habilitar @PreAuthorize |