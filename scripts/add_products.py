import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',         # Ensure this matches your SQLTools user
        password='password', # Ensure this matches your SQLTools password
        database='bar_pos_system' 
    )

def add_item(name, category_id, price, is_shot):
    conn = get_connection()
    cursor = conn.cursor()
    
    # query to insert product
    query = "INSERT INTO products (product_name, category_id, price, is_shot) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, category_id, price, is_shot))
    
    conn.commit()
    print(f"Added: {name}")
    conn.close()

# Let's add your specific Ghana stock
# Categories: 1=Bitters, 2=Beer, 3=Soft Drinks (Ensure these exist in your categories table)
if __name__ == "__main__":
    # 1. Top Selling Shots (Bitters)
    add_item("Alomo Bitters (Shot)", 1, 5.00, True)   # Example price 5 GHS
    add_item("Trigger (Shot)", 1, 5.00, True)
    add_item("Dates Bitters (Shot)", 1, 5.00, True)
    
    # 2. Top Selling Beer
    add_item("Club Beer", 2, 15.00, False)
    add_item("Heineken", 2, 20.00, False)
    add_item("Smirnoff Ice", 2, 15.00, False)
    
    # 3. Soft Drinks
    add_item("Malta Guinness", 3, 10.00, False)
    add_item("BB Cocktail", 3, 8.00, False)