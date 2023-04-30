from flask import Blueprint, render_template, url_for, redirect, request, jsonify, flash
from marvel_avatar.models import db,User, MarvelCharacter
from flask_login import login_user, logout_user, login_required, current_user

site = Blueprint('site', __name__, template_folder='site_templates')


@site.route('/')
@login_required
def home():
    profile = MarvelCharacter.query.filter_by(user_token=current_user.token).all()
    return render_template('home.html', profile=profile)


@site.route('/profile')
@login_required
def profile():
    characters = MarvelCharacter.query.filter_by(user_token=current_user.token).all()
    return render_template('profile.html', characters=characters)