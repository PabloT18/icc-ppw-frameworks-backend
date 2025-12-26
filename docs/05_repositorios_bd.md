# Programación y Plataformas Web

# Frameworks Backend: Entidades, Repositorios y Persistencia de Datos

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="80" alt="Java Logo">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="80" alt="TS Logo">
</div>

## Práctica 5: Persistencia de Datos – Entidades, Repositorios y Conexión a Base de Datos

### Autores

**Pablo Torres**

 📧 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

 💻 GitHub: PabloT18

---

# Introducción

Hasta el tema anterior (04), el backend funcionaba con:

* controladores
* servicios
* modelos
* DTOs
* mappers
* almacenamiento temporal en memoria (`List<>` en Spring, arrays en Nest)

Ese enfoque es útil para aprender la arquitectura, pero no permite:

* persistir datos
* consultar información real
* manejar concurrencia
* escalar aplicaciones
* ejecutar consultas complejas
* integrar sistemas con datos duraderos

En este tema se introducen los fundamentos de **persistencia con base de datos**, explicando:

* qué es una entidad persistente
* qué es un repositorio
* qué es un ORM (JPA / TypeORM)
* cómo fluye una solicitud desde servicio hasta la base de datos
* cómo se estructura la capa de persistencia
* por qué los servicios ya no deben manejar listas en memoria

Los detalles prácticos (PostgreSQL, configuración, anotaciones reales, migraciones y repositorios funcionales) se desarrollarán en:

📌 `spring-boot/05_repositorios_bd.md`
📌 `nest/05_repositorios_bd.md`
📌 `05_b_instalacion_postgres_docker.md`

Este documento se concentra en la **teoría universal de persistencia**, aplicable a cualquier framework o lenguaje.


# 1. ¿Qué significa persistencia?

Persistir datos significa **almacenarlos de manera permanente** en un sistema que no se pierde cuando la aplicación se reinicia.
Ejemplos:

* PostgreSQL
* MySQL
* SQLite
* SQL Server
* MongoDB
* Redis (según modo)

Un backend profesional no puede depender de:

* listas en memoria
* arreglos locales
* estructuras que desaparecen al cerrar el servidor

Porque se perdería:

* información de usuarios
* órdenes
* productos
* sesiones
* inventarios

Por eso es necesario incluir una **base de datos real**.


# 2. Entidades Persistentes

Una **entidad persistente** representa una tabla en la base de datos.
Es diferente de un **modelo de dominio** y también diferente de un **DTO**.

Comparación conceptual:

| Elemento                | Propósito                                                      |
| ----------------------- | -------------------------------------------------------------- |
| **DTO**                 | Datos que entran y salen de la API                             |
| **Modelo (Dominio)**    | Representa un concepto del negocio sin saber dónde se almacena |
| **Entidad Persistente** | Representa una tabla en la base de datos                       |
| **Mapper**              | Convierte entre DTO ↔ Modelo ↔ Entidad                         |

### Ejemplo conceptual de Entidad:

```
Tabla: users
Columnas: id, name, email, password, created_at
```

Una entidad tiene:

* atributos persistentes
* un identificador único (id)
* valores compatibles con columnas reales
* metadatos para mapearla mediante un ORM

Más adelante, en Spring Boot se usarán anotaciones como:

```
@Entity
@Table(name="users")
```

Y en NestJS / TypeORM:

```
@Entity('users')
```

Pero esas implementaciones prácticas corresponden al tema 05 del framework.


# 3. Repositorios

Un **repositorio** es la capa que administra cómo la aplicación accede a la base de datos.

Responsabilidades del repositorio:

* guardar entidades
* actualizar entidades
* eliminar entidades
* buscar entidades por diferentes criterios
* ejecutar queries personalizadas
* abstraer la base de datos del resto del sistema

Usar repositorios evita que los servicios escriban consultas SQL manualmente.


# 4. ¿Qué es un ORM?

ORM significa **Object–Relational Mapping**.

Es una herramienta que convierte automáticamente:

```
Objetos Java/TypeScript  ↔  Filas en tablas SQL
```

Permite:

* definir entidades como clases
* mapear atributos a columnas
* ejecutar CRUD sin escribir SQL directamente
* mantener independencia respecto al motor de BD
* manejar migraciones
* aplicar validaciones y relaciones

ORMs que se utilizarán:

* **Spring Boot → JPA + Hibernate**
* **NestJS → TypeORM**


# 5. Flujo interno usando repositorios reales

Cuando se integra una base de datos, el flujo del backend se vuelve:

```
Cliente
  ↓
Controlador  (recibe DTO)
  ↓
Servicio  (reglas de negocio)
  ↓
Repositorio  (operaciones CRUD)
  ↓
ORM  (traduce comandos a SQL)
  ↓
Base de Datos (almacena entidades)
  ↓
Servicio
  ↓
Controlador
  ↓
Cliente
```

Este ciclo garantiza:

* persistencia real
* consultas eficientes
* operaciones transaccionales
* validación automática
* independencia del motor SQL


# 6. Transición desde listas en memoria hacia repositorios

Antes:

```
List<User> users = new ArrayList<>();
users.add(new User(...));
```

Problemas:

* se borra al reiniciar la app
* no escala
* no permite consultas complejas
* no sirve en producción
* no permite concurrencia

Después:

```
userRepository.save(entity);
```

Ventajas:

* datos persistentes
* consultas optimizadas por BD
* manejo transaccional
* relaciones entre tablas
* escalabilidad real


# 7. Consultas comunes en repositorios

CRUD típico:

* findAll()
* findById(id)
* save(entity)
* delete(entity)

Consultas personalizadas:

* findByEmail(email)
* findByNameContaining(text)
* findByPriceBetween(min, max)

El ORM genera el SQL automáticamente.


# 8. Entidades, DTOs y Mappers trabajando juntos

Conceptualmente:

```
DTO (entrada)
   ↓
Servicio
   ↓ crea →
Entidad Persistente
   ↓ guarda →
Repositorio → Base de datos
   ↓ obtiene →
Entidad Persistente
   ↓ mapea →
DTO (salida)
```

Este flujo garantiza seguridad:

* No se exponen contraseñas
* No se exponen atributos internos
* El formato de la API es independiente de la BD


# 9. Preparación para la configuración real

En el siguiente tema (05 de cada framework) se configurará:

### Spring Boot

* dependencia `spring-boot-starter-data-jpa`
* configuración en `application.properties`
* repositorio `JpaRepository`
* entidades con anotaciones JPA
* pruebas de CRUD real con PostgreSQL

### NestJS

* instalación de `@nestjs/typeorm`
* configuración de conexión
* entidades TypeORM
* repositorios inyectables
* CRUD funcionando conectado a BD

Antes de eso, cada estudiante debe comprender esta arquitectura conceptual.


# Resultados Esperados

Al finalizar este tema, el estudiante comprende:

* qué es una entidad persistente
* qué es un repositorio
* qué es un ORM
* cómo fluye una petición hasta la base de datos
* por qué los servicios deben dejar de usar listas en memoria
* cómo se integrarán las bases de datos en los siguientes módulos
* cómo se relacionan DTO → Servicio → Repositorio → BD

Estos conceptos se aplicarán directamente en:

* [`spring-boot/05_repositorios_bd.md`](../spring-boot/p67/a_dodente/05_repositorios_bd.md)
* [`nest/05_repositorios_bd.md`](../nest/p67/a_dodente/05_repositorios_bd.md)
* [`Docker-Postgres`](../docs/05_b_instalacion_postgres_docker.md)

