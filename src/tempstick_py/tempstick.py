"""Module that interfaces with the https://tempstickapi.com interface"""
from datetime import datetime
import json
from urllib.error import HTTPError
import requests

from benedict import benedict

from furl import furl

from .exceptions import FilterRemovesRange, InvalidApiKeyError

from ._helpers import format_mac, format_datetime, set_attr_from_dict

GET_SENSORS = "/api/v1/sensors/all"
GET_SENSOR = "/api/v1/sensors/{}"
GET_READINGS = "/api/v1/sensors/{}/readings"
REQUEST_TYPES = [
    GET_SENSORS,
    GET_SENSOR,
    GET_READINGS,
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


def make_request(request_type: REQUEST_TYPES, api_key: str, sensor_id: str = None):
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
    url = furl("https://tempstickapi.com")
    url_adder = furl(request_type.format(sensor_id))

    print("Adder: {}".format(url_adder))
    logger.info("Adder: {}".format(url_adder))

    url.join(url, url_adder)

    payload = {}
    headers = {"X-API-KEY": api_key}

    url_str = url.tostr()

    print("URL String: {}".format(url_str))

    response = requests.get(url_str, headers=headers, data=payload)

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
