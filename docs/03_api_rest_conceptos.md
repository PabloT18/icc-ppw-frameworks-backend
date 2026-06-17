# Programación y Plataformas Web

# Frameworks Backend: Conceptos Fundamentales de API REST

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="80" alt="Java Logo">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="80" alt="TS Logo">
</div>

## Práctica 3: API REST – Conceptos Fundamentales

### Autores

**Pablo Torres**
 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)
GitHub: [PabloT18](https://github.com/PabloT18)

---

# Introducción

Una API REST es el mecanismo más utilizado actualmente para construir servicios backend que se comunican con aplicaciones web, móviles o sistemas externos.
Antes de implementarla con **Spring Boot** o **NestJS**, es necesario comprender sus conceptos fundamentales:

* qué es un recurso
* diseño correcto de rutas
* verbos HTTP y su semántica
* manejo de parámetros
* códigos de estado
* idempotencia
* paginación y filtrado
* buenas prácticas de diseño

Este tema proporciona la base conceptual para los temas:

📌 `spring-boot/03_api_rest.md`
📌 `nest/03_api_rest.md`

---

# 1. ¿Qué es una API REST?

**REST (Representational State Transfer)** es un estilo arquitectónico que define cómo deben comunicarse los sistemas utilizando HTTP de manera:

* sencilla
* predecible
* escalable
* orientada a recursos

Una API REST **no es un framework ni un protocolo**, sino una forma estandarizada de diseñar endpoints.

---

# 2. Principios de REST

REST se basa en 6 principios fundamentales:

| Principio                         | Descripción                                                                |
| --------------------------------- | -------------------------------------------------------------------------- |
| **Cliente–Servidor**              | El cliente (frontend) y el servidor (backend) están separados.             |
| **Stateless**                     | Cada petición es independiente; el servidor no guarda estado del cliente.  |
| **Cacheable**                     | Las respuestas pueden ser almacenadas en caché para optimizar rendimiento. |
| **Interfaz Uniforme**             | Todas las rutas siguen reglas coherentes y predecibles.                    |
| **Sistema en Capas**              | La API puede tener intermediarios (gateways, proxys).                      |
| **Código por demanda (opcional)** | El servidor puede enviar scripts ejecutables.                              |

El principio más importante para este curso es **Stateless**.

---

# 3. Recursos en REST

REST organiza la información en **recursos**, representados con sustantivos en plural.

Ejemplos:

```
users
products
orders
students
courses
```

## 3.1 Rutas para colecciones

```
GET    /api/users
POST   /api/users
```

## 3.2 Rutas para un recurso específico

```
GET    /api/users/{id}
PUT    /api/users/{id}
PATCH  /api/users/{id}
DELETE /api/users/{id}
```

REST **no usa verbos en las rutas**:

❌ `/api/createUser`
❌ `/api/deleteProduct`
✔ `/api/products/{id}`

---

# 4. Verbos HTTP y su semántica

| Verbo      | Propósito                           | Ejemplo               |
| ---------- | ----------------------------------- | --------------------- |
| **GET**    | Consultar información               | GET /api/users        |
| **POST**   | Crear un recurso                    | POST /api/products    |
| **PUT**    | Reemplazar completamente un recurso | PUT /api/users/10     |
| **PATCH**  | Actualizar parcialmente             | PATCH /api/users/10   |
| **DELETE** | Eliminar un recurso                 | DELETE /api/orders/20 |

---

# 5. Tipos de parámetros en REST

## 5.1 Parámetros de ruta (Path Variables)

Identifican un recurso específico:

```
GET /api/users/23
```

## 5.2 Parámetros de consulta (Query Params)

Usados para filtrar, ordenar o paginar:

```
GET /api/products?category=laptops&min_price=500
```

## 5.3 Cuerpo de la petición (Request Body)

Para datos complejos, se usa JSON:

```json
{
  "name": "Juan Pérez",
  "email": "juan@example.com"
}
```

---

# 6. Códigos de estado HTTP

La API REST debe responder con el código adecuado:

| Código                        | Significado             | Caso típico            |
| ----------------------------- | ----------------------- | ---------------------- |
| **200 OK**                    | Respuesta exitosa       | GET, PUT, PATCH        |
| **201 Created**               | Recurso creado          | POST                   |
| **204 No Content**            | Operación sin contenido | DELETE                 |
| **400 Bad Request**           | Datos inválidos         | Validaciones           |
| **401 Unauthorized**          | Falta autenticación     | Token ausente          |
| **403 Forbidden**             | Prohibido               | Permisos insuficientes |
| **404 Not Found**             | Recurso inexistente     | ID inválido            |
| **409 Conflict**              | Conflictos de negocio   | Duplicados             |
| **500 Internal Server Error** | Error inesperado        | Excepciones            |

---

# 7. Idempotencia

La idempotencia indica si una operación ejecutada varias veces produce el mismo resultado.

| Verbo  | Idempotente | Razón                                      |
| ------ | ----------- | ------------------------------------------ |
| GET    | Sí          | Solo consulta                              |
| PUT    | Sí          | Reemplaza completamente                    |
| DELETE | Sí          | Eliminar repetidamente no cambia resultado |
| PATCH  | Parcial     | Depende de implementación                  |
| POST   | ❌ No        | Crea múltiples recursos                    |

Es clave para reintentos, microservicios y clientes móviles.

---

# 8. Formato de las respuestas

El formato más común es **JSON**.

Ejemplo estándar:

```json
{
  "data": {
    "id": 23,
    "name": "Juan",
    "email": "juan@example.com"
  },
  "message": "Usuario encontrado",
  "timestamp": "2025-03-01T14:23:10Z",
  "path": "/api/users/23"
}
```

---

# 9. Paginación, ordenamiento y filtrado

APIs modernas deben soportar volumen alto de datos.

Ejemplo:

```
GET /api/products?page=1&limit=20&sort=price&order=asc&category=laptops
```

---

# 10. Versionado de APIs

Se utiliza cuando la API evoluciona.

Tipos:

### En la ruta:

```
/api/v1/users
/api/v2/users
```

### Por header:

```
Accept: application/vnd.ups.api-v2+json
```

---

# 11. Buenas prácticas para diseñar una API REST

✔ Usar plural en los recursos
✔ Usar sustantivos, no verbos
✔ Mantener rutas coherentes
✔ Utilizar códigos HTTP correctos
✔ No devolver contraseñas ni datos sensibles
✔ Separar responsabilidad (Controlador–Servicio–Repositorio)
✔ Documentar la API (Swagger / OpenAPI)
✔ Normalizar respuestas
✔ Validar entradas antes de procesar
✔ NO romper compatibilidad al actualizar versiones

---

# 12. Flujo completo de una petición REST

```
Cliente → HTTP Request
         ↓
Controlador
         ↓
Servicio (lógica de negocio)
         ↓
Repositorio (persistencia)
         ↓
Base de datos
         ↓
Servicio → Controlador → HTTP Response
```

Este flujo se implementará exactamente igual en Spring Boot y NestJS.

---

# Resultados Esperados

Al finalizar este tema se debe comprender:

* qué es una API REST
* qué son rutas, recursos y verbos HTTP
* cómo se estructuran peticiones y respuestas
* cómo se interpretan los códigos de estado
* qué implica el principio stateless
* cómo diseñar rutas correctas
* qué significa idempotencia
* cómo se versionan las APIs

Estos conceptos se aplicarán directamente en:

* [`spring-boot/02_estructura_proyecto.md`](../spring-boot/p67/a_dodente/03_api_rest.md)

* [`nest/02_estructura_proyecto.md`](../nest/p67/a_dodente/03_api_rest.md)

