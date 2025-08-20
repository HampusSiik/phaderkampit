from datetime import datetime
from .extensions import db


class SoundList(db.Model):
    __tablename__ = "sound_lists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    clips = db.relationship("SoundClip", back_populates="list", cascade="all, delete-orphan")


class SoundClip(db.Model):
    __tablename__ = "sound_clips"
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey("sound_lists.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    filename = db.Column(db.String(255), nullable=False)  # stored file name on disk
    original_name = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(128), nullable=True)
    difficulty = db.Column(db.String(20), nullable=True)  # 'easy', 'medium', 'hard'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    list = db.relationship("SoundList", back_populates="clips")
    answers = db.relationship("Answer", back_populates="clip", cascade="all, delete-orphan")


class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    answers = db.relationship("Answer", back_populates="team", cascade="all, delete-orphan")


class Answer(db.Model):
    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True)
    clip_id = db.Column(db.Integer, db.ForeignKey("sound_clips.id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)
    __table_args__ = (
        db.UniqueConstraint("clip_id", "team_id", name="uq_answer_clip_team"),
    )

    clip = db.relationship("SoundClip", back_populates="answers")
    team = db.relationship("Team", back_populates="answers")
