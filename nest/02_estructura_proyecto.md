# Programación y Plataformas Web

# Frameworks Backend: NestJS – Estructura del Proyecto

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nestjs/nestjs-original.svg" width="100" alt="Nest Logo">
</div>

## Práctica 2 (NestJS): Estructura del Proyecto, Arquitectura Interna y Organización Modular

### Autores

**Pablo Torres**

[ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: [PabloT18](https://github.com/PabloT18)

---

# 1. Introducción

En el tema anterior se revisó cómo crear un proyecto NestJS, ejecutar el servidor y crear un primer endpoint.

En esta práctica se profundiza en cómo se **estructura internamente un proyecto backend profesional**, cómo NestJS organiza sus componentes, cómo detecta módulos, controladores y servicios, y cómo aplicar una arquitectura modular basada en dominios.

El objetivo es comprender:

* cómo se organiza un proyecto NestJS a nivel de carpetas
* cómo funcionan módulos, controladores, servicios, modelos y DTOs dentro de MVCS
* por qué el módulo raíz es fundamental
* cómo NestJS registra los componentes mediante módulos
* cómo organizar el proyecto como si fuera una aplicación empresarial real

---

# 2. ¿Cómo organiza NestJS un proyecto?

NestJS utiliza tres elementos clave:

### **1. Módulo raíz**

Es el módulo principal de la aplicación:

```txt
app.module.ts
```

Ejemplo:

```ts
@Module({
  imports: [],
  controllers: [],
  providers: [],
})
export class AppModule {}
```

`AppModule` funciona como punto central de registro de los módulos principales del proyecto.

Esto significa:

* si un módulo no se importa en `AppModule`, no forma parte de la aplicación
* si un controlador no está registrado en un módulo, NestJS no lo expone
* si un servicio no está registrado como provider, no puede ser inyectado

---

### **2. Sistema de módulos**

Al iniciar la aplicación, NestJS:

```txt
1. Ejecuta main.ts
2. Crea la aplicación con NestFactory
3. Carga AppModule
4. Lee los módulos importados
5. Registra controllers
6. Registra providers o services
7. Configura las rutas HTTP
8. Inicia el servidor en el puerto configurado
```

Ejemplo de carga inicial:

```ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.setGlobalPrefix('api');
  await app.listen(3000);
}
bootstrap();
```

---

### **3. Decoradores**

NestJS utiliza decoradores para definir el rol de cada clase o método.

Ejemplos:

```txt
@Module()       → define un módulo
@Controller()   → define un controlador
@Injectable()   → define un servicio o provider
@Get()          → define un endpoint GET
@Post()         → define un endpoint POST
```

Estos decoradores permiten que NestJS identifique qué clase cumple cada responsabilidad dentro de la aplicación.

---

# 3. npm, pnpm y yarn

NestJS permite diferentes administradores de paquetes para instalar dependencias, ejecutar scripts y manejar el proyecto.

---

## 3.1 npm

**Características**:

* viene instalado junto con Node.js
* ampliamente utilizado en proyectos JavaScript y TypeScript
* usa el archivo `package-lock.json`
* permite instalar dependencias con `npm install`

**Ventajas**:

* no requiere instalación adicional
* alta compatibilidad
* documentación abundante

**Limitaciones**:

* puede ser más lento en proyectos grandes
* ocupa más espacio en algunas instalaciones

---

## 3.2 pnpm

**Características**:

* administrador de paquetes moderno
* usa el archivo `pnpm-lock.yaml`
* reutiliza dependencias mediante almacenamiento eficiente
* permite instalaciones rápidas

**Ventajas**:

* mayor velocidad
* menor uso de espacio en disco
* adecuado para proyectos modernos
* buena integración con proyectos TypeScript y monorepos

**Por qué se utilizará pnpm en este curso**:

* es eficiente para proyectos iterativos
* permite instalar dependencias rápidamente
* facilita trabajar con proyectos Node.js modernos
* mantiene un archivo de bloqueo claro mediante `pnpm-lock.yaml`
* estandariza el entorno de trabajo de los estudiantes

---

## 3.3 yarn

**Características**:

* administrador de paquetes alternativo
* usa el archivo `yarn.lock`
* fue muy usado antes de la adopción amplia de pnpm

**Ventajas**:

* estable
* compatible con muchos proyectos existentes

**Limitaciones**:

* no será el gestor utilizado en esta asignatura
* puede generar diferencias si se mezcla con npm o pnpm

---

# 4. Archivos esenciales en un proyecto NestJS

| Archivo               | Función                                               |
| --------------------- | ----------------------------------------------------- |
| `main.ts`             | Punto de entrada de la aplicación NestJS              |
| `app.module.ts`       | Módulo raíz donde se registran módulos principales    |
| `app.controller.ts`   | Controlador inicial generado por NestJS               |
| `app.service.ts`      | Servicio inicial generado por NestJS                  |
| `package.json`        | Define dependencias, scripts y metadatos del proyecto |
| `pnpm-lock.yaml`      | Registra versiones exactas de dependencias instaladas |
| `nest-cli.json`       | Configuración del CLI de NestJS                       |
| `tsconfig.json`       | Configuración general de TypeScript                   |
| `tsconfig.build.json` | Configuración de TypeScript para compilación          |

---

# 5. Estructura interna generada por NestJS

Estructura inicial:

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

Pero esta estructura es insuficiente para un proyecto real.

A continuación se presenta cómo organizar una API profesional.

---

# 6. Arquitectura MVCS aplicada a NestJS

En NestJS, MVCS se distribuye así:

| Capa                     | Elemento NestJS |
| ------------------------ | --------------- |
| Presentación             | `controllers/`  |
| Negocio                  | `services/`     |
| Dominio                  | `models/`       |
| Persistencia             | `repositories/` |
| Comunicación DTO         | `dtos/`         |
| Utilidades transversales | `utils/`        |
| Configuraciones globales | `config/`       |
| Organización modular     | `*.module.ts`   |

---

# 7. Estructura modular recomendada (proyecto grande)

Se utilizará **estructura por dominios o recursos**.

### Proyecto base:

```txt
src/
    ├── config/
    ├── utils/
    ├── products/
    ├── users/
    ├── auth/
    ├── app.module.ts
    └── main.ts
```

Cada carpeta representa un dominio o recurso de la aplicación.

Ejemplos:

```txt
users/      → gestión de usuarios
products/   → gestión de productos
auth/       → autenticación
config/     → configuraciones globales
utils/      → funciones auxiliares reutilizables
```

---

# 8. Estructura modular dentro de cada dominio

Cada módulo contiene **todas las capas necesarias**:

```txt
products/
    ├── controllers/
    ├── services/
    ├── repositories/
    ├── entities/
    ├── dtos/
    ├── mappers/
    ├── utils/
    └── products.module.ts
```

Lo mismo aplica para:

```txt
users/
auth/
orders/
payments/
etc.
```

En NestJS, cada dominio debe tener además su propio archivo de módulo:

```txt
users.module.ts
products.module.ts
auth.module.ts
```

Estos archivos permiten registrar los controladores y servicios de cada dominio.

---

# 9. Flujo interno de NestJS dentro de esta estructura

```txt
HTTP Request
        ↓
Servidor HTTP de NestJS
        ↓
AppModule
        ↓
Module del dominio
        ↓
Controller (products/controllers)
        ↓
Service (products/services)
        ↓
Repository (products/repositories)
        ↓
Base de Datos
        ↓
HTTP Response (DTO o JSON)
```

En esta práctica todavía no se implementa base de datos.

La estructura se prepara para que en prácticas posteriores se pueda incorporar persistencia.

---

# 10. Actividad práctica

En esta práctica se debe:

### 1. Reorganizar el proyecto con la estructura modular:

Crear dentro de:

```txt
src/
```

las carpetas:

```txt
config/
utils/
products/
users/
auth/
```

### 2. Dentro de `products/` crear carpetas similar a `users/`:

Crear las carpetas necesarias para organizar el módulo por capas.

### 3. Crear clases vacías para verificar la estructura modular:

Ejemplo en `products/controllers`:

```ts
@Controller('products')
export class ProductsController {}
```

Y en `products/services`:

```ts
@Injectable()
export class ProductsService {}
```

También se debe verificar el archivo del módulo:

```ts
@Module({
  controllers: [ProductsController],
  providers: [ProductsService],
})
export class ProductsModule {}
```

### 4. Ejecutar la aplicación

```bash
pnpm start:dev
```

El proyecto debe compilar correctamente aun con clases vacías.

---

# 11. Resultados y Evidencias

Cada estudiante debe agregar en su documento:

---

### 1. Captura del IDE mostrando la estructura modular:

Debe visualizarse claramente:

---

### 2. Captura del archivo `app.module.ts`

Se debe verificar:

* el módulo raíz
* los módulos importados
* la ubicación correcta que permite cargar los dominios

---


---

### 3. Explicación breve

Se debe redactar:

* por qué es importante tener módulos separados
