# Script to create the schema

import MySQLdb
import os

# Database "stores" must exist in MySQL
database = MySQLdb.connect(user = os.environ['DB_USER'], passwd = os.environ['DB_PASS'], db = "stores")

db = database.cursor()

def create_all_stores():
    try:
        db.execute("""CREATE TABLE all_stores (store_id int, name varchar(50), address varchar(200), rating int, lat float(6, 3), lng float(6, 3), constraint pk PRIMARY KEY(store_id))""")
    except Exception as e:
        print(e, 1)
def create_generic_medicine():
    try:
        db.execute("""CREATE TABLE generic_medicine (name varchar(100), rating int, g_id int, constraint pk PRIMARY KEY (g_id))""")
    except Exception as e:
        print(e, 2)
def create_brand_medicine():
    try:    
        db.execute("""CREATE TABLE brand_medicine (name varchar(100), g_id int, b_id int, constraint pk PRIMARY KEY (b_id), constraint fk FOREIGN KEY (g_id) REFERENCES generic_medicine(g_id))""") 
    except Exception as e:
        print(e, 3)
def create_store_to_generic():
    try:
        db.execute("""CREATE TABLE store_to_generic (store_id int, g_id int, constraint pk PRIMARY KEY (store_id, g_id), constraint fkg FOREIGN KEY (g_id) REFERENCES generic_medicine(g_id), constraint fks FOREIGN KEY (store_id) REFERENCES all_stores(store_id))""")      
    except Exception as e:
        print(e, 4)
def create_brand_store():
    try:   
        db.execute(""" CREATE TABLE brand_store (b_id int, store_id int, constraint pk PRIMARY KEY (b_id, store_id), constraint fkb FOREIGN KEY (b_id) REFERENCES brand_medicine(b_id), constraint fkst FOREIGN KEY(store_id) REFERENCES all_stores(store_id))""")
    except Exception as e:
        print(e, 5)

def create_tables():
    generic_medicine = "generic_medicine"
    brand_medicine = "brand_medicine"
    store_to_generic = "store_to_generic"
    brand_store = "brand_store"
    all_stores = "all_stores"
    # Drop Tables if they already exist (Not working. Manually delete existing tables)
    all_tables = [store_to_generic, brand_store, brand_medicine, generic_medicine, all_stores]
    for table in all_tables:
        db.execute(""" SHOW TABLES LIKE %s""", (table,))
        result = db.fetchall()
        #print(result)
        if len(result) > 0:
            db.execute(""" DROP TABLE %s""", (table, ))
    create_all_stores()
    create_generic_medicine()
    create_brand_medicine()
    create_store_to_generic()
    create_brand_store()

create_tables()