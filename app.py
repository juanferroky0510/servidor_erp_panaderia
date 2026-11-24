from flask import Flask
from flask_cors import CORS
from controllers.AuthController import auth_bp
from controllers.ProveedoresController import proveedores_bp

app = Flask(__name__)
CORS(app)  # Permite peticiones desde tus futuros archivos HTML/JS

# Registrar controladores
app.register_blueprint(auth_bp)
app.register_blueprint(proveedores_bp)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)