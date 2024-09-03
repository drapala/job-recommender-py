from .job_routes import job_bp
from .user_routes import user_bp
from .activity_routes import activity_bp

def register_blueprints(app):
    app.register_blueprint(job_bp, url_prefix='/jobs')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(activity_bp, url_prefix='/activities')
