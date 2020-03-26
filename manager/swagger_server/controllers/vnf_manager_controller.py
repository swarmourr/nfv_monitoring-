import connexion
import six

from swagger_server.models.admin_model_system import AdminModelSystem  # noqa: E501
from swagger_server.models.delete_agent import DeleteAgent  # noqa: E501
from swagger_server.models.update_model_vnf import UpdateModelVnf  # noqa: E501
from swagger_server import util


def add_agent_vnf(payload):  # noqa: E501
    """Add new VM and CNT monitoring agent

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = AdminModelSystem.from_dict(connexion.request.get_json())  # noqa: E501
    return payload


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
