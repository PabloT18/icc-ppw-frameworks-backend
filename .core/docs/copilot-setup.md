# 🤖 Configuración de GitHub Copilot para Angular 20

## 📁 Archivos de Configuración Creados

### 1. `.copilot-instructions.md` (Raíz del proyecto)
**Ubicación:** `/proyecto/.copilot-instructions.md`

Este archivo contiene las instrucciones específicas para que GitHub Copilot entienda que debe sugerir código usando Angular 20+ con:
- ✅ **Standalone Components**
- ✅ **Signals** (`signal()`, `computed()`, `effect()`)
- ✅ **Nuevo Control Flow** (`@if`, `@for`, `@switch`)
- ✅ **Función `inject()`** para dependency injection
- ❌ **NO usar** NgModules, `*ngIf`, `*ngFor`, etc.

### 2. `.vscode/settings.json`
**Ubicación:** `/proyecto/.vscode/settings.json`

Configuraciones de VS Code específicas para:
- GitHub Copilot habilitado
- Angular Language Service
- TypeScript con preferencias modernas
- Formateo automático

## 🚀 Cómo Activar la Configuración

### Paso 1: Reiniciar VS Code
Después de crear los archivos, reinicia VS Code para que las configuraciones surtan efecto:

```bash
# Desde terminal (si tienes 'code' command)
code .

# O simplemente cierra y abre VS Code
```

### Paso 2: Verificar que Copilot Está Activo
1. Abre cualquier archivo `.ts` en el proyecto
2. Escribe un comentario como:
   ```typescript
   // Crear un componente Angular 20 con signals
   ```
3. Presiona `Enter` y Copilot debería sugerir código moderno

### Paso 3: Probar las Sugerencias
Escribe estos ejemplos y ve las sugerencias:

```typescript
// Componente standalone con signals
import { Component, signal } from '@angular/core';

@Component({
  selector: 'app-test',
  standalone: true,
  template: `
    // Copilot debería sugerir @if en lugar de *ngIf
  `
})
export class TestComponent {
  // Copilot debería sugerir signals
}
```

## 🎯 Ejemplos de Uso

### ✅ Lo que Copilot DEBE sugerir ahora:

#### 1. Componente Moderno
```typescript
import { Component, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-example',
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (isVisible()) {
      <h2>{{ title() }}</h2>
      @for (item of items(); track item.id) {
        <div>{{ item.name }}</div>
      }
    }
  `
})
export class ExampleComponent {
  isVisible = signal(true);
  title = signal('Mi Componente');
  items = signal([]);
}
```

#### 2. Control Flow Moderno
```html
<!-- Conditional -->
@if (user()) {
  <p>Bienvenido {{ user().name }}</p>
} @else {
  <p>Por favor inicia sesión</p>
}

<!-- Loop -->
@for (product of products(); track product.id) {
  <div>{{ product.name }} - {{ product.price }}</div>
} @empty {
  <p>No hay productos</p>
}

<!-- Switch -->
@switch (status()) {
  @case ('loading') {
    <div>Cargando...</div>
  }
  @case ('error') {
    <div>Error al cargar</div>
  }
  @default {
    <div>Contenido cargado</div>
  }
}
```

### ❌ Lo que Copilot NO debe sugerir:

```typescript
// ❌ NgModules
@NgModule({...})

// ❌ Directivas estructurales antiguas
*ngIf="condition"
*ngFor="let item of items"

// ❌ RxJS para estado simple
private subject = new BehaviorSubject([]);
```

## 🔧 Comandos Útiles

### Para probar que funciona:
```typescript
// Escribe esto y presiona Tab o Enter para ver sugerencias:

// Crear componente Angular 20 con signals
// Implementar lista de productos con @for
// Agregar condicional con @if
```

### Snippets disponibles en VS Code:
- `cfeat` → Commit de nueva funcionalidad
- `cfix` → Commit de corrección
- `cinit` → Commit de inicialización

## 📚 Recursos Adicionales

### Documentación Angular 20:
- [Angular Signals](https://angular.dev/guide/signals)
- [Control Flow](https://angular.dev/guide/templates/control-flow)
- [Standalone Components](https://angular.dev/guide/components/importing)

### Verificar que funciona:
1. **Escribe comentarios descriptivos** sobre lo que quieres hacer
2. **Usa prompts específicos** como "crear componente con signals"
3. **Verifica las sugerencias** - deben usar sintaxis Angular 20+

## 🎓 Para Estudiantes

Cuando trabajen en sus documentaciones y ejemplos:

1. **Siempre usar la nueva sintaxis** Angular 20
2. **Documentar las diferencias** con versiones anteriores
3. **Incluir ejemplos comparativos** en sus archivos .md
4. **Aprovechar Copilot** para aprender los nuevos patrones

---

**📝 Nota:** Si Copilot sigue sugiriendo sintaxis antigua, verifica que:
- Los archivos de configuración estén en las ubicaciones correctas
- VS Code se haya reiniciado
- El proyecto esté abierto desde la raíz donde está `.copilot-instructions.md`