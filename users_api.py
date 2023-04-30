from flask import Blueprint, jsonify, request
from data.db_session import create_session
from data.users import User

bp = Blueprint("users_api", __name__, template_folder="templates")


@bp.route("/api/users")
def get_users():
    session = create_session()
    users = session.query(User).all()
    users_dict = {"users": [user.to_dict(only=[
        "id", "surname", "name", "age",
        "position", "speciality", "address",
        "email", "hashed_password", "modified_date"
    ]) for user in users]}
    return jsonify(users_dict)


@bp.route("/api/users/<int:user_id>")
def get_user(user_id: int):
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({"error": "User not found"})
    user_dict = {"user": user.to_dict(only=[
        "id", "surname", "name", "age",
        "position", "speciality", "address",
        "email", "hashed_password", "modified_date"
    ])}
    return jsonify(user_dict)


@bp.route("/api/users/add", methods=["POST"])
def add_user():
    valid_keys = [
        "id", "surname", "name", "age",
        "position", "speciality", "address",
        "email", "password"
    ]
    if not request.json:
        return jsonify({"error": "Empty request"})
    if not all(key in request.json for key in valid_keys):
        return jsonify({"error": "Bad request"})
    session = create_session()
    if session.query(User).get(request.json["id"]):
        return jsonify({"error": "Id already exists"})
    user = User(
        id=request.json["id"],
        surname=request.json["surname"],
        name=request.json["name"],
        age=request.json["age"],
        position=request.json["position"],
        speciality=request.json["speciality"],
        address=request.json["address"],
        email=request.json["email"]
    )
    user.set_password(request.json["password"])
    session.add(user)
    session.commit()
    return jsonify({"success": "User added successfully"})


@bp.route("/api/users/edit/<int:user_id>", methods=["POST"])
def edit_user(user_id: int):
    valid_keys = [
        "surname", "name", "age",
        "position", "speciality", "address",
        "email", "password"
    ]
    if not request.json:
        return jsonify({"error": "Empty request"})
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({"error": "User not found"})
    for key in request.json:
        if key in valid_keys:
            setattr(user, key, request.json[key])
    if "password" in request.json:
        user.set_password(request.json["password"])
    session.commit()
    return jsonify({"success": "User edited successfully"})


@bp.route("/api/users/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({"error": "User not found"})
    session.delete(user)
    session.commit()
    return jsonify({"success": "User deleted successfully"})
