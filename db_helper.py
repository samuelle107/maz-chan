import json
import mysql.connector
import os
from dotenv import load_dotenv


def insert(con: object, table_name: str, columns: list, values: list) -> bool:
    cur = con.cursor()
    
    try:
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({str(values).strip('[]')})"
        cur.execute(query)
        con.commit()
        cur.close()

        return cur.lastrowid
    except Exception as e:
        cur.close()
        return -1
    

def remove(con: object, table_name: str, column: str, value: any) -> bool:
    cur = con.cursor()

    try:
        query = f"DELETE FROM {table_name} where {column} = {json.dumps(value)}"
        cur.execute(query)
        con.commit()
        cur.close()

        return cur.rowcount
    except Exception as e:
        cur.close()
        return 0


def get(con: object, table_name: str, column: str, value: any) -> object:
    cur = con.cursor()

    try:
        query = f"SELECT * FROM {table_name} where {column} = {json.dumps(value)}"
        print(query)
        cur.execute(query)
        result = cur.fetchall()
        cur.close()

        return result
    except Exception as e:
        cur.close()
        return []


def get_all(con: object, table_name: str) -> list:
    cur = con.cursor()
    
    try:
        query = f"SELECT * FROM {table_name}"
        cur.execute(query)
        result = cur.fetchall()
        cur.close()

        return result
    except Exception as e:
        cur.close()
        return []


def does_exist(con: object, table_name: str, column: str, value: str) -> bool:
    cur = con.cursor()

    try:
        query = f"SELECT exists(SELECT * FROM {table_name} where {column} = {json.dumps(value)})"
        cur.execute(query)
        does_exist = bool(cur.fetchone()[0])
        cur.close()

        return does_exist
    except Exception as e:
        cur.close()
        return False

