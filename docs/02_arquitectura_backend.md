# Programación y Plataformas Web

# Frameworks Backend: Arquitectura Backend

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="80" alt="Java Logo">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="80" alt="TypeScript Logo">
</div>

## Arquitectura Backend

### Autor

**Pablo Torres**

[ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: [PabloT18](https://github.com/PabloT18)

---

# Introducción

La arquitectura backend define cómo se organiza internamente una aplicación del lado del servidor.

En una aplicación web moderna, el backend no se limita a recibir peticiones y devolver respuestas. También se encarga de organizar la lógica del negocio, comunicarse con bases de datos, validar información, proteger recursos, manejar errores, documentar servicios y preparar la aplicación para su despliegue.

Comprender la arquitectura backend es necesario antes de trabajar con frameworks como **Spring Boot** y **NestJS**, porque ambos promueven una organización basada en capas, controladores, servicios, modelos, DTOs, repositorios y módulos.

En este documento se estudian los conceptos principales que permiten entender cómo se estructura una aplicación backend.

---

# Objetivos

Al finalizar este tema, el estudiante será capaz de:

* Comprender qué es una API y cuál es su función dentro de una aplicación web.
* Identificar los elementos principales de una arquitectura backend.
* Diferenciar capas lógicas y responsabilidades dentro del servidor.
* Comprender el flujo de una petición desde el cliente hasta la base de datos.
* Reconocer patrones como MVC y MVCS.
* Diferenciar una arquitectura monolítica, modular y de microservicios.
* Relacionar los conceptos de arquitectura con Spring Boot y NestJS.

---

# 1. API

## 1.1 ¿Qué es una API?

Una **API** es un conjunto de reglas, endpoints y contratos que permiten que dos sistemas se comuniquen.

En desarrollo web, una API permite que el frontend, una aplicación móvil u otro sistema externo pueda solicitar información o ejecutar operaciones en el backend.

Ejemplo:

```txt
Frontend -> API Backend -> Base de Datos
```

Un frontend no debería acceder directamente a la base de datos. En su lugar, se comunica con el backend mediante una API.

---

## 1.2 API en una aplicación web

En una aplicación web, la API funciona como punto de entrada hacia la lógica del servidor.

Ejemplo:

```txt
Navegador
   |
   | HTTP Request
   v
API Backend
   |
   | Lógica de negocio
   v
Base de Datos
   |
   | Resultado
   v
API Backend
   |
   | HTTP Response
   v
Navegador
```

La API recibe solicitudes, procesa la información y devuelve una respuesta estructurada.

---

## 1.3 Endpoint

Un **endpoint** es una URL específica expuesta por el backend para realizar una operación.

Ejemplos:

```txt
GET    /users
GET    /users/1
POST   /users
PUT    /users/1
DELETE /users/1
```

Cada endpoint representa una acción disponible en la API.

---

## 1.4 Recurso

Un **recurso** representa una entidad o elemento del sistema que puede ser gestionado mediante la API.

Ejemplos de recursos:

```txt
/users
/products
/orders
/categories
```

En una API REST, los recursos normalmente se nombran con sustantivos en plural.

Ejemplo correcto:

```txt
GET /users
```

Ejemplo no recomendado:

```txt
GET /getUsers
```

La acción ya está representada por el verbo HTTP.

# 2. Arquitectura Backend

## 2.1 ¿Qué es la arquitectura backend?

La arquitectura backend es la forma en que se organiza internamente una aplicación del lado del servidor.

Define:

* cómo se reciben las peticiones;
* cómo se procesa la lógica;
* cómo se validan los datos;
* cómo se consulta la base de datos;
* cómo se manejan errores;
* cómo se devuelve una respuesta;
* cómo se separan responsabilidades.

Una buena arquitectura evita que todo el código esté mezclado en un solo archivo o en una sola clase.

---

## 2.2 Problema de una mala arquitectura

Una mala arquitectura ocurre cuando el backend mezcla responsabilidades.

Ejemplo no recomendado:

```txt
Controller
   - recibe la petición
   - valida datos
   - calcula reglas del negocio
   - consulta la base de datos
   - arma la respuesta
   - maneja errores
```

Esto genera problemas:

* código difícil de mantener;
* errores difíciles de corregir;
* duplicación de lógica;
* pruebas más complejas;
* dependencia fuerte entre partes del sistema;
* dificultad para escalar el proyecto.

---

# 3. Capas del Backend

## 3.1 Capa de presentación

En backend, la capa de presentación no se refiere a una interfaz gráfica. Se refiere a los puntos de entrada de la aplicación.

En esta capa se ubican:

* controladores;
* DTOs;
* rutas;
* endpoints;
* handlers.

Responsabilidades:

* recibir la petición HTTP;
* extraer parámetros;
* recibir el body;
* recibir headers;
* llamar al servicio correspondiente;
* devolver una respuesta.

No debería contener:

* lógica de negocio;
* consultas directas a la base de datos;
* reglas complejas;
* validaciones profundas de negocio.

Ejemplo conceptual:

```txt
HTTP Request -> DTO -> Controller -> Service

o

Service -> ResponseDTO -> Controller -> Response JSON
```

En Spring Boot:

```java
@RestController
@RequestMapping("/users")
public class UserController {
}
```

En NestJS:

```ts
@Controller('users')
export class UsersController {
}
```

---

## 3.2 Capa de negocio

La capa de negocio contiene las reglas principales de la aplicación.

En esta capa se ubican los servicios.

Responsabilidades:

* validar reglas de negocio;
* coordinar operaciones;
* ejecutar cálculos;
* aplicar condiciones;
* controlar flujos;
* llamar a repositorios;
* preparar resultados.

Ejemplo:

```txt
Crear usuario:
1. Verificar que el correo no exista.
2. Validar datos obligatorios.
3. Encriptar contraseña.
4. Guardar usuario.
5. Devolver respuesta.
```

En Spring Boot:

```java
@Service
public class UserService {
}
```

En NestJS:

```ts
@Injectable()
export class UsersService {
}
```

---

## 3.3 Capa de persistencia (Datos)

Responsabilidad: Manejar toda la comunicación con sistemas de almacenamiento (bases de datos, cache, archivos).

Implementada mediante:

- Repositorios: Interfaces para acceder a datos
- ORM (Object-Relational Mapping): Mapea objetos a tablas
- Entidades: Representan tablas de la base de datos

Conceptos clave:

- Abstrae los detalles de persistencia
- Facilita cambio de base de datos
- Proporciona métodos CRUD estándar
- Puede incluir `queries` personalizadas

Ejemplo conceptual:

```txt
Service -> Repository -> Database
```

En Spring Boot:

```java
public interface UserRepository extends JpaRepository<User, Long> {
}
```

En NestJS con TypeORM:

```ts
@Injectable()
export class UsersRepository {
}
```

### ORM

Un ORM permite convertir objetos del lenguaje de programación en registros de una base de datos relacional.

Ejemplo:

UserEntity
↓

Tabla users

Ventajas:

- Menos SQL manual.
- Portabilidad.
- Productividad.

Ejemplos:

- Hibernate (Spring Boot)
- TypeORM (NestJS)

---


## 3.4  Relacion entre capas

Flujo general de una petición:

```txt
1. Cliente envía petición HTTP
        ↓
2. [Capa de Presentación]
   - Controlador recibe la petición
   - Valida parámetros básicos
   - Extrae datos del request
        ↓
3. [Capa de Negocio]
   - Servicio aplica lógica de negocio
   - Valida reglas complejas
   - Orquesta operaciones
        ↓
4. [Capa de Persistencia]
   - Repositorio accede a la BD
   - ORM ejecuta queries SQL
   - Retorna entidades
        ↓
5. Base de Datos
   - Ejecuta operación
   - Retorna resultados
        ↓
6. Respuesta fluye de vuelta
   Repositorio → Servicio → Controlador → Cliente
```

Ejemplo aplicado:

```txt
GET /api/orders/123

┌──────────────────────────────────────────┐
│ Controlador (OrderController)            │
│ - Recibe petición                        │
│ - Extrae ID = 123                        │
└─────────────┬────────────────────────────┘
              ↓ orderService.findById(123)
┌──────────────────────────────────────────┐
│ Servicio (OrderService)                  │
│ - Valida que ID > 0                      │
│ - Verifica permisos del usuario          │
└─────────────┬────────────────────────────┘
              ↓ orderRepository.findById(123)
┌──────────────────────────────────────────┐
│ Repositorio (OrderRepository)            │
│ - Genera query SQL                       │
│ - SELECT * FROM orders WHERE id = 123    │
└─────────────┬────────────────────────────┘
              ↓
┌──────────────────────────────────────────┐
│ Base de Datos (PostgreSQL/MySQL)         │
│ - Ejecuta query                          │
│ - Retorna fila                           │
└─────────────┬────────────────────────────┘
              ↓ Entidad Order
┌──────────────────────────────────────────┐
│ Respuesta: HTTP 200                      │
│ {                                        │
│   "id": 123,                             │
│   "total": 99.99,                        │
│   "status": "pending"                    │
│ }                                        │
└──────────────────────────────────────────┘
```

---
## 3.5 Patrones de diseño MVC y MVCS

### MVC (Model-View-Controller)

Aunque más usado en frontend, en backend funciona como:

* **Modelo** → Datos y entidades
* **Vista** → Respuesta enviada (normalmente JSON)
* **Controlador** → Maneja rutas


### MVCS (Model-View-Controller-Service)

Este es el modelo más usado en backend moderno.

* Los **servicios** contienen la lógica del negocio.
* El controlador se encarga solamente de recibir peticiones.
* Limpio, modular y escalable.

## 3.6 Relación entre capas con MVCS

```txt
┌───────────────────────────────────────────────┐
│                CAPA DE PRESENTACIÓN           │
│                                               │
│  ┌───────────────┐     ┌───────────────────┐  │
│  │ Controller (C)│ ──▶ │ DTO Request (V)   │  │
│  └───────────────┘     └───────────────────┘  │
│            │                                  │
│            ▼                                  │
│       JSON Response (V)                       │
└───────────────┬───────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────┐
│                CAPA DE NEGOCIO                │
│                                               │
│  ┌─────────────────────────────────────────┐  │
│  │ Service / ServiceImpl (S)               │  │
│  │                                         │  │
│  │  - Lógica de negocio                    │  │
│  │  - Validaciones de negocio              │  │
│  │  - Orquestación de flujos               │  │
│  │  - Uso de Mappers y Validators          │  │
│  └─────────────────────────────────────────┘  │
│         ▲                 ▲                   │
│         │                 │                   │
│    Mappers (S)       Validators (S)           │
└───────────────┬───────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────┐
│              CAPA DE DOMINIO                  │
│                                               │
│  ┌─────────────────────────────────────────┐  │
│  │ Model (M)                               │  │
│  │                                         │  │
│  │  - Conceptos del dominio                │  │
│  │  - No depende de BD                     │  │
│  │  - No depende de frameworks             │  │
│  └─────────────────────────────────────────┘  │
└───────────────┬───────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────┐
│            CAPA DE PERSISTENCIA               │
│                                               │
│  ┌─────────────────────────────────────────┐  │
│  │ Repository                              │  │
│  └─────────────────────────────────────────┘  │
│                │                              │
│                ▼                              │
│  ┌─────────────────────────────────────────┐  │
│  │ Entity (@Entity) (M)                    │  │
│  │                                         │  │
│  │  - Representa tablas                    │  │
│  │  - Depende de JPA / ORM                 │  │
│  └─────────────────────────────────────────┘  │
└───────────────────────────────────────────────┘

┌───────────────────────────────────────────────┐
│            CAPA TRANSVERSAL                   │
│                                               │
│  Utils                                        │
│  - Fechas                                     │
│  - Strings                                    │
│  - Cálculos reutilizables                     │
└───────────────────────────────────────────────┘
``` 

![alt text](assets/01_arquitectura_backend-02.png)


# 4. DTOs

## 4.1 ¿Qué es un DTO?

DTO significa **Data Transfer Object**.

Un DTO define la estructura de los datos que entran o salen de la API.

Se usa para evitar que el backend reciba o devuelva datos sin control.

Ejemplo:

```json
{
  "name": "Juan",
  "email": "juan@example.com",
  "password": "123456"
}
```

Ese JSON puede representarse mediante un DTO.

---

## 4.2 DTO de entrada

Un DTO de entrada define qué datos acepta el backend.

Ejemplo conceptual:

```txt
CreateUserDto
  - name
  - email
  - password
```

En NestJS:

```ts
export class CreateUserDto {
  name: string;
  email: string;
  password: string;
}
```

En Spring Boot:

```java
public class CreateUserDto {
    private String name;
    private String email;
    private String password;
}
```

---

## 4.3 DTO de salida

Un DTO de salida define qué datos devuelve el backend.

Ejemplo:

```txt
UserResponseDto
  - id
  - name
  - email
```

No debería devolver datos sensibles como:

```txt
password
passwordHash
tokens internos
```

---

# 5. Arquitectura monolítica

Una arquitectura monolítica organiza toda la aplicación en un solo proyecto desplegable.

Ejemplo:

```txt
backend-app
  |
  |-- usuarios
  |-- productos
  |-- pedidos
  |-- pagos
```

Todo se compila, ejecuta y despliega como una sola aplicación.

---

## Ventajas del monolito

* Es más simple de desarrollar al inicio.
* Tiene menor complejidad operativa.
* Es más fácil de probar localmente.
* No requiere comunicación entre múltiples servicios.
* Es adecuado para proyectos pequeños o medianos.

---

## Desventajas del monolito

* Puede crecer demasiado.
* Puede volverse difícil de mantener.
* Un error puede afectar toda la aplicación.
* El despliegue afecta a todo el sistema.
* Escalar una sola parte del sistema es más complejo.

---

## Monolito modular

Un monolito modular sigue siendo una sola aplicación, pero organizada internamente por módulos.

Ejemplo:

```txt
backend-app
  |
  |-- users
  |    |-- controller
  |    |-- service
  |    |-- repository
  |
  |-- products
  |    |-- controller
  |    |-- service
  |    |-- repository
  |
  |-- orders
       |-- controller
       |-- service
       |-- repository
```

Este enfoque es recomendable para muchos proyectos académicos y profesionales porque mantiene una estructura clara sin aumentar demasiado la complejidad.

---

### Ventajas del monolito modular

* Organiza mejor el código.
* Facilita el mantenimiento.
* Permite separar funcionalidades.
* Reduce el acoplamiento interno.
* Puede evolucionar posteriormente hacia microservicios.

---

# 6. Microservicios

Los microservicios dividen una aplicación en varios servicios pequeños e independientes.

Ejemplo:

```txt
users-service
products-service
orders-service
payments-service
notifications-service
```

Cada servicio puede tener:

* su propio código;
* su propia base de datos;
* su propio despliegue;
* su propio equipo de desarrollo.

---

## Ventajas de los microservicios

* Escalabilidad por servicio.
* Independencia de despliegue.
* Separación clara de responsabilidades.
* Posibilidad de usar diferentes tecnologías.
* Mayor flexibilidad para sistemas grandes.

---

## Desventajas de los microservicios

* Mayor complejidad operativa.
* Requiere comunicación entre servicios.
* Aumenta el riesgo de fallos distribuidos.
* Requiere monitoreo, logs y trazabilidad.
* Puede generar problemas de consistencia de datos.

---

## Comparación Monolito vs Microservicios

| Criterio             | Monolito               | Monolito modular   | Microservicios   |
| -------------------- | ---------------------- | ------------------ | ---------------- |
| Complejidad inicial  | Baja                   | Media              | Alta             |
| Organización interna | Limitada               | Alta               | Alta             |
| Despliegue           | Uno solo               | Uno solo           | Múltiple         |
| Escalabilidad        | Global                 | Global             | Por servicio     |
| Mantenimiento        | Difícil si crece mucho | Más ordenado       | Complejo         |
| Uso recomendado      | Proyectos pequeños     | Proyectos medianos | Sistemas grandes |

---

# 7. Estilos de comunicación backend

## 7.1 REST

REST es uno de los estilos más usados para construir APIs web.

**Características principales**:
-  **Stateless**: Cada petición es independiente
-  **Basado en recursos**: URLs representan entidades
-  **Usa verbos HTTP**: GET, POST, PUT, DELETE, PATCH
-  **Respuestas en JSON o XML**
-  **Cacheable**: Soporta caché HTTP
-  **Cliente-Servidor**: Separación clara de responsabilidades

Ejemplo:

```txt
GET /products
POST /products
GET /products/10
DELETE /products/10
```

---

## 7.2 RPC

RPC significa **Remote Procedure Call**.

### Definición

RPC permite **invocar funciones remotas** como si fueran locales. El cliente llama a procedimientos que se ejecutan en el servidor.

**Características**:
-  Centrado en **acciones/funciones** (no en recursos)
-  Más simple que REST en algunos casos
-  Puede usar diferentes protocolos (HTTP, TCP)



** Cuándo usar RPC**:
- Comunicación entre microservicios internos
- Cuando las operaciones no mapean bien a recursos
- Sistemas de alto rendimiento


En RPC, el cliente llama una función remota como si fuera local.

Ejemplo:

```txt
POST /calculateTotal
POST /createInvoice
POST /sendEmail
```

A diferencia de REST, RPC suele centrarse más en acciones que en recursos.

---

## 7.3 gRPC

gRPC es un estilo de comunicación de alto rendimiento usado en sistemas distribuidos.

Características:

- **HTTP/2**: Multiplexación, compresión
- **Protocol Buffers**: Serialización binaria eficiente
- **Tipado fuerte**: Schemas definidos en `.proto`

**Características**:
-  Muy rápido (10x más rápido que REST)
-  Menor uso de ancho de banda
-  Streaming bidireccional
-  Generación automática de código cliente/servidor
-  Ideal para microservicios

---

## 7.4 WebSockets
**WebSocket** establece una **conexión persistente y bidireccional** entre cliente y servidor, permitiendo comunicación en tiempo real.

**Características**:
-  Conexión permanente (no request/response)
-  Comunicación bidireccional (cliente ↔ servidor)
-  Baja latencia
-  Ideal para tiempo real

**Flujo de WebSocket**:
```
Cliente                         Servidor
   |                               |
   |---- Handshake HTTP ---------->|
   |<--- Upgrade to WebSocket -----|
   |                               |
   |===== Conexión persistente ====|
   |                               |
   |---- sendMessage ------------->|
   |<--- newMessage ---------------|
   |<--- userJoined ---------------|
   |---- typing ------------------>|
   |<--- notification -------------|
   |                               |
   |===== Permanece abierta ======|
```

** Cuándo usar WebSockets**:
- **Chat en tiempo real**
- **Notificaciones push**
- **Juegos multiplayer**
- **Dashboards en vivo**
- **Colaboración en tiempo real** (Google Docs)
- **Trading/Bolsa** (precios actualizados)

---

## 7.5 GraphQL

GraphQL permite que el cliente solicite exactamente los datos que necesita.

Ejemplo:

```graphql
query {
  user(id: 1) {
    name
    email
  }
}
```

A diferencia de REST, no se trabaja necesariamente con muchos endpoints, sino con un esquema de consultas.

---

# 8. Concurrencia en backend



La concurrencia es la capacidad del backend para atender varias solicitudes en un mismo periodo de tiempo.

Ejemplo:

```txt
Usuario 1 -> GET /products
Usuario 2 -> POST /login
Usuario 3 -> GET /orders
Usuario 4 -> POST /payments
```

El servidor debe poder procesar múltiples solicitudes sin bloquear completamente la aplicación.

---

## 8.1 Concurrencia en Spring Boot

Spring Boot trabaja tradicionalmente con un modelo basado en hilos.

Cada petición puede ser atendida por un hilo del servidor.

Ejemplo conceptual:

```txt
Request 1 -> Thread 1
Request 2 -> Thread 2
Request 3 -> Thread 3
```

Este modelo es común en aplicaciones Java con servidores como Tomcat.

---

## 8.2 Concurrencia en NestJS

NestJS se ejecuta sobre Node.js.

Node.js usa un modelo basado en event loop y operaciones asíncronas.

Ejemplo conceptual:

```txt
Request -> Event Loop -> Operación asíncrona -> Response
```

Este modelo es eficiente para operaciones de entrada y salida, como consultas a bases de datos, archivos o servicios externos.

---



# 9. Relación con Spring Boot y NestJS

## 9.1 Spring Boot

Spring Boot organiza una aplicación backend usando componentes como:

```txt
Controller
Service
Repository
Entity
DTO
Configuration
```

Estructura típica:

```txt
src/main/java/com/example/app
  |
  |-- controllers
  |-- services
  |-- repositories
  |-- entities
  |-- dto
  |-- config
```

Flujo común:

```txt
Controller -> Service -> Repository -> Database
```

---

## 9.2 NestJS

NestJS organiza una aplicación backend mediante módulos.

Estructura típica:

```txt
src/
  |
  |-- users/
  |    |-- users.controller.ts
  |    |-- users.service.ts
  |    |-- users.module.ts
  |    |-- dto/
  |    |-- entities/
  |
  |-- app.module.ts
```

Flujo común:

```txt
Controller -> Service -> Repository/Provider -> Database
```

---

## 9.3 Comparación estructural

| Concepto                  | Spring Boot              | NestJS                                    |
| ------------------------- | ------------------------ | ----------------------------------------- |
| Controlador               | `@RestController`        | `@Controller()`                           |
| Servicio                  | `@Service`               | `@Injectable()`                           |
| Repositorio               | `JpaRepository`          | Repository, Provider o TypeORM Repository |
| DTO                       | Clase Java               | Clase TypeScript                          |
| Módulo                    | Paquetes o configuración | `@Module()`                               |
| Inyección de dependencias | Spring Container         | Nest IoC Container                        |

---


# 10. Buenas prácticas de arquitectura backend

Una arquitectura backend debe procurar:

* Separar responsabilidades.
* Evitar lógica de negocio en controladores.
* Usar servicios para reglas de negocio.
* Usar repositorios para acceso a datos.
* Validar datos de entrada.
* Devolver respuestas consistentes.
* Manejar errores de forma centralizada.
* Evitar exponer datos sensibles.
* Documentar los endpoints.
* Organizar el código por módulos o dominios.
* Usar variables de entorno para configuración.
* Mantener nombres claros y consistentes.

---

# 11. Errores comunes

## 11.1 Controladores con demasiada lógica

Problema:

```txt
Controller con validaciones, cálculos, consultas y reglas de negocio.
```

Corrección:

```txt
Mover la lógica al Service.
```

---

## 11.2 Acceso directo a la base de datos desde el controlador

Problema:

```txt
Controller -> Database
```

Corrección:

```txt
Controller -> Service -> Repository -> Database
```

---

## 11.3 Respuestas inconsistentes

Problema:

```json
{
  "error": "falló"
}
```

En otro endpoint:

```json
{
  "message": "No encontrado",
  "code": 404
}
```

Corrección:

```json
{
  "statusCode": 404,
  "message": "Usuario no encontrado",
  "path": "/users/1"
}
```

---

## 11.4 Entidades expuestas directamente

Problema:

```txt
Devolver toda la entidad de base de datos al cliente.
```

Corrección:

```txt
Usar DTOs de respuesta.
```

---

# 12. Actividad de análisis

Analizar la siguiente situación:

Una aplicación tiene un único archivo llamado `server.js` o una única clase llamada `UserController`.

En ese archivo se realiza lo siguiente:

* se reciben las peticiones.
* se validan datos.
* se consulta la base de datos.
* se calcula el precio de una orden.
* se actualiza el stock.
* se envían correos.
* se devuelven respuestas.

Responder:

1. ¿Qué problemas arquitectónicos existen?
2. ¿Qué responsabilidades están mezcladas?
3. ¿Qué capas deberían separarse?
4. ¿Qué elementos deberían moverse a un servicio?
5. ¿Qué elementos deberían moverse a un repositorio?
6. ¿Cómo quedaría el flujo corregido?

---


Estos conceptos se aplicarán directamente en:


* [`spring-boot/02_estructura_proyecto.md`](../spring-boot/p67/a_dodente/02_estructura_proyecto.md)

* [`nest/02_estructura_proyecto.md`](../nest/p67/a_dodente/02_estructura_proyecto.md)