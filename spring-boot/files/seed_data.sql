BEGIN;

-- Limpieza previa

TRUNCATE TABLE product_categories RESTART IDENTITY CASCADE;
TRUNCATE TABLE products RESTART IDENTITY CASCADE;
TRUNCATE TABLE category_entity RESTART IDENTITY CASCADE;
TRUNCATE TABLE users RESTART IDENTITY CASCADE;

-- =========================
-- 1. Crear 10 usuarios
-- =========================

INSERT INTO users (
    name,
    email,
    password_hash,
    created_at,
    updated_at,
    deleted
)
SELECT
    'Usuario ' || gs,
    'usuario' || gs || '@ups.edu.ec',
    'HASH_12345678',
    NOW(),
    NOW(),
    false
FROM generate_series(1, 10) AS gs;

-- =========================
-- 2. Crear 10 categorías
-- =========================

INSERT INTO category_entity (
    name,
    description,
    created_at,
    updated_at,
    deleted
)
VALUES
('Electrónicos', 'Productos electrónicos', NOW(), NOW(), false),
('Gaming', 'Productos para videojuegos', NOW(), NOW(), false),
('Oficina', 'Productos para oficina', NOW(), NOW(), false),
('Libros', 'Libros y material académico', NOW(), NOW(), false),
('Programación', 'Material relacionado con desarrollo de software', NOW(), NOW(), false),
('Educación', 'Productos educativos', NOW(), NOW(), false),
('Accesorios', 'Accesorios tecnológicos', NOW(), NOW(), false),
('Diseño', 'Productos para diseño gráfico', NOW(), NOW(), false),
('Redes', 'Equipos y accesorios de redes', NOW(), NOW(), false),
('Audio', 'Dispositivos de audio', NOW(), NOW(), false);

-- =========================
-- 3. Crear 20 000 productos
-- =========================

INSERT INTO products (
    name,
    price,
    stock,
    user_id,
    created_at,
    updated_at,
    deleted
)
SELECT
    'Producto ' || LPAD(gs::text, 5, '0'),
    ROUND((10 + random() * 4990)::numeric, 2),
    FLOOR(random() * 101)::int,
    (
        SELECT u.id
        FROM users u
        WHERE u.deleted = false
        ORDER BY random() + gs * 0
        LIMIT 1
    ),
    NOW(),
    NOW(),
    false
FROM generate_series(1, 20000) AS gs;

-- =========================
-- 4. Asociar 2 o 3 categorías por producto
-- =========================

INSERT INTO product_categories (
    product_id,
    category_id
)
SELECT
    p.id,
    c.id
FROM products p
CROSS JOIN LATERAL (
    SELECT ce.id
    FROM category_entity ce
    WHERE ce.deleted = false
    ORDER BY random() + p.id * 0
    LIMIT (2 + FLOOR(random() * 2))::int
) c;

COMMIT;

