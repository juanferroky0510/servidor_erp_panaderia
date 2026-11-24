import mysql.connector
from mysql.connector import Error

class Database:
    @staticmethod
    def conectar():
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                database="erp_panaderia",
                user="root",
                password="1234"
            )
            if conexion.is_connected():
                return conexion
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None