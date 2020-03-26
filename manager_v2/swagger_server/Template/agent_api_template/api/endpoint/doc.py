from flask import Flask,json
from flask_restplus import Resource, Api,fields,abort
from api.restplus import api
from converter import conv



ns=api.namespace('doc',description='get doc information')

@ns.route ('/')
class get_doc(Resource):
     def get(self):
       ff = open('schema.json', 'wb')
       ff.write(json.dumps(api.__schema__))
       ff.close()
       conv('schema.json')
       return api.__schema__
