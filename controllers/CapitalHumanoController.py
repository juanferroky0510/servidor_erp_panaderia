from flask import Blueprint, request, jsonify
from models.CapitalHumanoModel import CapitalHumanoModel
from models.ApiEstatusModel import ApiEstatusModel

capital_humano_bp = Blueprint("capital_humano_bp", __name__)


@capital_humano_bp.route("/api/capital-humano/asistencias/registrar", methods=["POST"])
def registrar_asistencia():
    estatus = ApiEstatusModel()
    body = request.get_json(silent=True) or {}

    id_empleado = body.get("idEmpleado")
    observaciones = body.get("observaciones", "")

    if not id_empleado:
        estatus.set_ban("0")
        estatus.set_msg("El idEmpleado es obligatorio para registrar la asistencia.")
        return jsonify(estatus.to_dict()), 400

    modelo = CapitalHumanoModel()
    respuesta = modelo.registrar_asistencia(id_empleado, observaciones)

    estatus.set_ban(respuesta["ban"])
    estatus.set_msg(respuesta["msg"])
    estatus.set_datos(respuesta["datos"])

    return jsonify(estatus.to_dict()), 200


@capital_humano_bp.route("/api/capital-humano/asistencias/estado/<int:id_empleado>", methods=["GET"])
def estado_asistencia(id_empleado):
    estatus = ApiEstatusModel()

    modelo = CapitalHumanoModel()
    respuesta = modelo.estado_asistencia_hoy(id_empleado)

    estatus.set_ban(respuesta["ban"])
    estatus.set_msg(respuesta["msg"])
    estatus.set_datos(respuesta["datos"])

    return jsonify(estatus.to_dict()), 200


@capital_humano_bp.route("/api/capital-humano/asistencias/reporte", methods=["GET"])
def reporte_asistencias():
    estatus = ApiEstatusModel()
    # Acepta ?q= (ID o nombre) o ?idEmpleado=
    busqueda = request.args.get("q") or request.args.get("idEmpleado")

    modelo = CapitalHumanoModel()
    respuesta = modelo.listar_asistencias(busqueda=busqueda)

    estatus.set_ban(respuesta["ban"])
    estatus.set_msg(respuesta["msg"])
    estatus.set_datos(respuesta["datos"])

    return jsonify(estatus.to_dict()), 200