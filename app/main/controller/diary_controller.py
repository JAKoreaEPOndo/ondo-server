from flask import request
from flask_restplus import Resource

from ..util.dto import DiaryDto
from ..service.diary_service import *

from app.main.util.decorator import token_required

api = DiaryDto.api
_diary = DiaryDto.diary

@api.route('/')
class DiaryList(Resource):
    @token_required
    @api.doc('list_of_my_diaries')
    @api.marshal_list_with(_diary,envelope='data')
    @api.doc(params={'year': {'description': 'diary year',
                                'type': 'string', 'required':False},
                    'month': {'description': 'diary month',
                                'type': 'string', 'required':False}})
    def get(self):
        year = request.args.get('year')
        month = request.args.get('month')
        return get_all_diaries(request=request,year = year,month=month)

    @token_required
    @api.response(201, 'Diary successfully created')
    @api.doc('create a new diary')
    @api.expect(_diary, validate=True)
    def post(self):
        return save_new_diary(request=request)


@api.route('/<id>')
@api.param('id','The Diary identifier')
@api.response(404,'Diary not found')
class Diary(Resource):
    @token_required
    @api.doc('get a diary')
    @api.marshal_with(_diary)
    def get (self,id):
        diary = get_a_diary(request=request,id=id)
        if not diary:
            api.abort(404)
        else:
            return diary

    @token_required
    @api.doc('modify a diary')
    @api.marshal_with(_diary)
    def delete (self,id):
        return delete_diary(request,id)

        