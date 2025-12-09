                  
# **Frameworks Backend**

## Manual de Trabajo en GitHub 

![alt text](.core/assets/ups-icc.png)


**Asignatura:** Programación y Plataformas Web

**Tema:** Frameworks Backend (Spring Boot, NestJS)

**Author Material:** Pablo Torres

---

El repositorio incluye también un módulo común en `/docs` con los **conceptos universales del backend**, que servirán como base teórica antes de implementar cada tema en los frameworks.

Incluye un aplicación de los conceptos de `/docs` en cada uno de los frameworks backend:

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg" width="110" alt="Spring Logo">
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nestjs/nestjs-original.svg" width="110" alt="Nest Logo"/>
        
</div>



Los estudiantes trabajarán, documentando paso a paso el desarrollo de sus prácticas backend en carpetas individuales dentro de cada framework. Para ello usaran sus ramas correspondientes y seguirán las mismas reglas de commits del proyecto.


---


## **Descripción general del proyecto**

Este repositorio es un espacio compartido donde cada grupo de estudiantes documentará el desarrollo de sus prácticas backend siguiendo el modelo:

1. **Estudiar el concepto** en la carpeta `/docs`.
2. **Aplicarlo técnicamente** en:

   * `/spring-boot/p67/apellidos/`
   * `/nest/p67/apellidos/`
3. Registrar paso a paso:

   * comandos
   * capturas
   * configuración
   * código relevante
   * explicación de cada avance

El objetivo es:

* comprender arquitectura backend
* construir APIs REST completas
* manejar servicios, repositorios, DTOs, validación, seguridad y pruebas
* aplicar buenas prácticas de Git y GitHub

---

## **Estructura del Repositorio**

```
/docs
   ├── 01_conceptos_backend.md
   ├── 02_arquitectura_backend.md
   ├── 03_api_rest_conceptos.md
   ├── 04_estructura_servidor.md
   ├── 05_controladores_servicios.md
   ├── 06_modelos_dtos_validacion.md
   ├── 07_conexion_bd.md
   ├── 08_manejo_errores.md
   ├── 09_autenticacion_autorizacion.md
   ├── 10_documentacion_openapi.md
   ├── 11_testing_backend.md
   ├── 12_despliegue_backend.md
   ├── 13_websockets.md
   ├── 14_grpc.md
   └── 15_graphql.md

/spring-boot
   └── p67
       └── estudiante1_estudiante2
           ├── 01_configuracion.md
           ├── .....
/nest
   └── p67
       └── estudiante1_estudiante2
           ├── 01_configuracion.md
           ├── .....
```

---

## **Índice general de temas (conceptos)**

A continuación una tabla resumen con **todos los temas teóricos** del backend y el enlace al archivo dentro de `/docs`.

| Nº | Tema                      | Descripción breve                                                | Archivo                                  |
| -- | ------------------------- | ---------------------------------------------------------------- | ---------------------------------------- |
| 01 | Conceptos Backend         | Qué es un servidor, ciclo de petición, HTTP, backend vs frontend | [`/docs/01_conceptos_backend.md`](./docs/01_conceptos_backend.md)          |
| 02 | Arquitectura Backend      | Capas, MVC, MVCS, microservicios, estilos de comunicación        | [`/docs/02_arquitectura_backend.md`](./docs/02_arquitectura_backend.md)       |
| 03 | API REST                  | Recursos, verbos, status codes, idempotencia                     | [`/docs/03_api_rest_conceptos.md`](./docs/03_api_rest_conceptos.md)         |
| 04 | Estructura del Servidor   | Flujo request → response, routers, middlewares                   | [`/docs/04_estructura_servidor.md`](./docs/04_estructura_servidor.md)        |
| 05 | Controladores y Servicios | Responsabilidades, separación de lógica                          | [`/docs/05_controladores_servicios.md`](./docs/05_controladores_servicios.md)    |
| 06 | Modelos y DTOs            | Validación, arquitectura por capas, contratos                    | [`/docs/06_modelos_dtos_validacion.md`](./docs/06_modelos_dtos_validacion.md)    |
| 07 | Conexión BD               | ORM, entidades, repositorios, migraciones                        | [`/docs/07_conexion_bd.md`](./docs/07_conexion_bd.md)                |
| 08 | Manejo de Errores         | Excepciones, filtros, respuestas consistentes                    | [`/docs/08_manejo_errores.md`](./docs/08_manejo_errores.md)             |
| 09 | Autenticación             | JWT, sesiones, roles, guards                                     | [`/docs/09_autenticacion_autorizacion.md`](./docs/09_autenticacion_autorizacion.md) |
| 10 | Swagger / OpenAPI         | Documentar API, generar especificaciones                         | [`/docs/10_documentacion_openapi.md`](./docs/10_documentacion_openapi.md)      |
| 11 | Testing Backend           | Unit tests, mocks, integración                                   | [`/docs/11_testing_backend.md`](./docs/11_testing_backend.md)            |
| 12 | Despliegue                | Docker, variables de entorno, servidores                         | [`/docs/12_despliegue_backend.md`](./docs/12_despliegue_backend.md)         |
| 13 | WebSockets                | Tiempo real, eventos                                             | [`/docs/13_websockets.md`](./docs/13_websockets.md)                 |
| 14 | gRPC                      | Peticiones binarias de alta velocidad                            | [`/docs/14_grpc.md`](./docs/14_grpc.md)                       |
| 15 | GraphQL                   | Schemas, resolvers, queries                                      | [`/docs/15_graphql.md`](./docs/15_graphql.md)                    |

---

## **Explicación de cada archivo de `/docs`**

### **01 – Conceptos Backend**

Fundamentos universales:

* qué es backend
* manejo de estado
* concurrencia
* ciclo request/response
* HTTP en profundidad
  Base teórica para comprender por qué existen los frameworks backend.

---

### **02 – Arquitectura Backend**

Incluye:

* capas (presentación, negocio, datos)
* MVC, MVCS, Clean Architecture
* monolito, modular, microservicios
* API Gateway
* estilos de comunicación: REST, RPC, gRPC, WebSockets, SSE, GraphQL
  Define cómo se diseñan sistemas backend modernos.

---

### **03 – API REST**

Conceptos:

* verbos HTTP
* recursos
* path vs query
* status codes
* idempotencia
* HATEOAS
  Tema esencial para backend.

---

### **04 – Estructura del Servidor**

Explica:

* routers
* pipelines
* middlewares
* interceptores
* flujo interno de una petición

---

### **05 – Controladores y Servicios**

Bases de la separación de responsabilidades.
Por qué no poner lógica en controladores.

---

### **06 – Modelos y DTOs**

Explica:

* entidades
* DTOs
* validación
* serialización
* contratos de entrada/salida

---

### **07 – Base de Datos**

Fundamentos de conexión y persistencia.
ORM, repositorios, migraciones.

---

### **08 – Manejo de Errores**

Errores controlados
Filtros
Respuestas consistentes

---

### **09 – Autenticación y Autorización**

* roles y permisos
* JWT
* guards
* seguridad en APIs

---

### **10 – Documentación OpenAPI**

Uso de Swagger
Estructura de documentación

---

### **11 – Testing Backend**

Mocking
Pruebas unitarias
Pruebas de integración

---

### **12 – Despliegue**

* Docker
* variables de entorno
* entornos dev/stage/prod

---

### **13, 14, 15 – Temas avanzados**

WebSockets, gRPC y GraphQL
Se estudian al final como alternativas a REST.

---

##  **Pasos para trabajar**

> Esta sección replica exactamente el flujo del repositorio frontend, pero adaptado al backend.

### 1. Clonar el repositorio

```bash
git clone https://github.com/PabloT18/icc-ppw-frameworks-backend.git
cd icc-ppw-frameworks-backend
```

### 2. Crear una rama personal

```bash
git checkout -b apellido1-apellido2-backend
```

### 3. Editar solo su carpeta

Cada grupo debe **editar únicamente los archivos de su propia carpeta** 

En cada archivo `.md` deberán incluir:

* Capturas de pantalla del proceso.
* Explicaciones de instalación, componentes, formularios, y otros temas vistos.


Ejemplo:

```
/spring-boot/p67/perez_torres/01_configuracion.md
/nest/p67/perez_torres/01_configuracion.md
```

### 4. Commit

```bash
git commit -m "Tema 01: configuración inicial Spring Boot"
```

**Directrices para Commits**

Es fundamental seguir ciertas directrices al realizar commits en este proyecto para asegurar la claridad y la organización del trabajo. A continuación, se presentan las pautas a seguir indicadas en el documento de directrices de commits. [`core/docs/commit-guidelines.md`](./.core/docs/commit-guidelines.md).


### 5. Pull y push

Antes de subir cambios, siempre sincronizar con la rama principal:

```bash
git pull origin main
```

Si surgen conflictos:

* Resolver solo los que afecten a sus propios archivos.
* No modificar carpetas ni archivos de otros compañeros.

```bash
git push origin apellido1-apellido2-backend
```

### 6. Crear un Pull Request (PR)

Cuando se haya comletado un avance importante (sera indicado en clases), crear un PR. 
En GitHub:

1. Ir al repositorio.
2. Seleccionar la rama creada (`estudiante1_estudiante2_backend`).
3. Hacer clic en **"New Pull Request"**.
4. Solicitar merge hacia `main`.

* Luego revisaré y aprobará el PR colocando la calificación

---

## Reglas Importantes

* No trabajar en `main`.
* No editar archivos ajenos.
* Avances al final de cada clase.
* Capturas obligatorias.
* Commit claros y ordenados.

---

##  GISTs de apoyo

(igual que en el proyecto frontend)

---

# **LISTO PARA COPIAR EN TU REPOSITORIO**


* [VS Code](https://gist.github.com/PabloT18/683e6d950b240f9620a98903cf92e87a)

* [Git y GitHub](https://gist.github.com/PabloT18/96343b6be1b5cfe237fe53e48eeeb6ef)

* [Node y PNPM](https://gist.github.com/PabloT18/8c0728e24b14c1c63a879b819f628299)


