from config.database import Database


class CapitalHumanoModel:
    def registrar_asistencia(self, id_empleado, observaciones=""):
        conexion = Database.conectar()
        if not conexion:
            return {"ban": "-1", "msg": "No se pudo conectar a la base de datos.", "datos": None}

        cursor = None
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.callproc("spRegistrarAsistencia", [id_empleado, observaciones])

            resultado = None
            for result in cursor.stored_results():
                resultado = result.fetchone()

            conexion.commit()

            if resultado and resultado.get("ban") == "1":
                ban = resultado.pop("ban")
                msg = resultado.pop("msg", "Asistencia registrada correctamente.")
                return {"ban": ban, "msg": msg, "datos": resultado}
            elif resultado:
                return {
                    "ban": resultado.get("ban", "0"),
                    "msg": resultado.get("msg", "No se pudo registrar la asistencia."),
                    "datos": None
                }
            else:
                return {"ban": "0", "msg": "No se obtuvo respuesta del servidor.", "datos": None}

        except Exception as e:
            if conexion:
                conexion.rollback()
            return {"ban": "-1", "msg": f"Error al registrar asistencia: {str(e)}", "datos": None}
        finally:
            if cursor:
                cursor.close()
            conexion.close()

    def estado_asistencia_hoy(self, id_empleado):
        conexion = Database.conectar()
        if not conexion:
            return {"ban": "-1", "msg": "No se pudo conectar a la base de datos.", "datos": None}

        cursor = None
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.callproc("spEstadoAsistenciaHoy", [id_empleado])

            resultado = None
            for result in cursor.stored_results():
                resultado = result.fetchone()

            if resultado and resultado.get("ban") == "1":
                ban = resultado.pop("ban")
                msg = resultado.pop("msg", "Consulta realizada.")
                return {"ban": ban, "msg": msg, "datos": resultado}
            elif resultado:
                return {
                    "ban": resultado.get("ban", "0"),
                    "msg": resultado.get("msg", "No se pudo consultar el estado."),
                    "datos": None
                }
            else:
                return {"ban": "0", "msg": "Sin información disponible.", "datos": None}

        except Exception as e:
            return {"ban": "-1", "msg": f"Error al consultar estado de asistencia: {str(e)}", "datos": None}
        finally:
            if cursor:
                cursor.close()
            conexion.close()

    def listar_asistencias(self, busqueda=None):
        conexion = Database.conectar()
        if not conexion:
            return {"ban": "-1", "msg": "No se pudo conectar a la base de datos.", "datos": []}

        cursor = None
        try:
            cursor = conexion.cursor(dictionary=True)
            texto = str(busqueda).strip() if busqueda is not None else ""

            if texto:
                sql = """
                    SELECT * FROM vwRptAsistencias
                    WHERE CAST(idEmpleado AS CHAR) = %s
                       OR nombreCompleto LIKE %s
                """
                cursor.execute(sql, (texto, f"%{texto}%"))
            else:
                cursor.execute("SELECT * FROM vwRptAsistencias")

            registros = cursor.fetchall()
            return {
                "ban": "1",
                "msg": f"Se encontraron {len(registros)} registros de asistencia.",
                "datos": registros
            }

        except Exception as e:
            return {"ban": "-1", "msg": f"Error al consultar el historial de asistencias: {str(e)}", "datos": []}
        finally:
            if cursor:
                cursor.close()
            conexion.close()