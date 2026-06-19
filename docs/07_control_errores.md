# Programación y Plataformas Web

# **Frameworks Backend: Control Global de Errores y Excepciones**

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="80">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="80">
</div>

## Práctica 7: Control de Errores, Excepciones y Respuestas Uniformes en Backend

### Autores

**Pablo Torres**

 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: PabloT18


# Introducción

En los temas anteriores se ha trabajado con:

* controladores
* servicios
* DTOs
* validación
* modelos de dominio
* persistencia

Sin embargo, hasta este punto, **los errores aún no han sido tratados de forma centralizada**.
Esto provoca que cada controlador o servicio maneje errores de forma distinta, generando:

* respuestas inconsistentes
* mensajes poco claros para el cliente
* duplicación de código
* dificultad para escalar y mantener la API

En este tema se introduce el **control global de errores**, un componente esencial de cualquier backend profesional, cuyo objetivo es garantizar que **todas las excepciones del sistema produzcan respuestas coherentes, predecibles y controladas**.

Este documento aborda **los conceptos generales**, independientes del framework o lenguaje.


# 1 ¿Qué es un error en un backend?

En un backend, un error representa una **interrupción del flujo normal de ejecución** debido a una condición no válida.

No todos los errores son iguales:

* Algunos son **esperados**
* Otros indican **fallos del sistema**
* Otros representan **violaciones de reglas de negocio**

Un backend profesional **no debe exponer errores crudos**, stacktraces ni mensajes internos al cliente.


# 2 Error vs Excepción

* **Error**: situación no válida desde el punto de vista de la aplicación
* **Excepción**: mecanismo técnico para propagar ese error

El error es conceptual.
La excepción es la herramienta para comunicarlo internamente.


# 3 Tipos de errores a nivel de aplicación

Desde la perspectiva de diseño, los errores se clasifican en:

### Errores de validación

* DTO inválido
* Campos obligatorios ausentes
* Formatos incorrectos

### Errores de negocio

* Reglas violadas
* Estados no permitidos
* Conflictos lógicos

### Errores técnicos

* Fallos de base de datos
* Servicios externos no disponibles
* Errores inesperados

Cada tipo **debe tratarse de forma distinta**, aunque todos deben producir **respuestas con el mismo formato**.


# 4 Respuesta de error uniforme

Un backend profesional **no devuelve mensajes arbitrarios**.

Toda respuesta de error debe seguir un **contrato fijo**, independiente del origen del error.

Campos recomendados:

* timestamp
* status
* error
* message
* path

Esto permite que:

* el frontend consuma errores sin lógica especial
* los errores sean predecibles
* el contrato de la API sea estable


# 5 Por qué evitar try/catch dispersos

Manejar errores con `try/catch` en cada controlador o servicio provoca:

* duplicación de código
* control inconsistente
* errores olvidados
* difícil mantenimiento

La solución correcta es **un manejo centralizado**, donde:

* los servicios lanzan excepciones
* un componente global las captura
* la respuesta se construye en un solo lugar


# 6 Excepciones personalizadas

Usar excepciones genéricas es una mala práctica.

Cada error relevante del dominio debe expresarse mediante:

* una excepción específica
* un mensaje claro
* un significado semántico

Ejemplos conceptuales:

* Recurso no encontrado
* Regla de negocio violada
* Operación no permitida
* Estado inconsistente

Las excepciones **no representan errores técnicos**, representan **intenciones del dominio**.


# 7 Control global de excepciones

El control global consiste en:

* interceptar cualquier excepción lanzada
* identificar su tipo
* transformarla en una respuesta uniforme

Beneficios:

* los controladores quedan limpios
* los servicios se enfocan en negocio
* el backend es coherente
* el frontend no depende de mensajes arbitrarios


# 8 Validación y errores

La validación genera errores que **no son fallos del sistema**, sino problemas de entrada.

Buenas prácticas:

* no mezclar validación con lógica de negocio
* devolver errores estructurados
* indicar claramente qué campos fallaron
* mantener el mismo formato de error


# 9 Logging y errores

No todos los errores deben loguearse como error crítico.

Principios básicos:

* errores de validación no son fallos del sistema
* errores de negocio son informativos
* errores técnicos deben registrarse
* nunca exponer información sensible al cliente

El logging debe servir para diagnóstico, no para contaminar la salida de la API.


# 10 Flujo completo de manejo de errores

```
Request
 ↓
Controller
 ↓
Service
 ↓
Excepción lanzada
 ↓
Handler global
 ↓
Respuesta de error uniforme
 ↓
Cliente
```

Este flujo desacopla completamente:

* lógica
* validación
* transporte
* presentación del error


# 11 Resultados esperados

Al finalizar este tema, el estudiante comprende:

* qué es un error a nivel de backend
* cómo diferenciar errores de validación, negocio y técnicos
* por qué se requieren excepciones personalizadas
* cómo funciona un control global de errores
* por qué la respuesta de error debe ser uniforme
* cómo se integra el manejo de errores en una arquitectura profesional


# 12 Aplicación directa en los siguientes módulos

Estos conceptos se aplicarán directamente en:

* [`spring-boot/07_control_errores.md`](../spring-boot/07_control_errores.md)
* [`nest/07_control_errores.md`](../nest/07_control_errores.md)

