from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Blog, Comment, User
from . import db
import json


views = Blueprint('views', __name__)

@views.route('/home', methods=['GET'])
def home():
    posts = Blog.query.all()
    return render_template('home.html', posts=posts, user=current_user)

@views.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = current_user.first_name
        print(f"{title}, {content}, {author}")
        new_post = Blog(title=title, content=content, author=author, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post added!', category="success")
        return redirect(url_for('views.home'))
    return render_template('create_post.html', user=current_user)

@views.route('/post/<postId>', methods=['GET', 'POST'])
def post(postId):
    if request.method == 'POST':
        comment = request.form.get('comment')
        userId = current_user.id
        postId = postId
        print(f"{comment}, {userId}, {postId}")
        new_comment = Comment(body=comment, user_id=userId, blog_id=postId)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added!', category='success')
    post = Blog.query.get(postId)
    users = User.query.all()
    return render_template('post.html', post=post, user=current_user, users=users)