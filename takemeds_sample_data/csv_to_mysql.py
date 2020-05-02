# Make sure that all tables are empty before running the script

import csv
import MySQLdb
import os

database = MySQLdb.connect(user = os.environ["DB_USER"], passwd = os.environ["DB_PASS"], db = "stores")
db = database.cursor()

tables = ["all_stores", "generic_medicine", "brand_medicine", "store_to_generic", "brand_store"]


for t in tables:
    file_name = t + ".csv"
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        fields = next(csv_reader)
        #print(fields)
        for row in csv_reader:
            value_string = " ".join(["%s, " for _ in range(len(row))]).strip(', ')
            insert_data = '(' + value_string + ')'
            query_string = "insert into " + t + " values " + insert_data
            query_data = []
            for z in row:
                try:
                    query_data.append(int(z))
                except:
                    query_data.append(z)
            query_data = tuple(query_data)
            print(query_string, query_data)
            db.execute(query_string, query_data)
        database.commit()
