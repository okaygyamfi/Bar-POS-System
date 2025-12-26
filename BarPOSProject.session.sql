SELECT p.product_name, i.quantity_on_hand 
FROM products p
JOIN inventory i ON p.id = i.product_id;