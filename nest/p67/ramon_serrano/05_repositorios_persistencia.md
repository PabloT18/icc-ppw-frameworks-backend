![Portada](assets\PortadaRS.png)

# **Práctica 05 – Persistencia y Repositorios con TypeORM y PostgreSQL en NestJS**

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nestjs/nestjs-original.svg" width="110" alt="Nest Logo">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="95">
</div>

---

## **Autores**

**Cinthya Ramón**  
📧 [cramonm1@est.ups.edu.ec](mailto:cramonm1@est.ups.edu.ec)  
💻 GitHub: [CinthyLu](https://github.com/CinthyLu)

**John Serrano**  
📧 [jserranom2@est.ups.edu.ec](mailto:jserranom2@est.ups.edu.ec)  
💻 GitHub: [Johnserrano09](https://github.com/Johnserrano09)


---

# **1. Introducción**

En esta práctica se implementó **persistencia real** en una aplicación backend desarrollada con NestJS.  
Se reemplazó el almacenamiento en memoria por una base de datos PostgreSQL utilizando **TypeORM** como ORM, permitiendo gestionar los datos mediante **repositorios** y siguiendo una arquitectura en capas alineada con el patrón MVCS.

El objetivo principal fue comprender cómo **configurar una conexión a base de datos**, definir **entidades persistentes** y utilizar **repositorios** para realizar operaciones CRUD de forma profesional.

---

# **2. Tecnologías utilizadas**

- **Node.js**
- **NestJS**
- **TypeORM**
- **PostgreSQL**
- **Docker**
- **VS Code**

---

# **3. Configuración de la base de datos**

La base de datos PostgreSQL se ejecuta dentro de un **contenedor Docker**, lo que permite un entorno aislado, reproducible y sin dependencias locales adicionales.

**Configuración utilizada:**

- Motor de base de datos: **PostgreSQL**
- Contenedor Docker: **postgres-nest**
- Base de datos: **devdb_nest**
- Usuario: **ups**
- Contraseña: **ups123**
- Puerto: **5432**

**IMAGEN 01** 
*Docker ejecutando PostgreSQL* 
![Docker ejecutando PostgreSQL](assets\01_repositorios_05.png)

El contenedor: postgres-nest
Estado: Up
Puerto: 5432->5432

---

# **4. Configuración de TypeORM en NestJS**

TypeORM se configuró en el módulo principal de la aplicación utilizando `TypeOrmModule.forRoot`, estableciendo la conexión con PostgreSQL y habilitando la detección automática de entidades persistentes.

Para el entorno de desarrollo se utilizó la opción `synchronize: true`, lo que permite que TypeORM cree y actualice automáticamente las tablas en la base de datos a partir de las entidades definidas en el proyecto.

**IMAGEN 02**  
*configuración de `TypeOrmModule.forRoot`*

![app.module.ts](assets\02_repositorios_05.png)

---

# **5. Entidad persistente ProductEntity**

Se creó la entidad **ProductEntity** para representar la tabla `products` en PostgreSQL.  
Esta entidad hereda de una clase base de auditoría que incluye campos comunes como:

- `id`
- `createdAt`
- `updatedAt`
- `deleted`

La entidad define los siguientes campos principales:

- `name`
- `description`
- `price`
- `stock`

Gracias a esta definición, TypeORM puede generar automáticamente la estructura de la tabla en la base de datos.

**IMAGEN 03**  
*Archivo product.entity.ts*
![app.module.ts](assets\03_repositorios_05.png)



---

# **6. Uso de repositorios con TypeORM**

En esta práctica se eliminó completamente el uso de **arreglos en memoria**.  
La persistencia se maneja mediante **repositorios de TypeORM**, específicamente con `Repository<ProductEntity>`.

El repositorio se inyecta en el servicio usando inyección de dependencias, lo que permite realizar operaciones como:

- `find`
- `findOne`
- `save`
- `delete`

De esta forma, toda la lógica de acceso a datos queda centralizada y desacoplada del controlador.

**IMAGEN 04**  
*Captura del archivo `products.service.ts`*

![productsservice](assets\04_repositorios_05.png)
![productsservice](assets\05_repositorios_05.png)

- Uso de `@InjectRepository`
- Uso de `productRepository.save`
- Ausencia de arreglos en memoria y manejo manual de IDs

---

# **7. Flujo de creación de un producto**

El flujo de creación de un producto sigue los siguientes pasos:

1. El controlador recibe la solicitud HTTP con un DTO
2. El servicio aplica reglas de negocio
3. El mapper transforma el DTO en una entidad persistente
4. El repositorio guarda la entidad en PostgreSQL
5. Se retorna un DTO de respuesta al cliente

Este flujo garantiza **separación de responsabilidades** y facilita el mantenimiento del sistema.

---

# **8. Creación automática de la tabla en PostgreSQL**

Al iniciar la aplicación, TypeORM genera automáticamente la tabla `products` en la base de datos a partir de la entidad definida, gracias a la opción `synchronize`.

Durante el arranque del servidor se pueden observar las sentencias SQL ejecutadas para la creación de la tabla.

**IMAGEN 05**  
*Ejecución de nest con `npm run start:dev`* 
![createTable](assets\06_repositorios_05.png)

---

# **9. Verificación de la persistencia**

Para verificar el correcto funcionamiento de la persistencia, se consultaron los datos almacenados en la tabla `products` desde PostgreSQL, confirmando que los registros creados desde la API se almacenan correctamente en la base de datos.

**IMAGEN 06**  
*Captura de la tabla creada con Docker*

![Docker](assets\07_repositorios_05.png)


# **10. Pruebas de los endpoints**

Se probó el funcionamiento del módulo Products mediante peticiones HTTP, verificando que los datos se guardan y se recuperan desde la base de datos correctamente.

**IMAGEN 07**  

*Captura de una peticiones con bruno*

- `POST /api/products`

![Bruno](assets\09_repositorios_05.png)

- `GET /api/products`
![Bruno](assets\08_repositorios_05.png)

---

# **11. Resultados obtenidos**

Como resultado de esta práctica, la aplicación backend cuenta ahora con:

- **Persistencia real en PostgreSQL**
- **Entidades TypeORM correctamente definidas**
- **Uso de repositorios para acceso a datos**
- **Creación automática de tablas**
- **Base sólida para aplicar validaciones y manejo global de errores en las siguientes prácticas**