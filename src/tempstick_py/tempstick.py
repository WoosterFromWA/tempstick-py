# import http.client
# import os
# from pathlib import Path
# import environ
from datetime import datetime
from email import message
import json
from urllib.error import HTTPError
import requests
from decimal import Decimal
# import json

from benedict import benedict

from furl import furl

from .exceptions import FilterRemovesRange, InvalidApiKeyError

from ._helpers import format_mac, format_datetime, set_attr_from_dict

# import macaddress

# BASE_DIR = Path(__file__).resolve()

# env_path = os.path.join(BASE_DIR, ".env")

# print(env_path)

# environ.Env.read_env(env_path)

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
    # __slots__ = (
    #     'sensor_id',
    #     'sensor_name',
    #     'sensor_mac_address'
    # )

    def __init__(
        self,
        sensor_id,
        sensor_name:str = None,
        sensor_mac_addr:str = None,
    ) -> None:
        self.sensor_id = sensor_id
        self.sensor_name = sensor_name
        try:
            self.sensor_mac_address = format(sensor_mac_addr)
        except AttributeError:
            self.sensor_mac_address = None

    @classmethod
    def from_get_sensor(cls, sensor:dict):
        set_attr_from_dict(cls, sensor)

        return cls

    @classmethod
    def get_sensors(cls, api_key:str) -> list:
        """Return list of sensors."""
        data = make_request(GET_SENSORS, api_key)

        data_b = benedict(data)

        sensors_list = []
        for sensor in data_b.get_list("data.items"):
            print("sensor_id: {}".format(sensor['sensor_id']))
            sensor_obj = cls.from_get_sensor(sensor)
            sensors_list.append(sensor_obj)

        return sensors_list

    def get_readings(self, api_key:str, filter_cutoff:datetime = None) -> list:
        """Return list of readings, optionally filtered cutoff date
        
        :param filter_cutoff: Filter all readings older than this datetime
        :type filter_cutoff: datetime, optional
        """

        
        response = make_request(GET_READINGS, api_key, self.sensor_id)

        print("response: ".format(response))

        data = response.get("data")
        readings = data.get("readings")

        # print("type(filter_cutoff): {}".format(type(filter_cutoff)))
        # print("type(start): {}".format(data))

        if filter_cutoff:
            try:
                filter_cutoff = format_datetime(filter_cutoff)
            except TypeError:
                logger.debug("Filter cutoff already datetime. [{}]".format(filter_cutoff))

            start = format_datetime(data.get("start"))
            
            length_before = len(readings)
            if start < filter_cutoff:
                readings = [x for x in readings if format_datetime(x.get("sensor_time")) > filter_cutoff]
                # readings = filter(lambda x: format_datetime(x['sensor_time']) > filter_cutoff, readings)

            length_after = len(readings)

            if length_after == 0:
                raise FilterRemovesRange(filter_cutoff, range_lower=start, range_upper=format_datetime(data.get("end")))
            elif (diff := length_before - length_after) > 0:
                print("{} readings removed.".format(diff))

        return readings

class Message:
    def __init__(
        self,
        temperature:Decimal,
        humidity:Decimal,
        sensor_time_utc,
        voltage:Decimal = None,
        rssi = None,
        time_to_connect = None,
        offline = None,
    ) -> None:
        self.sensor_values = {
            "temperature": temperature,
            "humidity": humidity,
            "voltage": voltage,
            "rssi": rssi
        }
        self.time_to_connect = time_to_connect
        self.sensor_time_utc = sensor_time_utc
        self.offline = offline

    @classmethod
    def fromreadings(cls, readings:list[dict]):
        message_list = []
        for reading in readings:
            message = cls.fromreading(reading)
            message_list.append(message)

        return message_list

    @classmethod
    def fromreading(cls, reading:dict):
        kwargs = {
            "temperature": reading.get("temperature"),
            "humidity": reading.get("humidity"),
            "sensor_time_utc": reading.get("sensor_time"),
            "offline": reading.get("offline")
        }
        return cls(**kwargs)

    @classmethod
    def fromsensor(cls, messages:list[dict]):
        message_list = []
        for message in messages:
            kwargs = {
                "temperature": message.get("temperature"),
                "humidity": message.get("humidity"),
                "sensor_time_utc": message.get("sensor_time_utc"),
                "time_to_connect": message.get("time_to_connect"),
                "rssi": message.get("RSSI"),
                "voltage": message.get("voltage"),
            }
            message_list.append(cls(**kwargs))

        return message_list

# def get_sensors(api_key:str) -> list[TempStickSensor]:
#     # logger.warning("key: {}".format(api_key))
#     print(api_key)
#     data = make_request(GET_SENSORS, api_key)

#     # logger.info("data: {}".format(data))

#     data_b = benedict(data)

#     sensors_list = []
#     for sensor in data_b.get_list("data.items"):
#         print("sensor: {}".format(sensor))
#         sensor_obj = TempStickSensor.fromsensor(**sensor)
#         sensors_list.append(sensor_obj)

#     return sensors_list



def make_request(request_type:REQUEST_TYPES, api_key:str, sensor_id:str = None):
    url = furl("https://tempstickapi.com")
    url_adder = furl(request_type.format(sensor_id))

    print("Adder: {}".format(url_adder))
    logger.info("Adder: {}".format(url_adder))

    url.join(url, url_adder)

    payload={}
    headers = {
    'X-API-KEY': api_key
    }

    url_str = url.tostr()

    print("URL String: {}".format(url_str))

    response = requests.get(url_str, headers=headers, data=payload)

    try:
        response.raise_for_status()
        response_json = response.json()

        print("Response Status: {}".format(response.status_code))
    except HTTPError as http_err:
        print('HTTP error occured: {}'.format(http_err))
        raise
    except Exception as err:
        print('Other error occured: {}'.format(err))
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