from flask import Flask, render_template
from routes import advices_bp, attendance_bp, exam_bp, classes_bp, exam_types_bp, marks_bp, roles_bp, students_bp, users_bp, teams_bp
app = Flask(__name__)

@app.route('/')
def index():
    return "API Backend de ProDe levantada correctamente."

app.register_blueprint(advices_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(exam_bp)
app.register_blueprint(exam_types_bp)
app.register_blueprint(classes_bp)
app.register_blueprint(marks_bp)
app.register_blueprint(roles_bp)
app.register_blueprint(students_bp)
app.register_blueprint(users_bp)
app.register_blueprint(teams_bp)

if __name__ == '__main__':
    app.run(debug=True)