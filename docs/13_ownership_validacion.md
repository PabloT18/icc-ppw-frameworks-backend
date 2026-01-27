# Programación y Plataformas Web

# Frameworks Backend: Ownership y Validación de Propiedad

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="80">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="80">
</div>

## Práctica 13: Ownership – Validación de Propiedad de Recursos

### Autores

**Pablo Torres**

📧 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

💻 GitHub: PabloT18

---

# **Introducción**

En la práctica anterior aprendimos sobre autorización basada en roles. Ahora vamos a implementar **validación de ownership** (propiedad), un concepto crucial para seguridad granular.

**Conceptos clave**:
- **Ownership**: Verificar que un recurso pertenezca al usuario
- **Validación contextual**: Autorización basada en datos del recurso
- **ADMIN bypass**: Permitir acceso administrativo sin restricciones
- **Separación de responsabilidades**: Validar en capa de servicio

**Prerequisitos**:
- Haber completado las Prácticas 11 (Autenticación) y 12 (Roles)
- Entender conceptos de RBAC
- Conocer patrones de autorización

---

# **1. ¿Qué es Ownership?**

## **1.1. Definición**

**Ownership** es el concepto de que un usuario es el **propietario** de un recurso y solo él (o un administrador) puede modificarlo o eliminarlo.

**Ejemplo**:
```
Usuario Pablo crea Producto ID=10
→ Pablo es el "owner" del Producto 10
→ Solo Pablo puede modificar el Producto 10
→ ADMIN también puede modificarlo (bypass)
→ Otro usuario NO puede modificarlo
```

## **1.2. Diferencia con Roles**

| Concepto | Roles (RBAC) | Ownership |
|----------|--------------|-----------|
| **Basado en** | Rol del usuario | Relación usuario-recurso |
| **Alcance** | Global (aplica a toda la aplicación) | Específico (aplica a recursos individuales) |
| **Ejemplo** | USER puede crear productos | USER puede modificar SUS productos |
| **Validación** | Verificar rol en token | Verificar owner_id en base de datos |

**Combinación de ambos**:
```
Usuario con rol USER:
- Puede crear productos (RBAC)
- Puede modificar SUS productos (Ownership)
-  NO puede modificar productos de otros (Ownership)

Usuario con rol ADMIN:
- Puede crear productos (RBAC)
- Puede modificar CUALQUIER producto (ADMIN bypass)
```

---

# **2. Extracción del Usuario Autenticado**

## **2.1. ¿De Dónde Viene el Usuario?**

Para validar ownership, necesitamos saber **quién es el usuario autenticado**. Este usuario viene del **token JWT** validado en el proceso de autenticación.

**Flujo de extracción**:
```
Request con JWT → Middleware de Autenticación
                 ↓
          Valida token y extrae payload
                 ↓
          Usuario autenticado en contexto
                 ↓
          Disponible para controlador/servicio
```

## **2.2. Patrón: Inyección en Controlador**

**Concepto**: El framework inyecta automáticamente el usuario autenticado en el método del controlador.

**Ejemplo conceptual**:
```javascript
// Pseudo-código
async function updateProduct(request, response) {
  const productId = request.params.id;
  const currentUser = request.user;  // ← Usuario del JWT
  
  // Pasar usuario al servicio para validación
  const updated = await ProductService.update(productId, request.body, currentUser);
  return response.json(updated);
}
```

**Ventajas**:
- **Explícito**: Se ve claramente qué métodos necesitan el usuario
- **Testeable**: Fácil pasar usuario mock en tests
- **Desacoplado**: No depende de estado global

## **2.3. Patrón Alternativo: Contexto Global**

**Concepto**: El usuario autenticado se guarda en un contexto global accesible desde cualquier parte.

**Ejemplo conceptual**:
```javascript
// Servicio
class ProductService {
  async update(productId, data) {
    const product = await ProductRepo.findById(productId);
    
    // Obtener usuario del contexto global
    const currentUser = SecurityContext.getCurrentUser();
    
    this.validateOwnership(product, currentUser);
    // ... actualizar
  }
}
```

**Desventajas**:
- Depende de estado global (menos testeable)
- No es obvio qué métodos usan el contexto
- Más acoplado al framework de seguridad

## **2.4. Recomendación: Pasar Usuario Como Parámetro**

**Mejor práctica**: Extraer usuario en el controlador y pasarlo al servicio.

```javascript
// CONTROLADOR
async function updateProduct(request, response) {
  const productId = request.params.id;
  const currentUser = request.user;  // ← Extraer del contexto del request
  
  // Pasar explícitamente al servicio
  const updated = await ProductService.update(productId, request.body, currentUser);
  return response.json(updated);
}

// SERVICIO
class ProductService {
  async update(productId, data, currentUser) {  // ← Recibir como parámetro
    const product = await ProductRepo.findById(productId);
    this.validateOwnership(product, currentUser);
    // ... actualizar
  }
  
  validateOwnership(product, user) {
    if (user.roles.includes('ADMIN')) return;
    if (product.ownerId !== user.id) {
      throw new ForbiddenException();
    }
  }
}
```

**Ventajas de este enfoque**:
- **Claridad**: La firma del método muestra qué necesita
- **Testing**: Fácil pasar diferentes usuarios en tests
- **Reutilización**: El servicio no asume de dónde viene el usuario
- **Principio de dependencia**: El servicio recibe lo que necesita

---

# **3. Patrones de Validación de Ownership**

## **3.1. Validación en Controlador (Menos Recomendado)**

```javascript
// Pseudo-código
async function updateProduct(request, response) {
  const productId = request.params.id;
  const userId = request.user.id; // Usuario autenticado
  
  // Cargar producto
  const product = await ProductRepository.findById(productId);
  
  //  Validación en controlador
  if (product.ownerId !== userId && !request.user.roles.includes('ADMIN')) {
    return response.status(403).json({ error: "No eres propietario" });
  }
  
  // Actualizar producto
  await ProductService.update(productId, request.body);
  return response.json({ message: "Actualizado" });
}
```

**Problemas**:
- Controlador tiene lógica de negocio (viola SRP)
- No reutilizable si otro servicio llama a update()
- Difícil de testear unitariamente
- Query duplicada a BD (una para validar, otra para actualizar)

## **3.2. Validación en Servicio (Recomendado)**

```javascript
// Pseudo-código
// CONTROLADOR (solo maneja HTTP)
async function updateProduct(request, response) {
  const productId = request.params.id;
  const user = request.user; // Usuario autenticado
  
  // Delegar validación al servicio
  const updatedProduct = await ProductService.update(productId, request.body, user);
  return response.json(updatedProduct);
}

// SERVICIO (lógica de negocio + validación)
class ProductService {
  async update(productId, data, currentUser) {
    // 1. Cargar producto
    const product = await ProductRepository.findById(productId);
    if (!product) throw new NotFoundException();
    
    // 2. Validar ownership
    this.validateOwnership(product, currentUser);
    
    // 3. Actualizar
    product.name = data.name;
    return await ProductRepository.save(product);
  }
  
  validateOwnership(product, user) {
    // Permitir si es ADMIN
    if (user.roles.includes('ADMIN')) {
      return; // ADMIN bypass
    }
    
    // Verificar ownership
    if (product.ownerId !== user.id) {
      throw new ForbiddenException("No eres propietario de este recurso");
    }
  }
}
```

**Ventajas**:
- **Una sola query** a BD (cargar y validar)
- **Lógica centralizada** en servicio
- **Reutilizable** por otros servicios
- **Testeable** unitariamente
- **Mensajes personalizados**

## **3.3. Validación con Interceptores (Alternativa)**

```javascript
// Pseudo-código de interceptor
function checkProductOwnership(request, response, next) {
  const productId = request.params.id;
  const userId = request.user.id;
  
  const product = await ProductRepository.findById(productId);
  
  if (!product) {
    return response.status(404).json({ error: "No encontrado" });
  }
  
  // Permitir si es ADMIN
  if (request.user.roles.includes('ADMIN')) {
    request.product = product; // Inyectar para no repetir query
    return next();
  }
  
  // Verificar ownership
  if (product.ownerId !== userId) {
    return response.status(403).json({ error: "No autorizado" });
  }
  
  request.product = product; // Inyectar producto
  next();
}

// Uso:
app.put('/products/:id', authenticate, checkProductOwnership, updateProduct);
```

**Ventajas**:
- Reutilizable en múltiples endpoints
- Separa validación de lógica de negocio

**Desventajas**:
- Query adicional si servicio también carga el producto
- Menos flexible para lógica compleja

---

# **4. Niveles de Validación de Seguridad**

## **4.1. Tabla Comparativa de Validaciones**

Una API moderna tiene **tres niveles de validación de seguridad** que se ejecutan en secuencia:

| Nivel | ¿Qué valida? | ¿Dónde se valida? | Excepción si falla | Código HTTP | Cuándo se ejecuta |
|-------|--------------|-------------------|-------------------|-------------|-------------------|
| **1. Autenticación** | ¿Tiene token válido? | Middleware de autenticación | AuthenticationException | 401 Unauthorized | Primera barrera |
| **2. Autorización por Rol** | ¿Tiene el rol necesario? | Guards/Anotaciones | AuthorizationException | 403 Forbidden | Segunda barrera |
| **3. Ownership** | ¿Es dueño del recurso? | Servicio (validateOwnership) | AccessDeniedException | 403 Forbidden | Tercera barrera |

## **4.2. Flujo Completo de Validación**

```
Request: PUT /api/products/10
Authorization: Bearer <token-user-B>
        ↓
┌─────────────────────────────────────────┐
│ NIVEL 1: AUTENTICACIÓN                  │
│ - Extraer token del header              │
│ - Validar firma y expiración            │
│ - Cargar usuario del payload            │
│ Token válido → Continuar              │
│  Token inválido → 401 Unauthorized     │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ NIVEL 2: AUTORIZACIÓN POR ROL           │
│ - Verificar roles requeridos            │
│ - Evaluar expresiones de seguridad      │
│ Tiene rol necesario → Continuar       │
│  Sin rol → 403 Forbidden               │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ NIVEL 3: OWNERSHIP                      │
│ - Cargar recurso de BD                  │
│ - Verificar ownerId vs userId           │
│ - Verificar si es ADMIN (bypass)        │
│ Es propietario o ADMIN → Continuar    │
│  No es propietario → 403 Forbidden     │
└─────────────────────────────────────────┘
        ↓
   200 OK - Recurso actualizado
```

## **4.3. Ejemplos por Nivel**

### **Nivel 1: Autenticación - 401 Unauthorized**

```http
# Sin token
PUT /api/products/10
→ 401 Unauthorized
{ "message": "Token de autenticación requerido" }

# Token inválido
PUT /api/products/10
Authorization: Bearer invalid-token
→ 401 Unauthorized
{ "message": "Token inválido o expirado" }
```

### **Nivel 2: Autorización por Rol - 403 Forbidden**

```http
# Usuario USER intenta acceder a endpoint solo para ADMIN
GET /api/admin/reports
Authorization: Bearer <token-user>
→ 403 Forbidden
{ "message": "Se requiere rol ADMIN" }
```

### **Nivel 3: Ownership - 403 Forbidden**

```http
# Usuario B intenta modificar producto de Usuario A
PUT /api/products/10 (owner_id=A)
Authorization: Bearer <token-user-B>
→ 403 Forbidden
{ "message": "No puedes modificar recursos ajenos" }

# Usuario A modifica su propio producto
PUT /api/products/10 (owner_id=A)
Authorization: Bearer <token-user-A>
→ 200 OK (permitido)

# ADMIN modifica producto de cualquiera
PUT /api/products/10 (owner_id=A)
Authorization: Bearer <token-admin>
→ 200 OK (bypass por rol)
```

## **4.4. Diferencia Entre 401 y 403**

**401 Unauthorized**:
- **Significado**: "No sé quién eres"
- **Causa**: Token ausente, inválido o expirado
- **Acción del cliente**: Debe hacer login
- **Usuario**: No autenticado

**403 Forbidden**:
- **Significado**: "Sé quién eres, pero no puedes hacer esto"
- **Causa**: Sin rol necesario o no es propietario
- **Acción del cliente**: Mostrar mensaje de permiso denegado
- **Usuario**: Autenticado pero sin permisos

---

# **5. Flujo Completo de Ownership**

## **5.1. Usuario Intenta Actualizar Producto Ajeno**

```
Cliente:
PUT /api/products/10
Authorization: Bearer <token-user-2>
Body: { "name": "Hacked" }
        ↓
1. Middleware de autenticación valida JWT
   → Usuario autenticado: id=2, roles=[USER]
        ↓
2. Controlador recibe request
   → Llama service.update(10, data, user)
        ↓
3. Servicio carga producto desde BD
   → Product: { id: 10, name: "Original", ownerId: 1 }
        ↓
4. validateOwnership(product, user)
   a. ¿Usuario es ADMIN? → NO
   b. ¿product.ownerId == user.id?
      → 1 == 2? → NO
   → Lanza ForbiddenException
        ↓
5. Exception Handler captura error
   → Convierte a respuesta HTTP
        ↓
Cliente recibe:
403 Forbidden
{
  "status": 403,
  "error": "Forbidden",
  "message": "No eres propietario de este recurso"
}
```

## **5.2. ADMIN Actualiza Producto de Otro Usuario**

```
Cliente:
PUT /api/products/10
Authorization: Bearer <token-admin>
Body: { "name": "Corrected" }
        ↓
1-3. [Mismos pasos]
   → Product: { id: 10, ownerId: 1 }
   → Usuario: { id: 3, roles: [ADMIN] }
        ↓
4. validateOwnership(product, user)
   a. ¿Usuario es ADMIN? → SÍ
   → return (permitir sin verificar ownerId)
        ↓
5. Actualizar producto
        ↓
6. Guardar en BD
        ↓
Cliente recibe:
200 OK
{
  "id": 10,
  "name": "Corrected",
  "ownerId": 1
}
```

## **5.3. Usuario Actualiza Su Propio Producto**

```
Cliente:
PUT /api/products/10
Authorization: Bearer <token-user-1>
Body: { "name": "Updated" }
        ↓
1-3. [Mismos pasos]
   → Product: { id: 10, ownerId: 1 }
   → Usuario: { id: 1, roles: [USER] }
        ↓
4. validateOwnership(product, user)
   a. ¿Usuario es ADMIN? → NO
   b. ¿product.ownerId == user.id?
      → 1 == 1? → SÍ
   → Permitir (método termina sin lanzar excepción)
        ↓
5. Actualizar producto
        ↓
Cliente recibe:
200 OK
{
  "id": 10,
  "name": "Updated",
  "ownerId": 1
}
```

---

# **6. Casos de Uso Avanzados**

## **6.1. Ownership con Equipos/Departamentos**

**Escenario**: Un documento pertenece a un equipo, cualquier miembro puede modificarlo.

```javascript
validateOwnership(document, user) {
  // Permitir ADMIN
  if (user.roles.includes('ADMIN')) return;
  
  // Verificar si usuario es miembro del equipo
  const isMember = document.team.members.some(m => m.id === user.id);
  if (!isMember) {
    throw new ForbiddenException("No eres miembro del equipo propietario");
  }
}
```

## **6.2. Ownership con Jerarquía**

**Escenario**: Un manager puede ver/modificar recursos de su departamento.

```javascript
validateOwnership(resource, user) {
  // ADMIN siempre puede
  if (user.roles.includes('ADMIN')) return;
  
  // Propietario directo
  if (resource.ownerId === user.id) return;
  
  // Manager del mismo departamento
  if (user.roles.includes('MANAGER') && 
      resource.owner.department === user.department) {
    return;
  }
  
  throw new ForbiddenException("Sin permisos");
}
```

## **6.3. Ownership con Permisos Delegados**

**Escenario**: Un usuario puede compartir su recurso con otros usuarios.

```javascript
validateOwnership(resource, user) {
  // ADMIN
  if (user.roles.includes('ADMIN')) return;
  
  // Propietario
  if (resource.ownerId === user.id) return;
  
  // Usuario con permiso explícito compartido
  const hasSharedAccess = resource.sharedWith.some(
    share => share.userId === user.id && share.canEdit
  );
  if (hasSharedAccess) return;
  
  throw new ForbiddenException("Sin permisos");
}
```

---

# **7. Mejores Prácticas**

## **7.1. Query Única**

**Regla**: Cargar y validar en una sola operación.

```javascript
 MAL (2 queries):
const product = await ProductRepo.findById(id);
validateOwnership(product, user);
const fullProduct = await ProductRepo.findByIdWithRelations(id);

BIEN (1 query):
const product = await ProductRepo.findByIdWithRelations(id);
validateOwnership(product, user);
// Usar el mismo objeto para actualizar
```

## **7.2. ADMIN Bypass Explícito**

**Regla**: Verificar ADMIN primero para evitar lógica innecesaria.

```javascript
validateOwnership(resource, user) {
  // Verificar ADMIN primero (bypass temprano)
  if (user.roles.includes('ADMIN')) {
    return; // Salir sin más validaciones
  }
  
  // Lógica compleja solo si no es ADMIN
  if (resource.ownerId !== user.id) {
    throw new ForbiddenException();
  }
}
```

## **7.3. Mensajes de Error Claros**

**Regla**: Indicar exactamente por qué se denegó el acceso.

```javascript
 MAL:
throw new ForbiddenException("Forbidden");

BIEN:
throw new ForbiddenException(
  "No puedes modificar este producto. Solo el propietario o un administrador tienen permiso."
);
```

## **7.4. Métodos con y sin Validación**

**Regla**: Ofrecer métodos específicos para diferentes casos.

```javascript
class ProductService {
  // Validación de ownership (uso general)
  async delete(id, user) {
    const product = await this.findById(id);
    this.validateOwnership(product, user);
    await ProductRepo.delete(product);
  }
  
  // Sin validación (uso administrativo)
  async adminDelete(id) {
    // Ya protegido con @RequiresRole('ADMIN') en controlador
    await ProductRepo.deleteById(id);
  }
}
```

---

# **8. Testing de Ownership**

## **8.1. Tests Unitarios de Validación**

```javascript
describe('validateOwnership', () => {
  test('permite si usuario es propietario', () => {
    const product = { id: 1, ownerId: 2 };
    const user = { id: 2, roles: ['USER'] };
    
    expect(() => service.validateOwnership(product, user))
      .not.toThrow();
  });
  
  test('lanza excepción si usuario no es propietario', () => {
    const product = { id: 1, ownerId: 2 };
    const user = { id: 3, roles: ['USER'] };
    
    expect(() => service.validateOwnership(product, user))
      .toThrow(ForbiddenException);
  });
  
  test('permite si usuario es ADMIN', () => {
    const product = { id: 1, ownerId: 2 };
    const admin = { id: 99, roles: ['ADMIN'] };
    
    expect(() => service.validateOwnership(product, admin))
      .not.toThrow();
  });
});
```

## **8.2. Tests de Integración**

```http
# Test 1: Usuario actualiza su propio recurso
PUT /api/products/1 (owner_id=2)
Authorization: Bearer <token-user-2>
→ 200 OK

# Test 2: Usuario intenta actualizar recurso ajeno
PUT /api/products/1 (owner_id=2)
Authorization: Bearer <token-user-3>
→ 403 Forbidden

# Test 3: ADMIN actualiza recurso ajeno
PUT /api/products/1 (owner_id=2)
Authorization: Bearer <token-admin>
→ 200 OK

# Test 4: Usuario elimina su recurso
DELETE /api/products/1 (owner_id=2)
Authorization: Bearer <token-user-2>
→ 204 No Content

# Test 5: ADMIN usa endpoint sin validación
DELETE /api/products/1/admin
Authorization: Bearer <token-admin>
→ 204 No Content
```

---

# **9. Errores Comunes**

## **9.1. No Validar Ownership en Backend**

```javascript
 MAL:
// Confiar en frontend
// Frontend oculta botón "Editar" si no es propietario
// Pero request HTTP puede hacerse igual

BIEN:
// Siempre validar en backend
validateOwnership(resource, user);
```

## **9.2. Exponer Información en Errores**

```javascript
 MAL:
throw new ForbiddenException(
  `Este producto pertenece al usuario ${product.owner.email}`
);

BIEN:
throw new ForbiddenException(
  "No tienes permisos para modificar este recurso"
);
```

## **9.3. Olvidar ADMIN Bypass**

```javascript
 MAL:
if (resource.ownerId !== user.id) {
  throw new ForbiddenException();
}
// ADMIN también será bloqueado

BIEN:
if (user.roles.includes('ADMIN')) return;
if (resource.ownerId !== user.id) {
  throw new ForbiddenException();
}
```

---

# **10. Monitoreo y Auditoría**

## **10.1. Logs de Ownership Violations**

```javascript
validateOwnership(resource, user) {
  if (user.roles.includes('ADMIN')) return;
  
  if (resource.ownerId !== user.id) {
    // Registrar intento de acceso no autorizado
    logger.warn({
      event: 'OWNERSHIP_VIOLATION',
      userId: user.id,
      resourceType: 'Product',
      resourceId: resource.id,
      ownerId: resource.ownerId,
      timestamp: new Date()
    });
    
    throw new ForbiddenException();
  }
}
```

## **10.2. Métricas de Seguridad**

```
Métricas a monitorear:
- Intentos de acceso denegados por ownership
- Usuarios con más violaciones de ownership
- Recursos más atacados
- Patrones sospechosos (ej: intentar acceder a múltiples recursos ajenos)
```

---

# **11. Conclusión**

Has aprendido conceptos avanzados de ownership:

**Validación de propiedad** de recursos  
**Patrones de implementación**: Servicio, interceptores  
**ADMIN bypass** para acceso administrativo  
**Casos avanzados**: Equipos, jerarquías, permisos delegados  
**Mejores prácticas**: Query única, mensajes claros, testing  

**Combinación con roles**:
```
Autenticación → ¿Quién eres? → JWT válido
      ↓
Roles → ¿Qué puedes hacer globalmente? → RBAC
      ↓
Ownership → ¿Puedes acceder a ESTE recurso? → Validación
```

---

# **Aplicación en Frameworks**

Estos conceptos se implementan en los módulos específicos:

### Spring Boot

📄 [`spring-boot/p67/a_dodente/13_ownership_validacion.md`](../spring-boot/p67/a_dodente/13_ownership_validacion.md)

- validateOwnership() en servicios
- AccessDeniedException
- @Transactional para operaciones
- GlobalExceptionHandler

### NestJS

📄 [`nest/p67/a_dodente/13_ownership_validation.md`](../nest/p67/a_dodente/13_ownership_validation.md)

- Custom guards para ownership
- @UserFromToken decorator
- HttpException handling
- Resource ownership patterns

---

# **Resumen Final**

| Concepto | Implementación |
|----------|----------------|
| **Ownership** | Usuario propietario del recurso |
| **Validación** | Verificar ownerId == userId |
| **ADMIN bypass** | Permitir sin verificar ownership |
| **Ubicación** | Capa de servicio (no controlador) |
| **Excepción** | ForbiddenException (403) |
| **Mejor práctica** | Query única + validación + actualización |

Has completado los conceptos de autenticación, autorización y ownership. ¡Ahora puedes implementar seguridad robusta en tus APIs!
