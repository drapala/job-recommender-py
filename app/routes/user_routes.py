from flask import Blueprint, jsonify, request
from ..models import db, User
from ..services_init import recommendation_service

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(
        username=data['username'],
        email=data['email']
    )
    db.session.add(user)
    db.session.commit()

    recommendation_service.publish_event('user_created', {'id': user.id, 'username': user.username})

    return jsonify({'message': 'User created successfully', 'user_id': user.id}), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    })

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    
    db.session.commit()

    recommendation_service.publish_event('user_updated', {'id': user.id, 'username': user.username})

    return jsonify({'message': 'User updated successfully'})

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    recommendation_service.publish_event('user_deleted', {'id': user.id})

    return jsonify({'message': 'User deleted successfully'})
