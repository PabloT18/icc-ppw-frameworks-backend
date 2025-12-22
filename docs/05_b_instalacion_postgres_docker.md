# Programación y Plataformas Web

# Instalación de PostgreSQL mediante Docker y Configuración para Entornos de Desarrollo

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="100" alt="Docker Logo">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="100" alt="PostgreSQL Logo">
</div>

## Guía Complementaria 05-B: Instalación y configuración de PostgreSQL con Docker

### Autores

**Pablo Torres**

 📧 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

 💻 GitHub: PabloT18

---

# Introducción

A partir de la práctica 05, los proyectos Spring Boot y NestJS necesitan conectarse a una **base de datos real**.
PostgreSQL es el motor recomendado por su:

* rendimiento
* estabilidad
* soporte avanzado para tipos
* amplia adopción en la industria
* compatibilidad con Hibernate/JPA y TypeORM

En entornos de desarrollo, la forma más práctica y reproducible de ejecutar PostgreSQL es mediante **Docker**, evitando instalaciones manuales del motor en el sistema operativo.

Este documento explica:

* qué es un contenedor de base de datos
* cómo preparar una base PostgreSQL lista para Spring/Nest
* cómo crear y persistir datos mediante volúmenes
* cómo inspeccionar y administrar la base
* cómo preparar un ambiente estándar para todos los estudiantes

La configuración final funcionará tanto para:

* `spring-boot/05_repositorios_bd.md`
* `nest/05_repositorios_bd.md`


# 1. ¿Por qué usar Docker para PostgreSQL?

Ventajas principales:

### **1. Entorno limpio y reproducible**

No depende del sistema operativo. El mismo contenedor funciona igual en Windows, macOS y Linux.

### **2. Aislamiento**

El motor de base de datos no interfiere con instalaciones existentes.

### **3. Eliminación rápida**

Al finalizar un curso o proyecto, el contenedor puede eliminarse sin dejar rastros.

### **4. Volúmenes persistentes**

Los datos sobreviven aunque el contenedor se reinicie o se elimine.

### **5. Facilidad de creación**

Un solo archivo o comando levanta todo el ambiente.


# 2. Requisitos previos

* Docker Desktop instalado
  [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

* Conexión estable a Internet (solo para descargar la imagen inicial)

* Terminal habilitada (cmd, PowerShell, Bash, zsh, etc.)


# 3. Creación del volumen persistente

Para garantizar que los datos de PostgreSQL permanezcan disponibles aunque el contenedor se elimine, se utiliza un volumen.

Se crea el volumen:

```bash
docker volume create pgdata
```

Verificar que existe:

```bash
docker volume ls
```


# 4. Crear y ejecutar el contenedor PostgreSQL

Se levanta un contenedor PostgreSQL configurado para desarrollo local:

```bash
docker run -d \
  --name postgres-dev \
  -e POSTGRES_USER=ups \
  -e POSTGRES_PASSWORD=ups123 \
  -e POSTGRES_DB=devdb \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16
```

### Parámetros explicados:

| Parámetro                            | Descripción                             |
| ------------------------------------ | --------------------------------------- |
| `--name postgres-dev`                | Nombre del contenedor                   |
| `POSTGRES_USER`                      | Usuario administrador                   |
| `POSTGRES_PASSWORD`                  | Contraseña                              |
| `POSTGRES_DB`                        | Base inicial creada automáticamente     |
| `-p 5432:5432`                       | Expone el puerto para Spring/Nest       |
| `-v pgdata:/var/lib/postgresql/data` | Persistencia de datos                   |
| `postgres:16`                        | Imagen oficial de PostgreSQL versión 16 |


# 5. Verificar estado del servidor

Consultar contenedores en ejecución:

```bash
docker ps
```

La salida debe mostrar:

```
postgres-dev  ...   0.0.0.0:5432->5432/tcp
```


# 6. Acceder a PostgreSQL desde la terminal

Ejecutar la herramienta `psql` dentro del contenedor:

```bash
docker exec -it postgres-dev psql -U ups -d devdb
```

Dentro de `psql`, comandos útiles:

```sql
\dt         -- listar tablas
\du         -- listar usuarios
\q          -- salir
```


# 7. Conexión desde un cliente gráfico

Puede usarse:

* DBeaver
* TablePlus
* PgAdmin
* DataGrip

Parámetros para la conexión:

| Parámetro  | Valor     |
| ---------- | --------- |
| Host       | localhost |
| Puerto     | 5432      |
| Usuario    | ups       |
| Contraseña | ups123    |
| Base       | devdb     |


# 8. Reiniciar o detener el contenedor

Detener:

```bash
docker stop postgres-dev
```

Iniciar nuevamente:

```bash
docker start postgres-dev
```

Eliminar contenedor (los datos NO se pierden por estar en un volumen):

```bash
docker rm postgres-dev
```

Si se desea eliminar también los datos:

```bash
docker volume rm pgdata
```


# 9. Preparación para integración con Spring Boot y NestJS

Las aplicaciones backend deben utilizar estos parámetros:

### Conexión (valores estándar para desarrollo)

| Campo         | Valor     |
| ------------- | --------- |
| host          | localhost |
| puerto        | 5432      |
| usuario       | ups       |
| contraseña    | ups123    |
| base de datos | devdb     |

Estos parámetros se usarán en:

✔ `application.properties` (Spring Boot)
✔ `DataSourceOptions` de TypeORM (NestJS)

Además, los repositorios de ambos frameworks requieren:

* entidades persistentes (`@Entity`)
* adaptadores ORM (JPA / TypeORM)
* operaciones CRUD mapeadas a la base
* definiciones de relaciones (en temas posteriores)


# 10. Resultados esperados

Al finalizar este documento, el estudiante debe:

* comprender qué es un contenedor de base de datos
* crear un servidor PostgreSQL con datos persistentes
* inspeccionar y administrar el motor con Docker
* conectarse al motor mediante herramientas externas
* preparar el entorno para los próximos temas de integración con ORM

Este contenido sirve como prerequisito directo para:

* `spring-boot/05_repositorios_bd.md`
* `nest/05_repositorios_bd.md`
