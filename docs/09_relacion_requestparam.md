# Programación y Plataformas Web

# Frameworks Backend: Relaciones con Request Parameters y Contexto Semántico

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="80">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="80">
</div>


## Práctica 9: Request Parameters en Consultas Relacionadas – Contexto y Filtrado

### Autores

**Pablo Torres**

 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: PabloT18

## Introducción

En el tema anterior se abordaron las **relaciones entre entidades** desde un enfoque teórico y estructural.

Ahora, en aplicaciones reales, no basta con definir relaciones: es necesario **consultar y filtrar** los datos relacionados de manera eficiente y semánticamente correcta.

Los principales desafíos son:

* **¿Desde qué contexto se debe exponer una consulta relacionada?**
* **¿Cómo aplicar filtros a consultas que involucran múltiples entidades?**
* **¿Cuál es la diferencia entre navegación de relaciones y consultas explícitas?**
* **¿Cómo diseñar endpoints que reflejen la semántica del dominio?**

Ejemplos reales:

* Listar productos de un usuario específico
* Buscar órdenes de un cliente con filtros de fecha
* Encontrar estudiantes de una carrera por estado académico
* Consultar artículos de un autor con criterios de publicación

Este documento introduce los **conceptos de contexto semántico y request parameters** en consultas relacionadas, desde un enfoque **teórico y universal**, sin depender de sintaxis específica de ningún framework.

## 1. ¿Qué es el contexto semántico en APIs REST?

El **contexto semántico** define **desde qué perspectiva** se accede a un recurso relacionado en la arquitectura REST.

### 1.1 Principio fundamental

**El endpoint debe reflejar la relación lógica del dominio**, no necesariamente la estructura técnica de la base de datos.

### 1.2 Ejemplo conceptual

**Escenario**: Obtener productos de un usuario específico

**Opciones de diseño**:

```
Opción A: /users/{id}/products          ← Contexto de usuario
Opción B: /products?userId={id}         ← Contexto de productos
Opción C: /products/user/{id}           ← Híbrido confuso
```

**¿Cuál es la correcta?**

**Opción A** es semánticamente superior porque:
* Los productos **pertenecen** al usuario
* El usuario es el **contexto principal**
* Se consulta una **subcolección** del usuario
* La relación es **clara e intuitiva**

### 1.3 Regla general

```
/{contexto-principal}/{id}/{recurso-relacionado}
```

Ejemplos:
* `/users/123/products` - Productos del usuario 123
* `/customers/456/orders` - Órdenes del cliente 456
* `/authors/789/articles` - Artículos del autor 789
* `/universities/101/students` - Estudiantes de la universidad 101

## 2. Request Parameters en consultas relacionadas

Los **request parameters** permiten **filtrar y personalizar** las consultas relacionadas sin cambiar la semántica del endpoint.

### 2.1 Estructura básica

```
/{contexto}/{id}/{recurso}?param1=valor1&param2=valor2
```

### 2.2 Tipos de parámetros

#### **Filtros de búsqueda**
```
/users/123/products?name=laptop
```
- Buscar productos que contengan "laptop" en el nombre

#### **Rangos numéricos**
```
/users/123/products?minPrice=500&maxPrice=1500
```
- Productos con precio entre $500 y $1500

#### **Filtros por relación**
```
/users/123/products?categoryId=5
```
- Solo productos de la categoría 5

#### **Criterios de estado**
```
/customers/456/orders?status=completed
```
- Solo órdenes completadas

#### **Fechas y períodos**
```
/customers/456/orders?fromDate=2024-01-01&toDate=2024-12-31
```
- Órdenes dentro del período especificado

### 2.3 Combinación de parámetros

Los parámetros deben poder **combinarse** para consultas complejas:

```
/users/123/products?name=gaming&minPrice=800&categoryId=2&available=true
```

Esto representa: "Productos del usuario 123 que contengan 'gaming', cuesten más de $800, sean de categoría 2 y estén disponibles"

## 3. Navegación vs Consulta Explícita

### 3.1 Navegación de relaciones (problemática)

**Concepto**: Acceder a datos relacionados a través del grafo de objetos.

```
// Pseudocódigo problemático
user = userRepository.findById(123)
products = user.getProducts()  ← Navegación
```

**Problemas**:
* **Carga lazy**: Posibles excepciones de sesión cerrada
* **Carga eager**: Consumo innecesario de memoria
* **Sin control**: No se pueden aplicar filtros eficientemente
* **N+1**: Consultas múltiples ocultas
* **No escala**: Con miles de productos se vuelve inviable

### 3.2 Consulta explícita (recomendada)

**Concepto**: Usar el repositorio correspondiente para consultas directas.

```
// Pseudocódigo recomendado
products = productRepository.findByOwnerId(123)  ← Consulta explícita
```

**Ventajas**:
* **Control total**: Se especifica exactamente qué traer
* **Filtros eficientes**: Se aplican a nivel de base de datos
* **Performance predecible**: Una consulta, resultado conocido
* **Escalable**: Funciona con cualquier volumen de datos
* **Mantenible**: Lógica clara y explícita

### 3.3 Comparación práctica

| Aspecto | Navegación | Consulta Explícita |
|---------|------------|-------------------|
| **Performance** | ⚠️ Impredecible | ✅ Controlada |
| **Escalabilidad** | ❌ Limitada | ✅ Excelente |
| **Filtros** | ❌ En memoria | ✅ En BD |
| **Mantenimiento** | ⚠️ Dependencias ocultas | ✅ Lógica explícita |
| **Testing** | ❌ Complejo | ✅ Directo |

## 4. Principio de Responsabilidad en Consultas

### 4.1 Regla fundamental

**El repositorio correcto es el del agregado consultado, independientemente del contexto del endpoint.**

### 4.2 Ejemplo práctico

**Endpoint**: `/users/123/products`

**Responsabilidades**:
* **UserController**: Define el endpoint y valida que el usuario exista
* **UserService**: Orquesta la operación
* **ProductRepository**: Realiza la consulta de productos ← **Repositorio correcto**

**¿Por qué ProductRepository y no UserRepository?**
* Los **datos consultados son productos**
* Product es el **agregado raíz** de los datos retornados
* ProductRepository tiene el **conocimiento especializado** sobre consultas de productos
* Permite **optimizaciones específicas** de productos (índices, joins, etc.)

### 4.3 Patrón de implementación

```
Capa de Presentación
    UserController.getProducts(userId, filters)
            ↓
Capa de Aplicación  
    UserService.getProductsByUserId(userId, filters)
            ↓
Capa de Persistencia
    ProductRepository.findByOwnerIdWithFilters(userId, filters)  ← Repositorio correcto
```

## 5. Validación de contexto

### 5.1 ¿Cuándo usar cada contexto?

**Usar contexto de entidad padre cuando**:
* La relación representa **pertenencia** o **composición**
* El recurso hijo **depende existencialmente** del padre
* La consulta es una **subcolección lógica**

Ejemplos:
* `/users/{id}/addresses` - Direcciones pertenecen al usuario
* `/orders/{id}/items` - Items pertenecen a la orden
* `/courses/{id}/students` - Estudiantes inscritos en el curso

**Usar contexto genérico cuando**:
* La consulta es **transversal** a múltiples contextos
* No hay una relación de **pertenencia clara**
* Se requiere **búsqueda global**

Ejemplos:
* `/products?search=laptop` - Búsqueda global de productos
* `/orders?status=pending` - Todas las órdenes pendientes
* `/reports/sales` - Reportes generales

### 5.2 Antipatrones comunes

**❌ Contexto ambiguo**:
```
/products/user/123  ← Confuso, ¿es un producto llamado "user"?
```

**❌ Demasiado anidado**:
```
/users/123/addresses/456/deliveries/789/tracking
```

**❌ Contexto inconsistente**:
```
/users/123/products     ← Contexto de usuario
/categories/456/items   ← ¿Por qué "items" y no "products"?
```

## 6. Diseño de Request Parameters

### 6.1 Convenciones de nombres

**Usar nombres descriptivos y consistentes**:

```
// ✅ Claro y consistente
?name=laptop
?minPrice=500
?maxPrice=1500
?categoryId=3
?available=true

// ❌ Ambiguo o inconsistente
?n=laptop
?min=500
?max=1500
?cat=3
?avail=1
```

### 6.2 Tipos de datos coherentes

**Números**:
```
?price=1250.50
?quantity=10
?categoryId=5
```

**Booleanos**:
```
?available=true
?featured=false
?inStock=true
```

**Fechas** (formato ISO):
```
?createdAfter=2024-01-15
?updatedBefore=2024-12-31T23:59:59
```

**Strings** (búsqueda parcial):
```
?name=gaming
?description=laptop
?brand=apple
```

### 6.3 Parámetros opcionales vs obligatorios

**Regla**: Los parámetros de filtro deben ser **opcionales** por defecto.

```
// ✅ Todos los parámetros son opcionales
/users/123/products?name=laptop&minPrice=500

// ❌ Parámetros obligatorios crean endpoints rígidos
/users/123/products/{category}/{priceRange}
```

## 7. Validación de parámetros

### 7.1 Validación básica

**Rangos numéricos**:
* `minPrice >= 0`
* `maxPrice >= minPrice`
* `quantity > 0`

**Formatos de fecha**:
* Fechas válidas en formato ISO
* `fromDate <= toDate`

**IDs de referencia**:
* IDs positivos
* Existencia de entidades referenciadas

### 7.2 Valores por defecto

Cuando no se especifican parámetros, debe haber **comportamiento predecible**:

```
// Sin parámetros = todos los productos del usuario
/users/123/products

// Con parámetros = filtros aplicados
/users/123/products?available=true
```

### 7.3 Combinaciones inválidas

Detectar y manejar **combinaciones lógicamente inconsistentes**:

```
// ❌ Inconsistente
?minPrice=1000&maxPrice=500

// ❌ Contradictorio
?available=true&inStock=false
```

## 8. Response y metadatos

### 8.1 Estructura de respuesta

La respuesta debe incluir **metadatos sobre los filtros aplicados**:

```json
{
  "data": [
    // ... productos filtrados ...
  ],
  "filters": {
    "userId": 123,
    "name": "laptop",
    "minPrice": 500,
    "categoryId": 3
  },
  "metadata": {
    "totalItems": 15,
    "appliedFilters": 3
  }
}
```

### 8.2 Información contextual

Incluir **información del contexto** cuando sea relevante:

```json
{
  "data": [ /* productos */ ],
  "context": {
    "userId": 123,
    "userName": "Juan Pérez",
    "userEmail": "juan@email.com"
  },
  "filters": { /* filtros aplicados */ }
}
```

## 9. Performance y escalabilidad

### 9.1 Consultas eficientes

Los filtros deben traducirse a **consultas SQL optimizadas**:

```sql
-- ✅ Filtros en WHERE clause
SELECT p.* FROM products p 
JOIN users u ON p.user_id = u.id 
WHERE u.id = 123 
  AND p.name ILIKE '%laptop%'
  AND p.price BETWEEN 500 AND 1500
  AND p.category_id = 3;

-- ❌ Traer todo y filtrar en memoria
SELECT p.* FROM products p JOIN users u ON p.user_id = u.id WHERE u.id = 123;
-- + filtrado en aplicación
```

### 9.2 Índices requeridos

Los campos usados en filtros deben estar **indexados**:

```sql
CREATE INDEX idx_products_user_id ON products(user_id);
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_category ON products(category_id);
```

### 9.3 Limitación de resultados

Considerar **límites automáticos** para prevenir consultas masivas:

```
// Límite implícito para proteger el sistema
/users/123/products → máximo 1000 resultados

// Límite explícito
/users/123/products?limit=50
```

## 10. Casos de uso avanzados

### 10.1 Búsqueda full-text

Cuando el parámetro requiere **búsqueda semántica**:

```
/users/123/products?search=gaming+laptop+high+performance
```

### 10.2 Filtros por múltiples relaciones

```
/users/123/products?categoryName=electronics&brandName=apple
```

Requiere **joins con múltiples tablas** manteniendo performance.

### 10.3 Filtros de agregación

```
/customers/456/orders?totalAmount_gt=1000
/categories/789/products?averageRating_gte=4.0
```

Campos calculados que requieren **consultas especializadas**.

## 11. Errores comunes y antipatrones

### 11.1 Errores técnicos

* **Navigar relaciones**: Usar `user.getProducts()` en lugar de consulta explícita
* **Filtros en memoria**: Traer todos los datos y filtrar en la aplicación
* **N+1 ocultos**: Cargar relaciones sin control
* **Sin validación**: Aceptar parámetros sin validar tipos o rangos

### 11.2 Errores de diseño

* **Contexto incorrecto**: `/products?userId=123` en lugar de `/users/123/products`
* **Parámetros ambiguos**: Nombres poco descriptivos o inconsistentes
* **Endpoints rígidos**: Requerir parámetros que deberían ser opcionales
* **Sobreingeniería**: Demasiados niveles de anidación

### 11.3 Errores de performance

* **Sin índices**: Filtros en campos no indexados
* **Consultas ineficientes**: Múltiples consultas en lugar de joins
* **Sin límites**: Permitir consultas que retornen millones de registros
* **Cacheo inadecuado**: No considerar estrategias de cache

## 12. Buenas prácticas

### 12.1 Diseño de endpoints

* **Contexto semántico claro**: El endpoint debe reflejar la relación lógica
* **Consistencia**: Usar convenciones uniformes en toda la API
* **Simplicidad**: Evitar anidaciones excesivas
* **Flexibilidad**: Parámetros opcionales que permitan refinamiento

### 12.2 Implementación técnica

* **Consultas explícitas**: Usar el repositorio del agregado consultado
* **Validación robusta**: Validar tipos, rangos y existencia
* **Performance**: Índices, límites y consultas optimizadas
* **Documentación**: Especificar parámetros disponibles y comportamiento

### 12.3 Mantenibilidad

* **Separación de responsabilidades**: Cada capa con su función específica
* **Testing**: Pruebas para diferentes combinaciones de parámetros
* **Monitoreo**: Métricas de uso y performance de los filtros
* **Evolución**: Diseño que permita agregar nuevos filtros sin romper compatibilidad

## 13. Resultados esperados

Al finalizar este tema, el estudiante comprende:

* qué es el contexto semántico en APIs REST
* diferencia entre navegación de relaciones y consulta explícita
* cómo diseñar endpoints que reflejen el dominio
* uso correcto de request parameters para filtrado
* principios de responsabilidad en consultas relacionadas
* consideraciones de performance y escalabilidad
* buenas prácticas y errores comunes
* preparación para implementación real

## 14. Aplicación directa en los siguientes módulos

Estos conceptos se aplicarán directamente en los módulos específicos de cada framework.

### Spring Boot

[`spring-boot/09_relacion_requestparam.md`](../spring-boot/09_relacion_requestparam.md)

* @RequestParam y validación
* Specification para filtros dinámicos
* @Query personalizada con parámetros
* PathVariable vs RequestParam
* ejemplos con /users/{id}/products

### NestJS

[`nest/09_relacion_requestparam.md`](../nest/09_relacion_requestparam.md)

* @Query() decorators
* ValidationPipe con DTOs de filtros
* QueryBuilder con parámetros dinámicos
* Custom decorators para validación
* ejemplos con /users/{id}/products