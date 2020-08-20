import connexion
import six

from swagger_server.models.fatigue_body import FatigueBody  # noqa: E501
from swagger_server.models.hour_response import HourResponse  # noqa: E501
from swagger_server.models.quarters_response import QuartersResponse  # noqa: E501
from swagger_server.models.time_request import TimeRequest  # noqa: E501
from swagger_server import util


def v1_drivers_fatigue_post(body):  # noqa: E501
    """фиксировани усталости водителй

    приём (запись) данных о времени \&quot;на линии\&quot; и время на заказе для каждого водителя из заданного подможества # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = FatigueBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def v1_drivers_on_order_post(body):  # noqa: E501
    """Получение информации \&quot;на заказе\&quot; для группы водителей

    были ли водители на заказе в течение часа с момента __timestamp__ # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: QuartersResponse
    """
    if connexion.request.is_json:
        body = TimeRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def v1_drivers_online_hourly_post(body):  # noqa: E501
    """Получение информации \&quot;на линии\&quot; (online) для группы водителей.

    были ли водители на линии в течение часа с момента __timestamp__ # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: HourResponse
    """
    if connexion.request.is_json:
        body = TimeRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def v1_drivers_online_quater_hourly_post(body):  # noqa: E501
    """Получение информации \&quot;на линии\&quot; (online) для группы водителей

    были ли водители на линии в течение часа с момента __timestamp__ с информацией на каждые 15 мин # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: QuartersResponse
    """
    if connexion.request.is_json:
        body = TimeRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
