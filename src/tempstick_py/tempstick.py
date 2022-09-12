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
        set_attr_from_dict(cls, sensor)

        return cls

    @classmethod
    def get_sensors(cls, api_key: str) -> list:
        """Return list of 'TempStickSensor's given API key."""
        data = make_request(GET_SENSORS, api_key)

        data_b = benedict(data)

        sensors_list = [cls.from_get_sensor(x) for x in data_b.get_list("data.items")]

        return sensors_list

    def get_readings(self, api_key: str, filter_cutoff: datetime = None) -> list:
        """Return list of readings, optionally filtered cutoff date

        :param filter_cutoff: Filter all readings older than this datetime
        :type filter_cutoff: datetime, optional
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
        """Return sensor values."""
        sensor = make_request(GET_SENSOR, api_key, self.sensor_id)

        sensor_obj = self.from_get_sensor(sensor)

        set_attr_from_dict(self, sensor)

        return self


def make_request(request_type: REQUEST_TYPES, api_key: str, sensor_id: str = None):
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
