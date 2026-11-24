from flask import Blueprint, request, jsonify
from models.ProveedoresModel import ProveedoresModel
from models.ApiEstatusModel import ApiEstatusModel

proveedores_bp = Blueprint("proveedores_bp", __name__)

@proveedores_bp.route("/api/proveedores/insertar", methods=["POST"])
def insertar():
    estatus = ApiEstatusModel()
    body = request.get_json(silent=True) or {}

    modelo = ProveedoresModel()
    respuesta = modelo.insertar_proveedor(body)

    estatus.set_ban(respuesta["ban"])
    estatus.set_msg(respuesta["msg"])
    estatus.set_datos(respuesta["datos"])

    return jsonify(estatus.to_dict()), 200

@proveedores_bp.route("/api/proveedores/actualizar", methods=["PUT"])
def actualizar():
    estatus = ApiEstatusModel()
    body = request.get_json(silent=True) or {}

    modelo = ProveedoresModel()
    respuesta = modelo.actualizar_proveedor(body)

    estatus.set_ban(respuesta["ban"])
    estatus.set_msg(respuesta["msg"])
    estatus.set_datos(respuesta["datos"])

    return jsonify(estatus.to_dict()), 200

@proveedores_bp.route("/api/proveedores/reporte", methods=["GET"])
def reporte():
    estatus = ApiEstatusModel()
    # Permite filtrar opcionalmente con ?activos=1 (útil para combos/selects)
    solo_activos = request.args.get("activos", "0") == "1"

    modelo = ProveedoresModel()
    respuesta = modelo.reporte_proveedores(solo_activos=solo_activos)

    estatus.set_ban(respuesta["ban"])
    estatus.set_msg(respuesta["msg"])
    estatus.set_datos(respuesta["datos"])

    return jsonify(estatus.to_dict()), 200

@proveedores_bp.route("/api/proveedores/buscar", methods=["GET"])
def buscar():
    estatus = ApiEstatusModel()
    busqueda = request.args.get("q", "")

    modelo = ProveedoresModel()
    respuesta = modelo.buscar_proveedor(busqueda)

    estatus.set_ban(respuesta["ban"])
    estatus.set_msg(respuesta["msg"])
    estatus.set_datos(respuesta["datos"])

    return jsonify(estatus.to_dict()), 200