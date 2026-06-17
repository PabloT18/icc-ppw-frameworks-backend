# Programación y Plataformas Web

# Frameworks Backend: Roles y Autorización Basada en Permisos

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="80">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="80">
</div>

## Práctica 12: Roles y Autorización – Control de Acceso Basado en Roles

### Autores

**Pablo Torres**

 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: PabloT18

---

# **Introducción**

En la práctica anterior aprendimos sobre autenticación (verificar quién es el usuario). Ahora vamos a profundizar en **autorización basada en roles**.

**Conceptos clave**:
- **Roles**: Grupos de permisos asignados a usuarios
- **RBAC**: Role-Based Access Control
- **Protección de endpoints**: Controlar acceso según roles
- **Expresiones de seguridad**: Verificar permisos dinámicamente

**Prerequisitos**:
- Haber completado la Práctica 11 (Autenticación y JWT)
- Entender conceptos de autenticación y tokens
- Conocer diferencia entre autenticación y autorización

---

# **1. Sistemas de Autorización**

## **1.1. Control Basado en Roles (RBAC)**

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
* Modelo más usado en aplicaciones web

**Desventajas**:
* Roles rígidos, no contextuales
* Explosión de roles en sistemas complejos
* Difícil manejar permisos temporales

**Ejemplo de jerarquía de roles**:

```
┌─────────────────────────────────────┐
│          SUPER_ADMIN                │  → Todos los permisos
│  (acceso total al sistema)          │
└───────────────┬─────────────────────┘
                │
    ┌───────────┴──────────┐
    │                      │
┌───▼──────────┐    ┌──────▼─────────┐
│    ADMIN     │    │   MODERATOR    │
│ (gestión)    │    │ (supervisión)  │
└───┬──────────┘    └──────┬─────────┘
    │                      │
    └──────────┬───────────┘
               │
        ┌──────▼──────┐
        │    USER     │  → Permisos básicos
        │  (estándar) │
        └─────────────┘
```

## **1.2. Control Basado en Atributos (ABAC)**

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
* Contexto dinámico (hora, ubicación, etc.)
* Reglas complejas posibles
* Mejor para sistemas enterprise

**Desventajas**:
* Complejo de implementar
* Difícil de debuggear
* Performance overhead
* Curva de aprendizaje alta

**Ejemplo de evaluación**:

```
Atributos del Usuario:
- role: "MANAGER"
- department: "SALES"
- location: "Ecuador"

Atributos del Recurso:
- owner_department: "SALES"
- classification: "PUBLIC"
- region: "LATAM"

Atributos del Contexto:
- time: "10:00 AM"
- day: "Monday"
- network: "internal"

Política:
IF user.role == "MANAGER" AND
   user.department == resource.owner_department AND
   resource.classification != "CONFIDENTIAL" AND
   context.time BETWEEN "8 AM" AND "6 PM"
THEN ALLOW
ELSE DENY
```

## **1.3. Listas de Control de Acceso (ACL)**

**Concepto**: Cada recurso tiene una **lista explícita** de quién puede hacer qué.

```
Documento ID=123:
- Pablo Torres: READ, WRITE, DELETE
- Ana García: READ
- Team Managers: READ, WRITE
```

**Ventajas**:
* Control granular por recurso
* Claro y explícito
* Fácil auditar permisos individuales

**Desventajas**:
* Difícil de mantener a escala
* No escalable con muchos recursos/usuarios
* Duplicación de permisos

**Ejemplo de implementación**:

```
┌──────────────────────────────────────────────┐
│  Resource: /projects/42                      │
├──────────────────────────────────────────────┤
│  User: pablo@example.com                     │
│  Permissions: [READ, WRITE, DELETE, ADMIN]   │
├──────────────────────────────────────────────┤
│  User: ana@example.com                       │
│  Permissions: [READ, WRITE]                  │
├──────────────────────────────────────────────┤
│  Group: developers                           │
│  Permissions: [READ, WRITE]                  │
├──────────────────────────────────────────────┤
│  Public: *                                   │
│  Permissions: [READ]                         │
└──────────────────────────────────────────────┘
```

---

# **2. Patrones de Implementación**

## **2.1. Middleware de Autorización**

**Concepto**: Componente que intercepta requests y verifica permisos antes de llegar al controlador.

```
Request → Auth Middleware → Authorization Middleware → Controlador
           ↓                    ↓
    ¿Token válido?         ¿Tiene permisos?
    SÍ: continuar         SÍ: continuar
    NO: 401               NO: 403
```

**Ejemplo conceptual**:

```javascript
// Pseudo-código de middleware de roles
function requireRole(allowedRoles) {
  return function(request, response, next) {
    const user = request.user; // Ya autenticado
    
    if (!user) {
      return response.status(401).json({ error: "No autenticado" });
    }
    
    const hasRole = user.roles.some(role => allowedRoles.includes(role));
    
    if (!hasRole) {
      return response.status(403).json({ 
        error: "No tienes permisos para esta acción" 
      });
    }
    
    next(); // Usuario autorizado, continuar
  }
}

// Uso:
app.delete('/api/users/:id', requireRole(['ADMIN']), deleteUser);
```

## **2.2. Guards/Decoradores de Autorización**

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

@RequiresAnyRole(["ADMIN", "MODERATOR"])
async banUser(id: string) {
  // Usuarios con ADMIN o MODERATOR pueden ejecutar
}
```

**Flujo de evaluación**:

```
Cliente → Request DELETE /api/users/5
          Authorization: Bearer <token>
            ↓
Framework intercepta método deleteUser()
            ↓
Evalúa @RequiresRole("ADMIN")
            ↓
Extrae usuario del token
            ↓
Verifica roles del usuario
            ↓
¿Tiene rol "ADMIN"?
  SÍ → Ejecuta método → 200 OK
  NO → Lanza excepción → 403 Forbidden
```

## **2.3. Interceptores de Autorización Contextual**

**Concepto**: Verifican permisos basándose en el contexto del request (parámetros, datos, estado).

```
PUT /users/123/profile

Interceptor verifica:
1. ¿El usuario autenticado es el ID 123? → Permitir
2. ¿El usuario tiene rol ADMIN? → Permitir  
3. Sino → 403 Forbidden
```

**Ejemplo de lógica contextual**:

```javascript
// Pseudo-código de interceptor de ownership
function checkOwnership(request, response, next) {
  const authenticatedUserId = request.user.id;
  const targetUserId = request.params.id;
  
  // Permitir si es el mismo usuario
  if (authenticatedUserId === targetUserId) {
    return next();
  }
  
  // Permitir si es ADMIN
  if (request.user.roles.includes('ADMIN')) {
    return next();
  }
  
  // Denegar en caso contrario
  return response.status(403).json({ 
    error: "Solo puedes modificar tu propio perfil" 
  });
}

// Uso:
app.put('/users/:id/profile', authenticate, checkOwnership, updateProfile);
```

---

# **3. Niveles de Protección de Endpoints**

## **3.1. Endpoints Públicos**

**Sin autenticación ni autorización**

```http
GET /api/products
→ 200 OK (cualquiera puede ver productos)

POST /auth/login
→ 200 OK (endpoint público de login)
```

**Casos de uso**:
- Listado de productos
- Páginas de información
- Endpoints de autenticación (login, register)

## **3.2. Endpoints Protegidos (Solo Autenticados)**

**Requieren token válido**

```http
GET /api/users/me
Authorization: Bearer <token>
→ 200 OK (usuario autenticado ve su perfil)

GET /api/users/me (sin token)
→ 401 Unauthorized
```

**Casos de uso**:
- Ver perfil propio
- Crear recursos propios
- Operaciones básicas de usuario logueado

## **3.3. Endpoints con Roles Específicos**

**Requieren rol particular**

```http
DELETE /api/users/5
Authorization: Bearer <token-admin>
→ 204 No Content (ADMIN puede eliminar)

DELETE /api/users/5
Authorization: Bearer <token-user>
→ 403 Forbidden (USER no puede eliminar)
```

**Casos de uso**:
- Operaciones administrativas
- Gestión de usuarios
- Reportes restringidos

## **3.4. Endpoints con Validación de Ownership**

**Requieren ser propietario del recurso o tener rol privilegiado**

```http
PUT /api/products/10
Authorization: Bearer <token-owner>
→ 200 OK (propietario puede actualizar)

PUT /api/products/10
Authorization: Bearer <token-otro-usuario>
→ 403 Forbidden (no eres propietario)

PUT /api/products/10
Authorization: Bearer <token-admin>
→ 200 OK (ADMIN puede actualizar cualquier producto)
```

**Casos de uso**:
- Modificar recursos propios
- Ver datos personales
- Gestionar contenido creado por el usuario

---

# **4. Expresiones de Autorización**

## **4.1. Verificaciones Comunes**

| Expresión | Significado | Uso |
|-----------|-------------|-----|
| `isAuthenticated()` | Usuario tiene token válido | Endpoints protegidos básicos |
| `hasRole('ADMIN')` | Usuario tiene rol específico | Operaciones administrativas |
| `hasAnyRole('USER', 'ADMIN')` | Usuario tiene al menos uno | Acceso compartido |
| `hasAuthority('DELETE_USER')` | Usuario tiene permiso específico | Permisos granulares |
| `permitAll()` | Cualquiera puede acceder | Endpoints públicos |
| `denyAll()` | Nadie puede acceder | Endpoints deshabilitados |

## **4.2. Expresiones Compuestas**

```
// Solo ADMIN o el mismo usuario
@PreAuthorize("hasRole('ADMIN') or #id == authentication.principal.id")
updateUser(Long id, UserDto dto)

// ADMIN o propietario del recurso
@PreAuthorize("hasRole('ADMIN') or @productService.isOwner(#id, authentication.principal.id)")
deleteProduct(Long id)

// Verificación compleja con múltiples condiciones
@PreAuthorize("isAuthenticated() and (hasRole('ADMIN') or (#user.department == authentication.principal.department and hasRole('MANAGER')))")
approveRequest(RequestDto request, User user)
```

---

# **5. Casos de Uso Reales**

## **5.1. E-commerce**

**Roles**:
```
- CUSTOMER: Ver productos, hacer pedidos, ver sus pedidos
- SELLER: Gestionar sus productos, ver ventas propias
- ADMIN: Gestionar todo el sistema, ver todos los pedidos
```

**Matriz de permisos**:

| Acción | CUSTOMER | SELLER | ADMIN |
|--------|----------|--------|-------|
| Ver productos | ✅ | ✅ | ✅ |
| Crear pedido | ✅ | ❌ | ✅ |
| Crear producto | ❌ | ✅ (solo suyos) | ✅ |
| Ver todos los pedidos | ❌ | ❌ | ✅ |
| Modificar producto ajeno | ❌ | ❌ | ✅ |
| Ver reportes | ❌ | ✅ (solo suyos) | ✅ |

## **5.2. Sistema Educativo**

**Roles**:
```
- STUDENT: Ver sus cursos, enviar tareas, ver calificaciones
- TEACHER: Gestionar sus cursos, calificar, comunicarse
- ADMIN: Gestionar usuarios, cursos, configuración
```

**Autorización contextual**:

```
Recurso: Calificaciones de curso "Matemáticas 101"

Reglas:
- Estudiante solo ve SUS calificaciones
- Profesor solo ve calificaciones de SUS cursos
- Admin ve todas las calificaciones
```

## **5.3. API Pública**

**Niveles de acceso**:
```
- FREE: 100 requests/hora, endpoints básicos
- BASIC: 1000 requests/hora, más endpoints
- PREMIUM: 10000 requests/hora, todos los endpoints
```

**Implementación**:

```
API Key → Identifica el plan
         ↓
Rate limiting basado en plan
         ↓
Feature gating (habilitar/deshabilitar endpoints)
         ↓
Permitir o denegar acceso
```

---

# **6. Mejores Prácticas**

## **6.1. Principio de Mínimo Privilegio**

**Regla**: Dar solo los permisos mínimos necesarios.

```
❌ MAL: Todos los usuarios registrados tienen rol ADMIN
✅ BIEN: Usuarios nuevos tienen rol USER, promoción manual a ADMIN
```

## **6.2. Roles Jerárquicos**

**Regla**: Roles superiores heredan permisos de roles inferiores.

```
ADMIN hereda permisos de USER
MODERATOR hereda permisos de USER
SUPER_ADMIN hereda permisos de ADMIN
```

## **6.3. Separación de Responsabilidades**

**Regla**: Validar autorización en capa de servicio, no solo en controlador.

```
❌ MAL:
Controller: Verifica rol ADMIN → OK
Service: Ejecuta operación (sin verificar)

✅ BIEN:
Controller: Verifica autenticación
Service: Verifica autorización + lógica de negocio
```

## **6.4. Auditoría de Permisos**

**Regla**: Registrar accesos denegados y cambios de roles.

```
Log ejemplo:
[2024-01-26 10:30:00] FORBIDDEN: user_id=123, action=DELETE_USER, reason=missing_role_ADMIN
[2024-01-26 10:31:00] ROLE_CHANGE: user_id=456, from=USER, to=ADMIN, by=admin_id=1
```

---


# **7. Próximos Pasos**

En la **Práctica 13: Ownership y Validación de Propiedad** aprenderemos:
- Validar que recursos pertenezcan al usuario
- Implementar lógica de ownership en servicios
- Combinar roles con validación de propiedad
- Manejar excepciones de autorización

📄 Ver [13_ownership_validacion.md](13_ownership_validacion.md)

---

# **Conclusión**

Has aprendido conceptos clave de autorización:

✅ **Sistemas de autorización**: RBAC, ABAC, ACL  
✅ **Patrones de implementación**: Middleware, guards, interceptores  
✅ **Niveles de protección**: Público, autenticado, con roles, con ownership  
✅ **Expresiones de seguridad**: hasRole(), isAuthenticated(), etc.  
✅ **Mejores prácticas**: Mínimo privilegio, separación de responsabilidades  

---

# **Aplicación en Frameworks**

Estos conceptos se implementan en los módulos específicos:

### Spring Boot

📄 [`spring-boot/p67/a_dodente/12_roles_preauthorize.md`](../spring-boot/p67/a_dodente/12_roles_preauthorize.md)

- @PreAuthorize y @Secured
- Role hierarchy configuration
- Method security expressions
- @AuthenticationPrincipal

### NestJS

📄 [`nest/p67/a_dodente/12_roles_authorization.md`](../nest/p67/a_dodente/12_roles_authorization.md)

- @Roles decorator
- RolesGuard implementation
- Custom decorators para permisos
- Reflector para metadata
  