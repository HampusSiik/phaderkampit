import os
from datetime import datetime
from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from .extensions import db
from .models import SoundList, SoundClip, Team, Answer


bp = Blueprint("routes", __name__)


ALLOWED_EXTENSIONS = {"mp3", "wav", "ogg", "m4a", "flac"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/")
def index():
    lists = SoundList.query.order_by(SoundList.created_at.desc()).all()
    teams = Team.query.order_by(Team.created_at.desc()).all()
    return render_template("index.html", lists=lists, teams=teams)


@bp.route("/lists", methods=["POST"])
def create_list():
    name = request.form.get("name")
    description = request.form.get("description")
    if not name:
        flash("List name is required", "error")
        return redirect(url_for("routes.index"))
    lst = SoundList(name=name.strip(), description=description)
    db.session.add(lst)
    db.session.commit()
    flash("List created", "success")
    return redirect(url_for("routes.view_list", list_id=lst.id))


@bp.route("/lists/<int:list_id>")
def view_list(list_id):
    lst = SoundList.query.get_or_404(list_id)
    clips = SoundClip.query.filter_by(list_id=list_id).order_by(SoundClip.created_at.desc()).all()
    teams = Team.query.order_by(Team.created_at.desc()).all()
    # Build a simple scoreboard: correct answers per team across this list
    team_scores = {t.id: 0 for t in teams}
    for clip in clips:
        for ans in clip.answers:
            if ans.is_correct:
                team_scores[ans.team_id] = team_scores.get(ans.team_id, 0) + 1
    return render_template("list.html", lst=lst, clips=clips, teams=teams, team_scores=team_scores)


@bp.route("/teams", methods=["POST"])
def create_team():
    name = request.form.get("name")
    if not name:
        flash("Team name is required", "error")
        return redirect(request.referrer or url_for("routes.index"))
    team = Team(name=name.strip())
    db.session.add(team)
    db.session.commit()
    flash("Team created", "success")
    return redirect(request.referrer or url_for("routes.index"))


@bp.route("/clips/upload/<int:list_id>", methods=["POST"])
def upload_clip(list_id):
    lst = SoundList.query.get_or_404(list_id)
    file = request.files.get("file")
    title = request.form.get("title") or (file.filename if file else None)
    description = request.form.get("description")

    if not file or file.filename == "":
        flash("No file provided", "error")
        return redirect(url_for("routes.view_list", list_id=list_id))

    if not allowed_file(file.filename):
        flash("Unsupported file type", "error")
        return redirect(url_for("routes.view_list", list_id=list_id))

    filename = secure_filename(f"{datetime.utcnow().timestamp()}_{file.filename}")
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    clip = SoundClip(
        list_id=lst.id,
        title=title or file.filename,
        description=description,
        filename=filename,
        original_name=file.filename,
        mime_type=file.mimetype,
    )
    db.session.add(clip)
    db.session.commit()
    flash("Clip uploaded", "success")
    return redirect(url_for("routes.view_list", list_id=list_id))


@bp.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@bp.route("/answers", methods=["POST"])
def record_answer():
    team_id = request.form.get("team_id", type=int)
    clip_id = request.form.get("clip_id", type=int)
    is_correct = request.form.get("is_correct") == "true"
    notes = request.form.get("notes")

    if not team_id or not clip_id:
        flash("Team and clip required", "error")
        return redirect(request.referrer or url_for("routes.index"))

    team = Team.query.get_or_404(team_id)
    clip = SoundClip.query.get_or_404(clip_id)

    # Upsert-like behavior: one answer per team+clip
    existing = Answer.query.filter_by(team_id=team.id, clip_id=clip.id).first()
    if existing:
        existing.is_correct = is_correct
        existing.notes = notes
        existing.submitted_at = datetime.utcnow()
        ans = existing
    else:
        ans = Answer(team=team, clip=clip, is_correct=is_correct, notes=notes)
        db.session.add(ans)
    db.session.commit()
    flash("Answer recorded", "success")
    return redirect(request.referrer or url_for("routes.index"))

*** End Patch
