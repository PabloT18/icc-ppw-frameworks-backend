# Frameworks Backend

## Manual de Trabajo en GitHub

![Logo UPS](.core/assets/ups-icc.png)

**Asignatura:** Programación y Plataformas Web
**Tema:** Frameworks Backend
**Frameworks:** Spring Boot y NestJS
**Autor del material:** Pablo Torres

---

## Descripción general del proyecto

Este repositorio contiene material conceptual y guías prácticas para el estudio de frameworks backend modernos dentro de la asignatura Programación y Plataformas Web.

El repositorio está organizado en tres bloques principales:

1. `/docs`: material teórico y conceptos universales del backend.
2. `/spring`: prácticas guiadas usando Spring Boot.
3. `/nest`: prácticas guiadas usando NestJS.

La lógica de trabajo es la siguiente:

1. Estudiar primero el concepto en la carpeta `/docs`.
2. Revisar la práctica correspondiente en `/spring` o `/nest`.
3. Implementar la práctica en un proyecto backend propio.
4. Registrar evidencias, commits y avances en el repositorio personal del estudiante.

Este repositorio funciona como material base de consulta y guía. No es un repositorio para que cada estudiante edite carpetas individuales dentro de él.

---

## Tecnologías principales

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg" width="100" alt="Spring Boot Logo">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nestjs/nestjs-original.svg" width="100" alt="NestJS Logo">
</div>

---

## Objetivo del repositorio

El objetivo de este repositorio es servir como guía técnica para que los estudiantes puedan:

* comprender los conceptos fundamentales del backend;
* construir APIs REST;
* aplicar arquitectura por capas;
* trabajar con controladores, servicios, modelos, DTOs y repositorios;
* conectar aplicaciones backend con bases de datos;
* implementar validaciones y manejo de errores;
* aplicar autenticación y autorización;
* documentar APIs con OpenAPI o Swagger;
* realizar pruebas y preparar despliegues;
* mantener buenas prácticas de Git y GitHub.

---

## Estructura del repositorio

```txt
/
├── docs/
│   ├── 01_conceptos_backend.md
│   ├── 02_arquitectura_backend.md
│   ├── 03_api_rest_conceptos.md
│   ├── 04_controladores_servicios.md
│   ├── 05_repositorios_bd.md
│   ├── 06_modelos_dtos_validacion.md
│   ├── 07_control_errores.md
│   ├── 08_relacion_entidades.md
│   ├── 09_relacion_requestparam.md
│   ├── 10_paginacion.md
│   ├── 11_autenticacion_autorizacion.md
│   ├── 12_roles_autorizacion.md
│   ├── 13_ownership_validacion.md
│   └── 14_despliegue_backend.md
│
├── spring/
│   ├── 01-instalacion-configuracion/
│   ├── 02-estructura-proyecto/
│   ├── 03-api-rest-controladores/
│   ├── 04-servicios-inyeccion-dependencias/
│   ├── 05-persistencia-repositorios/
│   ├── 06-modelos-dtos-validacion/
│   ├── 07-manejo-errores/
│   ├── 08-relaciones-entidades/
│   ├── 09-paginacion-filtros/
│   ├── 10-autenticacion-jwt/
│   ├── 11-roles-autorizacion/
│   ├── 12-documentacion-openapi/
│   ├── 13-testing/
│   └── 14-despliegue/
│
├── nest/
│   ├── 01-instalacion-configuracion/
│   ├── 02-estructura-proyecto/
│   ├── 03-api-rest-controladores/
│   ├── 04-servicios-inyeccion-dependencias/
│   ├── 05-persistencia-repositorios/
│   ├── 06-modelos-dtos-validacion/
│   ├── 07-manejo-errores/
│   ├── 08-relaciones-entidades/
│   ├── 09-paginacion-filtros/
│   ├── 10-autenticacion-jwt/
│   ├── 11-roles-autorizacion/
│   ├── 12-documentacion-openapi/
│   ├── 13-testing/
│   └── 14-despliegue/
│
└── README.md
```

---

## Índice de conceptos generales

| Nº | Tema                          | Descripción                                                     | Archivo                                                                            |
| -- | ----------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| 01 | Conceptos Backend             | Servidor, cliente, HTTP, request, response, backend vs frontend | [`docs/01_conceptos_backend.md`](./docs/01_conceptos_backend.md)                   |
| 02 | Arquitectura Backend          | Capas, MVC, monolito, microservicios, arquitectura modular      | [`docs/02_arquitectura_backend.md`](./docs/02_arquitectura_backend.md)             |
| 03 | API REST                      | Recursos, verbos HTTP, status codes, idempotencia               | [`docs/03_api_rest_conceptos.md`](./docs/03_api_rest_conceptos.md)                 |
| 04 | Controladores y Servicios     | Separación de responsabilidades y flujo de petición             | [`docs/04_controladores_servicios.md`](./docs/04_controladores_servicios.md)       |
| 05 | Repositorios y Base de Datos  | Persistencia, ORM, consultas y repositorios                     | [`docs/05_repositorios_bd.md`](./docs/05_repositorios_bd.md)                       |
| 06 | Modelos, DTOs y Validación    | Entidades, contratos de entrada/salida y validaciones           | [`docs/06_modelos_dtos_validacion.md`](./docs/06_modelos_dtos_validacion.md)       |
| 07 | Manejo de Errores             | Excepciones, respuestas consistentes y control de errores       | [`docs/07_control_errores.md`](./docs/07_control_errores.md)                       |
| 08 | Relaciones entre Entidades    | Relaciones uno a uno, uno a muchos y muchos a muchos            | [`docs/08_relacion_entidades.md`](./docs/08_relacion_entidades.md)                 |
| 09 | Request Params y Query Params | Parámetros de ruta, consulta y filtros                          | [`docs/09_relacion_requestparam.md`](./docs/09_relacion_requestparam.md)           |
| 10 | Paginación                    | Paginación, ordenamiento y filtros en APIs                      | [`docs/10_paginacion.md`](./docs/10_paginacion.md)                                 |
| 11 | Autenticación y Autorización  | JWT, login, protección de rutas y seguridad                     | [`docs/11_autenticacion_autorizacion.md`](./docs/11_autenticacion_autorizacion.md) |
| 12 | Roles y Permisos              | Control de acceso basado en roles                               | [`docs/12_roles_autorizacion.md`](./docs/12_roles_autorizacion.md)                 |
| 13 | Ownership                     | Validación de propiedad de recursos                             | [`docs/13_ownership_validacion.md`](./docs/13_ownership_validacion.md)             |
| 14 | Despliegue Backend            | Variables de entorno, Docker, servidores y publicación          | [`docs/14_despliegue_backend.md`](./docs/14_despliegue_backend.md)                 |

---

## Prácticas en Spring Boot

| Nº | Práctica                              | Carpeta                                                                                      |
| -- | ------------------------------------- | -------------------------------------------------------------------------------------------- |
| 01 | Instalación y configuración inicial   | [`spring/01-instalacion-configuracion`](./spring/01-instalacion-configuracion)               |
| 02 | Estructura del proyecto Spring Boot   | [`spring/02-estructura-proyecto`](./spring/02-estructura-proyecto)                           |
| 03 | API REST y controladores              | [`spring/03-api-rest-controladores`](./spring/03-api-rest-controladores)                     |
| 04 | Servicios e inyección de dependencias | [`spring/04-servicios-inyeccion-dependencias`](./spring/04-servicios-inyeccion-dependencias) |
| 05 | Persistencia y repositorios           | [`spring/05-persistencia-repositorios`](./spring/05-persistencia-repositorios)               |
| 06 | Modelos, DTOs y validación            | [`spring/06-modelos-dtos-validacion`](./spring/06-modelos-dtos-validacion)                   |
| 07 | Manejo de errores                     | [`spring/07-manejo-errores`](./spring/07-manejo-errores)                                     |
| 08 | Relaciones entre entidades            | [`spring/08-relaciones-entidades`](./spring/08-relaciones-entidades)                         |
| 09 | Paginación y filtros                  | [`spring/09-paginacion-filtros`](./spring/09-paginacion-filtros)                             |
| 10 | Autenticación con JWT                 | [`spring/10-autenticacion-jwt`](./spring/10-autenticacion-jwt)                               |
| 11 | Roles y autorización                  | [`spring/11-roles-autorizacion`](./spring/11-roles-autorizacion)                             |
| 12 | Documentación con OpenAPI             | [`spring/12-documentacion-openapi`](./spring/12-documentacion-openapi)                       |
| 13 | Testing backend                       | [`spring/13-testing`](./spring/13-testing)                                                   |
| 14 | Despliegue                            | [`spring/14-despliegue`](./spring/14-despliegue)                                             |

---

## Prácticas en NestJS

| Nº | Práctica                              | Carpeta                                                                                  |
| -- | ------------------------------------- | ---------------------------------------------------------------------------------------- |
| 01 | Instalación y configuración inicial   | [`nest/01-instalacion-configuracion`](./nest/01-instalacion-configuracion)               |
| 02 | Estructura del proyecto NestJS        | [`nest/02-estructura-proyecto`](./nest/02-estructura-proyecto)                           |
| 03 | API REST y controladores              | [`nest/03-api-rest-controladores`](./nest/03-api-rest-controladores)                     |
| 04 | Servicios e inyección de dependencias | [`nest/04-servicios-inyeccion-dependencias`](./nest/04-servicios-inyeccion-dependencias) |
| 05 | Persistencia y repositorios           | [`nest/05-persistencia-repositorios`](./nest/05-persistencia-repositorios)               |
| 06 | Modelos, DTOs y validación            | [`nest/06-modelos-dtos-validacion`](./nest/06-modelos-dtos-validacion)                   |
| 07 | Manejo de errores                     | [`nest/07-manejo-errores`](./nest/07-manejo-errores)                                     |
| 08 | Relaciones entre entidades            | [`nest/08-relaciones-entidades`](./nest/08-relaciones-entidades)                         |
| 09 | Paginación y filtros                  | [`nest/09-paginacion-filtros`](./nest/09-paginacion-filtros)                             |
| 10 | Autenticación con JWT                 | [`nest/10-autenticacion-jwt`](./nest/10-autenticacion-jwt)                               |
| 11 | Roles y autorización                  | [`nest/11-roles-autorizacion`](./nest/11-roles-autorizacion)                             |
| 12 | Documentación con OpenAPI             | [`nest/12-documentacion-openapi`](./nest/12-documentacion-openapi)                       |
| 13 | Testing backend                       | [`nest/13-testing`](./nest/13-testing)                                                   |
| 14 | Despliegue                            | [`nest/14-despliegue`](./nest/14-despliegue)                                             |

---

## Cómo trabajar con este repositorio

### 1. Clonar el repositorio de material

```bash
git clone https://github.com/PabloT18/icc-ppw-frameworks-backend.git
cd icc-ppw-frameworks-backend
```

Este repositorio contiene el material de referencia y las guías de práctica.

---

### 2. Revisar primero la teoría

Antes de implementar una práctica, revisar el archivo correspondiente en `/docs`.

Ejemplo:

```txt
docs/03_api_rest_conceptos.md
```

Luego revisar la implementación en el framework asignado:

```txt
spring/03-api-rest-controladores/
nest/03-api-rest-controladores/
```

---

### 3. Crear un proyecto backend propio

Cada estudiante o grupo debe crear su propio proyecto independiente.

Para Spring Boot:

```bash
# Crear proyecto desde Spring Initializr
# https://start.spring.io/

# Recomendado:
# Java 17 o superior
# Spring Web
# Spring Data JPA
# PostgreSQL Driver
# Validation
# Spring Security
```

Para NestJS:

```bash
npm i -g @nestjs/cli
nest new mi-proyecto-nest
cd mi-proyecto-nest
npm run start:dev
```

---

### 4. Crear repositorio personal en GitHub

Cada estudiante o grupo debe crear su propio repositorio para las prácticas.

Nombre recomendado:

```txt
icc-ppw-backend-[framework]-[apellido]
```

Ejemplos:

```txt
icc-ppw-backend-spring-perez
icc-ppw-backend-nest-perez
```

Subir el proyecto:

```bash
git init
git add .
git commit -m "init: proyecto backend"
git branch -M main
git remote add origin https://github.com/usuario/icc-ppw-backend-[framework]-[apellido].git
git push -u origin main
```

---

## Convención de commits

Los commits deben ser claros y relacionados con la práctica desarrollada.

Ejemplos para iniciar una práctica:

```bash
git add .
git commit -m "feat: práctica 01 configuración inicial"
git push origin main
```

Ejemplos para agregar avances:

```bash
git add .
git commit -m "add: práctica 03 controladores REST"
git push origin main
```

Ejemplos para actualizar o corregir:

```bash
git add .
git commit -m "fix: práctica 05 corrección conexión base de datos"
git push origin main
```

Ejemplo para finalizar una práctica:

```bash
git add .
git commit -m "end: práctica 06 modelos DTOs y validación"
git push origin main
```

Referencia: [`core/docs/commit-guidelines.md`](./.core/docs/commit-guidelines.md)

---

## README del proyecto del estudiante

El proyecto personal del estudiante debe incluir un `README.md` con esta estructura mínima:

````md
# Proyecto Backend - [Spring Boot / NestJS]

## Datos del estudiante

- Nombre:
- Carrera:
- Asignatura:


## Descripción

Proyecto backend desarrollado como parte de las prácticas de Programación y Plataformas Web.

## Tecnologías utilizadas

- Framework:
- Lenguaje:
- Base de datos:
- ORM:
- Herramientas adicionales:

## Prácticas realizadas

| Nº | Práctica | Estado |
|---|---|---|
| 01 | Instalación y configuración | Completada |
| 02 | Estructura del proyecto | Completada |
| 03 | API REST y controladores | En proceso |

## Instalación

```bash
# Instalar dependencias
```

## Ejecución

```bash
# Ejecutar en modo desarrollo
```

## Variables de entorno

```env
PORT=
DATABASE_URL=
JWT_SECRET=
```

## Evidencias

Las evidencias se encuentran en la carpeta:

```txt
/assets
```

````

---

## Estructura recomendada del proyecto del estudiante

```txt
mi-proyecto-backend/
├── src/
│   ├── controllers/
│   ├── services/
│   ├── models/
│   ├── dto/
│   ├── repositories/
│   └── config/
│
├── assets/
│   ├── 01-instalacion-configuracion.png
│   ├── 02-estructura-proyecto.png
│   └── 03-api-rest-controladores.png
│
├── README.md
└── .gitignore
````

La estructura interna puede variar según el framework, pero siempre debe mantenerse una carpeta de evidencias (assets) clara y ordenada.

---

## Formato sugerido para cada práctica

El sigueinte formato se debe adicionar al final del README del proyecto del estudiante para cada práctica realizada, ejemplo:


````md
## Práctica 03: API REST y Controladores

- Fecha:

### Desarrollo

Explicar brevemente qué se hizo en esta práctica, qué endpoints se implementaron y qué funcionalidades se lograron. Se pueden incluir detalles técnicos relevantes, como el uso de anotaciones, rutas, métodos HTTP, etc.
Ejemplos: 

#### Comandos utilizados

```bash
comando utilizado
```

#### Código relevante

```ts
// Código importante
```

o

```java
// Código importante
```

### Capturas de evidencia (segun como se pida en cada práctica)

![Captura de la práctica](assets/03-api-rest.png)

````

## Qué entregar en el AVAC

Para cada práctica se debe entregar:

1. Enlace al repositorio personal de GitHub.
2. Se debe evidenciar en el README del proyecto personal el desarrollo de la práctica con el formato requerido.
3. Capturas claras de la aplicación funcionando.
4. Código subido correctamente al repositorio.

El repositorio debe estar público o accesible para revisión.

---

## GISTs de apoyo

- [VS Code](https://gist.github.com/PabloT18/683e6d950b240f9620a98903cf92e87a)
- [Git y GitHub](https://gist.github.com/PabloT18/96343b6be1b5cfe237fe53e48eeeb6ef)
- [Node y PNPM](https://gist.github.com/PabloT18/8c0728e24b14c1c63a879b819f628299)

