import mysql.connector
from mysql.connector import Error

def connect_to_mysql():
    """Connect to MySQL database running in Docker"""
    try:
        # Connect to MySQL
        # host='localhost' because we're connecting from OUTSIDE Docker
        # port=3306 is exposed by Docker container
        connection = mysql.connector.connect(
            host='localhost',      # MySQL is in Docker, but we use localhost
            port=3306,             # Port exposed by Docker
            user='root',           # MySQL root user
            password='rootpassword',  # Password we set in docker-compose
            database='testdb'      # Database we'll create
        )
        
        if connection.is_connected():
            print("✅ Successfully connected to MySQL database!")
            print(f"📍 MySQL Server version: {connection.get_server_info()}")
            
            # Create a cursor to execute queries
            cursor = connection.cursor()
            
            # Create a simple table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    email VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ Table 'users' created successfully!")
            
            # Insert some data
            cursor.execute("""
                INSERT INTO users (name, email) 
                VALUES ('Alice', 'alice@example.com')
            """)
            connection.commit()
            print("✅ Inserted user: Alice")
            
            # Fetch all users
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            
            print("\n📊 All users in database:")
            print("-" * 50)
            for user in users:
                print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
            print("-" * 50)
            
            cursor.close()
            
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
    
    finally:
        if connection.is_connected():
            connection.close()
            print("\n✅ MySQL connection closed")

if __name__ == "__main__":
    print("🐍 Python Script (Running on your computer)")
    print("🐳 MySQL Database (Running in Docker)")
    print("=" * 50)
    connect_to_mysql()
