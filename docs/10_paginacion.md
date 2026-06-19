# Programación y Plataformas Web

# Frameworks Backend: Paginación de Datos y Navegación de Resultados

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="80">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="80">
</div>


## Práctica 10: Paginación de Datos – Optimización y User Experience

### Autores

**Pablo Torres**

 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: PabloT18

## Introducción

En aplicaciones reales, las consultas **NO devuelven todos los registros** de una sola vez.

Cuando una tabla contiene miles o millones de registros, devolver toda la información en una sola consulta genera:

* **Consumo excesivo de memoria**
* **Tiempo de respuesta lento**
* **Sobrecarga de red**
* **Experiencia de usuario deficiente**
* **Posibles timeouts**

Ejemplos reales:

* Un catálogo de productos con 100,000 artículos
* Una lista de usuarios con 50,000 registros
* Un feed de noticias con miles de publicaciones
* Historial de transacciones bancarias
* Resultados de búsqueda en Google

Este documento introduce el **concepto de paginación**, desde un enfoque **teórico y universal**, sin depender de sintaxis específica de ningún framework.

Las implementaciones concretas se desarrollarán posteriormente en los materiales propios de cada framework.

## 1. ¿Qué es la paginación?

La **paginación** es una técnica que divide un conjunto grande de datos en **páginas o fragmentos más pequeños**, permitiendo navegar entre ellos de manera eficiente.

Conceptualmente:

* Divide resultados en "páginas" de tamaño fijo
* Permite navegación secuencial (anterior/siguiente)
* Mejora el rendimiento del sistema
* Optimiza la experiencia del usuario

### Analogía física

Como un **libro**:
* El libro completo = todos los registros
* Cada página = un subconjunto de registros
* Índice = información de navegación
* Marcador = posición actual

## 2. Elementos de un sistema de paginación

### 2.1 Parámetros de entrada

* **page**: Número de página (empezando en 1 o 0)
* **size/limit**: Cantidad de registros por página
* **sort**: Criterio de ordenamiento
* **direction**: Dirección del ordenamiento (ASC/DESC)

### 2.2 Información de respuesta

* **content/data**: Los registros de la página actual
* **totalElements**: Total de registros en la consulta
* **totalPages**: Total de páginas disponibles
* **currentPage**: Página actual
* **pageSize**: Tamaño de página usado
* **hasNext**: Si existe página siguiente
* **hasPrevious**: Si existe página anterior

### 2.3 Ejemplo conceptual

```
Consulta: usuarios?page=2&size=10

Respuesta:
{
  data: [...10 usuarios...],
  totalElements: 1250,
  totalPages: 125,
  currentPage: 2,
  pageSize: 10,
  hasNext: true,
  hasPrevious: true
}
```

## 3. Tipos de paginación

### 3.1 Paginación por Offset/Limit (más común)

**Concepto**: Saltar N registros y tomar los siguientes M.

Fórmula:
```
offset = (page - 1) * size
limit = size
```

**Ventajas**:
* Navegación a cualquier página
* Fácil implementación
* Soporte nativo en la mayoría de bases de datos

**Desventajas**:
* Rendimiento degradado en páginas altas
* Inconsistencias si se agregan/eliminan registros

### 3.2 Paginación por Cursor (para alta performance)

**Concepto**: Usar un marcador (cursor) para continuar desde un punto específico.

Ejemplo:
```
productos?cursor=eyJ0aW1lc3RhbXAiOjE2MjM0NTY3ODl9&size=20
```

**Ventajas**:
* Rendimiento constante
* Consistente ante cambios
* Ideal para feeds en tiempo real

**Desventajas**:
* Solo navegación secuencial
* Implementación más compleja
* No permite saltar a páginas específicas

### 3.3 Paginación por Seek (híbrida)

**Concepto**: Usar valores conocidos para continuar la búsqueda.

Ejemplo:
```
productos?after_id=1234&size=20
```

**Uso típico**: Feeds de redes sociales, chats, logs

## 4. Beneficios de la paginación

### 4.1 Performance

* **Menos memoria**: Solo se cargan registros necesarios
* **Consultas más rápidas**: Menos datos procesados
* **Menor ancho de banda**: Transferencias más pequeñas

### 4.2 User Experience

* **Carga más rápida**: Páginas responden inmediatamente
* **Navegación intuitiva**: Similar a libros/revistas
* **Búsqueda eficiente**: Filtros combinados con paginación

### 4.3 Escalabilidad

* **Crecimiento sostenible**: El sistema funciona con millones de registros
* **Recursos predecibles**: Consumo de memoria controlado

## 5. Paginación y ordenamiento

La paginación **siempre debe ir acompañada de ordenamiento** para garantizar resultados consistentes.

### Problema sin ordenamiento

Sin ordenamiento explícito:
```
Página 1: [registro A, B, C]
Página 2: [registro C, D, E]  ← C aparece duplicado
```

### Solución con ordenamiento

Con ordenamiento por ID:
```
Página 1: [registro 1, 2, 3]
Página 2: [registro 4, 5, 6]  ← Consistente
```

### Ordenamientos comunes

* **Por ID**: Garantiza unicidad y consistencia
* **Por fecha**: Para cronología (createdAt, updatedAt)
* **Por nombre**: Para listados alfabéticos
* **Por relevancia**: Para resultados de búsqueda

## 6. Estrategias de implementación

### 6.1 En la capa de servicio

El servicio recibe parámetros de paginación y los delega al repositorio:

```
serviceFindAll(page, size, sort)
```

### 6.2 En el repositorio

El repositorio traduce los parámetros a consultas específicas de la base de datos:

```
SQL: SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 20
```

### 6.3 En la respuesta

Se construye un objeto de respuesta estandarizado con metadatos de paginación:

```
{
  content: [...],
  pagination: {
    totalElements: 1250,
    totalPages: 125,
    currentPage: 3,
    pageSize: 10
  }
}
```

## 7. Consideraciones de performance

### 7.1 Índices de base de datos

Los campos usados en **ORDER BY** deben estar indexados:

```
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_products_name ON products(name);
```

### 7.2 Límites razonables

* **Tamaño mínimo**: 5-10 registros (evita demasiadas consultas)
* **Tamaño máximo**: 50-100 registros (evita sobrecarga)
* **Tamaño por defecto**: 10-20 registros

### 7.3 Problemas con OFFSET alto

En páginas muy altas (ej: página 10,000), `OFFSET` se vuelve ineficiente:

```
-- Muy lento en páginas altas
SELECT * FROM products ORDER BY id LIMIT 20 OFFSET 200000;
```

**Alternativas**:
* Usar paginación por cursor
* Implementar búsqueda en lugar de navegación
* Limitar el número máximo de páginas

## 8. Paginación y filtros

La paginación debe **combinarse con filtros** para ser útil:

```
productos?category=electronics&page=1&size=20&sort=price,asc
```

**Flujo**:
1. Aplicar filtros
2. Contar total de resultados filtrados
3. Aplicar ordenamiento
4. Aplicar paginación
5. Retornar página + metadatos

## 9. Casos de uso comunes

### 9.1 Listados de administración

* Usuarios del sistema
* Productos del catálogo
* Órdenes de compra
* Logs de auditoria

### 9.2 APIs públicas

* Catálogo de productos
* Artículos de blog
* Resultados de búsqueda
* Feeds de contenido

### 9.3 Reportes

* Transacciones por fecha
* Ventas por período
* Actividad de usuarios
* Métricas del sistema

## 10. Errores comunes en paginación

### 10.1 Errores técnicos

* **Sin ordenamiento**: Resultados inconsistentes entre páginas
* **Parámetros sin validar**: Páginas negativas o tamaños excesivos
* **Sin límites**: Permitir consultas de millones de registros
* **Índices faltantes**: Consultas lentas en páginas altas

### 10.2 Errores de UX

* **Sin indicadores de progreso**: Usuario no sabe dónde está
* **Sin información total**: No mostrar cuántos registros hay
* **Navegación limitada**: Solo anterior/siguiente
* **Tamaños inadecuados**: Muy pocos o demasiados registros

## 11. Buenas prácticas

### 11.1 Validación de parámetros

* Página mínima: 1 (o 0 según convención)
* Tamaño mínimo/máximo definido
* Ordenamiento válido y seguro
* Valores por defecto sensatos

### 11.2 Respuesta consistente

* Formato estándar para todas las APIs
* Metadatos completos de paginación
* Información para construir navegación
* URLs de navegación (opcional)

### 11.3 Performance

* Índices en campos de ordenamiento
* Límites de tamaño de página
* Cache de conteos totales (si es apropiado)
* Monitoreo de consultas lentas

## 12. Evolución y escalabilidad

### 12.1 De simple a complejo

1. **Básico**: Paginación por offset/limit
2. **Intermedio**: Filtros + ordenamiento múltiple
3. **Avanzado**: Paginación por cursor
4. **Experto**: Búsqueda full-text + paginación

### 12.2 Consideraciones futuras

* Migrar a cursor para high-traffic
* Implementar cache de resultados
* Agregar búsqueda personalizada
* Optimizar para mobile (tamaños diferentes)

## 13. Resultados esperados

Al finalizar este tema, el estudiante comprende:

* qué es la paginación y por qué es necesaria
* tipos de paginación y cuándo usar cada una
* elementos de una respuesta paginada
* relación entre paginación, ordenamiento y filtros
* consideraciones de performance
* buenas prácticas y errores comunes
* preparación para implementación real

## 14. Aplicación directa en los siguientes módulos

Estos conceptos se aplicarán directamente en los módulos específicos de cada framework.

### Spring Boot

[`spring-boot/10_paginacion.md`](../spring-boot/10_paginacion.md)

* Spring Data JPA Pageable
* Page y Slice
* Sort y ordenamiento
* PageRequest y PageImpl
* ejemplos reales con PostgreSQL

### NestJS

[`nest/10_paginacion.md`](../nest/10_paginacion.md)

* TypeORM FindOptions
* take y skip
* QueryBuilder con pagination
* custom pagination DTOs
* ejemplos reales con PostgreSQL