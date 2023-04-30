from flask import jsonify
from flask_restful import abort, Resource

from data.db_session import create_session
from data.jobs import Jobs
from parse_args2 import parser


def job_not_found(job_id):
    session = create_session()
    job = session.query(Jobs).get(job_id)
    session.close()
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        job_not_found(job_id)
        session = create_session()
        job = session.query(Jobs).get(job_id)
        result = job.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators',
                                   'start_date', 'end_date', 'is_finished'))
        session.close()
        return jsonify({'job': result})

    def put(self, job_id):
        args = parser.parse_args()
        job_not_found(job_id)
        session = create_session()
        job = session.query(Jobs).get(job_id)
        job.team_leader = args['team_leader']
        job.job = args['job']
        job.work_size = args['work_size']
        job.collaborators = args['collaborators']
        job.is_finished = args['is_finished']
        job.start_date = args['start_date']
        job.end_date = args['end_date']
        session.commit()
        session.close()
        return jsonify({'success': 'OK'})

    def delete(self, job_id):
        job_not_found(job_id)
        session = create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        session.close()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = create_session()
        jobs = session.query(Jobs).all()
        results = [job.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators',
                                     'start_date', 'end_date', 'is_finished')) for job in jobs]
        session.close()
        return jsonify({'jobs': results})

    def post(self):
        args = parser.parse_args()
        session = create_session()
        job = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished'],
            start_date=args['start_date'],
            end_date=args['end_date']
        )
        session.add(job)
        session.commit()
        session.close()
        return jsonify({'success': 'OK'})
