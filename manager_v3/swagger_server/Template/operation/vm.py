from flask import Flask, json, request
import requests
from flask_restplus import Resource, Api, fields, abort, Api, reqparse
from collections import OrderedDict
from api.restplus import api
from api.models.vm_model import *
import yaml
from converter import *
from api.impl.agent_vm import *
import sys
import ast


ns = api.namespace('vnf', description='get vnf information')


@ns.response(404, 'element not found')
@ns.route('/cpu/')
class get_cpu(Resource):
    def get(self):
        """get cpu usage of an vnf  in vnf  with name or pid """
        return getcpuload()


@ns.response(404, 'element not found')
@ns.route('/cpu/<name>')
class get_cpu_core(Resource):
    def get(self, name):
        """get cpu usage of an vnf  in vnf  with name or pid """
        return getcpuloadcore(name)

@ns.route('/mem/')
@ns.response(404, 'element not found')
class get_ram(Resource):
    def get(self):
        """get ram usage of an vnf  in vnf  by name   """
        return getRAM()

@ns.route('/all/')
@ns.response(404, 'element not found')
@ns.response(500, 'wroooong')
class get_all_data (Resource):
    def get(self):
        """get all other data  """
        return {
                "System":get_info(),
                "RAM" : getRAM() ,
                "CPU" : getcpuload() ,
                "Disk" : getdiskUsage() ,
                "Network": getNetTrBytes()
                }


@ns.route('/update/')
@ns.response(404, 'element not found')
@ns.response(204, 'element updated ')
class update_metics(Resource):
    def put(self):
        """update metrics  """
        update_agent_vm(ast.literal_eval(request.form.to_dict().keys()[0]))
