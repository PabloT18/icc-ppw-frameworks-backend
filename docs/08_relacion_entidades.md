
# Programación y Plataformas Web

# Frameworks Backend: Relación entre Entidades y Modelado de Datos

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="80">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="80">
</div>


## Práctica 8: Relaciones entre Entidades – Diseño y Persistencia

### Autores

**Pablo Torres**

📧 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

💻 GitHub: PabloT18

## Introducción

Hasta este punto, el backend ha trabajado con **entidades independientes**, donde cada entidad representa una tabla aislada en la base de datos.

En sistemas reales, los datos **no existen de forma aislada**.
Las entidades se relacionan entre sí para representar correctamente el dominio del problema.

Ejemplos reales:

* Un usuario tiene múltiples direcciones
* Un producto pertenece a una categoría
* Una orden contiene varios productos
* Un estudiante pertenece a una carrera
* Una carrera pertenece a una universidad

Este documento introduce el **concepto de relaciones entre entidades**, desde un enfoque **teórico y universal**, sin depender de anotaciones, decoradores o sintaxis específica de ningún framework.

Las implementaciones concretas se desarrollarán posteriormente en los materiales propios de cada framework.

## 1. ¿Qué es una relación entre entidades?

Una **relación entre entidades** representa un **vínculo lógico y estructural** entre tablas de una base de datos.

Conceptualmente:

* Una entidad no siempre es autosuficiente
* Sus datos pueden depender de otra entidad
* Las relaciones permiten evitar duplicación
* Mantienen integridad y consistencia

En bases de datos relacionales, estas relaciones se implementan mediante:

* claves primarias
* claves foráneas
* restricciones de integridad referencial

## 2. Entidades aisladas vs entidades relacionadas

### Entidades aisladas

```
users
- id
- name
- email
```

Problema:

* No hay contexto
* No se puede representar relaciones reales

### Entidades relacionadas

```
users
- id
- name
- email

orders
- id
- date
- user_id
```

Ahora:

* Una orden pertenece a un usuario
* Un usuario puede tener múltiples órdenes

Esto refleja el **modelo real del negocio**.

## 3. Tipos de relaciones entre entidades

Existen tres tipos fundamentales de relaciones en sistemas backend.

### 3.1 Relación Uno a Uno (1:1)

Una instancia de una entidad se relaciona con **una sola instancia** de otra entidad.

Ejemplo conceptual:

```
users
- id
- name

profiles
- id
- phone
- user_id
```

Regla:

* Un usuario tiene un solo perfil
* Un perfil pertenece a un solo usuario

Uso típico:

* Separar datos sensibles
* Extender información sin sobrecargar una tabla principal

### 3.2 Relación Uno a Muchos (1:N)

Una instancia de una entidad se relaciona con **muchas instancias** de otra entidad.

Ejemplo conceptual:

```
categories
- id
- name

products
- id
- name
- category_id
```

Regla:

* Una categoría tiene muchos productos
* Un producto pertenece a una sola categoría

Es la relación **más común** en sistemas backend.

### 3.3 Relación Muchos a Muchos (N:M)

Muchas instancias de una entidad se relacionan con muchas instancias de otra.

Ejemplo conceptual:

```
students
- id
- name

subjects
- id
- name

student_subject
- student_id
- subject_id
```

Regla:

* Un estudiante cursa muchas materias
* Una materia tiene muchos estudiantes

Se implementa mediante una **tabla intermedia**.

## 4. Claves primarias y claves foráneas

### Clave primaria

* Identifica de forma única una fila
* No se repite
* No es nula

Ejemplo:

```
users.id
```

### Clave foránea

* Apunta a la clave primaria de otra tabla
* Representa la relación
* Garantiza integridad referencial

Ejemplo:

```
orders.user_id → users.id
```

Regla:

* No puede existir un valor que no esté en la tabla referenciada

## 5. Relaciones y diseño del modelo de dominio

Las relaciones deben surgir del **análisis del dominio**, no del framework.

Preguntas clave:

* ¿Una entidad depende de otra?
* ¿Puede existir sin la otra?
* ¿Cuántas instancias se relacionan?
* ¿La relación es obligatoria u opcional?

Ejemplo:

* Un producto puede existir sin ventas
* Una venta no puede existir sin producto

Esto define:

* cardinalidad
* obligatoriedad
* tipo de relación

## 6. Relaciones y servicios

Los **servicios** no gestionan relaciones manualmente mediante IDs sueltos.

Responsabilidades del servicio:

* Validar existencia de entidades relacionadas
* Coordinar creación o asociación
* Aplicar reglas de negocio

Ejemplo conceptual:

```
crearOrden(usuarioId, productos)
```

El servicio:

* valida que el usuario exista
* valida que los productos existan
* crea la orden
* asocia productos a la orden
* persiste el resultado

## 7. Relaciones y DTOs

Las relaciones **no se exponen directamente** en los DTOs de entrada y salida.

Buenas prácticas:

* DTOs de entrada usan IDs
* DTOs de salida devuelven datos controlados
* Nunca exponer entidades completas sin control

Ejemplo:

Entrada:

```
orderCreateDto
- userId
- productIds
```

Salida:

```
orderResponseDto
- id
- date
- userName
- total
```

Esto evita:

* ciclos infinitos
* sobreexposición de datos
* acoplamiento con la base de datos

## 8. Relaciones y ORM

Los ORM permiten:

* definir relaciones entre entidades
* cargar datos relacionados
* manejar integridad
* evitar SQL manual

Conceptualmente, el ORM:

```
Entidad A ↔ Entidad B
```

Se encarga de:

* joins
* inserciones relacionadas
* actualizaciones consistentes
* eliminación controlada

La sintaxis concreta depende del framework y se verá en los módulos específicos.

## 9. Eliminación y relaciones

Eliminar entidades relacionadas requiere reglas claras.

Opciones conceptuales:

* eliminación en cascada
* bloqueo de eliminación
* eliminación lógica

Ejemplo:

* No eliminar un usuario si tiene órdenes
* O eliminar órdenes automáticamente
* O marcar como inactivo

La decisión es **de negocio**, no técnica.

## 10. Errores comunes en relaciones

Errores frecuentes en estudiantes:

* Usar IDs sin validar existencia
* Duplicar información en varias tablas
* Crear relaciones innecesarias
* Exponer entidades completas en la API
* No pensar en cardinalidad real

Este tema busca prevenir estos errores desde el diseño.

## 11. Resultados esperados

Al finalizar este tema, el estudiante comprende:

* qué es una relación entre entidades
* tipos de relaciones
* uso de claves foráneas
* impacto en diseño de dominio
* rol de servicios y DTOs
* errores comunes
* preparación para implementación real


## 12. Aplicación directa en los siguientes módulos

Estos conceptos se aplicarán directamente en los módulos específicos de cada framework.


### Spring Boot

 [`spring-boot/08_relacion_entidades.md.md`](../spring-boot/p67/a_dodente/08_relacion_entidades.md.md)

* relaciones JPA
* anotaciones de cardinalidad
* carga de relaciones
* cascadas
* ejemplos reales con PostgreSQL

### NestJS

[`nest/08_relacion_entidades.md.md`](../nest/p67/a_dodente/08_relacion_entidades.md.md)

* relaciones TypeORM
* entidades relacionadas
* manejo de joins
* carga eager y lazy
* ejemplos reales con PostgreSQL


