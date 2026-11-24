from config.database import Database

class AuthModel:
    def validar_acceso(self, correo, contrasena):
        conexion = Database.conectar()
        if not conexion:
            return {"ban": "-1", "msg": "No se pudo conectar a la base de datos.", "datos": None}

        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.callproc("spValidarAcceso", [correo, contrasena])

            resultado = None
            for result in cursor.stored_results():
                resultado = result.fetchone()

            if resultado and resultado.get("ban") == "1":
                ban = resultado.pop("ban")
                msg = resultado.pop("msg", "Acceso concedido.")
                return {"ban": ban, "msg": msg, "datos": resultado}
            elif resultado:
                return {
                    "ban": resultado.get("ban", "0"),
                    "msg": resultado.get("msg", "Acceso denegado."),
                    "datos": None
                }
            else:
                return {"ban": "0", "msg": "No se obtuvo respuesta del servidor.", "datos": None}

        except Exception as e:
            return {"ban": "-1", "msg": f"Error en el servidor: {str(e)}", "datos": None}
        finally:
            cursor.close()
            conexion.close()