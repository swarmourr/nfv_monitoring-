from flask import Flask, json, Blueprint
from flask_restplus import Resource, Api, fields, abort, Api
from api.restplus import api
from collections import OrderedDict
import settings
import yaml
from converter import *
from api.endpoint.vm import ns as vnfv  # vnf in virtual machine
from api.endpoint.cnt import ns as vnfc  # vnf in docker container
from api.endpoint.jvm import ns as anf
from api.endpoint.doc import ns as dct1
import ConfigParser
import os
from  api.impl.passive_vm  import *
from  api.impl.passive_jvm  import *
from  api.impl.passive_cnt import *
from flask_apscheduler import APScheduler
import uuid

config = ConfigParser.ConfigParser()
config.read(str(os.getcwd())+"/agent/api/builder/agent/config.conf")

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
app.config.SWAGGER_UI_JSONEDITOR = True
app.app_context().__enter__()

blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)
api.add_namespace(vnfc)
api.add_namespace(vnfv)
api.add_namespace(anf)
app.register_blueprint(blueprint)
#app.apscheduler.add_job(func=get_data,trigger='interval',seconds=1,id=config.get("agent", "id")+"_"+str(uuid.uuid4()))
#app.apscheduler.add_job(func=send_data_all,trigger='interval',seconds=int(config.get("agent", "refresh_period")),id=config.get("agent", "id")+"_"+str(uuid.uuid4()))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=config.get("host", "port"))
