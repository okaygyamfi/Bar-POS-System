import configparser
import mysql.connector
from backup_db import run_backup
from make_sale import record_sale 

# Load the configuration from the file
config = configparser.ConfigParser()
config.read('config.ini')

def get_db_connection():
    try:
        return mysql.connector.connect(
            host=config['mysql']['host'],
            user=config['mysql']['user'],
            password=config['mysql']['password'],
            database=config['mysql']['database']
        )
    except Exception as e:
        print(f"Connection Error: Check your config.ini file settings. {e}")
        return None

def main_menu():
    while True:
        print("\n================================")
        print("   BAR POS: AKROPONG BRANCH     ")
        print("================================")
        print("1. Make a Sale")
        print("2. Check Stock Levels")
        print("3. End-of-Day Report")
        print("4. Restock Existing Items")
        print("5. Add BRAND NEW Product")
        print("6. Update Product Price")  
        print("7. View Sales History")
        print("8. Monthly Performance Report")
        print("9. Void/Delete Sale")
        print("10. Exit & Backup")
        
        choice = input("\nSelect: ")
        if choice == '1': process_customer_order()
        elif choice == '2': show_stock()
        elif choice == '3': show_daily_report()
        elif choice == '4': add_stock()
        elif choice == '5': add_new_product_to_system()
        elif choice == '6': update_product_price()
        elif choice == '7': view_sales_history()
        elif choice == '8': show_monthly_performance() 
        elif choice == '9': void_sale()
        elif choice == '10':
            print("Running closing backup...")
            run_backup() 
            print("System Closed Safely.")
            break

def void_sale():
    print("\n--- VOID/CANCEL A SALE ---")
    try:
        s_id = int(input("Enter Sale ID to void: "))
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor()

        cursor.execute("SELECT product_id, quantity FROM sale_items WHERE sale_id = %s", (s_id,))
        items = cursor.fetchall()

        if not items:
            print("!!! Sale ID not found.")
            return

        confirm = input(f"Are you sure you want to void Sale #{s_id} and return items to stock? (y/n): ").lower()
        if confirm == 'y':
            for p_id, qty in items:
                cursor.execute("UPDATE inventory SET quantity_on_hand = quantity_on_hand + %s WHERE product_id = %s", (qty, p_id))
            
            cursor.execute("DELETE FROM sales WHERE id = %s", (s_id,))
            conn.commit()
            print(f"--- Sale #{s_id} successfully voided. Stock restored. ---")
        
        conn.close()
    except Exception as e:
        print(f"Error voiding sale: {e}")

def show_monthly_performance():
    print("\n--- MONTHLY PERFORMANCE REPORT ---")
    month = input("Enter Month (01-12): ")
    year = input("Enter Year (e.g., 2025): ")
    
    try:
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor()

        query = """
        SELECT p.product_name, SUM(si.quantity) as total_qty, SUM(si.subtotal) as total_revenue
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        JOIN sales s ON si.sale_id = s.id
        WHERE MONTH(s.sale_date) = %s AND YEAR(s.sale_date) = %s
        GROUP BY p.product_name
        ORDER BY total_revenue DESC
        """
        
        cursor.execute(query, (month, year))
        results = cursor.fetchall()

        if not results:
            print(f"\nNo sales data found for {month}/{year}.")
        else:
            print(f"\nReport for {month}/{year}")
            print(f"{'Product':<25} | {'Qty Sold':<10} | {'Revenue'}")
            print("-" * 50)
            
            grand_total = 0
            for row in results:
                print(f"{row[0]:<25} | {row[1]:<10} | GHS {row[2]:.2f}")
                grand_total += row[2]
            
            print("-" * 50)
            print(f"TOTAL MONTHLY REVENUE: GHS {grand_total:.2f}")

        conn.close()
    except Exception as e:
        print(f"Error: {e}")

def view_sales_history():
    print("\n--- SALES HISTORY ---")
    print("1. View Last 10 Sales")
    print("2. Search by Specific Date (YYYY-MM-DD)")
    
    choice = input("Select option: ")
    query = ""
    param = None
    
    if choice == '1':
        query = "SELECT id, sale_date, total_amount, payment_type FROM sales ORDER BY sale_date DESC LIMIT 10"
    elif choice == '2':
        target_date = input("Enter date (e.g., 2023-10-25): ")
        query = "SELECT id, sale_date, total_amount, payment_type FROM sales WHERE DATE(sale_date) = %s ORDER BY sale_date DESC"
        param = (target_date,)
    else:
        print("Invalid choice.")
        return

    try:
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor()

        if param:
            cursor.execute(query, param)
        else:
            cursor.execute(query)
            
        sales = cursor.fetchall()

        if not sales:
            print("\n!!! No sales records found for that selection.")
            return

        for sale in sales:
            s_id, s_date, s_total, s_pay = sale
            print(f"\n[SALE #{s_id}] | Time: {s_date} | Total: GHS {s_total:.2f} | Paid: {s_pay}")
            
            cursor.execute("""
                SELECT p.product_name, si.quantity, si.subtotal 
                FROM sale_items si 
                JOIN products p ON si.product_id = p.id 
                WHERE si.sale_id = %s
            """, (s_id,))
            
            for item in cursor.fetchall():
                print(f"  > {item[0]} x{item[1]} (GHS {item[2]:.2f})")
            print("-" * 45)

        conn.close()
    except Exception as e:
        print(f"Error: {e}")

def update_product_price():
    print("\n--- UPDATE PRODUCT PRICE ---")
    try:
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor()

        p_id = int(input("Enter Product ID to update: "))
        cursor.execute("SELECT product_name, price FROM products WHERE id = %s", (p_id,))
        product = cursor.fetchone()

        if product:
            p_name, old_price = product[0], product[1]
            print(f"\nProduct: {p_name}")
            print(f"Current Price: GHS {old_price:.2f}")
            
            new_price = float(input(f"Enter New Price for {p_name}: "))
            confirm = input(f"Change {p_name} from GHS {old_price:.2f} to GHS {new_price:.2f}? (y/n): ").lower()
            
            if confirm == 'y':
                cursor.execute("UPDATE products SET price = %s WHERE id = %s", (new_price, p_id))
                conn.commit()
                print(f"--- Success! Price updated to GHS {new_price:.2f} ---")
            else:
                print("Update cancelled.")
        else:
            print("!!! Product ID not found.")

        conn.close()
    except Exception as e:
        print(f"Error: {e}")

def process_customer_order():
    print("\n--- AVAILABLE PRODUCTS ---")
    print(f"{'ID':<4} | {'Product Name':<25} | {'Price'}")
    print("-" * 40)
    
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("SELECT id, product_name, price FROM products")
    for row in cursor.fetchall():
        print(f"{row[0]:<4} | {row[1]:<25} | GHS {row[2]}")
    conn.close()

    order_items = []
    print("\n--- Current Sale ---")
    
    while True:
        try:
            p_id = int(input("Enter Product ID (or 0 to finish): "))
            if p_id == 0: break
            qty = int(input("Enter Quantity: "))
            
            price = get_product_price(p_id)
            if price:
                subtotal = price * qty
                order_items.append((p_id, qty, subtotal))
                print(f"Added: {qty} unit(s). Subtotal: GHS {subtotal}")
            else:
                print("!!! Product ID not found.")
        except ValueError:
            print("!!! Invalid input.")

    if order_items:
        pay_type = input("Payment Method (Cash/MoMo): ").strip()
        record_sale(order_items, pay_type)

def get_product_price(p_id):
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM products WHERE id = %s", (p_id,))
    res = cursor.fetchone()
    conn.close()
    return res[0] if res else None

def show_stock():
    print("\n--- INVENTORY STATUS (Akropong Branch) ---")
    try:
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor()
        
        query = "SELECT p.product_name, p.tracking_type, i.quantity_on_hand, p.total_volume_ml FROM products p JOIN inventory i ON p.id = i.product_id"
        cursor.execute(query)
        results = cursor.fetchall()

        print(f"{'Product':<25} | {'Stock Status':<20} | {'Alert'}")
        print("-" * 65)

        for row in results:
            name, track_type, qty, vol = row[0], row[1], row[2], row[3]
            alert = ""
            if track_type == 'ML':
                status = f"{int(qty // vol)} Bot ({int(qty % vol)} ML)"
                if qty < 375: alert = "!!! LOW STOCK (Refill Soon)"
            else:
                status = f"{int(qty)} Bottle(s)"
                if qty < 5: alert = "!!! LOW STOCK (Restock)"

            print(f"{name:<25} | {status:<20} | {alert}")
        conn.close()
    except Exception as e:
        print(f"Error checking stock: {e}")

def add_stock():
    print("\n--- RESTOCK INVENTORY (Akropong Branch) ---")
    try:
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor()
        p_id = int(input("Enter Product ID to restock: "))
        cursor.execute("SELECT product_name, tracking_type FROM products WHERE id = %s", (p_id,))
        product = cursor.fetchone()

        if product:
            p_name, track_type = product[0], product[1]
            if track_type == 'ML':
                num_bottles = int(input(f"How many NEW full bottles of {p_name}? "))
                amount_to_add = num_bottles * 750
            else:
                amount_to_add = int(input(f"How many NEW bottles of {p_name}? "))

            cursor.execute("UPDATE inventory SET quantity_on_hand = quantity_on_hand + %s WHERE product_id = %s", (amount_to_add, p_id))
            conn.commit()
            print("--- Restock Successful! ---")
        else:
            print("!!! Product ID not found.")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

def add_new_product_to_system():
    print("\n--- ADD NEW PRODUCT (Akropong Branch) ---")
    try:
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor()

        name = input("Enter Product Name: ")
        price = float(input("Enter Price (GHS): "))
        is_shot = input("Is this sold as shots? (yes/no): ").lower() == 'yes'
        track_type, vol, cat = ('ML', 750, 1) if is_shot else ('UNIT', None, int(input("Category (2 for Beer, 3 for Soft): ")))

        cursor.execute("INSERT INTO products (product_name, price, is_shot, total_volume_ml, category_id, tracking_type) VALUES (%s, %s, %s, %s, %s, %s)", (name, price, is_shot, vol, cat, track_type))
        cursor.execute("INSERT INTO inventory (product_id, quantity_on_hand) VALUES (%s, 0)", (cursor.lastrowid,))
        conn.commit()
        print(f"--- Success! {name} added ---")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

def show_daily_report():
    print("\n--- DAILY SALES SUMMARY ---")
    try:
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor()
        query = "SELECT payment_type, COUNT(*), SUM(total_amount) FROM sales WHERE DATE(sale_date) = CURDATE() GROUP BY payment_type"
        cursor.execute(query)
        results = cursor.fetchall()
        
        if not results:
            print("No sales recorded today.")
        else:
            grand_total = 0
            print(f"{'Method':<10} | {'Sales':<12} | {'Total Revenue'}")
            print("-" * 40)
            for row in results:
                print(f"{row[0]:<10} | {row[1]:<12} | GHS {row[2]:.2f}")
                grand_total += row[2]
            print(f"GRAND TOTAL: GHS {grand_total:.2f}")
        conn.close()
    except Exception as e:
        print(f"Error generating report: {e}")

if __name__ == "__main__":
    main_menu()