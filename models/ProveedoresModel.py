from config.database import Database

class ProveedoresModel:
    def insertar_proveedor(self, datos):
        conexion = Database.conectar()
        if not conexion:
            return {"ban": "-1", "msg": "No se pudo conectar a la base de datos.", "datos": None}

        try:
            cursor = conexion.cursor(dictionary=True)
            parametros = [
                datos.get("idEmpleado"),
                datos.get("nombreProv"),
                datos.get("correoProv"),
                datos.get("telefonoProv"),
                datos.get("rfc"),
                datos.get("pais"),
                datos.get("estado"),
                datos.get("municipio"),
                datos.get("calle"),
                datos.get("tiempoEntregaDias")
            ]
            cursor.callproc("spInsertarProveedor", parametros)
            conexion.commit()

            resultado = None
            for result in cursor.stored_results():
                resultado = result.fetchone()

            if resultado:
                ban = resultado.pop("ban")
                msg = resultado.pop("msg")
                return {"ban": ban, "msg": msg, "datos": resultado if ban == "1" else None}
            return {"ban": "0", "msg": "No se obtuvo respuesta del procedimiento.", "datos": None}

        except Exception as e:
            conexion.rollback()
            return {"ban": "-1", "msg": f"Error al insertar proveedor: {str(e)}", "datos": None}
        finally:
            cursor.close()
            conexion.close()

    def actualizar_proveedor(self, datos):
        conexion = Database.conectar()
        if not conexion:
            return {"ban": "-1", "msg": "No se pudo conectar a la base de datos.", "datos": None}

        try:
            cursor = conexion.cursor(dictionary=True)
            parametros = [
                datos.get("idEmpleado"),
                datos.get("idProveedor"),
                datos.get("nombreProv"),
                datos.get("correoProv"),
                datos.get("telefonoProv"),
                datos.get("rfc"),
                datos.get("pais"),
                datos.get("estado"),
                datos.get("municipio"),
                datos.get("calle"),
                datos.get("tiempoEntregaDias"),
                datos.get("estadoProveedor")
            ]
            cursor.callproc("spActualizarProveedor", parametros)
            conexion.commit()

            resultado = None
            for result in cursor.stored_results():
                resultado = result.fetchone()

            if resultado:
                ban = resultado.pop("ban")
                msg = resultado.pop("msg")
                return {"ban": ban, "msg": msg, "datos": resultado if ban == "1" else None}
            return {"ban": "0", "msg": "No se obtuvo respuesta del procedimiento.", "datos": None}

        except Exception as e:
            conexion.rollback()
            return {"ban": "-1", "msg": f"Error al actualizar proveedor: {str(e)}", "datos": None}
        finally:
            cursor.close()
            conexion.close()
    
    def reporte_proveedores(self, solo_activos=False):
        conexion = Database.conectar()
        if not conexion:
            return {"ban": "-1", "msg": "No se pudo conectar a la base de datos.", "datos": []}

        try:
            cursor = conexion.cursor(dictionary=True)
            if solo_activos:
                cursor.execute("SELECT * FROM vwRptProveedor WHERE estadoProveedor = 'ACTIVO'")
            else:
                cursor.execute("SELECT * FROM vwRptProveedor")

            registros = cursor.fetchall()
            return {
                "ban": "1",
                "msg": f"Se encontraron {len(registros)} proveedores.",
                "datos": registros
            }
        except Exception as e:
            return {"ban": "-1", "msg": f"Error al consultar proveedores: {str(e)}", "datos": []}
        finally:
            cursor.close()
            conexion.close()

    def buscar_proveedor(self, busqueda):
        conexion = Database.conectar()
        if not conexion:
            return {"ban": "-1", "msg": "No se pudo conectar a la base de datos.", "datos": []}

        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.callproc("spBuscarProveedor", [busqueda])

            filas = []
            for result in cursor.stored_results():
                filas = result.fetchall()

            if filas and filas[0].get("ban") == "1":
                ban = filas[0]["ban"]
                msg = filas[0]["msg"]
                # Limpiar las columnas ban y msg de cada objeto de datos
                for fila in filas:
                    fila.pop("ban", None)
                    fila.pop("msg", None)
                return {"ban": ban, "msg": msg, "datos": filas}
            elif filas:
                return {"ban": filas[0].get("ban", "0"), "msg": filas[0].get("msg", "Sin resultados."), "datos": []}
            else:
                return {"ban": "0", "msg": "No se encontraron resultados.", "datos": []}

        except Exception as e:
            return {"ban": "-1", "msg": f"Error al buscar proveedor: {str(e)}", "datos": []}
        finally:
            cursor.close()
            conexion.close()