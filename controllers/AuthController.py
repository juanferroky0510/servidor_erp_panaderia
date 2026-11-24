from flask import Blueprint, request, jsonify
from models.AuthModel import AuthModel
from models.ApiEstatusModel import ApiEstatusModel

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    estatus = ApiEstatusModel()
    body = request.get_json(silent=True) or {}

    correo = body.get("correo", "")
    contrasena = body.get("contrasena", "")

    if not correo or not contrasena:
        estatus.set_ban("0")
        estatus.set_msg("Debes enviar correo y contraseña.")
        return jsonify(estatus.to_dict()), 400

    modelo = AuthModel()
    respuesta = modelo.validar_acceso(correo, contrasena)

    estatus.set_ban(respuesta["ban"])
    estatus.set_msg(respuesta["msg"])
    estatus.set_datos(respuesta["datos"])

    return jsonify(estatus.to_dict()), 200