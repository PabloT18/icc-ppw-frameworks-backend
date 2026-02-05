![Portada](./assets/PORTADA.png)

# **Práctica 6 (NestJS): Diseño de Modelos, DTOs y Validación Profesional**

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nestjs/nestjs-original.svg" width="110" alt="Nest Logo">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="95">
</div>

---

## **Autor**

**Cinthya Ramón**  
📧 [cramonm1@est.ups.edu.ec](mailto:ptorresp@ups.edu.ec)  
💻 GitHub: [CinthyLu](https://github.com/CinthyLu)

---

# **1. Introducción**

En esta práctica se implementó un **diseño profesional de DTOs, modelos de dominio y validación de datos** en una aplicación backend desarrollada con NestJS.

Se incorporó el uso de **class-validator** y **class-transformer** para validar automáticamente los datos de entrada, asegurando que la información recibida por la API cumpla con reglas sintácticas y de negocio antes de ser procesada y almacenada en la base de datos PostgreSQL.

El objetivo principal fue comprender la **separación clara de responsabilidades** entre:
- DTOs (transporte y validación)
- Modelos de dominio (reglas de negocio)
- Entidades persistentes (TypeORM)


---

# **2. Tecnologías utilizadas**

- **Node.js**
- **NestJS**
- **TypeORM**
- **PostgreSQL**
- **Docker**
- **class-validator**
- **clas-transformer**
- **VS Code**

---

# **3. Instalación de librerías de validación**

Para habilitar la validación automática de datos se instalaron las siguientes dependencias:

- **class-validator**
- **class-transformer**

Estas librerías permiten definir reglas de validación directamente sobre los DTOs mediante decoradores, integrándose de forma nativa con NestJS..

IMAGEN 01  
Instalación de dependencias de validación

![instalacion](assets\01_modelos_06.png)

---

# **4. Definición de DTOs con validación**

Se definieron DTOs específicos para el módulo Products, encargados de controlar y validar los datos recibidos por la API.

DTOs implementados:
- CreateProductDto
- UpdateProductDto
- PartialUpdateProductDto
- ProductResponseDto

Cada DTO contiene reglas de validación como:
- campos obligatorios
- longitudes mínimas
- valores numéricos no negativos

IMAGEN 02  
DTOs de Products con validaciones

![dtos](assets\02_modelos_06.png)

---

# 5. Activación del ValidationPipe global

La validación automática se habilitó de forma global mediante el uso de ValidationPipe en el archivo main.ts.

Esto garantiza que:
- los datos inválidos no lleguen a los servicios
- los campos no permitidos sean rechazados
- los tipos sean transformados correctamente

IMAGEN 03  
Configuración de ValidationPipe global

![main](assets\03_modelos_06.png)

---

# 6. Modelo de dominio Product

Se implementó un **modelo de dominio Product**, separado de la entidad persistente, responsable de aplicar reglas de negocio como:
- validación de precios
- validación de stock
- control del flujo de creación y actualización

El modelo actúa como intermediario entre los DTOs y las entidades de TypeORM.

IMAGEN 04  
Archivo product.model.ts

![model](assets\04_modelos_06.png)
![model](assets\05_modelos_06.png)

---

# 7. Flujo de validación de datos

El flujo completo de validación es el siguiente:

- El controlador recibe un DTO
- ValidationPipe valida automáticamente los datos
- El servicio ejecuta la lógica de negocio
- El modelo de dominio transforma la información
- La entidad persistente se guarda en PostgreSQL
- Se retorna un DTO de respuesta

Este flujo evita errores, mejora la mantenibilidad y garantiza coherencia en los datos.

---

# 8. Pruebas de validación

Se realizaron pruebas enviando datos inválidos a la API, comprobando que el sistema responde con errores HTTP 400 cuando los datos no cumplen las reglas definidas.

IMAGEN 05  
Error por datos inválidos en POST /api/products usando bruno
*error 400*
![error](assets\06_modelos_06.png)

---

# 9. Resultados obtenidos

Como resultado de esta práctica, la aplicación backend cuenta ahora con:

- DTOs con validación profesional
- Separación clara entre DTO, dominio y entidad
- Validación automática antes del servicio
- Reducción de errores en tiempo de ejecución
- Base sólida para el manejo global de errores en la siguiente práctica

---

# 10. Conclusión

La implementación de DTOs con validación y modelos de dominio permite construir APIs robustas, seguras y mantenibles, alineadas con estándares profesionales utilizados en aplicaciones backend empresariales.