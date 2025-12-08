#  Guías para Comentarios de Commits - PRW-P67 Frameworks Backend

##  Instrucciones para GitHub Copilot

Este archivo contiene las directrices para generar comentarios de commits consistentes y descriptivos en el proyecto de frameworks backend PRW-P67 (Spring Boot y NestJS).

##  Estructura General de Commits

### Formato Básico
```
<tipo>(<alcance>): <descripción>

[cuerpo opcional]

[pie opcional]
```

### Tipos de Commit

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `feat` | Nueva funcionalidad | `feat(spring-boot): agregar controlador de usuarios` |
| `fix` | Corrección de errores | `fix(nest): corregir error en servicio de autenticación` |
| `docs` | Documentación | `docs: actualizar README con instrucciones de instalación` |
| `style` | Cambios de formato/estilo | `style(nest): aplicar formato ESLint` |
| `refactor` | Refactorización de código | `refactor(spring-boot): optimizar servicio de productos` |
| `test` | Agregar o modificar tests | `test(nest): agregar tests unitarios para módulo de usuarios` |
| `chore` | Tareas de mantenimiento | `chore: actualizar dependencias` |
| `init` | Inicialización de proyecto | `init(spring-boot): configurar proyecto base` |
| `config` | Configuración | `config(nest): configurar conexión a base de datos` |
| `scripts` | Scripts y herramientas | `scripts: agregar generador de estructura` |

### Alcances Comunes

| Alcance | Descripción |
|---------|-------------|
| `spring-boot` | Cambios específicos del proyecto Spring Boot |
| `nest` | Cambios específicos del proyecto NestJS |
| `docs` | Documentación general en `/docs` |
| `scripts` | Scripts de utilidad del proyecto |
| `config` | Archivos de configuración |
| `deps` | Dependencias |
| `api` | Cambios en endpoints o API REST |
| `service` | Cambios en servicios |
| `controller` | Cambios en controladores |
| `entity` | Cambios en entidades/modelos |
| `dto` | Cambios en DTOs |
| `auth` | Cambios en autenticación/autorización |
| `db` | Cambios relacionados con base de datos |


## Reglas de nomenclatura de archivos y carpetas

- Nombres de carpetas de estudiantes: `<apellido1>_<apellido2>` (todo en minúsculas, sin espacios).
- Nombres de archivos Markdown de documentación: `01_configuracion.md`, `02_api_rest.md`, etc.
- Nombres de clases Java (Spring Boot): Usar PascalCase (ejemplo: `UserController`, `ProductService`, `OrderEntity`).
- Nombres de clases TypeScript (NestJS): Usar PascalCase con sufijos descriptivos (ejemplo: `UserController`, `ProductService`, `OrderDto`).
- Nombres de métodos y funciones: Usar camelCase (ejemplo: `getUserById`, `createProduct`, `validateToken`).
- Nombres de variables: Usar camelCase (ejemplo: `userId`, `productList`, `authToken`).
- Nombres de paquetes Java: Usar lowercase separado por puntos (ejemplo: `com.ups.backend.controller`).

### Estructura de carpetas por framework

**Spring Boot**: 
```
spring-boot/
  └── p67/
      └── apellido1_apellido2/
          ├── 01_configuracion.md
          ├── 02_api_rest.md
          └── assets/
              └── images/
```

**NestJS**:
```
nest/
  └── p67/
      └── apellido1_apellido2/
          ├── 01_configuracion.md
          ├── 02_modulos_controladores.md
          └── assets/
              └── images/
```

### Assets estáticos (imágenes, diagramas, etc.) deben ubicarse en carpetas específicas dentro de cada proyecto de estudiante en la carpeta `assets`.

* **imágenes** → `/assets/images/`
    * Los nombres de archivos de imagen deben ser descriptivos y en minúsculas, separados por guiones
    * Ejemplo: `diagrama_arquitectura.png`, `postman_request.jpg`
    * **Para prácticas específicas**: incluir el número de práctica al final del nombre con formato `p##`
        * Práctica 01: `01-configuracion`
        * Imagen: `01-spring-boot-setup-p01.png`
        * Práctica 03: `03-api-rest`
        * Imagen: `03-nest-swagger-docs-p03.png`

## Ejemplos de Commits por Contexto

### 📝  Estructura de Estudiantes

```bash
# Al crear carpetas de estudiantes
feat(scripts): agregar generador automático de estructura de estudiantes

- Crear script para generar carpetas por framework backend
- Incluir .gitignore automático en cada carpeta
- Soporte para configuración JSON de estudiantes

# Al agregar estudiantes específicos
feat(nest): agregar proyecto base para torres_garcia

# Al modificar estructura
refactor(scripts): mejorar lógica de generación de carpetas backend
```

### 🔧 Desarrollo Backend

```bash
# Controladores nuevos
feat(spring-boot): implementar UserController con endpoints REST

feat(nest): crear módulo de autenticación con JWT

# Servicios
feat(spring-boot): agregar ProductService con lógica de negocio

feat(nest): implementar servicio de validación de usuarios

# Entidades y modelos
feat(spring-boot): crear entidad User con anotaciones JPA

feat(nest): definir schema de Product con TypeORM

# DTOs
feat(nest): agregar DTOs de creación y actualización de usuarios

# APIs y endpoints
feat(spring-boot): implementar endpoints CRUD para productos

feat(nest): agregar endpoint de login con validación

# Base de datos
feat(spring-boot): configurar conexión a PostgreSQL

config(nest): configurar TypeORM con MySQL
```

### 🐛 Correcciones

```bash
# Errores de funcionalidad
fix(spring-boot): corregir error de validación en UserController

fix(nest): resolver problema de autenticación en guard

# Problemas de configuración
fix(spring-boot): corregir configuración de CORS

fix(nest): resolver conflicto en módulo de base de datos

# Errores de base de datos
fix(spring-boot): corregir query en UserRepository

fix(nest): resolver problema de migración en entidad Product
```

### 📚 Documentación

```bash
# README y documentación
docs: actualizar instrucciones de instalación por framework

docs(spring-boot): agregar guía de configuración de Maven

docs(nest): documentar estructura de módulos y servicios

# Documentación de conceptos
docs: completar tema 03 sobre API REST

docs: agregar ejemplos de DTOs en tema 06

# Swagger/OpenAPI
docs(spring-boot): configurar Swagger UI

docs(nest): agregar decoradores de documentación en controladores
```

### 🔧 Configuración y Herramientas

```bash
# Dependencias
chore(deps): actualizar Spring Boot a versión 3.2.0

chore(deps): actualizar NestJS y dependencias relacionadas

# Configuración de proyecto
config(spring-boot): configurar application.properties para múltiples entornos

config(nest): optimizar configuración de build

# Scripts de utilidad
scripts: agregar comando para inicializar proyectos backend

scripts: crear generador de estructura de controladores
```

### 🧪 Testing

```bash
# Tests unitarios
test(spring-boot): agregar tests para UserService

test(nest): implementar tests para AuthController

# Tests de integración
test(spring-boot): agregar tests de integración para API de productos

test(nest): implementar tests E2E para módulo de usuarios
```

## 🎯 Mejores Prácticas para Commits

### ✅ Hacer (DO)

1. **Usar presente imperativo**: "agregar" no "agregado" o "agregando"
2. **Ser específico**: Mencionar qué archivo/componente se modificó
3. **Incluir el framework**: Usar el alcance apropiado
4. **Describir el "qué" y "por qué"**: No solo el "cómo"
5. **Commits atómicos**: Un commit = un cambio lógico

### ❌ Evitar (DON'T)

1. **Commits genéricos**: "fix stuff", "update files"
2. **Commits masivos**: Muchos cambios no relacionados
3. **Faltas de ortografía**: Revisar antes de commit
4. **Commits sin contexto**: Sin explicar el propósito

## 📐 Plantillas por Contexto

### Para Proyectos de Estudiantes

```bash
# Estructura inicial
init(<framework>): configurar proyecto base para <apellido1>_<apellido2>

# Ejemplos:
init(spring-boot): configurar proyecto base para torres_garcia
init(nest): configurar proyecto base para gonzalez_marca
```

### Para Funcionalidades Backend

```bash
# Nueva característica - Controlador
feat(<framework>): implementar <nombre>Controller con endpoints <funcionalidad>

# Ejemplo:
feat(spring-boot): implementar UserController con endpoints CRUD
feat(nest): implementar AuthController con login y registro

# Nueva característica - Servicio
feat(<framework>): agregar <nombre>Service con lógica de <funcionalidad>

# Ejemplo:
feat(spring-boot): agregar ProductService con validación de stock
feat(nest): agregar EmailService con envío de notificaciones

# Nueva característica - Entidad/Modelo
feat(<framework>): crear entidad <nombre> con <relaciones>

# Ejemplo:
feat(spring-boot): crear entidad Order con relación a User y Product
feat(nest): crear schema Category con relación Many-to-Many
```

### Para Correcciones

```bash
# Error específico
fix(<framework>): corregir <problema> en <ubicación>

# Ejemplo:
fix(spring-boot): corregir error de validación en UserDto
fix(nest): corregir problema de inyección en ProductService
```

### Para Documentación de Temas

```bash
# Documentación de conceptos teóricos
docs: completar tema <número> - <nombre del tema>

# Ejemplo:
docs: completar tema 05 - Controladores y Servicios
docs: actualizar tema 07 con ejemplos de TypeORM

# Documentación técnica por framework
docs(<framework>): documentar <tema> en proyecto <apellidos>

# Ejemplo:
docs(spring-boot): documentar configuración JPA en proyecto perez_torres
docs(nest): agregar ejemplos de guards en proyecto martinez_lopez
```

## 🤖 Instrucciones para GitHub Copilot

Al generar comentarios de commit, considera:

1. **Contexto del archivo**: Framework backend (Spring Boot o NestJS), tipo de archivo (controlador, servicio, entidad, DTO, configuración)
2. **Cambios realizados**: Qué se modificó exactamente (endpoint, lógica de negocio, modelo de datos)
3. **Impacto**: A qué parte de la API o arquitectura afecta el cambio
4. **Convenciones**: Seguir el formato establecido para proyectos backend

### Ejemplos de Prompts para Copilot

```
// Para generar commit de nueva funcionalidad en Spring Boot
// feat(spring-boot): implementar [descripción específica de controlador/servicio]

// Para corrección en NestJS
// fix(nest): corregir [problema específico] en [módulo/servicio/controlador]

// Para documentación de conceptos backend
// docs: completar tema [número] - [nombre del tema]

// Para configuración de base de datos
// config(spring-boot): configurar conexión a PostgreSQL con JPA

// Para tests
// test(nest): agregar tests unitarios para [módulo/servicio]
```

## 📊 Casos de Uso Frecuentes

### Proyectos de Estudiantes

```bash
# Inicialización
init(spring-boot): configurar proyecto inicial para torres_garcia
init(nest): configurar proyecto inicial para gonzalez_marca

# Desarrollo de API
feat(spring-boot/torres_garcia): implementar API REST de usuarios
feat(nest/gonzalez_marca): agregar módulo de autenticación con JWT

# Configuración de BD
config(spring-boot/torres_garcia): configurar JPA con PostgreSQL
config(nest/gonzalez_marca): configurar TypeORM con MySQL

# Correcciones
fix(spring-boot/martinez_lopez): corregir problema de validación en DTO
fix(nest/perez_gomez): resolver error de inyección de dependencias
```

### Documentación de Conceptos Backend

```bash
# Temas teóricos en /docs
docs: completar tema 01 - Conceptos Backend
docs: actualizar tema 03 - API REST con ejemplos prácticos
docs: agregar diagramas en tema 02 - Arquitectura Backend

# Documentación técnica por framework
docs(spring-boot): documentar configuración de Spring Security
docs(nest): agregar ejemplos de decoradores y pipes
```

### Desarrollo de Características Backend

```bash
# Controladores
feat(spring-boot): implementar UserController con endpoints CRUD
feat(nest): crear ProductController con validación de DTOs

# Servicios
feat(spring-boot): agregar OrderService con lógica de negocio
feat(nest): implementar AuthService con estrategia JWT

# Entidades y Modelos
feat(spring-boot): crear entidad Product con relaciones JPA
feat(nest): definir schema User con TypeORM

# DTOs
feat(spring-boot): agregar DTOs de validación para usuarios
feat(nest): crear DTOs de entrada y salida para productos

# Autenticación y Seguridad
feat(spring-boot): implementar JWT con Spring Security
feat(nest): agregar guards de autorización por roles
```

### Scripts y Herramientas

```bash
# Nuevos scripts para backend
scripts: agregar generador automático de estructura de proyectos backend
scripts: implementar script de inicialización de base de datos

# Mejoras
refactor(scripts): optimizar generador de módulos backend
fix(scripts): corregir manejo de rutas en generador
```

## 🔄 Workflow Recomendado

1. **Antes del commit**: Revisar cambios con `git diff`
2. **Escribir commit**: Seguir el formato establecido
3. **Revisar mensaje**: Verificar ortografía y claridad
4. **Commit atómico**: Un cambio lógico por commit

---

## 📝 Nota para Desarrolladores

Este archivo debe mantenerse actualizado con nuevas convenciones y ejemplos específicos del proyecto. Si agregas nuevos frameworks o cambias la estructura, actualiza las plantillas correspondientes.

**Recuerda**: Un buen commit message es una inversión en el futuro del proyecto. Facilita la revisión de código, el debugging y la comprensión del historial.