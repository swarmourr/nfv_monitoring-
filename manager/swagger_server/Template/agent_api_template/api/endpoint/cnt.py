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


ns = api.namespace('vnf', description='get container vnf information')
