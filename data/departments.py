import sqlalchemy as sqla
from .db_session import SqlAlchemyBase


class Departments(SqlAlchemyBase):
    __tablename__ = "departments"

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    title = sqla.Column(sqla.String)
    chief = sqla.Column(sqla.Integer)
    members = sqla.Column(sqla.String)
    email = sqla.Column(sqla.String)
