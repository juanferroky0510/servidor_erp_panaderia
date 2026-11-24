class ApiEstatusModel:
    def __init__(self, ban="0", msg="", datos=None):
        self.__ban = ban
        self.__msg = msg
        self.__datos = datos

    # Getters
    def get_ban(self):
        return self.__ban

    def get_msg(self):
        return self.__msg

    def get_datos(self):
        return self.__datos

    # Setters
    def set_ban(self, ban):
        self.__ban = str(ban)

    def set_msg(self, msg):
        self.__msg = msg

    def set_datos(self, datos):
        self.__datos = datos

    # Conversión a diccionario para retornar JSON en Flask
    def to_dict(self):
        return {
            "ban": self.__ban,
            "msg": self.__msg,
            "datos": self.__datos
        }