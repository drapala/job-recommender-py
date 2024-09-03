from flask import Blueprint, jsonify, request
from ..models import db, Job
from ..services_init import recommendation_service

job_bp = Blueprint('job_bp', __name__)

@job_bp.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    job = Job(
        title=data['title'],
        description=data.get('description'),
        company=data.get('company'),
        location=data.get('location'),
        requirements=data.get('requirements'),
        salary=data.get('salary')
    )
    db.session.add(job)
    db.session.commit()

    recommendation_service.publish_event('job_created', {'id': job.id, 'title': job.title})

    return jsonify({'message': 'Job created successfully', 'job_id': job.id}), 201

@job_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'message': 'Job not found'}), 404
    return jsonify({
        'id': job.id,
        'title': job.title,
        'description': job.description,
        'company': job.company,
        'location': job.location,
        'requirements': job.requirements,
        'salary': job.salary
    })

@job_bp.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'message': 'Job not found'}), 404

    data = request.get_json()
    job.title = data.get('title', job.title)
    job.description = data.get('description', job.description)
    job.company = data.get('company', job.company)
    job.location = data.get('location', job.location)
    job.requirements = data.get('requirements', job.requirements)
    job.salary = data.get('salary', job.salary)
    
    db.session.commit()

    # Publicar evento no Kafka
    recommendation_service.publish_event('job_updated', {'id': job.id, 'title': job.title})

    return jsonify({'message': 'Job updated successfully'})

@job_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'message': 'Job not found'}), 404

    db.session.delete(job)
    db.session.commit()

    # Publicar evento no Kafka
    recommendation_service.publish_event('job_deleted', {'id': job.id})

    return jsonify({'message': 'Job deleted successfully'})
