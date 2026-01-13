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

En esta práctica se implementa persistencia real en una aplicación NestJS mediante el uso de TypeORM y una base de datos PostgreSQL.  
El objetivo es reemplazar el almacenamiento en memoria por una base de datos relacional, utilizando entidades y repositorios, siguiendo una arquitectura profesional en capas.

---

## 2. Instalación de dependencias necesarias

Para habilitar la persistencia con PostgreSQL se instalaron las siguientes dependencias:

- @nestjs/typeorm
- typeorm
- pg

Comando utilizado:

```bash
pnpm install --save @nestjs/typeorm typeorm pg
