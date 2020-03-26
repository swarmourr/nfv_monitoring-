from flask import Flask, json, request
import requests
from flask_restplus import Resource, Api, fields, abort, Api, reqparse
from collections import OrderedDict
from api.restplus import api
#from api.models.jvm_model import *
import yaml
from converter import *
from api.impl.jvm_agents import *
import sys
import ast


ns = api.namespace('jvm', description='get jvm information')


# @ns.route('/ressources')
@ns.response(404, 'element not found')
@ns.response(500, 'wroooong')
class get_all_jvm (Resource):
    def get(self):
        """get all moniroted jvm  and metrics """
        return info_m()


# @ns.route('/connections/')
@ns.response(404, 'element not found')
@ns.response(500, 'wroooong')
class get_open_conx (Resource):
    def get(self):
        """get all opened connections jvm """
        return get_connections()


# @ns.route('/threads/')
@ns.response(404, 'element not found')
@ns.response(500, 'wroooong')
class get_thrds (Resource):
    def get(self):
        """get all jvm threads """
        return get_threads()


# @ns.route('/gc/')
@ns.response(404, 'element not found')
@ns.response(500, 'wroooong')
class get_gc1 (Resource):
    def get(self):
        """get all jvm gc  """
        return  get_gc()

@ns.route('/update/')
@ns.response(404, 'element not found')
@ns.response(204, 'element updated ')
class update_metics(Resource):
    def put(self):
        """update metrics  """
        update_agent_anf(ast.literal_eval(request.form.to_dict().keys()[0]))
