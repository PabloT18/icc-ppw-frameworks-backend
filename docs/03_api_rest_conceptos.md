# Programación y Plataformas Web

# Frameworks Backend: Diseño de API REST

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="80" alt="Java Logo">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="80" alt="TypeScript Logo">
</div>

## Tema 03: Diseño de API REST

### Autor

**Pablo Torres**

[ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: [PabloT18](https://github.com/PabloT18)

---

# Introducción

Una API REST permite que una aplicación backend exponga recursos para que puedan ser utilizados por clientes externos, como aplicaciones web, aplicaciones móviles u otros sistemas.

En los temas anteriores se revisaron conceptos como API, HTTP, JSON, request, response, DTO, controlador, servicio y repositorio. En este tema se estudia cómo diseñar correctamente una API REST antes de implementarla con Spring Boot o NestJS.

El objetivo no es escribir todavía controladores, sino aprender a definir recursos, rutas, parámetros, filtros, búsquedas, paginación, versionado y respuestas consistentes.

Una API REST bien diseñada debe ser:

* clara;
* predecible;
* coherente;
* mantenible;
* fácil de consumir;
* fácil de documentar;
* preparada para crecer.

---

# Objetivos

Al finalizar este tema, el estudiante será capaz de:

* Diseñar rutas REST orientadas a recursos.
* Diferenciar recursos principales y subrecursos.
* Usar correctamente path variables y query params.
* Definir filtros, búsquedas, ordenamiento y paginación.
* Diseñar respuestas consistentes.
* Identificar errores comunes en el diseño de APIs REST.
* Plantear una API REST antes de implementarla en un framework backend.

---

# 1. Recordatorio: API REST

REST significa **Representational State Transfer**.

Es un estilo arquitectónico usado para diseñar APIs orientadas a recursos.

Una API REST no se diseña alrededor de acciones, sino alrededor de recursos del sistema.

Ejemplo de recursos:

```txt
users
products
orders
students
courses
```

Ejemplo no recomendado:

```txt
/createUser
/getAllProducts
/deleteOrder
```

Ejemplo recomendado:

```txt
/users
/products
/orders
```

La acción se expresa mediante el método HTTP. La ruta expresa el recurso.

---

# 2. Diseño orientado a recursos

## 2.1 ¿Qué es un recurso?

Un recurso representa una entidad o concepto importante dentro del sistema.

Ejemplos en un sistema académico:

```txt
students
teachers
courses
enrollments
grades
```

Ejemplos en un sistema de ventas:

```txt
products
customers
orders
payments
invoices
```

Ejemplos en un sistema de biblioteca:

```txt
books
authors
loans
users
categories
```

Un recurso debe nombrarse con sustantivos, no con verbos.

---

## 2.2 Recursos principales

Los recursos principales representan elementos centrales del sistema.

Ejemplo:

```txt
/students
/courses
/teachers
```

Cada recurso principal puede tener operaciones de consulta, creación, actualización o eliminación.

Ejemplo:

```txt
GET    /students
POST   /students
GET    /students/{id}
PUT    /students/{id}
PATCH  /students/{id}
DELETE /students/{id}
```

---

## 2.3 Recursos en plural

En REST se recomienda usar sustantivos en plural.

Correcto:

```txt
/users
/products
/orders
/students
```

No recomendado:

```txt
/user
/product
/order
/student
```

El plural indica que el endpoint representa una colección de recursos.

---

# 3. URI y estructura de rutas

## 3.1 ¿Qué es una URI?

Una URI identifica un recurso dentro de la API.

Ejemplo:

```txt
/api/students/10
```

Esta URI identifica al estudiante con ID 10.

---

## 3.2 Estructura recomendada

Una ruta REST debe ser clara y jerárquica.

Estructura general:

```txt
/api/[version]/[resource]/{id}/[subresource]
```

Ejemplo:

```txt
/api/v1/students/10/enrollments
```

Interpretación:

```txt
api        -> prefijo general de la API
v1         -> versión
students   -> recurso principal
10         -> identificador del estudiante
enrollments -> subrecurso
```

---

## 3.3 Prefijo de API

Es común usar `/api` como prefijo para separar rutas backend de otras rutas del sistema.

Ejemplo:

```txt
/api/students
/api/courses
/api/orders
```

También puede combinarse con versionado:

```txt
/api/v1/students
/api/v1/courses
/api/v1/orders
```

---

## 3.4 Rutas limpias

Una ruta limpia debe ser fácil de leer.

Correcto:

```txt
GET /api/v1/products/15
```

No recomendado:

```txt
GET /api/v1/getProductById?id=15
```

La ruta debe representar el recurso. Los parámetros deben complementar la consulta.

---

# 4. Colecciones y recursos individuales

## 4.1 Colección

Una colección representa un conjunto de recursos.

Ejemplo:

```txt
/students
```

Operaciones frecuentes sobre colección:

```txt
GET  /students
POST /students
```

Interpretación:

```txt
GET /students  -> obtener lista de estudiantes
POST /students -> crear un nuevo estudiante
```

---

## 4.2 Recurso individual

Un recurso individual representa un elemento específico de una colección.

Ejemplo:

```txt
/students/{id}
```

Operaciones frecuentes sobre recurso individual:

```txt
GET    /students/{id}
PUT    /students/{id}
PATCH  /students/{id}
DELETE /students/{id}
```

Interpretación:

```txt
GET /students/10    -> obtener estudiante 10
PUT /students/10    -> reemplazar estudiante 10
PATCH /students/10  -> actualizar parcialmente estudiante 10
DELETE /students/10 -> eliminar estudiante 10
```

---

# 5. Subrecursos

## 5.1 ¿Qué es un subrecurso?

Un subrecurso representa información relacionada con un recurso principal.

Ejemplo:

```txt
/students/{id}/enrollments
```

Esto representa las matrículas de un estudiante específico.

---

## 5.2 Ejemplos de subrecursos

Sistema académico:

```txt
/students/{id}/enrollments
/students/{id}/grades
/courses/{id}/students
/teachers/{id}/courses
```

Sistema de ventas:

```txt
/customers/{id}/orders
/orders/{id}/payments
/products/{id}/reviews
/categories/{id}/products
```

---

## 5.3 Cuándo usar subrecursos

Se recomienda usar subrecursos cuando existe una relación clara de pertenencia o dependencia.

Ejemplo correcto:

```txt
GET /students/10/enrollments
```

Porque las matrículas consultadas pertenecen al estudiante 10.

Ejemplo que puede ser mejor como filtro:

```txt
GET /enrollments?studentId=10
```

Ambas opciones pueden ser válidas. La elección depende del diseño de la API.

---

## 5.4 Regla práctica

Usar subrecursos cuando se quiere expresar relación jerárquica:

```txt
/students/{id}/enrollments
```

Usar query params cuando se quiere filtrar una colección:

```txt
/enrollments?studentId=10
```

---

# 6. Path Variables

## 6.1 ¿Qué son las path variables?

Las path variables son valores dinámicos que forman parte de la ruta.

Ejemplo:

```txt
GET /students/10
```

En este caso:

```txt
10
```

es una path variable.

Se suele representar así:

```txt
GET /students/{id}
```

---

## 6.2 Uso correcto

Las path variables se usan para identificar recursos específicos.

Ejemplos:

```txt
GET /users/{id}
GET /products/{id}
GET /orders/{id}
GET /courses/{id}
```

---

## 6.3 Más de una path variable

Una ruta puede tener más de una path variable cuando existe una relación entre recursos.

Ejemplo:

```txt
GET /students/{studentId}/enrollments/{enrollmentId}
```

Interpretación:

```txt
Buscar la matrícula enrollmentId asociada al estudiante studentId.
```

---

## 6.4 Cuándo no usar path variables

No se recomienda usar path variables para filtros opcionales.

No recomendado:

```txt
GET /products/category/laptops/min-price/500
```

Recomendado:

```txt
GET /products?category=laptops&minPrice=500
```

---

# 7. Query Params

## 7.1 ¿Qué son los query params?

Los query params son parámetros enviados después del signo `?` en una URL.

Ejemplo:

```txt
GET /products?category=laptops&minPrice=500
```

En este caso:

```txt
category=laptops
minPrice=500
```

son query params.

---

## 7.2 Para qué se usan

Los query params se usan principalmente para:

* filtrar;
* buscar;
* ordenar;
* paginar;
* seleccionar campos;
* cambiar formato de respuesta;
* aplicar condiciones opcionales.

---

## 7.3 Ejemplos

Filtrar por categoría:

```txt
GET /products?category=laptops
```

Filtrar por rango de precio:

```txt
GET /products?minPrice=500&maxPrice=1500
```

Ordenar:

```txt
GET /products?sort=price&order=asc
```

Paginar:

```txt
GET /products?page=1&limit=20
```

Combinar criterios:

```txt
GET /products?category=laptops&minPrice=500&maxPrice=1500&page=1&limit=20
```

---


# 8. Versionado de APIs

## 8.1 ¿Qué es versionar una API?

Versionar una API significa mantener diferentes versiones de sus endpoints cuando la estructura o comportamiento cambia.

Ejemplo:

```txt
/api/v1/users
/api/v2/users
```

Esto permite que clientes antiguos sigan funcionando mientras se introduce una nueva versión.

---

## 8.2 Cuándo versionar

Se recomienda versionar cuando existen cambios incompatibles.

Ejemplos:

* cambiar nombres de campos;
* eliminar campos de una respuesta;
* modificar estructura de datos;
* cambiar reglas de negocio;
* reemplazar endpoints existentes.

---

## 8.3 Versionado por ruta

Es la forma más sencilla para cursos y proyectos académicos.

Ejemplo:

```txt
/api/v1/products
/api/v2/products
```

Ventaja:

```txt
Es fácil de leer, probar y documentar.
```

Desventaja:

```txt
La versión queda visible en la URL.
```

---

## 8.4 Versionado por header

Otra opción es versionar usando headers.

Ejemplo:

```txt
Accept: application/vnd.ups.api-v2+json
```

Ventaja:

```txt
La URL se mantiene limpia.
```

Desventaja:

```txt
Es menos visible para estudiantes, pruebas manuales y documentación inicial.
```

Para este curso se recomienda versionado por ruta.

---

# 9. Respuestas consistentes

## 9.1 ¿Qué es una respuesta consistente?

Una respuesta consistente mantiene una estructura similar en todos los endpoints.

Ejemplo:

```json
{
  "data": {},
  "message": "Operación exitosa",
  "timestamp": "2026-06-18T10:30:00Z",
  "path": "/api/v1/users/1"
}
```

Esto facilita que el frontend consuma la API.

---

## 9.2 Respuesta de recurso único

Ejemplo:

```json
{
  "data": {
    "id": 1,
    "name": "Ana Torres",
    "email": "ana@example.com"
  },
  "message": "Usuario encontrado",
  "timestamp": "2026-06-18T10:30:00Z",
  "path": "/api/v1/users/1"
}
```

---

## 9.3 Respuesta de colección

Ejemplo:

```json
{
  "data": [
    {
      "id": 1,
      "name": "Ana Torres"
    },
    {
      "id": 2,
      "name": "Juan Pérez"
    }
  ],
  "message": "Usuarios encontrados",
  "timestamp": "2026-06-18T10:30:00Z",
  "path": "/api/v1/users"
}
```

---

## 9.4 Respuesta paginada

Ejemplo:

```json
{
  "data": [
    {
      "id": 1,
      "name": "Laptop Lenovo"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "totalItems": 150,
    "totalPages": 8
  },
  "message": "Productos encontrados",
  "timestamp": "2026-06-18T10:30:00Z",
  "path": "/api/v1/products"
}
```

---

# 10. Respuestas de error

## 10.1 Error consistente

Los errores también deben mantener una estructura común.

Ejemplo:

```json
{
  "statusCode": 404,
  "message": "Usuario no encontrado",
  "error": "Not Found",
  "timestamp": "2026-06-18T10:30:00Z",
  "path": "/api/v1/users/50"
}
```

---

## 10.2 Error de validación

Cuando los datos enviados no cumplen las reglas esperadas, se puede devolver una lista de errores.

Ejemplo:

```json
{
  "statusCode": 400,
  "message": "Error de validación",
  "errors": [
    {
      "field": "email",
      "message": "El correo es obligatorio"
    },
    {
      "field": "password",
      "message": "La contraseña debe tener mínimo 8 caracteres"
    }
  ],
  "timestamp": "2026-06-18T10:30:00Z",
  "path": "/api/v1/users"
}
```

---

## 10.3 Error de negocio

Un error de negocio ocurre cuando la petición tiene formato correcto, pero rompe una regla del sistema.

Ejemplo:

```json
{
  "statusCode": 409,
  "message": "El correo ya se encuentra registrado",
  "error": "Conflict",
  "timestamp": "2026-06-18T10:30:00Z",
  "path": "/api/v1/users"
}
```

---


# 11. Diseño de endpoints REST

## 11.1 Plantilla de diseño

Antes de programar, se recomienda diseñar los endpoints en una tabla.

| Método | Ruta             | Descripción           | Parámetros                | Respuesta              |
| ------ | ---------------- | --------------------- | ------------------------- | ---------------------- |
| GET    | `/students`      | Listar estudiantes    | `page`, `limit`, `search` | Lista paginada         |
| GET    | `/students/{id}` | Obtener estudiante    | `id`                      | Estudiante             |
| POST   | `/students`      | Crear estudiante      | body                      | Estudiante creado      |
| PATCH  | `/students/{id}` | Actualizar estudiante | `id`, body                | Estudiante actualizado |
| DELETE | `/students/{id}` | Eliminar estudiante   | `id`                      | Sin contenido          |

---

## 11.2 Ejemplo: API de estudiantes

Recurso principal:

```txt
students
```

Endpoints:

```txt
GET    /api/v1/students
GET    /api/v1/students/{id}
POST   /api/v1/students
PATCH  /api/v1/students/{id}
DELETE /api/v1/students/{id}
```

Filtros:

```txt
GET /api/v1/students?career=computacion
GET /api/v1/students?semester=3
GET /api/v1/students?search=ana
GET /api/v1/students?page=1&limit=20
```

Subrecursos:

```txt
GET /api/v1/students/{id}/enrollments
GET /api/v1/students/{id}/grades
```

---

## 11.3 Ejemplo: API de cursos

Recurso principal:

```txt
courses
```

Endpoints:

```txt
GET    /api/v1/courses
GET    /api/v1/courses/{id}
POST   /api/v1/courses
PATCH  /api/v1/courses/{id}
DELETE /api/v1/courses/{id}
```

Filtros:

```txt
GET /api/v1/courses?level=basic
GET /api/v1/courses?teacherId=5
GET /api/v1/courses?search=backend
```

Subrecursos:

```txt
GET /api/v1/courses/{id}/students
GET /api/v1/courses/{id}/teacher
```

---

# 12. Anti-patrones en APIs REST

## 12.1 Usar verbos en rutas

No recomendado:

```txt
POST /createUser
GET /getUsers
DELETE /deleteUser/10
```

Correcto:

```txt
POST /users
GET /users
DELETE /users/10
```

---

## 12.2 Mezclar idiomas

No recomendado:

```txt
GET /usuarios
GET /products
GET /materias
```

Correcto:

```txt
GET /users
GET /products
GET /courses
```

La API debe usar un solo idioma en sus rutas.

---

## 12.3 Rutas demasiado profundas

No recomendado:

```txt
GET /universities/1/faculties/2/careers/3/students/4/enrollments/5/grades
```

Corrección:

```txt
GET /grades?studentId=4&enrollmentId=5
```

Las rutas muy profundas son difíciles de mantener.

---

## 12.4 Usar query params para identificar recursos únicos

No recomendado:

```txt
GET /users?id=10
```

Correcto:

```txt
GET /users/10
```

El identificador principal de un recurso debe ir en la ruta.

---

## 12.5 Devolver datos sensibles

No recomendado:

```json
{
  "id": 1,
  "name": "Ana",
  "email": "ana@example.com",
  "password": "123456",
  "passwordHash": "$2a$10..."
}
```

Correcto:

```json
{
  "id": 1,
  "name": "Ana",
  "email": "ana@example.com"
}
```

---



