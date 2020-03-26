import connexion
import six

from swagger_server.models.osgi_host import OsgiHost  # noqa: E501
from swagger_server.models.osgi_model_jvm import OsgiModelJvm  # noqa: E501
from swagger_server import util
from swagger_server.services.builder.operations import *
from swagger_server.services.builder.compresser import *
from swagger_server.services.deployer.configure import *
from swagger_server.services.deployer.connector import *


def add_agent_anf(payload):  # noqa: E501
    """Add new applicatif  monitoring agent

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = OsgiModelJvm.from_dict(connexion.request.get_json())  # noqa: E501
    #try:
    create_osgi_agent(payload.__dict__)
    return "AGENT CREATED",200
    """except"  Exception as e:
           return "AGENT NOT CREATED",403"""
    return 'do some magic!'


def delete_agent():  # noqa: E501
    """Stop and delete applicatif  monitoring agent

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = OsgiHost.from_dict(connexion.request.get_json())  # noqa: E501
    #try:
    delete_agents_osgi(payload.__dict__)
    return "AGENT DELETED",200
    """except Exception as e:
            return "AGENT NOT DELETED",403"""
    return 'do some magic!'


def disable_agent(payload):  # noqa: E501
    """Stop an applicatif  monitoring agent

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = OsgiHost.from_dict(connexion.request.get_json())  # noqa: E501
    try:
        disable_agents_osgi(payload.__dict__)
        return "AGENT DISABLED",200
    except Exception as e:
            return "AGENT NOT DISABLED",403
    return 'do some magic!'


def enable_agent(payload):  # noqa: E501
    """Start an applicatif monitoring agent

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = OsgiHost.from_dict(connexion.request.get_json())  # noqa: E501
    #try:
    enable_agents_osgi(payload.__dict__)
    return "AGENT ENABLED",200
    """except Exception as e:
            return "AGENT NOT ENABLED",403"""
    return 'do some magic!'


def update_agent_anf(payload):  # noqa: E501
    """Update the configuration of an applicatif agent

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    """if connexion.request.is_json:
        payload = OsgiModelJvm.from_dict(connexion.request.get_json())  # noqa: E501"""
    #try:
    print(payload)
    update_agents_osgi(payload)
    return "ANF AGENT UPDATED",200
    #except Exception as e:
    #        return "ANF AGENT NOT FOUND ",403
    return 'do some magic!'
