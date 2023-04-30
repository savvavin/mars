from flask import Blueprint, jsonify, request
from data.db_session import create_session
from data.jobs import Jobs

bp = Blueprint("jobs_api", __name__, template_folder="templates")


@bp.route("/api/jobs")
def get_jobs():
    with create_session() as session:
        jobs = session.query(Jobs).all()
        return jsonify({"jobs": [job.to_dict(only=[
            "id", "team_leader", "job", "work_size", "collaborators",
            "start_date", "end_date", "is_finished"]) for job in jobs]})


@bp.route("/api/jobs/<int:job_id>")
def get_job(job_id: int):
    with create_session() as session:
        job = session.query(Jobs).get(job_id)
        if not job:
            return jsonify({"error": "Job not found"})
        return jsonify({"job": job.to_dict(only=[
            "id", "team_leader", "job", "work_size", "collaborators",
            "start_date", "end_date", "is_finished"])})


@bp.route("/api/jobs", methods=["POST"])
def add_job():
    if not request.json:
        return jsonify({"error": "Empty request"})
    expected_keys = ["id", "team_leader", "job", "work_size", "collaborators",
                     "start_date", "end_date", "is_finished"]
    if not all(key in request.json for key in expected_keys):
        return jsonify({"error": "Bad request"})
    with create_session() as session:
        if session.query(Jobs).get(request.json["id"]):
            return jsonify({"error": "Id already exists"})
        job = Jobs(**request.json)
        session.add(job)
        session.commit()
        return jsonify({"success": "OK"})


@bp.route("/api/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id: int):
    with create_session() as session:
        job = session.query(Jobs).get(job_id)
        if not job:
            return jsonify({"error": "Not found"})
        session.delete(job)
        session.commit()
        return jsonify({"success": "OK"})


@bp.route("/api/jobs/edit/<int:job_id>", methods=["POST"])
def edit_job(job_id: int):
    valid_keys = ["team_leader", "job", "work_size", "collaborators",
                  "start_date", "end_date", "is_finished"]
    if not request.json:
        return jsonify({"error": "Empty request"})
    with create_session() as session:
        job = session.query(Jobs).filter(Jobs.id == job_id).first()
        if not job:
            return jsonify({"error": "Not found"})
        updates = {key: request.json[key] for key in valid_keys if key in request.json}
        session.query(Jobs).filter(Jobs.id == job_id).update(updates)
        session.commit()
        return jsonify({"success": "OK"})
