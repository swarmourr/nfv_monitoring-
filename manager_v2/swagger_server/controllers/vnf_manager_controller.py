import connexion
import six

from swagger_server.models.admin_model_system import AdminModelSystem  # noqa: E501
from swagger_server.models.delete_agent import DeleteAgent  # noqa: E501
from swagger_server.models.update_model_vnf import UpdateModelVnf  # noqa: E501
from swagger_server import util
from swagger_server.services.builder.operations import *


def add_agent_vnf(payload):  # noqa: E501
    """Add new VM and CNT monitoring agent

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = AdminModelSystem.from_dict(connexion.request.get_json())  # noqa: E501
    print(payload.access_host)
    if (payload.access_host["type"]).lower() == "vm":
            try:
                create_vm_agent(payload)
                return "AGENT CREATED",201
            except Exception as e:
                print("vm")
                return "AGENT NOT CREATED",403

    elif (payload.access_host["type"]).lower() == "cnt":
            try:
                create_cnt_agent(payload)
                return "AGENT CREATED",201
            except Exception as e:
                print("cnt")
                return "AGENT NOT CREATED ",403
    else :
            return "Type not supported for VNF  ==> AGENT NOT CREATED",400
    return 'do some magic!'


def delete_agent_vnf(payload):  # noqa: E501
    """Stop and delete VM AND CNT monitoring agent

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = DeleteAgent.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def disable_agent_vnf(payload):  # noqa: E501
    """Stop a VM and CNT monitoring agent

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = DeleteAgent.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def enable_agent_vnf(payload):  # noqa: E501
    """Start a VM and CNT monitoring agent

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = DeleteAgent.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_agent_vnf(payload):  # noqa: E501
    """Update the configuration of a VM and CNT agent

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = UpdateModelVnf.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
