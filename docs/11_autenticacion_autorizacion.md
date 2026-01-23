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

## 5. Sistemas de autorización

### 5.1 Control basado en roles (RBAC)

**Concepto**: Los usuarios tienen **roles**, los roles tienen **permisos**.

```
Usuario Pablo → Rol "ADMIN"
Rol "ADMIN" → Permisos: ["CREATE_USER", "DELETE_USER", "VIEW_REPORTS"]

Usuario Ana → Rol "USER" 
Rol "USER" → Permisos: ["VIEW_PRODUCTS", "CREATE_ORDER"]
```

**Ventajas**:
* Simple de entender e implementar
* Fácil gestión de permisos por grupos
* Escalable para organizaciones

**Desventajas**:
* Roles rígidos, no contextuales
* Explosión de roles en sistemas complejos

### 5.2 Control basado en atributos (ABAC)

**Concepto**: Los permisos se evalúan basándose en **atributos** del usuario, recurso y contexto.

```
Regla: Un usuario puede ver un documento SI:
- Es el propietario del documento, O
- Es manager del departamento del propietario, Y
- El documento no está marcado como confidencial, Y
- La hora actual está entre 8 AM y 6 PM
```

**Ventajas**:
* Muy flexible y granular
* Contexto dinámico
* Reglas complejas

**Desventajas**:
* Complejo de implementar
* Difícil de debuggear
* Performance overhead

### 5.3 Listas de control de acceso (ACL)

**Concepto**: Cada recurso tiene una **lista explícita** de quién puede hacer qué.

```
Documento ID=123:
- Pablo Torres: READ, WRITE, DELETE
- Ana García: READ
- Managers: READ
```

**Ventajas**:
* Control granular por recurso
* Claro y explícito

**Desventajas**:
* Difícil de mantener
* No escalable con muchos recursos/usuarios

## 6. Patrones de implementación

### 6.1 Middleware de autenticación

**Concepto**: Componente que intercepta requests y verifica autenticación antes de llegar al controlador.

```
Request → Middleware Auth → Controlador → Response
           ↓
    Token válido? → SÍ: continuar
                  → NO: 401 Unauthorized
```

### 6.2 Guards/Decoradores de autorización

**Concepto**: Protegen endpoints específicos con requerimientos de permisos.

```
@RequiresRole("ADMIN")
async deleteUser(id: string) {
  // Solo usuarios con rol ADMIN pueden ejecutar esto
}

@RequiresPermission("PRODUCTS:DELETE")
async deleteProduct(id: string) {
  // Solo usuarios con este permiso específico
}
```

### 6.3 Interceptores de autorización

**Concepto**: Verifican permisos basándose en el contexto del request (parámetros, datos).

```
PUT /users/123/profile

Interceptor verifica:
- ¿El usuario autenticado es el ID 123? → Permitir
- ¿El usuario tiene rol ADMIN? → Permitir  
- Sino → 403 Forbidden
```

## 7. Tokens de seguridad

### 7.1 Access tokens

**Propósito**: Autenticar requests a APIs.

**Características**:
* Vida corta (15-60 minutos)
* Contienen información del usuario/permisos
* Se incluyen en header Authorization

### 7.2 Refresh tokens

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

### 7.3 API keys

**Propósito**: Autenticar aplicaciones/servicios (no usuarios específicos).

**Características**:
* Vida larga o indefinida
* Identifican la aplicación cliente
* Menos granularidad que tokens de usuario

## 8. Mejores prácticas de seguridad

### 8.1 Manejo de contraseñas

* **Hash con salt**: Nunca almacenar contraseñas en texto plano
* **Algoritmos seguros**: bcrypt, Argon2, PBKDF2
* **Políticas de contraseñas**: Longitud mínima, complejidad
* **Protección contra brute force**: Límites de intentos, CAPTCHA

### 8.2 Gestión de tokens

* **Expiración corta**: Access tokens de 15-60 minutos
* **Almacenamiento seguro**: HttpOnly cookies, secure storage
* **Invalidación**: Blacklist, token versioning
* **Rotación**: Refresh tokens deben rotar

### 8.3 Comunicación segura

* **HTTPS obligatorio**: Todas las comunicaciones cifradas
* **Headers de seguridad**: CORS, CSP, X-Frame-Options
* **Validación de entrada**: Sanitizar datos de usuario
* **Logs de seguridad**: Auditar intentos de acceso

## 9. Errores comunes de seguridad

### 9.1 Problemas de autenticación

* **Credenciales por defecto**: admin/admin, root/root
* **Contraseñas débiles**: Permitir "123456", "password"
* **Transmisión insegura**: Credenciales por HTTP
* **Sesiones sin expirar**: Tokens que nunca caducan

### 9.2 Problemas de autorización

* **Falta de verificación**: Confiar solo en frontend
* **Escalación de privilegios**: Usuario normal accede a funciones admin
* **Referencias directas**: /users/123 sin verificar ownership
* **Mass assignment**: Permitir modificar campos no autorizados

### 9.3 Problemas con tokens

* **Secrets débiles**: Claves fáciles de adivinar
* **Información sensible**: Passwords en payload
* **Sin validación**: Aceptar cualquier token sin verificar
* **Exposición**: Tokens en URLs, logs

## 10. Consideraciones de performance

### 10.1 Caching de autenticación

* **Cache de tokens**: Evitar validar en BD cada request
* **Cache de permisos**: Almacenar roles/permisos temporalmente
* **Session storage**: Redis, Memcached para sesiones

### 10.2 Optimizaciones

* **JWT stateless**: Evitar lookups de base de datos
* **Lazy loading**: Cargar permisos solo cuando se necesiten
* **Batch operations**: Verificar múltiples permisos juntos

## 11. Casos de uso reales

### 11.1 E-commerce

```
Roles:
- CUSTOMER: Ver productos, hacer pedidos
- SELLER: Gestionar sus productos
- ADMIN: Gestionar todo el sistema

Flujo:
- Login → JWT con roles
- Ver producto → Público (sin auth)
- Comprar → Requiere CUSTOMER
- Subir producto → Requiere SELLER
- Ver reportes → Requiere ADMIN
```

### 11.2 Sistema educativo

```
Roles:
- STUDENT: Ver sus cursos, enviar tareas
- TEACHER: Gestionar sus cursos, calificar
- ADMIN: Gestionar usuarios y cursos

Autorización contextual:
- Estudiante solo ve SUS cursos
- Profesor solo gestiona SUS cursos
- Admin ve todo
```

### 11.3 API pública

```
Niveles de acceso:
- PUBLIC: Endpoints básicos, límite bajo
- BASIC: Más endpoints, límite medio  
- PREMIUM: Todos los endpoints, límite alto

Implementación:
- API Key identifica el plan
- Rate limiting basado en plan
- Features gating por nivel
```

## 12. Testing de seguridad

### 12.1 Tests de autenticación

* **Credenciales válidas**: Login exitoso
* **Credenciales inválidas**: Login fallido
* **Tokens expirados**: Acceso denegado
* **Tokens malformados**: Error apropiado

### 12.2 Tests de autorización

* **Acceso permitido**: Usuario con permisos correctos
* **Acceso denegado**: Usuario sin permisos
* **Escalación**: Intentar acceder a recursos superiores
* **Ownership**: Solo propietario puede modificar

### 12.3 Tests de seguridad

* **Injection attacks**: SQL, NoSQL injection
* **XSS attacks**: Cross-site scripting
* **CSRF attacks**: Cross-site request forgery
* **Brute force**: Múltiples intentos de login

## 13. Monitoreo y auditoría

### 13.1 Logs de seguridad

* **Intentos de login**: Exitosos y fallidos
* **Accesos denegados**: 401, 403 responses
* **Escalación de privilegios**: Intentos sospechosos
* **Operaciones críticas**: Cambios de permisos, eliminaciones

### 13.2 Métricas importantes

* **Tasa de login exitoso/fallido**
* **Tokens activos/expirados**
* **Endpoints más atacados**
* **Usuarios con más errores de autorización**

### 13.3 Alertas de seguridad

* **Múltiples logins fallidos**
* **Acceso desde IPs sospechosas**
* **Patrones de ataque conocidos**
* **Tokens con comportamiento anómalo**

## 14. Evolución y tendencias

### 14.1 OAuth 2.0 y OpenID Connect

* **Delegación de autenticación**: Login con Google, Facebook
* **Single Sign-On (SSO)**: Una autenticación para múltiples aplicaciones
* **Federación de identidades**: Conectar sistemas organizacionales

### 14.2 Zero Trust Architecture

* **"Never trust, always verify"**
* **Verificación continua**: No solo al login
* **Contexto dinámico**: Ubicación, dispositivo, comportamiento
* **Micro-segmentación**: Permisos muy granulares

### 14.3 Biometría y MFA

* **Multi-factor authentication**: Algo que sabes + algo que tienes
* **Biometría**: Huella, reconocimiento facial
* **Hardware tokens**: YubiKey, RSA SecurID
* **TOTP**: Time-based One-Time Passwords (Google Authenticator)

## 15. Resultados esperados

Al finalizar este tema, el estudiante comprende:

* **Diferencia entre autenticación y autorización**
* **Métodos de autenticación**: Basic, session, token-based
* **Estructura y uso de JWT**: Header, payload, signature
* **Sistemas de autorización**: RBAC, ABAC, ACL
* **Patrones de implementación**: Middleware, guards, interceptores
* **Mejores prácticas de seguridad**
* **Errores comunes y cómo evitarlos**
* **Testing y monitoreo de seguridad**

## 16. Aplicación directa en los siguientes módulos

Estos conceptos se aplicarán directamente en los módulos específicos de cada framework.

### Spring Boot

[`spring-boot/11_autenticacion_autorizacion.md`](../spring-boot/p67/a_dodente/11_autenticacion_autorizacion.md)

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
* JWT module configuration