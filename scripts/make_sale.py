import mysql.connector

def record_sale(items, payment_type):
    # Import the connection helper from your app script
    from app import get_db_connection
    
    print("--- Initializing Transaction... ---")
    connection = get_db_connection()
    
    if not connection:
        print("!!! Error: Could not connect to database using config settings.")
        return

    try:
        cursor = connection.cursor()
        connection.start_transaction()

        total_amount = sum(item[2] for item in items)
        
        # 1. Create Sale Header
        sale_query = "INSERT INTO sales (total_amount, payment_type) VALUES (%s, %s)"
        cursor.execute(sale_query, (total_amount, payment_type))
        sale_id = cursor.lastrowid
        print(f"Created Sale ID: {sale_id}")

        # 2. Process Items
        item_insert_query = "INSERT INTO sale_items (sale_id, product_id, quantity, subtotal) VALUES (%s, %s, %s, %s)"
        
        for item in items:
            p_id, qty, subtotal = item[0], item[1], item[2]
            
            # Record item detail
            cursor.execute(item_insert_query, (sale_id, p_id, qty, subtotal))

            # Deduct Inventory
            cursor.execute("SELECT tracking_type, product_name FROM products WHERE id = %s", (p_id,))
            res = cursor.fetchone()
            
            if res:
                tracking_type, p_name = res[0], res[1]
                # If tracking by ML, deduct 30ml per shot. Otherwise, deduct 1 unit.
                deduction = 30.0 * qty if tracking_type == 'ML' else 1.0 * qty
                
                cursor.execute("UPDATE inventory SET quantity_on_hand = quantity_on_hand - %s WHERE product_id = %s", 
                               (deduction, p_id))
                print(f"Deducted {deduction} from {p_name}")
            else:
                print(f"Warning: Product ID {p_id} not found!")

        connection.commit()
        print("--- Success: Transaction Committed to Database ---")

    except Exception as e:
        print(f"!!! CRITICAL ERROR: {e}")
        if connection:
            connection.rollback()
            print("--- Transaction Rolled Back ---")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("--- Connection Closed ---")

# For testing independently
if __name__ == "__main__":
    print("Starting Sale Script Test...")
    test_order = [
        (4, 1, 5.00), 
        (5, 1, 5.00)
    ]
    record_sale(test_order, 'MoMo')