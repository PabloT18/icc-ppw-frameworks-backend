# Programación y Plataformas Web

# Frameworks Backend: NestJS – Instalación y Configuración

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nestjs/nestjs-original.svg" width="110" alt="Nest Logo"/>
</div>

## Práctica 1 (NestJS): Instalación, Configuración Inicial y Primer Endpoint

### Autores

**Pablo Torres**

[ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: [PabloT18](https://github.com/PabloT18)

---

# 1. Introducción al framework

**NestJS** es un framework backend para Node.js escrito en TypeScript. Permite construir aplicaciones web de forma estructurada, modular y escalable.

NestJS se inspira en arquitecturas empresariales similares a Spring Boot, usando una organización basada en:

* módulos
* controladores
* servicios
* decoradores
* inyección de dependencias
* TypeScript como lenguaje principal

NestJS se caracteriza por:

* trabajar sobre Node.js
* utilizar TypeScript de forma nativa
* organizar la aplicación mediante módulos
* separar controladores y servicios
* permitir la creación de APIs REST
* facilitar la inyección de dependencias
* ofrecer una arquitectura clara para aplicaciones backend

Documentación oficial:
https://docs.nestjs.com/

---

# 2. Requisitos oficiales

Según la documentación de NestJS, se requiere:

## Node.js

* Node.js **18** como mínimo
* Recomendado: Node.js **20 LTS** o superior

Verificación:

```bash
node -v
```

Salida esperada:

```bash
v20.x.x
```

---

## Administradores de paquetes compatibles

NestJS puede trabajar con diferentes gestores de paquetes:

| Gestor | Uso        |
| ------ | ---------- |
| npm    | Compatible |
| pnpm   | Compatible |
| yarn   | Compatible |

> En esta asignatura se utilizará **pnpm** para la creación y ejecución del proyecto.

Verificación:

```bash
pnpm -v
```

---

## NestJS CLI

El CLI de NestJS permite generar proyectos, módulos, controladores y servicios desde la terminal.

Instalación global:

```bash
pnpm install -g @nestjs/cli
```

Verificación:

```bash
nest --version
```

---

## Servidor HTTP en NestJS

NestJS se ejecuta sobre Node.js y utiliza por defecto un servidor HTTP basado en Express.

Esto significa que no se instala un servidor externo como Tomcat. El servidor se levanta directamente desde la aplicación Node.js.

Cuando la aplicación NestJS inicia, también se inicia el servidor HTTP interno.

Ejemplo de log:

```bash
Nest application successfully started
```

El desarrollador no necesita:

* instalar un servidor externo
* desplegar archivos `.war`
* configurar Tomcat manualmente

Toda la ejecución se realiza desde el propio proyecto con comandos de Node.js.

---

## ¿Cuál servidor usa esta materia?

En esta materia se utilizará la configuración por defecto de NestJS, basada en Express.

Esta configuración es suficiente para construir APIs REST y comprender la estructura backend.

---

## ¿Ventajas de este modelo?

| Ventaja                    | Explicación                                         |
| -------------------------- | --------------------------------------------------- |
| Desarrollo rápido          | No requiere instalación de servidores externos      |
| Integración con TypeScript | Permite tipado fuerte y mejor organización          |
| Modularidad                | Cada funcionalidad puede organizarse en módulos     |
| Facilidad para APIs REST   | Permite crear endpoints de forma directa            |
| Escalabilidad              | Facilita separar controladores, servicios y módulos |

---

## ¿Cómo se relaciona esto con la estructura del proyecto?

Dentro del proyecto, NestJS inicia la aplicación desde:

```txt
src/main.ts
```

Este archivo crea la aplicación y levanta el servidor.

Ejemplo general del ciclo:

```txt
[Aplicación NestJS]
   │
   │ inicia desde main.ts
   ↓
[Servidor HTTP interno]
   │
   │ escucha en el puerto 3000
   ↓
http://localhost:3000/api/status
```

---

# 3. Configuración del entorno de desarrollo

## 3.1 Instalación de Node.js

Node.js debe estar instalado previamente.

Sitio recomendado:

https://nodejs.org/

Verificación:

```bash
node -v
```

Salida esperada:

```bash
v20.x.x
```

---

## 3.2 Entornos recomendados

### Visual Studio Code

Adecuado para proyectos NestJS por su integración con:

* TypeScript
* terminal integrada
* extensiones para Node.js
* soporte para ESLint y Prettier

Extensiones recomendadas:

* ESLint
* Prettier
* TypeScript Importer
* Thunder Client o REST Client

### IntelliJ IDEA

También puede utilizarse, especialmente por su soporte para:

* TypeScript
* Node.js
* navegación entre clases
* refactorización

---

# 4. Creación del proyecto

El proyecto NestJS se genera mediante el CLI oficial.

En esta práctica se utilizará **pnpm** como administrador de paquetes y TypeScript como lenguaje principal.

---

## 4.1 Crear el proyecto

Ejecutar:

```bash
nest new fundamentos01
```

Durante la creación, NestJS solicita seleccionar el gestor de paquetes.

Seleccionar:

```txt
pnpm
```

---

## 4.2 Selección inicial del proyecto

Para esta práctica se utilizarán los siguientes valores:

| Campo               | Selección     |
| ------------------- | ------------- |
| Framework           | NestJS        |
| Lenguaje            | TypeScript    |
| Gestor de paquetes  | pnpm          |
| Nombre del proyecto | fundamentos01 |
| Puerto por defecto  | 3000          |

---

## 4.3 Datos técnicos del proyecto

### Nombre del proyecto

```txt
fundamentos01
```

### Lenguaje

```txt
TypeScript
```

### Administrador de paquetes

```txt
pnpm
```

### Punto de entrada

```txt
src/main.ts
```

### Módulo raíz

```txt
src/app.module.ts
```

---

## 4.4 Apertura del proyecto

Una vez creado el proyecto, ingresar a la carpeta:

```bash
cd fundamentos01
```

Abrir el proyecto en el editor seleccionado.

En Visual Studio Code:

```bash
code .
```

---

# 5. Estructura inicial del proyecto

El proyecto genera la siguiente estructura base:

```txt
fundamentos01/
 ├── src/
 │    ├── app.controller.ts
 │    ├── app.controller.spec.ts
 │    ├── app.module.ts
 │    ├── app.service.ts
 │    └── main.ts
 ├── test/
 ├── package.json
 ├── pnpm-lock.yaml
 ├── tsconfig.json
 ├── tsconfig.build.json
 └── nest-cli.json
```

### Elementos clave:

| Archivo             | Función                                 |
| ------------------- | --------------------------------------- |
| `main.ts`           | Punto de entrada de la aplicación       |
| `app.module.ts`     | Módulo raíz del proyecto                |
| `app.controller.ts` | Controlador inicial                     |
| `app.service.ts`    | Servicio inicial                        |
| `package.json`      | Configuración de scripts y dependencias |
| `nest-cli.json`     | Configuración del CLI de NestJS         |
| `tsconfig.json`     | Configuración de TypeScript             |

NestJS organiza la aplicación en módulos. El módulo raíz es `AppModule`.

---

# 6. Ejecución del proyecto

Una vez abierto el proyecto, el servidor se inicia con:

```bash
pnpm start
```

También se puede usar modo desarrollo con recarga automática:

```bash
pnpm start:dev
```

Al final del proceso, se visualiza algo similar a:

```bash
[Nest] 8421  - 2025-02-28 14:12:33  LOG [NestFactory] Starting Nest application...
[Nest] 8421  - 2025-02-28 14:12:33  LOG [InstanceLoader] AppModule dependencies initialized
[Nest] 8421  - 2025-02-28 14:12:33  LOG [RoutesResolver] AppController {/}: +1ms
[Nest] 8421  - 2025-02-28 14:12:33  LOG [NestApplication] Nest application successfully started
```

La aplicación estará disponible en:

```txt
http://localhost:3000
```

---

## Salida esperada

![Salida de consola](assets/01-configuracion_01-nest.png)

---

# 7. Creación del primer endpoint

Se implementará un endpoint REST que devuelva el estado del servicio.

La ruta será:

```txt
/api/status
```

Para mantener una estructura similar a Spring Boot, se configurará el prefijo global `/api` en `main.ts`.

---

## 7.1 Configurar prefijo global `/api`

Modificar el archivo:

```txt
src/main.ts
```

Contenido:

```ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.setGlobalPrefix('api');

  await app.listen(3000);
}
bootstrap();
```

Con esta configuración, todos los endpoints tendrán el prefijo:

```txt
/api
```

---

## 7.2 Crear un módulo para status

Ejecutar:

```bash
nest g module status
```

Resultado:

```txt
src/status/status.module.ts
```

Este comando registra el módulo dentro de `app.module.ts`.

---

## 7.3 Crear el controlador

Ejecutar:

```bash
nest g controller status
```

Resultado:

```txt
src/status/status.controller.ts
```

Modificar el contenido:

```ts
import { Controller, Get } from '@nestjs/common';

@Controller('status')
export class StatusController {
  @Get()
  getStatus() {
    return {
      service: 'NestJS API',
      status: 'running',
      timestamp: new Date().toISOString(),
    };
  }
}
```

Como el prefijo global es `/api`, la ruta final queda:

```txt
/api/status
```

---

## 7.4 Verificar el módulo raíz

En `src/app.module.ts` debe estar registrado el módulo `StatusModule`.

Ejemplo:

```ts
import { Module } from '@nestjs/common';
import { StatusModule } from './status/status.module';

@Module({
  imports: [StatusModule],
})
export class AppModule {}
```

---

## 7.5 Acceder al endpoint

Ejecutar el servidor:

```bash
pnpm start:dev
```

Acceder a:

```txt
http://localhost:3000/api/status
```

Ejemplo de salida:

```json
{
  "service": "NestJS API",
  "status": "running",
  "timestamp": "2025-02-28T15:44:10.192Z"
}
```

## Salida esperada

![Salida endpoint](assets/02-configuracion_01-nest.png)

---

# 8. Explicación breve de los decoradores utilizados

### `@Module()`

Define un módulo de NestJS.

Un módulo agrupa controladores, servicios y otros proveedores relacionados.

En esta práctica, `StatusModule` agrupa el controlador de estado.

---

### `@Controller()`

Indica que la clase administra rutas HTTP.

Ejemplo:

```ts
@Controller('status')
```

Define que la clase atenderá rutas relacionadas con:

```txt
/status
```

Como existe un prefijo global `/api`, la ruta final será:

```txt
/api/status
```

---

### `@Get()`

Indica que el método responde a solicitudes HTTP GET.

Ejemplo:

```ts
@Get()
```

Como está dentro de `StatusController`, responde a:

```txt
GET /api/status
```

---

# 9. Sección práctica de esta actividad

En esta práctica se:

1. Configura el entorno de Node.js y NestJS.
2. Genera un proyecto con Nest CLI usando pnpm.
3. Inicia el servidor en el puerto 3000.
4. Configura el prefijo global `/api`.
5. Implementa un endpoint para verificar el estado del servicio.
6. Observa la estructura del proyecto y su punto de entrada.

---

# 10. Resultados y Evidencias

Cada estudiante o grupo debe completar su archivo agregando:



### 1. Captura del endpoint `/api/status` funcionando en el navegador o Postman o Bruno

Debe incluir la respuesta JSON.


### 6. Explicación breve escrita por el estudiante

Debe describir:

* qué función cumple `main.ts`
* qué función cumple `AppModule`
* qué similitudes encontró con Spring Boot
