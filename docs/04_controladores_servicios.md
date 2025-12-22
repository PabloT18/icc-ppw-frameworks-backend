# Programación y Plataformas Web

# Frameworks Backend: Controladores, Servicios e Inyección de Dependencias

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="80" alt="Java Logo">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="80" alt="TS Logo">

</div>

## Práctica 4: Controladores, Servicios e Inyección de Dependencias

### Autores

**Pablo Torres**
📧 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)
💻 GitHub: [PabloT18](https://github.com/PabloT18)


# Introducción

En el tema anterior (03) se construyó un CRUD REST básico directamente desde el **controlador**, utilizando solo:

* controladores
* modelos
* DTOs
* mappers
* un arreglo en memoria

Eso permitió aprender cómo funcionan los endpoints REST.

A partir de este tema, comenzamos a estructurar el backend según el patrón recomendado para sistemas profesionales: **MVCS** (Modelo–Vista–Controlador–Servicio).

Este módulo explica:

* qué es un controlador
* qué es un servicio
* por qué se separan sus responsabilidades
* cómo funciona la inyección de dependencias
* cómo fluye una solicitud dentro del servidor
* cómo se prepara el proyecto para agregar repositorios y bases de datos más adelante

Los temas siguientes utilizarán esta base:

📌 `spring-boot/04_servicios_y_logica_negocio.md`
📌 `nest/04_servicios_inyeccion_dependencias.md`


# 1. ¿Qué es un controlador?

El **controlador** es la capa que recibe las solicitudes del cliente.

Funciones principales:

* definir rutas y endpoints
* recibir parámetros de la petición
* validar formato básico
* delegar la lógica a un servicio
* retornar la respuesta al cliente

El controlador **no debe contener lógica de negocio**.

Su responsabilidad es estrictamente comunicacional:

```
Cliente HTTP → Controlador → Servicio → Resultado → Controlador → Cliente
```

### ¿Qué NO hace un controlador?

❌ No calcula reglas de negocio
❌ No procesa datos complejos
❌ No accede a archivos ni base de datos
❌ No construye entidades internas
❌ No contiene algoritmos

Un controlador solo **dirige el tráfico**.


# 2. ¿Qué es un servicio?

El **servicio** es la capa que contiene toda la lógica del negocio.

Funciones del servicio:

* procesar reglas de negocio
* validar condiciones complejas
* transformar datos
* aplicar cálculos
* consultar y actualizar datos (más adelante, usando repositorios)
* preparar objetos de dominio

El servicio es el corazón del backend.

Aquí es donde se ubican métodos como:

* calcular totales
* validar stock
* verificar permisos
* aplicar descuentos
* ejecutar flujos
* administrar listas o colecciones

Mientras que el controlador recibe la orden,
el servicio **decide qué hacer** con esa orden.


# 3. Separación de responsabilidades (SRP)

Se aplica el **Principio de Responsabilidad Única (SRP)**:

| Capa            | Responsabilidad principal  |
| --------------- | -------------------------- |
| **Controlador** | Recibir petición y delegar |
| **Servicio**    | Procesar lógica de negocio |

Esto permite:

* mantener el código limpio
* facilitar pruebas unitarias
* cambiar reglas sin afectar endpoints
* reutilizar lógica en múltiples controladores
* preparar el sistema para agregar repositorios y BD

Ejemplo conceptual:

```
Controlador:
- recibe DTO
- llama servicio
- retorna resultado

Servicio:
- valida
- calcula
- transforma
- genera entidad
- retorna resultado
```


# 4. Inyección de dependencias (Dependency Injection)

Tanto Spring Boot como NestJS utilizan **inyección de dependencias (DI)** para conectar controladores y servicios sin necesidad de instanciarlos manualmente.

La DI permite que:

* los servicios se creen una sola vez
* puedan compartirse entre varias clases
* el framework gestione su ciclo de vida
* el código sea más modular y limpio


## 4.1 Cómo funciona la DI

### Spring Boot

El servicio se marca con:

```java
@Service
```

El controlador recibe el servicio por constructor:

```java
public UsersController(UserService service) {
    this.service = service;
}
```

Spring se encarga de:

* crear la instancia
* mantenerla en memoria
* entregarla al controlador

### NestJS

El servicio se marca con:

```ts
@Injectable()
```

Y el controlador lo recibe mediante constructor:

```ts
constructor(private readonly usersService: UsersService) {}
```

NestJS hace el mismo trabajo que Spring Boot:
gestiona el ciclo de vida del servicio.


# 5. Flujo interno de una petición usando servicios

A partir de este tema, todas las peticiones siguen este ciclo:

```
1. Cliente envía una solicitud HTTP
2. El Controlador recibe la petición
3. El Controlador envía los datos al Servicio
4. El Servicio ejecuta la lógica de negocio
5. El Servicio transforma datos usando modelos o mappers
6. El Servicio retorna el resultado al Controlador
7. El Controlador devuelve una respuesta HTTP al cliente
```

Diagrama:

```
Cliente
  ↓
Controlador (rutas, DTOs, parámetros)
  ↓
Servicio (reglas, validaciones, cálculos)
  ↓
[Posteriormente: Repositorio → BD]
  ↓
Servicio
  ↓
Controlador
  ↓
Cliente
```


# 6. ¿Por qué trasladar la lógica del controlador al servicio?

En el tema 03, los controladores incluían lógica para:

* buscar elementos en listas
* crear objetos
* actualizar información
* eliminar registros

Eso no escala en un backend real.

Los servicios permiten:

* reutilizar lógica
* mantener controladores ligeros
* probar reglas sin conocer la web
* cambiar la fuente de datos sin tocar el controlador
* reemplazar listas en memoria por BD sin romper nada

Ejemplo de beneficio:

Si mañana se cambia:

```
users = []  →  consulta a PostgreSQL
```

Solo cambia el servicio.
El controlador sigue funcionando exactamente igual.


# 7. Esta estructura prepara el camino para repositorios y bases de datos

A partir del tema 05 se agregará:

* Repositorios (Spring Data JPA, TypeORM)
* Base de datos real (PostgreSQL)
* DTOs más completos
* Validaciones avanzadas
* Persistencia transaccional

Los servicios serán responsables de coordinar todo esto.


# Resultados Esperados

Al finalizar este tema, el estudiante comprende:

* la diferencia entre controlador y servicio
* cómo fluye una petición dentro del backend
* qué capa debe contener cada responsabilidad
* qué es la inyección de dependencias
* por qué separar lógica de negocio
* cómo se prepara el sistema para usar repositorios y bases de datos

Este conocimiento será aplicado directamente en:

* [`spring-boot/04_servicios.md`](../spring-boot/p67/a_dodente/04_servicios.md)

* [`nest/04_servicios.md`](../nest/p67/a_dodente/04_servicios.md)

