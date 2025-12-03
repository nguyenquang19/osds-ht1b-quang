import sqlite3

#1. Kết nối đến cơ sở dữ liệu

conn = sqlite3.connect('inventory.db')

# Tạo đối tượng cursor để thực thi các lệnh SQL
cursor = conn.cursor()

#2. Thao tác với Database và Table

# Lệnh Sql để tạo bảng products
sql1 = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price NUMERIC NOT NULL,
    quantity INTEGER NOT NULL
)
"""

# Thực thi câu lệnh tạo bảng
cursor.execute(sql1)
conn.commit() #Lưu thay đổi vào db

#3. CRUD
#3.1. Thêm (INSERT)
products_data = [
    ('Laptop A100', 999.99, 15),
    ('Mouse Wireless', 25.50, 50),
    ('Monitor 24 inch', 150.00, 20)
]
# Lệnh SQL để chèn dữ liệu
sql2 = """
INSERT INTO products (name, price, quantity)
VALUES (?, ?, ?)
"""

#Thêm nhiều bản ghi cùng lúc
cursor.executemany(sql2, products_data)
conn.commit() #Lưu thay đổi vào db

#3.2 READ (SELECT)
sql3 = "SELECT * FROM products"

# Thực thi truy vấn
cursor.execute(sql3)

# Lấy tất cả kết quả
all_products = cursor.fetchall()

# In tiêu đề
print(f"{'ID':<5} {'Name':<20} {'Price':<10} {'Quantity':<10}")

# Lặp và in ra
for p in all_products:
    print(f"{p[0]:<5} {p[1]:<20} {p[2]:<10} {p[3]:<10}")    
    
#3.3 UPDATE
sql4 = """
UPDATE products
SET price = ?, quantity = ?
WHERE id = ?
"""
cursor.execute(sql4, (999.00, 10, 1))
conn.commit()
print("\nSau khi UPDATE id = 1:")
cursor.execute(sql3)
for p in cursor.fetchall():
    print(f"{p[0]:<4} | {p[1]:<20} | {p[2]:<10} | {p[3]:<10}")

# 3.4 DELETE (Xóa dữ liệu)
# Ví dụ: xóa sản phẩm có id = 2
sql5 = "DELETE FROM products WHERE id = ?"
cursor.execute(sql5, (2,))
conn.commit()

print("\nSau khi DELETE id = 2:")
cursor.execute(sql3)
for p in cursor.fetchall():
    print(f"{p[0]:<4} | {p[1]:<20} | {p[2]:<10} | {p[3]:<10}")