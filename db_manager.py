import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',          
            password='password',  
            database='bar_pos'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def add_category(category_name):
    conn = create_connection()
    cursor = conn.cursor()
    query = "INSERT INTO categories (name) VALUES (%s)"
    cursor.execute(query, (category_name,))
    conn.commit()
    print(f"Category '{category_name}' added successfully.")
    conn.close()

# Let's test it by adding your initial categories
if __name__ == "__main__":
    add_category("Bitters")
    add_category("Beer")
    add_category("Soft Drinks")