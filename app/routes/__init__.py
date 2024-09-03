from .job_routes import job_bp
from .user_routes import user_bp
from .activity_routes import activity_bp

def register_blueprints(app):
    app.register_blueprint(job_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(activity_bp)
