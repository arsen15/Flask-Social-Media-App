import base64
from flask import Blueprint, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Post
from . import db
import json

# Store route for website

views = Blueprint("views", __name__)

# Decorator, when hit this route, calls function home()


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        post = request.form.get("post")

        if len(post) < 1:
            flash("Post is too short!", category="error")
        else:
            image = request.files["img"]
            filename = secure_filename(image.filename)
            mimetype = image.mimetype
            read = base64.b64encode(image.read())
            read = read.decode("ascii")
            print(type(read))
            print(mimetype)
            new_post = Post(
                content=post,
                img=read,
                name=filename,
                mimetype=mimetype,
                user_id=current_user.id,
            )
            db.session.add(new_post)
            db.session.commit()

            flash("Post Added", category="success")
    data = Post.query.order_by(Post.id.desc()).all()
    return render_template("home.html", data=data, user=current_user)


# @views.route("/delete-note", methods=["POST"])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note["noteId"]
#     note = Post.query.get(noteId)

#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})
