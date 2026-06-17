
# Programación y Plataformas Web

# Frameworks Backend: Fundamentos del Backend

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg" width="80" alt="Node Logo">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="80" alt="Java Logo">
</div>

## 1: Conceptos Fundamentales del Backend

### Autores

**Pablo Torres**
📧 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)
💻 GitHub: [PabloT18](https://github.com/PabloT18)

---

# Introducción al Backend

El **backend** es la parte de una aplicación que se ejecuta en el servidor y se encarga de:

* procesar solicitudes
* ejecutar la lógica del negocio
* comunicarse con la base de datos
* enviar respuestas al cliente (generalmente JSON)

Mientras el frontend controla lo que el usuario ve, el backend controla **cómo funciona** la aplicación detrás de escena.



<img src="assets/01-conceptos-01.png" alt="alt text" style="max-width: 800px; display: block; margin: 0 auto; margin-bottom: 30px;">


---

## ¿Qué es un servidor?

Un servidor es un programa que:

1. **Recibe peticiones** desde el cliente (browser, app móvil, otro servidor)
2. **Procesa la solicitud**
3. **Devuelve una respuesta**

Ejemplo conceptual:

```
Cliente → (HTTP Request) → Servidor → Procesa → (HTTP Response) → Cliente
```

En backend trabajamos con servicios web que atienden miles de peticiones por segundo.

<!-- ![alt text](assets/01-conceptos-02.png) -->


<img src="assets/01-conceptos-02.png" alt="alt text" style="max-width: 800px; display: block; margin: 0 auto; margin-bottom: 30px;">


---

## Ciclo de vida de una petición HTTP

Cada vez que un cliente se comunica con el backend ocurre este flujo:

1. El cliente envía una **petición HTTP**
2. El servidor recibe la petición
3. Se ejecuta la lógica del negocio (servicios)
4. Se accede a la base de datos si es necesario
5. Se genera una respuesta
6. El servidor devuelve un **HTTP Response**

Ejemplo básico (vista en consola):

```http
GET /api/users HTTP/1.1
Host: localhost:3000
```

Respuesta:

```json
[
  { "id": 1, "name": "Ana" },
  { "id": 2, "name": "Luis" }
]
```




<img src="assets/01-conceptos-03.png" alt="alt text" style="max-width: 800px; display: block; margin: 0 auto; margin-bottom: 30px;">

---

## Backend vs Frontend

| Característica  | Frontend      | Backend                   |
| --------------- | ------------- | ------------------------- |
| Ejecuta en…     | Navegador     | Servidor                  |
| Lenguajes       | HTML, CSS, JS | Java, JS/TS, Python, etc. |
| Responsable de… | Interfaz (UI) | Lógica del negocio        |
| Comunicación    | Llama APIs    | Expone APIs               |
| Seguridad       | Menor         | Alta responsabilidad      |

---

## Concurrencia y Multihilo

Un servidor debe manejar **múltiples usuarios simultáneamente**.

## Dos formas comunes:

### Multihilo (Java, Spring Boot)

Cada petición puede ejecutarse en su propio hilo.
Ventajas: robustez, estabilidad.
Desventajas: requiere buena gestión de memoria.

<img src="assets/01-conceptos-04.png" alt="alt text" style="max-width: 500px;">

### Event Loop (Node/NestJS)

Modelo de un solo hilo con operaciones asincrónicas.
Ideal para miles de conexiones concurrentes.


<img src="assets/01-conceptos-05.png" alt="alt text" style="max-width: 500px;">


---

## HTTP en profundidad

El backend trabaja sobre el protocolo **HTTP(S)** (HyperText Transfer Protocol / Secure).

HTTP es el protocolo de comunicación que permite la transferencia de información en la web. Define cómo se estructuran y envían los mensajes entre cliente y servidor.

### Anatomía de una petición HTTP

Una petición HTTP completa tiene:

```http
POST /api/users HTTP/1.1
Host: localhost:3000
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "name": "Ana García",
  "email": "ana@example.com"
}
```

**Componentes:**
- **Método HTTP**: POST
- **Ruta (Path)**: /api/users
- **Headers**: Metadatos de la petición
- **Body**: Datos enviados (solo en POST, PUT, PATCH)



<img src="assets/01-conceptos-06.png" alt="alt text" style="max-width: 700px; display: block; margin: 0 auto; margin-bottom: 30px; margin-top: 30px;">
---

### Métodos HTTP (HTTP Verbs)

Los métodos HTTP definen la **acción** que queremos realizar sobre un recurso.


<img src="assets/01-conceptos-07.png" alt="alt text" style="max-width: 700px; display: block; margin: 0 auto; margin-bottom: 30px; margin-top: 30px;">


#### GET - Obtener/Consultar datos

**Propósito**: Recuperar información del servidor sin modificarla.

**Características**:
- No tiene body
- Los parámetros van en la URL (query params)
- Es **idempotente** (puede repetirse sin efectos secundarios)
- Debe ser **seguro** (no modifica datos)

**Ejemplos**:

```http
GET /api/users
GET /api/users/123
GET /api/products?category=electronics&price_max=500
GET /api/orders?status=pending&page=2
```

**Cuándo usar**: Para consultar listados, buscar información, obtener detalles de un recurso.

---

#### POST - Crear recursos

**Propósito**: Enviar datos al servidor para crear un nuevo recurso.

**Características**:
- Tiene body con los datos a crear
- **NO es idempotente** (ejecutarlo varias veces crea múltiples recursos)
- Retorna típicamente código **201 Created**

**Ejemplos**:

```http
POST /api/users
Content-Type: application/json

{
  "name": "Luis Pérez",
  "email": "luis@example.com",
  "password": "securePass123"
}
```

```http
POST /api/products
Content-Type: application/json

{
  "name": "Laptop HP",
  "price": 899.99,
  "stock": 15
}
```

**Cuándo usar**: Crear usuarios, productos, órdenes, posts, comentarios, etc.

---

#### PUT - Actualizar completo

**Propósito**: Reemplazar completamente un recurso existente.

**Características**:
- Requiere **todos los campos** del recurso
- Es **idempotente** (ejecutarlo varias veces da el mismo resultado)
- Si el recurso no existe, algunos sistemas lo crean (depende de la implementación)

**Ejemplo**:

```http
PUT /api/users/123
Content-Type: application/json

{
  "name": "Luis Pérez García",
  "email": "luis.nuevo@example.com",
  "password": "newPassword456",
  "age": 28,
  "city": "Quito"
}
```

**Cuándo usar**: Cuando necesitas reemplazar todo el recurso con nueva información.

---

#### PATCH - Actualizar parcial

**Propósito**: Modificar solo algunos campos de un recurso existente.

**Características**:
- Solo envías los campos que deseas cambiar
- Es **idempotente**
- Más eficiente que PUT cuando solo cambias pocos campos

**Ejemplo**:

```http
PATCH /api/users/123
Content-Type: application/json

{
  "email": "nuevo.email@example.com"
}
```

```http
PATCH /api/products/456
Content-Type: application/json

{
  "stock": 20,
  "price": 799.99
}
```

**Cuándo usar**: Actualizar solo algunos campos (email, precio, estado, etc.)

---

#### DELETE - Eliminar recursos

**Propósito**: Eliminar un recurso del servidor.

**Características**:
- Puede o no tener body
- Es **idempotente** (eliminarlo varias veces da el mismo resultado)
- Retorna típicamente **204 No Content** o **200 OK**

**Ejemplos**:

```http
DELETE /api/users/123
```

```http
DELETE /api/products/456
```

```http
DELETE /api/orders/789
Authorization: Bearer token123
```

**Cuándo usar**: Eliminar usuarios, productos, comentarios, órdenes canceladas.

---

#### Otros métodos HTTP menos comunes

| Método | Descripción | Uso |
|--------|-------------|-----|
| **HEAD** | Igual que GET pero solo devuelve headers (sin body) | Verificar existencia o metadatos |
| **OPTIONS** | Consulta qué métodos están permitidos en un endpoint | CORS, preflight requests |
| **CONNECT** | Establece un túnel hacia el servidor | Proxies, HTTPS |
| **TRACE** | Devuelve la petición tal como la recibe | Debugging (raramente usado) |


<img src="assets/01-conceptos-08.png" alt="alt text" style="max-width: 700px;">

---

### Códigos de Respuesta HTTP (Status Codes)

Los códigos HTTP indican el **resultado** de la operación.

#### **1xx - Informativos** (Respuestas provisionales)

| Código | Nombre | Significado |
|--------|--------|-------------|
| 100 | Continue | El cliente puede continuar con la petición |
| 101 | Switching Protocols | El servidor acepta cambiar de protocolo |

---

#### **2xx - Éxito** 

| Código | Nombre | Significado | Cuándo usar |
|--------|--------|-------------|-------------|
| **200** | OK | Petición exitosa | GET, PUT, PATCH exitosos |
| **201** | Created | Recurso creado exitosamente | POST exitoso |
| **202** | Accepted | Petición aceptada pero aún procesándose | Operaciones asíncronas |
| **204** | No Content | Éxito pero sin contenido para devolver | DELETE exitoso |

**Ejemplos**:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 123,
  "name": "Ana García",
  "email": "ana@example.com"
}
```

```http
HTTP/1.1 201 Created
Location: /api/users/124

{
  "id": 124,
  "name": "Usuario nuevo",
  "createdAt": "2024-03-15T10:30:00Z"
}
```

---

#### **3xx - Redirección**

| Código | Nombre | Significado |
|--------|--------|-------------|
| **301** | Moved Permanently | El recurso se movió permanentemente a otra URL |
| **302** | Found | Redirección temporal |
| **304** | Not Modified | El recurso no ha cambiado (cache) |

---

#### **4xx - Errores del Cliente**

Estos errores indican que **el cliente hizo algo mal**.

| Código | Nombre | Significado | Ejemplo |
|--------|--------|-------------|---------|
| **400** | Bad Request | Petición malformada o inválida | JSON mal formado, campos faltantes |
| **401** | Unauthorized | Falta autenticación | Token no enviado o inválido |
| **403** | Forbidden | No tiene permisos | Usuario autenticado pero sin acceso |
| **404** | Not Found | Recurso no encontrado | `/api/users/999` no existe |
| **405** | Method Not Allowed | Método no permitido en ese endpoint | DELETE en endpoint de solo lectura |
| **409** | Conflict | Conflicto con el estado actual | Email duplicado, recurso ya existe |
| **422** | Unprocessable Entity | Datos válidos pero no procesables | Validación de negocio falló |
| **429** | Too Many Requests | Demasiadas peticiones (rate limit) | Usuario excedió límite de peticiones |

**Ejemplos**:

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": "Bad Request",
  "message": "El campo 'email' es requerido",
  "statusCode": 400
}
```

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error": "Unauthorized",
  "message": "Token JWT inválido o expirado",
  "statusCode": 401
}
```

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": "Not Found",
  "message": "Usuario con ID 999 no encontrado",
  "statusCode": 404
}
```

---

#### **5xx - Errores del Servidor** 

Estos errores indican que **el servidor falló** al procesar una petición válida.

| Código | Nombre | Significado | Ejemplo |
|--------|--------|-------------|---------|
| **500** | Internal Server Error | Error genérico del servidor | Excepción no controlada |
| **501** | Not Implemented | Funcionalidad no implementada | Endpoint en desarrollo |
| **502** | Bad Gateway | Error en servidor intermediario | Proxy/Gateway falló |
| **503** | Service Unavailable | Servidor temporalmente no disponible | Mantenimiento, sobrecarga |
| **504** | Gateway Timeout | Timeout en servidor intermediario | Servidor tardó demasiado |

**Ejemplo**:

```http
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "error": "Internal Server Error",
  "message": "Error al conectar con la base de datos",
  "statusCode": 500
}
```

---

###  Recursos para explorar todos los códigos HTTP

**Lista completa de códigos de estado HTTP**:
- [MDN Web Docs - HTTP Status Codes](https://developer.mozilla.org/es/docs/Web/HTTP/Status)
- [HTTP Status Dogs](https://httpstatusdogs.com/) (versión divertida con perros)
- [HTTP Cats](https://http.cat/) (versión con gatos)
- [RFC 7231 - HTTP/1.1 Semantics](https://tools.ietf.org/html/rfc7231)


---

### Headers HTTP

Los headers son **metadatos** que acompañan la petición o respuesta.



<img src="assets/01-conceptos-09.png" alt="alt text" style="max-width: 700px; display: block; margin: 0 auto; margin-bottom: 30px; margin-top: 30px;">

#### Headers comunes de petición (Request):

| Header | Propósito | Ejemplo |
|--------|-----------|---------|
| `Content-Type` | Tipo de contenido enviado | `application/json` |
| `Authorization` | Credenciales de autenticación | `Bearer token123` |
| `Accept` | Tipos de respuesta aceptados | `application/json` |
| `User-Agent` | Información del cliente | `Mozilla/5.0...` |
| `Cookie` | Cookies del navegador | `sessionId=abc123` |

#### Headers comunes de respuesta (Response):

| Header | Propósito | Ejemplo |
|--------|-----------|---------|
| `Content-Type` | Tipo de contenido devuelto | `application/json` |
| `Set-Cookie` | Establecer cookies | `token=xyz; HttpOnly` |
| `Cache-Control` | Control de caché | `no-cache, no-store` |
| `Location` | URL del recurso creado | `/api/users/124` |
| `Access-Control-Allow-Origin` | CORS | `*` o `https://example.com` |

---

### Body de la petición y respuesta

El **body** contiene los datos principales de la comunicación.

**Formatos comunes**:

#### JSON (más usado en APIs REST):
```json
{
  "name": "Ana",
  "email": "ana@example.com",
  "age": 25
}
```

#### Form Data (formularios tradicionales):
```
name=Ana&email=ana@example.com&age=25
```

#### XML (menos común en APIs modernas):
```xml
<user>
  <name>Ana</name>
  <email>ana@example.com</email>
  <age>25</age>
</user>
```

---

## Estado (State) y Stateless

Los servidores modernos implementan arquitectura **sin estado (stateless)**:

* cada petición se procesa de manera independiente
* el servidor no recuerda peticiones anteriores
* uso de tokens (JWT) en lugar de sesiones tradicionales

Esto permite mayor escalabilidad.

---

## Ejemplo conceptual de un servidor

### Pseudocódigo:

```
al recibir petición:

  si ruta == "/saludo":
      devolver { mensaje: "Hola desde el servidor" }

  si ruta == "/hora":
      devolver { fecha: new Date() }

  si ruta no existe:
      devolver error 404
```

Esto es justo lo que frameworks como Spring Boot y NestJS automatizan.

---

## Herramientas típicas en backend

* **Controladores (Controllers)**
* **Servicios (Services)**
* **Repositorios (Repositories)**
* **DTOs (Data Transfer Objects)**
* **ORMs (JPA/Hibernate, TypeORM)**
* **JWT y Guardias de acceso**
* **Swagger/OpenAPI para documentación**

Estos conceptos se verán en profundidad en las siguientes prácticas.



<img src="assets/01-conceptos-10.png" alt="alt text" style="max-width: 700px; display: block; margin: 0 auto; margin-bottom: 30px; margin-top: 30px;">



# Práctica 

Al finalizar este tema, se debe comprender:

* cómo funciona un servidor
* qué es una petición y una respuesta
* la diferencia entre frontend y backend
* qué es la concurrencia
* cómo opera HTTP
* conceptos indispensables para construir APIs REST

Estos fundamentos se aplicarán en:


* [`spring-boot/01_configuracion.md`](../spring-boot/p67/a_dodente/01_configuracion.md)
* [`nest/01_configuracion.md`](../nest/p67/a_dodente/01_configuracion.md)


---

