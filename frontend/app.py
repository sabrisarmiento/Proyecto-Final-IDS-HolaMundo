from flask import Flask
from routes import landing_bp, advertisements_bp, materials_bp, dashboard_bp, calendar_bp

app = Flask(__name__)

app.register_blueprint(landing_bp)
app.register_blueprint(advertisements_bp)
app.register_blueprint(materials_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(calendar_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5001)