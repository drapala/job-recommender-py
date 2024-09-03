from flask import Blueprint, jsonify, request
from ..models import db, UserActivity, JobSearch

activity_bp = Blueprint('activities', __name__)

# Route to create a new user activity
@activity_bp.route('/activities', methods=['POST'])
def create_activity():
    data = request.get_json()
    
    # Validate received data
    if not data or not data.get('user_id') or not data.get('activity_type'):
        return jsonify({'message': 'Invalid data. User ID and activity type are required.'}), 400

    # Create the new activity
    activity = UserActivity(
        user_id=data['user_id'],
        activity_type=data['activity_type'],
        timestamp=data.get('timestamp'),
        details=data.get('details')
    )
    db.session.add(activity)
    db.session.commit()
    
    return jsonify({'message': 'Activity created successfully', 'activity_id': activity.id}), 201

# Route to get all activities of a user
@activity_bp.route('/users/<int:user_id>/activities', methods=['GET'])
def get_user_activities(user_id):
    activities = UserActivity.query.filter_by(user_id=user_id).all()
    
    # Check if the user has activities
    if not activities:
        return jsonify({'message': 'No activities found for this user.'}), 404
    
    activities_list = [{
        'id': activity.id,
        'activity_type': activity.activity_type,
        'timestamp': activity.timestamp,
        'details': activity.details
    } for activity in activities]
    
    return jsonify({'activities': activities_list})

# Route to create a new job search
@activity_bp.route('/job_searches', methods=['POST'])
def create_job_search():
    data = request.get_json()
    
    # Validate received data
    if not data or not data.get('user_id') or not data.get('search_term'):
        return jsonify({'message': 'Invalid data. User ID and search term are required.'}), 400

    # Create the new job search
    job_search = JobSearch(
        user_id=data['user_id'],
        search_term=data['search_term'],
        timestamp=data.get('timestamp')
    )
    db.session.add(job_search)
    db.session.commit()
    
    return jsonify({'message': 'Job search created successfully', 'search_id': job_search.id}), 201

# Route to get all job searches of a user
@activity_bp.route('/users/<int:user_id>/job_searches', methods=['GET'])
def get_user_job_searches(user_id):
    job_searches = JobSearch.query.filter_by(user_id=user_id).all()
    
    # Check if the user has job searches
    if not job_searches:
        return jsonify({'message': 'No job searches found for this user.'}), 404

    searches_list = [{
        'id': search.id,
        'search_term': search.search_term,
        'timestamp': search.timestamp
    } for search in job_searches]
    
    return jsonify({'job_searches': searches_list})
