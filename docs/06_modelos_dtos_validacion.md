
# Programación y Plataformas Web

# **Modelos de Dominio, DTOs y Validación de Datos**

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="80">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="80">
</div>

## **Práctica 6: Diseño de Modelos de Dominio, DTOs y Validación**

### **Autores**

**Pablo Torres**

 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: PabloT18


# **Introducción**

En los temas anteriores se implementó:

* Controladores
* Servicios
* Entidades persistentes
* Repositorios
* Conexión a PostgreSQL

Pero falta un elemento fundamental para cualquier API profesional:

### **Validar correctamente los datos que entran y salen de la aplicación**

Por lo tanto, este documento desarrolla tres conceptos clave:

1. **Modelos de dominio**
2. **DTOs (Data Transfer Objects)**
3. **Validación de datos (backend validation)**

Estos conceptos permiten:

* garantizar la integridad de los datos
* evitar que entren datos inválidos al servicio o base de datos
* definir qué datos se reciben y qué datos se exponen
* mantener separadas las capas de dominio, API y persistencia
* preparar la arquitectura para autenticación, reglas de negocio y seguridad

El tema se aplica en ambos frameworks:

* Spring Boot → `spring-boot/06_modelos_dtos_validacion.md`
* NestJS → `nest/06_modelos_dtos_validacion.md`

Este documento explica **la teoría general**, sin depender de un framework en particular.


# **1. ¿Qué es un Modelo de Dominio?**

Un **modelo de dominio** representa conceptos de negocio, no conceptos de base de datos ni de API.

Un dominio define:

* reglas de negocio
* invariantes (condiciones que siempre deben cumplirse)
* métodos que expresan comportamientos
* restricciones que no dependen de SQL ni HTTP

Ejemplos:

* Un `User` debe tener un email válido.
* Un `Product` no puede tener precio negativo.
* Un `Order` debe asegurar que todos los ítems pertenecen al mismo cliente.
* Un método `applyDiscount()` nunca debe permitir descuento mayor al 100%.

### **Importante: El dominio NO expone datos sensibles.**

Por ejemplo:

* La entidad persistente tiene `password`
* El DTO de salida **no debe incluirla**
* El dominio puede tener lógica para validar contraseñas, pero nunca para exponerlas


# **2. ¿Qué es un DTO y para qué sirve?**

DTO significa **Data Transfer Object**.

### Un DTO define qué datos entran y salen de la aplicación.

Tipos de DTO:

| Tipo             | Propósito                                     |
| ---------------- | --------------------------------------------- |
| **Request DTO**  | Datos que envía el cliente (POST, PUT, PATCH) |
| **Response DTO** | Datos que devuelve el backend                 |
| **Partial DTO**  | Actualizaciones parciales (PATCH)             |
| **Auth DTO**     | Login, registro, tokens, etc.                 |

### **Los DTO NO deben contener lógica de negocio.**

Son estructuras simples usadas para comunicación.

### **Los DTO NO deben ser entidades.**

Las entidades contienen lógica de persistencia.


# **3. Problema: Entradas sin validar**

Sin validación:

* `email` puede venir vacío
* `price` puede ser negativo
* `stock` puede ser un texto
* un cliente puede crear productos con datos corruptos
* puede insertarse basura en la base de datos

Ejemplo incorrecto:

```
POST /users
{
  "name": "",
  "email": "notaemail",
  "password": 12345
}
```

Si no se valida:

1. El servicio recibe datos inválidos
2. La entidad se construye mal
3. Hibernate intenta guardar algo inválido
4. La BD rechaza o, peor, acepta valores inconsistentes
5. La API expone información errónea

Por eso se debe validar **antes de ejecutar la lógica del servicio**.


# **4. Validación: Reglas universales**

Independientemente del framework, toda API debe validar:

### **4.1. Validaciones comunes en strings**

* no vacío (`not empty`)
* longitud mínima/máxima (`minLength`, `maxLength`)
* formato (`email`, `uuid`, `regex`)
* contenido permitido

### **4.2. Validaciones numéricas**

* `min`
* `max`
* valores negativos prohibidos
* rango permitido
  EJ: `0 ≤ price ≤ 10000`

### **4.3. Validaciones lógicas del dominio**

Ejemplos:

* un usuario no puede cambiar email a uno ya existente
* no se puede dejar stock en negativo
* un producto sin nombre no existe
* la actualización parcial NO debe borrar valores si no se envían

### **4.4. Validaciones de seguridad**

* no aceptar campos que el cliente no debería modificar (ej. `id`, `createdAt`, `deleted`)
* no dejar que el cliente defina permisos o roles arbitrarios


# **5. Responsabilidad de cada capa**

| Capa                  | Qué valida                                                   |
| --------------------- | ------------------------------------------------------------ |
| **DTO**               | Estructura básica: formato, tipos, restricciones sintácticas |
| **Modelo de dominio** | Reglas de negocio                                            |
| **Servicio**          | Consistencia del uso: duplicados, relaciones, dependencias   |
| **Repositorio / BD**  | Reglas estructurales (únicos, relaciones, constraints)       |

### **La validación NUNCA debe hacerse solo en la base de datos.**


# **6. Ciclo completo de validación**

```
Cliente
  ↓
DTO de Entrada (validación sintáctica)
  ↓
Modelo de Dominio (validación de negocio)
  ↓
Entidad persistente (estructura compatible con la BD)
  ↓
Repositorio (validación por constraints)
  ↓
BD
  ↓
Entidad persistente
  ↓
Modelo de Dominio
  ↓
DTO de Respuesta
  ↓
Cliente
```


# **7. Diseño del Modelo de Dominio con invariantes**

Un buen modelo debe garantizar que **no existan estados inválidos**.

Ejemplo: dominio `Product`

```java
class Product {
    private String name;
    private BigDecimal price;
    private int stock;

    public Product(String name, BigDecimal price, int stock) {
        if (name == null || name.isBlank())
            throw new IllegalArgumentException("Name required");

        if (price.compareTo(BigDecimal.ZERO) < 0)
            throw new IllegalArgumentException("Price must be >= 0");

        if (stock < 0)
            throw new IllegalArgumentException("Stock must be >= 0");

        this.name = name;
        this.price = price;
        this.stock = stock;
    }
}
```

**El dominio te protege incluso si el DTO falla**.


# **8. Validación en DTOs (concepto general)**

Un DTO debe tener reglas claras como:

* obligatorio
* tamaño
* formato
* unicidad (no en el DTO, pero sí en el servicio)
* tipo correcto

Ejemplo conceptual:

```
CreateUserDto:
  - name: obligatorio, min 3, max 150
  - email: obligatorio, formato email
  - password: obligatorio, min 8

UpdateUserDto:
  - igual que create pero sin cambiar email (según reglas)

PartialUpdateUserDto:
  - todo opcional pero sin permitir nulos inválidos
```


# **9. Validación en el Servicio**

El servicio valida reglas como:

* email ya existe
* un producto con stock negativo no se puede vender
* no se puede actualizar un usuario eliminado
* no se puede eliminar un producto con órdenes activas
* integridad en relaciones (User → Orders)

El servicio coordina:

```
Validar → Convertir → Persistir → Retornar
```


# **10. Validación en la Base de Datos**

Se logra mediante:

* `NOT NULL`
* `UNIQUE`
* `CHECK (price >= 0)`
* `FOREIGN KEY`
* `ON DELETE CASCADE | RESTRICT`

La BD sirve como **última barrera de seguridad**, no como la principal.


# **11. Patrones de Validación Modernos**

### **11.1. Patrón “Fail Fast”**

Si un dato es inválido, se aborta inmediatamente.

### **11.2. Patrón “Value Object”**

En lugar de strings sueltos, encapsular valores importantes:

```
Email → value object
Money → value object
Phone → value object
```

### **11.3. Patrón “Domain Guard”**

Métodos estáticos que validan invariantes:

```
Guard.notEmpty(name, "Name required")
Guard.range(price, 0, 10000)
```


# **12. Relación entre Modelo, DTO y Entidad**

```
DTO  → Validación sintáctica
Modelo de Dominio → Validación de reglas
Entidad JPA/TypeORM → Persistencia
```

Ejemplo de flujo:

```
POST /products
   ↓
CreateProductDto (validaciones básicas)
   ↓
Product.fromDto(dto)  // reglas de negocio
   ↓
product.toEntity()    // conversión a tabla
   ↓
repository.save()
   ↓
Product.fromEntity()  // dominio nuevamente
   ↓
product.toResponseDto()
   ↓
Cliente
```


# **13. Actividad práctica**

Cada estudiante debe:

### **13.1. Crear DTOs completos para products/**

* `CreateProductDto`
* `UpdateProductDto`
* `PartialUpdateProductDto`
* `ProductResponseDto`

Con reglas claras:

* name → obligatorio
* price → >= 0
* stock → >= 0

### **13.2. Crear modelo de dominio Product**

Con métodos:

* `Product.fromDto()`
* `Product.fromEntity()`
* `product.toEntity()`
* `product.toResponseDto()`
* `product.update()`
* `product.partialUpdate()`

### **13.3. Agregar validaciones lógicas**

Ejemplos:

* precio no puede ser negativo
* stock no puede ser negativo

### **13.4. Integrar validaciones con el servicio**

El servicio debe:

1. validar que el nombre no esté en blanco
2. validar que el email (si existiera) sea único
3. validar reglas del dominio
4. validar referencia a entidades relacionadas (si existieran)

### **13.5. Probar fallos esperados**

El estudiante debe demostrar que la API rechaza:

* precio negativo
* stock negativo
* campos vacíos
* emails inválidos



Estos conceptos se aplicarán directamente en:

* [`spring-boot/06_modelos_dtos_validacion.md`](../spring-boot/p67/a_dodente/06_modelos_dtos_validacion.md)
* [`nest/06_modelos_dtos_validacion.md`](../nest/p67/a_dodente/06_modelos_dtos_validacion.md)


