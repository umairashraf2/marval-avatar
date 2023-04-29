from flask import render_template, url_for, redirect, request, jsonify, flash
from app import app, db
from models import User, MarvelCharacter
from forms import LoginForm, RegistrationForm, MarvelCharacterForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import os


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        new_user.token = hashlib.sha256(os.urandom(60)).hexdigest()
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/')
@login_required
def home():
    profile = MarvelCharacter.query.filter_by(user_token=current_user.token).all()
    return render_template('home.html', profile=profile)


@app.route('/add_character', methods=['POST'])
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

@app.route('/profile')
@login_required
def profile():
    characters = MarvelCharacter.query.filter_by(user_token=current_user.token).all()
    return render_template('profile.html', characters=characters)


@app.route('/delete_character/<int:character_id>', methods=['DELETE'])
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
