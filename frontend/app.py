import os
from flask import Flask
from routes import landing_bp, advertisements_bp, materials_bp, dashboard_bp, calendar_bp, login_bp, courses_bp, attendance_bp, profile_bp, logs_bp

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

app.register_blueprint(landing_bp)
app.register_blueprint(advertisements_bp)
app.register_blueprint(materials_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(calendar_bp)
app.register_blueprint(login_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(logs_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5001)), debug=True)