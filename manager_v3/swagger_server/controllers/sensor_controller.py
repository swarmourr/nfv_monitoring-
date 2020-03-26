import connexion
import six

from swagger_server.models.notification_model import NotificatinModel  # noqa: E501
from swagger_server.models.symptome import Symptome  # noqa: E501
from swagger_server import util


def add_db_config(payload):  # noqa: E501
    """Add database et data flow configuration

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = DbModel.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_all_agents(path):  # noqa: E501
    """Get all agent deployed

     # noqa: E501

    :param path: 
    :type path: str

    :rtype: None
    """
    return 'do some magic!'


def get_all_data(path):  # noqa: E501
    """Get all data of an agent

     # noqa: E501

    :param path: 
    :type path: str

    :rtype: None
    """
    return 'do some magic!'


def new_information_stored(payload):  # noqa: E501
    """get notification about new data

     # noqa: E501

    :param path: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = payload[0]["body"]
    print(payload)
    return 'do some magic!'
 

def send_new_symptome(payload):  # noqa: E501
    """send new symptome

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = Symptome.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
