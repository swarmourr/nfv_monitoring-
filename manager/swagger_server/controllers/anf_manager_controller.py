import connexion
import six

from swagger_server.models.osgi_host import OsgiHost  # noqa: E501
from swagger_server.models.osgi_model_jvm import OsgiModelJvm  # noqa: E501
from swagger_server import util


def add_agent_anf(payload):  # noqa: E501
    """Add new applicatif  monitoring agent

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = OsgiModelJvm.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_agent(payload):  # noqa: E501
    """Stop and delete applicatif  monitoring agent

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = OsgiHost.from_dict(connexion.request.get_json())  # noqa: E501
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
    return 'do some magic!'


def update_agent_anf(payload):  # noqa: E501
    """Update the configuration of an applicatif agent

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = OsgiModelJvm.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
