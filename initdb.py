import pymysql

# 数据库连接信息
host = 'localhost'
user = 'root'
password = '123456'  # 更新为你的数据库密码
database = 'eduDB'

# 创建连接
conn = pymysql.connect(host=host, user=user, password=password, database=database)
cursor = conn.cursor()

# SQL语句创建表
create_student_table = """
CREATE TABLE IF NOT EXISTS STUDENT (
    username VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(20)
);
"""

create_institution_table = """
CREATE TABLE IF NOT EXISTS INSTITUTION (
    username VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(20)
);
"""

create_admin_table = """
CREATE TABLE IF NOT EXISTS ADMIN (
    username VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL
);
"""

create_service_table = """
CREATE TABLE IF NOT EXISTS SERVICE (
    servicename VARCHAR(255),
    institution VARCHAR(255),
    dishinfo TEXT,
    nutriention TEXT,
    price DECIMAL(10, 2),
    sales INT DEFAULT 0,
    imagesrc VARCHAR(255),
    isSpecialty INT,
    PRIMARY KEY (servicename, institution),
    FOREIGN KEY (institution) REFERENCES INSTITUTION(username)
);
"""

create_order_comment_table = """
CREATE TABLE IF NOT EXISTS ORDER_COMMENT (
    orderID INT AUTO_INCREMENT PRIMARY KEY,
    institution VARCHAR(255),
    username VARCHAR(255),
    servicename VARCHAR(255),
    transactiontime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cost DECIMAL(10, 2),
    text TEXT,
    c_rank INT,
    isFinished INT,
    FOREIGN KEY (institution) REFERENCES INSTITUTION(username),
    FOREIGN KEY (username) REFERENCES STUDENT(username)
);
"""

create_shopping_cart_table = """
CREATE TABLE IF NOT EXISTS SHOPPINGCART (
    username VARCHAR(255),
    institution VARCHAR(255),
    servicename VARCHAR(255),
    price DECIMAL(10, 2),
    imagesrc VARCHAR(255),
    PRIMARY KEY (username, servicename, institution),
    FOREIGN KEY (username) REFERENCES STUDENT(username),
    FOREIGN KEY (institution) REFERENCES INSTITUTION(username)
);
"""

# 执行SQL语句
try:
    cursor.execute(create_student_table)
    cursor.execute(create_institution_table)
    cursor.execute(create_admin_table)
    cursor.execute(create_service_table)
    cursor.execute(create_order_comment_table)
    cursor.execute(create_shopping_cart_table)
    conn.commit()  # 提交事务
    print("All tables created successfully")
except pymysql.Error as e:
    print("Failed to create tables:", e)
    conn.rollback()  # 回滚事务


# 添加一个管理员账号的过程
try:
    # 先检查用户名是否已存在
    check_user_query = "SELECT * FROM ADMIN WHERE username = %s"
    cursor.execute(check_user_query, ('admin',))
    if cursor.fetchone() is None:
        # 如果不存在，执行插入操作
        add_admin_query = "INSERT INTO ADMIN (username, password) VALUES (%s, %s)"
        cursor.execute(add_admin_query, ('admin', 'admin123'))  # Example username and password
        conn.commit()  # 提交事务
        print("Administrator added successfully")
    else:
        print("Administrator already exists, not added.")
except pymysql.Error as e:
    print("Failed to add administrator:", e)
    conn.rollback()  # 出错则回滚


# 关闭连接
cursor.close()
conn.close()

# # 创建连接
# conn = pymysql.connect(host=host, user=user, password=password, database=database)
# cursor = conn.cursor()


# finally:
#     cursor.close()
#     conn.close()
