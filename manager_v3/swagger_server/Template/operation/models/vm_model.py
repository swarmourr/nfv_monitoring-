from flask_restplus import Resource, Api, fields, abort, Api, reqparse, marshal
from collections import OrderedDict
from api.restplus import api

path_params_vm = api.model('params_path_vm', {
    'ip_vm': fields.String(description='ip of vm', required=True),

})

java_params = api.model('java_path', {
    'ip_vm': fields.String(description='ip of vm', required=True),

})

update_agent = api.model('update', {
    'metric': fields.String(description='metrics', required=True),
    'operation': fields.String(description='ENABLE/DISABLE', required=True, enum=["ENABLE", "DISABLE"]),
})

pg = reqparse.RequestParser()
pg.add_argument('metric', type=str, choices=["cpu", "ram", "disk", "net"])
pg.add_argument('option', type=str, choices=["ENABLE", "DISABLE"])
