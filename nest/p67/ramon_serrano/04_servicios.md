![Portada](assets\PortadaRS.png)


# Práctica 05 – Persistencia y Repositorios con TypeORM y PostgreSQL en NestJS

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nestjs/nestjs-original.svg" width="110">
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

## 1. Introducción

En esta sección se describe la implementación de la lógica de negocio mediante servicios en NestJS.  
Los servicios actúan como intermediarios entre los controladores y los repositorios, aplicando el principio de separación de responsabilidades.

---

## 2. ProductsService

El servicio ProductsService contiene toda la lógica relacionada con la gestión de productos:

- Creación
- Consulta
- Actualización completa
- Actualización parcial
- Eliminación

El servicio utiliza inyección de dependencias para acceder al repositorio de TypeORM.

---

## 3. Inyección de dependencias

NestJS gestiona automáticamente la creación e inyección del repositorio mediante:

- @Injectable()
- @InjectRepository()

Esto permite desacoplar la lógica de negocio del acceso a datos.

---

## 4. Evidencias

Evidencia del servicio ProductsService implementado:

![Servicio Products](assets/04_repositorios_04.png)
