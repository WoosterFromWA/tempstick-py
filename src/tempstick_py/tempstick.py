"""Module that interfaces with the https://tempstickapi.com interface"""
from datetime import datetime
from doctest import REPORT_UDIFF
import json
from urllib.error import HTTPError
import requests

from benedict import benedict

from furl import furl

from .exceptions import FilterRemovesRange, InvalidApiKeyError

from ._helpers import format_mac, format_datetime, set_attr_from_dict

GET_SENSORS = "GET", "/api/v1/sensors/all"
GET_SENSOR = "GET", "/api/v1/sensors/{sensor_id}"
GET_READINGS = "GET", "/api/v1/sensors/{sensor_id}/readings"
UPDATE_SENSOR_SETTINGS = "POST", "api/v1/sensor/{sensor_id}"
REQUEST_TYPES = [
    GET_SENSORS,
    GET_SENSOR,
    GET_READINGS,
    UPDATE_SENSOR_SETTINGS,
]

import logging

logger = logging.getLogger(__name__)


class TempStickSensor:
    """Object representing a Temperature Stick

    :param id: ID of the sensor; not to be confused with `sensor_id`; provided by the API
    :type id: str, required
    :param sensor_id: Sensor ID, also provided by the API
    :type sensor_id: str, required
    :param sensor_name: Name of sensor; from API, can be specified in their dashboard
    :type sensor_name: str, optional
    :param sensor_mac_address: MAC address of device; attribute will be none if invalid
    :type sensor_mac_address: str, optional
    """

    # __slots__ = ("id" "sensor_id", "sensor_name", "sensor_mac_address")

    def __init__(
        self,
        id,
        sensor_id: str,
        sensor_name: str = None,
        sensor_mac_addr: str = None,
    ) -> None:
        self.id = id
        self.sensor_id = sensor_id
        self.sensor_name = sensor_name
        if sensor_mac_addr:
            try:
                self.sensor_mac_address = format_mac(sensor_mac_addr)
            except AssertionError:
                self.sensor_mac_address = None
        else:
            self.sensor_mac_address = None

    @classmethod
    def from_get_sensor(cls, sensor: dict):
        """Return :class:`TempStickSensor` given JSON/dict input.

        :param sensor: dict of sensor properties obtained from API; must include required properties of class
        :type sensor: dict, required
        :return: sensor object
        :rtype: :class:`TempStickSensor`
        """
        set_attr_from_dict(cls, sensor)

        return cls

    @classmethod
    def get_sensors(cls, api_key: str) -> list:
        """Return list of :class:`TempStickSensor` s given API key.

        :param api_key: API key obtained from https://tempstick.com 's dashboard
        :type api_key: str, required
        :return: list of sensor objects
        :rtype: list[:class:`TempStickSensor`]
        """
        data = make_request(GET_SENSORS, api_key)

        data_b = benedict(data)

        sensors_list = [cls.from_get_sensor(x) for x in data_b.get_list("data.items")]

        return sensors_list

    def get_readings(self, api_key: str, filter_cutoff: datetime = None) -> list:
        """Return list of readings, optionally filtered cutoff date

        :param filter_cutoff: Filter all readings older than this datetime
        :type filter_cutoff: datetime, optional
        :return: list of reading dicts
        :rtype: list[dict]
        """
        response = make_request(GET_READINGS, api_key, self.sensor_id)

        print("response: ".format(response))

        data = response.get("data")
        readings = data.get("readings")

        if filter_cutoff:
            try:
                filter_cutoff = format_datetime(filter_cutoff)
            except TypeError:
                logger.debug(
                    "Filter cutoff already datetime. [{}]".format(filter_cutoff)
                )

            start = format_datetime(data.get("start"))

            length_before = len(readings)
            if start < filter_cutoff:
                readings = [
                    x
                    for x in readings
                    if format_datetime(x.get("sensor_time")) > filter_cutoff
                ]

            length_after = len(readings)

            if length_after == 0:
                raise FilterRemovesRange(
                    filter_cutoff,
                    range_lower=start,
                    range_upper=format_datetime(data.get("end")),
                )
            elif (diff := length_before - length_after) > 0:
                print("{} readings removed.".format(diff))

        return readings

    def get_sensor(self, api_key: str):
        """Update :class:`TempStickSensor` with data from API

        :param api_key: API key obtained from https://tempstick.com 's dashboard
        :type api_key: str, required
        """
        sensor = make_request(GET_SENSOR, api_key, self.sensor_id)

        # sensor_obj = self.from_get_sensor(sensor)

        set_attr_from_dict(self, sensor)

        return self

    def update_sensor_settings(self, api_key: str, settings: dict):
        """Post new settings to sensor

        :param api_key: API key obtained from https://tempstick.com 's dashboard
        :type api_key: str, required
        :param settings: dictionary containing any settings to be updated; see docs for available settings
        :type settings: dict, required
        """
        update = make_request(
            UPDATE_SENSOR_SETTINGS, api_key, sensor_id=self.sensor_id, settings=settings
        )

        set_attr_from_dict(self, update.get("data"))

        return update.get("message")


def api_post(
    request_type: REQUEST_TYPES, api_key: str, sensor_id: str, payload: dict
) -> dict:
    """Update data using API POST"""
    url = furl("https://tempstickapi.com")
    method, request_type = request_type
    url_adder = furl(request_type.format(sensor_id))

    url.join(url, url_adder)

    payload = {
        "sensor_name": "Network Closet",
        "use_alert_interval": "1",
        "send_interval": "1800",
        "alert_interval": "600",
        "connection_sensitivity": "2",
        "use_offset": "0",
        "temp_offset": "0",
        "humidity_offset": "0",
        "alert_temp_below": "21.11",
        "alert_temp_above": "25",
        "alert_humidity_above": "50",
    }


def normalize_settings(sensor: TempStickSensor, settings: dict) -> dict:
    settings_b = benedict(settings)

    required_settings = [
        ("sensor_name", "sensor_name"),
        ("use_alert_interval", "use_alert_interval"),
        ("send_interval", "send_interval"),
        ("connection_sensitivity", "connection_sensitivity"),
        ("use_offset", "use_offset"),
        ("temp_offset", "temp_offset"),
        ("humidity_offset", "humidity_offset"),
    ]

    new_dict = {}
    for s, a in required_settings:
        attr = getattr(sensor, a, None)
        new_dict[s] = settings_b.get_str(s, attr)

    return new_dict


def make_request(
    request_type: REQUEST_TYPES,
    api_key: str,
    sensor_id: str = None,
    sensor: TempStickSensor = None,
    settings: dict = None,
):
    """Return data from API request

    :param request_type: which API call is being made; api/v1/sensors/all, api/v1/sensors/{sensor_id}, api/v1/sensors/{sensor_id}/readings
    :type request_type: str, required
    :param api_key: API key obtained from https://tempstick.com 's dashboard
    :type api_key: str, required
    :param sensor_id: unique sensor_id as obtained from get_sensors; used for individual calls
    :type sensor_id: str, optional
    :return: API response, parsed as required
    :rtype: json
    """
    method, request_type = request_type

    url = furl("https://tempstickapi.com")
    url_adder = furl(request_type.format(sensor_id=sensor_id))

    print("Adder: {}".format(url_adder))
    logger.info("Adder: {}".format(url_adder))

    url.join(url, url_adder)

    # payload = {}
    headers = {"X-API-KEY": api_key}

    url_str = url.tostr()

    print("URL String: {}".format(url_str))

    if method == "GET":
        payload = {}
        response = requests.get(url_str, headers=headers, data=payload)
    elif method == "POST":
        payload = normalize_settings(sensor, settings)
        response = requests.post(url_str, data=payload, headers=headers)

    try:
        response.raise_for_status()
        response_json = response.json()

        print("Response Status: {}".format(response.status_code))
    except HTTPError as http_err:
        print("HTTP error occured: {}".format(http_err))
        raise
    except Exception as err:
        print("Other error occured: {}".format(err))
        raise

    if not isinstance(response_json, dict):
        try:
            response_json = json.loads(response_json)
        except ValueError as val_err:
            print("Could not parse as JSON: {}".format(response_json))

    response_type = response_json.get("type")
    if response_type == "error":
        raise InvalidApiKeyError(response_type, response_json.get("message"))

    return response_json
