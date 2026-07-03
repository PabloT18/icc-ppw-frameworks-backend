-- =========================
-- 5. Verificación
-- =========================

select count(*) as total_users
  from users;

select count(*) as total_categories
  from category_entity;

select count(*) as total_products
  from products;

select count(*) as total_product_category_relations
  from product_categories;

select min(total_categories) as min_categories_per_product,
       max(total_categories) as max_categories_per_product,
       round(
          avg(total_categories),
          2
       ) as avg_categories_per_product
  from (
   select product_id,
          count(*) as total_categories
     from product_categories
    group by product_id
) t;