# Programación y Plataformas Web

# Frameworks Backend: Autenticación y Autorización de Usuarios

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="80">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="80">
</div>

## Práctica 11: Autenticación y Autorización – Seguridad y Control de Acceso

### Autores

**Pablo Torres**

📧 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

💻 GitHub: PabloT18

## Introducción

En aplicaciones reales, **NO todos los usuarios pueden acceder a toda la información** ni realizar cualquier acción.

Los sistemas modernos requieren **identificar quién es el usuario** (autenticación) y **qué puede hacer** (autorización).

Sin estos mecanismos de seguridad:

* **Datos sensibles expuestos**
* **Acciones no autorizadas**
* **Vulnerabilidades de seguridad**
* **Pérdida de confianza del usuario**
* **Problemas legales y regulatorios**

Ejemplos reales que requieren autenticación/autorización:

* Un sistema bancario donde solo el titular ve su cuenta
* Una plataforma educativa donde estudiantes no pueden cambiar notas
* Un e-commerce donde solo administradores gestionan productos
* Una red social donde cada usuario controla su perfil
* Un sistema médico donde solo doctores autorizados ven historiales

Este documento introduce los **conceptos de autenticación y autorización**, desde un enfoque **teórico y universal**, sin depender de sintaxis específica de ningún framework.

Las implementaciones concretas se desarrollarán posteriormente en los materiales propios de cada framework.

## 1. Conceptos fundamentales

### 1.1 Autenticación (Authentication)

La **autenticación** es el proceso de **verificar la identidad** de un usuario.

Responde a la pregunta: **"¿Quién eres?"**

* Confirma que el usuario es quien dice ser
* Generalmente mediante credenciales (usuario/contraseña)
* Puede usar factores múltiples (2FA, biometría)
* Resultado: usuario identificado o acceso denegado

### 1.2 Autorización (Authorization)

La **autorización** es el proceso de **verificar permisos** de un usuario autenticado.

Responde a la pregunta: **"¿Qué puedes hacer?"**

* Determina qué recursos puede acceder
* Define qué acciones puede ejecutar
* Se basa en roles, permisos o políticas
* Resultado: acceso permitido o denegado a recursos específicos

### 1.3 Diferencia clave

```
Autenticación: ¿Eres Pablo Torres?     → SÍ (credenciales válidas)
Autorización:  ¿Puedes borrar usuarios? → NO (no tienes rol admin)
```

**Analogía física**:
* **Autenticación** = Mostrar cédula en un edificio
* **Autorización** = Verificar si tu pase permite acceder al piso 10

## 2. Flujo básico de seguridad

### 2.1 Proceso completo

1. **Usuario proporciona credenciales** (login)
2. **Sistema verifica identidad** (autenticación)
3. **Sistema genera token de sesión** (si es válido)
4. **Usuario incluye token en requests** (cada petición)
5. **Sistema verifica token y permisos** (autorización)
6. **Sistema permite o deniega acción**

### 2.2 Ejemplo conceptual

```
POST /auth/login
{ "email": "pablo@example.com", "password": "secret123" }

Respuesta:
{
  "token": "eyJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "name": "Pablo Torres",
    "roles": ["USER"]
  }
}

GET /api/products (con token en header)
→ Permitido: usuario autenticado

DELETE /api/users/5 (con token en header)  
→ Denegado: requiere rol ADMIN
```

## 3. Métodos de autenticación

### 3.1 Autenticación básica (Basic Auth)

**Concepto**: Usuario/contraseña en cada request (codificado en Base64).

**Ventajas**:
* Simple de implementar
* Estándar HTTP nativo

**Desventajas**:
* Credenciales viajan en cada request
* Vulnerable si no usa HTTPS
* No hay control de sesión

**Uso**: APIs internas, servicios simples

### 3.2 Autenticación por sesión (Session-based)

**Concepto**: Servidor mantiene estado de sesión, cliente usa cookie/ID de sesión.

**Flujo**:
1. Login exitoso → servidor crea sesión
2. Servidor envía ID de sesión (cookie)
3. Cliente incluye cookie en requests
4. Servidor valida sesión en cada request

**Ventajas**:
* Control total del servidor
* Fácil invalidación de sesiones
* Datos de sesión en servidor

**Desventajas**:
* Servidor debe mantener estado
* Problemas con escalado horizontal
* Dependiente de cookies

### 3.3 Autenticación por token (Token-based)

**Concepto**: Cliente recibe token tras login, lo incluye en headers de requests posteriores.

**Flujo**:
1. Login exitoso → servidor genera token
2. Cliente almacena token
3. Cliente incluye token en header Authorization
4. Servidor valida token en cada request

**Ventajas**:
* Servidor sin estado (stateless)
* Escalable horizontalmente
* Compatible con móviles/SPAs
* Cross-domain friendly

**Desventajas**:
* Token puede ser interceptado
* Dificultad para invalidar tokens
* Tamaño del token

## 4. JSON Web Tokens (JWT)

### 4.1 ¿Qué es JWT?

**JWT** es un estándar abierto (RFC 7519) para crear **tokens de acceso** de forma segura.

Permite transmitir información entre partes como un objeto JSON **firmado digitalmente**.

### 4.2 Estructura de JWT

Un JWT consta de **tres partes** separadas por puntos:

```
header.payload.signature
```

**Ejemplo**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

#### Header (Cabecera)
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```
* **alg**: Algoritmo de firma (HS256, RS256, etc.)
* **typ**: Tipo de token (JWT)

#### Payload (Carga útil)
```json
{
  "sub": "1234567890",
  "name": "Pablo Torres",
  "email": "pablo@example.com",
  "roles": ["USER"],
  "iat": 1516239022,
  "exp": 1516325422
}
```
* **sub**: Subject (ID del usuario)
* **iat**: Issued at (cuándo se emitió)
* **exp**: Expiration (cuándo expira)
* **Custom claims**: roles, permisos, etc.

#### Signature (Firma)
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

### 4.3 Ventajas de JWT

* **Self-contained**: Toda la información necesaria está en el token
* **Stateless**: No requiere almacenamiento en servidor
* **Portable**: Funciona entre diferentes dominios/servicios
* **JSON-based**: Fácil de procesar
* **Compact**: URL-safe, ideal para headers HTTP

### 4.4 Desventajas de JWT

* **Tamaño**: Más grande que IDs de sesión simples
* **Invalidación**: Difícil de revocar antes de expiración
* **Seguridad**: Si se compromete el secret, todos los tokens son vulnerables
* **Información sensible**: El payload es visible (solo codificado, no encriptado)

### 4.5 Claims estándar de JWT

| Claim | Descripción | Ejemplo |
|-------|-------------|---------|
| **iss** | Issuer (quién emitió el token) | "auth-service" |
| **sub** | Subject (ID del usuario) | "123" |
| **aud** | Audience (para quién es el token) | "api-service" |
| **exp** | Expiration (cuándo expira) | 1516325422 |
| **iat** | Issued at (cuándo se emitió) | 1516239022 |
| **nbf** | Not before (válido desde) | 1516239022 |
| **jti** | JWT ID (identificador único) | "abc123" |

## 5. Patrones de Implementación de Autenticación

### 5.1 Middleware de autenticación

**Concepto**: Componente que intercepta requests y verifica autenticación antes de llegar al controlador.

```
Request → Middleware Auth → Controlador → Response
           ↓
    Token válido? → SÍ: continuar
                  → NO: 401 Unauthorized
```

**Flujo detallado**:
```
1. Cliente envía request con header Authorization
2. Middleware extrae token del header
3. Valida token (firma, expiración)
4. Si válido: establece usuario en contexto
5. Si inválido: retorna 401 Unauthorized
6. Controlador recibe usuario autenticado
```

### 5.2 Filtros de autenticación

**Concepto**: Interceptan todas las peticiones HTTP para validar tokens antes de que lleguen a los controladores.

```
Todas las requests → Filtro JWT → Valida token → Establece SecurityContext
                                      ↓
                              Token inválido → 401
```

## 6. Tokens de seguridad

### 6.1 Access tokens

**Propósito**: Autenticar requests a APIs.

**Características**:
* Vida corta (15-60 minutos)
* Contienen información del usuario/permisos
* Se incluyen en header Authorization

### 6.2 Refresh tokens

**Propósito**: Obtener nuevos access tokens sin re-login.

**Características**:
* Vida larga (días/semanas)
* Solo para endpoint de refresh
* Almacenados de forma segura

**Flujo**:
```
1. Login → access_token (30min) + refresh_token (7 días)
2. Usar access_token para APIs
3. Access_token expira → usar refresh_token
4. Refresh → nuevo access_token + nuevo refresh_token
```

### 6.3 API keys

**Propósito**: Autenticar aplicaciones/servicios (no usuarios específicos).

**Características**:
* Vida larga o indefinida
* Identifican la aplicación cliente
* Menos granularidad que tokens de usuario

## 7. Mejores prácticas de seguridad

### 7.1 Manejo de contraseñas

* **Hash con salt**: Nunca almacenar contraseñas en texto plano
* **Algoritmos seguros**: bcrypt, Argon2, PBKDF2
* **Políticas de contraseñas**: Longitud mínima, complejidad
* **Protección contra brute force**: Límites de intentos, CAPTCHA

### 7.2 Gestión de tokens

* **Expiración corta**: Access tokens de 15-60 minutos
* **Almacenamiento seguro**: HttpOnly cookies, secure storage
* **Invalidación**: Blacklist, token versioning
* **Rotación**: Refresh tokens deben rotar

### 7.3 Comunicación segura

* **HTTPS obligatorio**: Todas las comunicaciones cifradas
* **Headers de seguridad**: CORS, CSP, X-Frame-Options
* **Validación de entrada**: Sanitizar datos de usuario
* **Logs de seguridad**: Auditar intentos de acceso

## 8. Errores comunes de seguridad

### 8.1 Problemas de autenticación

* **Credenciales por defecto**: admin/admin, root/root
* **Contraseñas débiles**: Permitir "123456", "password"
* **Transmisión insegura**: Credenciales por HTTP
* **Sesiones sin expirar**: Tokens que nunca caducan

### 8.2 Problemas con tokens

* **Secrets débiles**: Claves fáciles de adivinar
* **Información sensible**: Passwords en payload
* **Sin validación**: Aceptar cualquier token sin verificar
* **Exposición**: Tokens en URLs, logs
* **Token replay**: Reutilizar tokens interceptados

## 10. Consideraciones de performance

### 10.1 Caching de autenticación

* **Cache de tokens**: Evitar validar en BD cada request
* **Cache de permisos**: Almacenar roles/permisos temporalmente
* *9ession storage**: Redis, Memcached para sesiones

### 9.2 Optimizaciones

* **JWT stateless**: Evitar lookups de base de datos
* **Lazy loading**: Cargar permisos solo cuando se necesiten
* **Batch operations**: Verificar múltiples permisos juntos

## 19 Casos de uso reales

### 11.1 E-commerce

```
Roles:
- CU0. Testing de Autenticación

### 10.1 Tests de login

* **Credenciales válidas**: Login exitoso con token
* **Credenciales inválidas**: Login fallido con 401
* **Tokens expirados**: Acceso denegado con 401
* **Tokens malformados**: Error apropiado con 401

### 10.2 Tests de seguridad

* **Injection attacks**: Intentos de inyección en credenciales
* **Brute force**: Múltiples intentos de login
* **Token replay**: Reutilización de tokens interceptados
* **HTTPS enforcement**: Verificar comunicación segura

---

# **Próximos Pasos**

Has completado la Práctica 11 sobre **Autenticación con JWT**. Has aprendido:

- Conceptos de autenticación y autorización
- Métodos de autenticación (Basic, Session, Token)
- Estructura y funcionamiento de JWT
- Mejores prácticas de seguridad
- Testing de autenticación

**Continúa con las siguientes prácticas**:

## **Práctica 12: Roles y Autorización**

Aprenderás sobre:
- Control basado en roles (RBAC)
- Control basado en atributos (ABAC)
- Patrones de autorización
- Protección de endpoints por roles
- Expresiones de seguridad

📄 Ver [12_roles_autorizacion.md](12_roles_autorizacion.md)

## **Práctica 13: Ownership y Validación de Propiedad**

Aprenderás sobre:
- Validación de ownership (propiedad)
- Autorización contextual
- ADMIN bypass
- Validación en capa de servicio
- Casos de uso avanzados

📄 Ver [13_ownership_validacion.md](13_ownership_validacion.md)

---

## 11. Resultados esperados

Al finalizar este tema, el estudiante comprende:

* **Diferencia entre autenticación y autorización**
* **Métodos de autenticación**: Basic, session, token-based
* **Estructura y uso de JWT**: Header, payload, signature
* **Flujos de login y registro**
* **Mejores prácticas de seguridad**
* **Errores comunes y cómo evitarlos**
* **Testing de autenticación**

---

## 12. Aplicación directa en framework./spring-boot/p67/a_dodente/11_autenticacion_autorizacion.md)

* Spring Security configuración
* JWT con Spring Boot
* @PreAuthorize y @Secured
* UserDetailsService implementation
* Password encoding con BCrypt
* Security filters y authentication providers

### NestJS

[`nest/11_autenticacion_autorizacion.md`](../nest/p67/a_dodente/11_autenticacion_autorizacion.md)

* Guards de autenticación
* JWT strategy con Passport
* Role-based access control
* Custom decorators para permisos
* Bcrypt para hashing passwords
* JWT module configurationimplementan en las prácticas específicas de cada framework:

### Spring Boot

📄 **Práctica 11**: [`spring-boot/p67/a_dodente/11_autenticacion_autorizacion.md`](../spring-boot/p67/a_dodente/11_autenticacion_autorizacion.md)

* Spring Security configuración
* JWT con jjwt library
* UserDetailsService implementation
* Password encoding con BCrypt
* JwtAuthenticationFilter
* SecurityConfig completo

📄 **Práctica 12**: [`spring-boot/p67/a_dodente/12_roles_preauthorize.md`](../spring-boot/p67/a_dodente/12_roles_preauthorize.md)

* @PreAuthorize annotations
* Role-based endpoint protection
* @AuthenticationPrincipal
* Method security expressions

📄 **Práctica 13**: [`spring-boot/p67/a_dodente/13_ownership_validacion.md`](../spring-boot/p67/a_dodente/13_ownership_validacion.md)

* validateOwnership() method
* AccessDeniedException handling
* Service layer authorization
* ADMIN bypass patterns

### NestJS

📄 **Práctica 11**: [`nest/p67/a_dodente/11_autenticacion_jwt.md`](../nest/p67/a_dodente/11_autenticacion_jwt.md)

* JWT strategy con Passport
* JwtAuthGuard implementation
* Bcrypt para hashing passwords
* JWT module configuration

📄 **Práctica 12**: [`nest/p67/a_dodente/12_roles_authorization.md`](../nest/p67/a_dodente/12_roles_authorization.md)

* @Roles decorator
* RolesGuard implementation
* Custom decorators
* Reflector metadata

📄 **Práctica 13**: [`nest/p67/a_dodente/13_ownership_validation.md`](../nest/p67/a_dodente/13_ownership_validation.md)

* Custom ownership guards
* @UserFromToken decorator
* Resource ownership patterns
* Exception handling