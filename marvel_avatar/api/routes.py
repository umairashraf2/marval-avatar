from flask import Blueprint,request, jsonify
from marvel_avatar.models import db, MarvelCharacter
from flask_login import login_required, current_user

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/add_character', methods=['POST'])
@login_required
def add_character():
    character_data = request.json
    new_character = MarvelCharacter(
        name=character_data['name'],
        description=character_data['description'],
        comics=character_data['comics'],
        image=character_data["image"],
        user_token=current_user.token,
    )

    try:
        db.session.add(new_character)
        db.session.commit()
        return jsonify(success=True)
    except:
        db.session.rollback()
        return jsonify(success=False)
    
    
@api.route('/delete_character/<int:character_id>', methods=['DELETE'])
@login_required
def delete_character(character_id):
    character = MarvelCharacter.query.filter_by(id=character_id, user_token=current_user.token).first()
    if character:
        try:
            db.session.delete(character)
            db.session.commit()
            return jsonify(success=True)
        except:
            db.session.rollback()
            return jsonify(success=False)
    else:
        return jsonify(success=False)

