
## 4.1 REST (Representational State Transfer)

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg" width="50" alt="Spring Logo">
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nestjs/nestjs-original.svg" width="50" alt="Nest Logo"/>
        
</div>

Eejemplo de arquitectura backend basada en REST para la gestión de productos en una tienda en línea.

Ejemplos practicos de cómo implementar un servidor REST y cómo consumirlo desde el cliente.

Desde servicores como Spring Boot (Java) o NestJS (TypeScript) hasta clientes en JavaScript usando Fetch API o Axios.



### Ejemplo de servidor REST (Spring Boot)

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {
    
    @Autowired
    private ProductService productService;
    
    // GET /api/products
    @GetMapping
    public List<Product> getAllProducts() {
        return productService.findAll();
    }
    
    // GET /api/products/5
    @GetMapping("/{id}")
    public Product getProduct(@PathVariable Long id) {
        return productService.findById(id);
    }
    
    // POST /api/products
    @PostMapping
    public Product createProduct(@RequestBody ProductDTO dto) {
        return productService.create(dto);
    }
    
    // PUT /api/products/5
    @PutMapping("/{id}")
    public Product updateProduct(@PathVariable Long id, @RequestBody ProductDTO dto) {
        return productService.update(id, dto);
    }
    
    // DELETE /api/products/5
    @DeleteMapping("/{id}")
    public void deleteProduct(@PathVariable Long id) {
        productService.delete(id);
    }
}
```

### Ejemplo de servidor REST (NestJS)

```typescript
@Controller('products')
export class ProductController {
    constructor(private readonly productService: ProductService) {}
    
    @Get()
    async getAllProducts(): Promise<Product[]> {
        return this.productService.findAll();
    }
    
    @Get(':id')
    async getProduct(@Param('id') id: string): Promise<Product> {
        return this.productService.findById(+id);
    }
    
    @Post()
    async createProduct(@Body() dto: CreateProductDto): Promise<Product> {
        return this.productService.create(dto);
    }
    
    @Put(':id')
    async updateProduct(
        @Param('id') id: string,
        @Body() dto: UpdateProductDto
    ): Promise<Product> {
        return this.productService.update(+id, dto);
    }
    
    @Delete(':id')
    async deleteProduct(@Param('id') id: string): Promise<void> {
        return this.productService.delete(+id);
    }
}
```

### Cómo consumir API REST desde el cliente

#### **JavaScript/TypeScript (Frontend)**

```javascript
// GET - Obtener todos los productos
fetch('http://localhost:3000/api/products')
    .then(response => response.json())
    .then(products => console.log(products))
    .catch(error => console.error(error));

// GET - Obtener un producto específico
fetch('http://localhost:3000/api/products/5')
    .then(response => response.json())
    .then(product => console.log(product));

// POST - Crear producto
fetch('http://localhost:3000/api/products', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer token123'
    },
    body: JSON.stringify({
        name: 'Laptop HP',
        price: 899.99,
        stock: 15
    })
})
    .then(response => response.json())
    .then(newProduct => console.log('Creado:', newProduct));

// PUT - Actualizar producto completo
fetch('http://localhost:3000/api/products/5', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        name: 'Laptop HP Actualizada',
        price: 799.99,
        stock: 20
    })
})
    .then(response => response.json())
    .then(updated => console.log('Actualizado:', updated));

// PATCH - Actualizar parcialmente
fetch('http://localhost:3000/api/products/5', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        stock: 25  // Solo actualizar stock
    })
})
    .then(response => response.json())
    .then(updated => console.log('Stock actualizado:', updated));

// DELETE - Eliminar producto
fetch('http://localhost:3000/api/products/5', {
    method: 'DELETE'
})
    .then(response => {
        if (response.ok) {
            console.log('Producto eliminado');
        }
    });
```

#### **Usando Axios (más moderno)**

```javascript
import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:3000/api',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer token123'
    }
});

// GET
const products = await api.get('/products');
console.log(products.data);

// POST
const newProduct = await api.post('/products', {
    name: 'Laptop HP',
    price: 899.99
});

// PUT
const updated = await api.put('/products/5', {
    name: 'Laptop HP Pro',
    price: 999.99
});

// DELETE
await api.delete('/products/5');
```

#### **cURL (Línea de comandos)**

```bash
# GET
curl http://localhost:3000/api/products

# GET específico
curl http://localhost:3000/api/products/5

# POST
curl -X POST http://localhost:3000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop HP","price":899.99}'

# PUT
curl -X PUT http://localhost:3000/api/products/5 \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop Updated","price":799.99}'

# DELETE
curl -X DELETE http://localhost:3000/api/products/5
```

#### **Postman / Bruno**

```
Method: GET
URL: http://localhost:3000/api/products
Headers:
  - Content-Type: application/json
  - Authorization: Bearer token123
```

** Cuándo usar REST**:
- APIs públicas y privadas
- Aplicaciones web y móviles
- CRUD tradicional
- Sistemas que requieren caché
- Integraciones simples