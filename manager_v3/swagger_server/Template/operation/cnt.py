from flask import Flask, json, request
import requests
from flask_restplus import Resource, Api, fields, abort, Api, reqparse
from collections import OrderedDict
from api.restplus import api
from api.models.vm_model import *
import yaml
from converter import *
from api.impl.agent_cnt import *
import sys
import ast


ns = api.namespace('vnf', description='get vnf information')

@ns.response(404, 'element not found')
# @ns.route('/cpu/')
class get_cpu(Resource):
    def get(self):
        """get cpu usage of an vnf  in vnf  with name or pid """
        return cpu_c()

# @ns.route('/mem/')
@ns.response(404, 'element not found')
class get_ram(Resource):
    def get(self):
        """get ram usage of an vnf  in vnf  by name   """
        return {"RAM" : mem_cnt()["consumption"]}

@ns.route('/all/')
@ns.response(404, 'element not found')
@ns.response(500, 'wroooong')
class get_open_conx (Resource):
    def get(self):
        """get all opened connections vnf """
        return {"CONTAINER":info_cnt(),
                "RAM":mem_cnt(),
                "CPU":cpu_c(),
                "DISK":disk_cnt(),
                "NET":net_i_o(),
                "CONNECTIONS":getconnections()}

@ns.route('/update/')
@ns.response(404, 'element not found')
@ns.response(204, 'element updated ')
class update_metics(Resource):
    def put(self):
        """update metrics  """
        print "je suis la update"
        print ast.literal_eval(request.form.to_dict().keys()[0])
        return update_agent_cnt(ast.literal_eval(request.form.to_dict().keys()[0]))
