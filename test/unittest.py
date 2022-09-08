from datetime import datetime
import json
import sys
import unittest
import pprint

from benedict import benedict

import responses
from responses import matchers

import requests

import logging

# from os import environ

# from src.tempstick_py import _helpers, tempstick

from src.tempstick_py.tempstick import TempStickSensor, make_request, GET_SENSORS, GET_SENSOR, GET_READINGS, REQUEST_TYPES
from src.tempstick_py._helpers import format_mac, format_datetime
from src.tempstick_py.exceptions import FilterRemovesRange, InvalidApiKeyError

from .data import INVALID_KEY_RESPONSE, SENSOR, GENERATED_API_KEY, GET_SENSORS_DICT, GET_SENSOR_READING_DICT

GET_SENSORS_JSON = json.dumps(GET_SENSORS_DICT)
GET_SENSOR_READINGS_JSON = json.dumps(GET_SENSOR_READING_DICT)
INVALID_KEY_RESPONSE_JSON = json.dumps(INVALID_KEY_RESPONSE)

SENSOR_ID = SENSOR.get("sensor_id", None)

API_KEY = GENERATED_API_KEY

class TestNonApiFunctions(unittest.TestCase):
    def test_format_mac(self):
        self.assertEqual(format_mac("A4:E5:7C:02:11:12"), "a4:e5:7c:02:11:12")

    def test_mac_wrong_length(self):
        self.assertRaises(AssertionError, format_mac, "A4:E5:7C:02:11:1")
        # self.failUnlessRaises(AssertionError, format_mac, "A4:E5:7C:02:11:1")

    def test_mac_invalid_chars(self):
        self.assertRaises(AssertionError, format_mac, "A4:E5:7C:02:11:1°")


class TestSensorApi(unittest.TestCase):
    def setUp(self):
        self.r_mock = responses.RequestsMock(assert_all_requests_are_fired=False)
        self.r_mock.start()

        self.headers = {'X-API-KEY': API_KEY}

        # valid for get_sensors
        self.r_mock.get(
            url="https://tempstickapi.com/api/v1/sensors/all",
            headers=self.headers,
            json=GET_SENSORS_JSON,
            match=[matchers.header_matcher({"X-API-KEY": API_KEY})],
        )
        # valid for get_sensor_readings
        self.r_mock.get(
            url="https://tempstickapi.com/api/v1/sensors/{sensor_id}/readings".format(sensor_id=SENSOR_ID),
            headers=self.headers,
            json=GET_SENSOR_READINGS_JSON,
            match=[matchers.header_matcher({"X-API-KEY": API_KEY})],
        )
        # valid for get_sensors, but with response for invalid API key
        self.r_mock.get(
            url="https://tempstickapi.com/api/v1/sensors/all",
            headers=self.headers,
            json=INVALID_KEY_RESPONSE_JSON,
        )

        sensor = TempStickSensor(SENSOR_ID, 'test sensor 1')
        self.simple_sensor = sensor

        print("{} | setup -> sensor_id: {}".format(logger_name(self), sensor.sensor_id))
        # print("")
        # print("GET_SENSORS_JSON:\n{}".format(GET_SENSORS_JSON))
        # responses.add(
        #     method='GET',
        #     url='https://tempstickapi.com/api/v1/sensors/all',
        #     headers={'X-API-KEY': API_KEY},
        #     json=GET_SENSORS_JSON,
        # )

    def tearDown(self) -> None:
        self.r_mock.stop()
        self.r_mock.reset()

    @unittest.skip("used to test testing")
    def test_simple(self):
        name = logger_name(self)
        log = logging.getLogger(name)
        print("Log name: {}".format(log.name))
        log.debug("Log Name: {}".format(log.name))
        self.assertEqual(1,1)

    # @responses.activate
    def test_make_request_get_sensors(self):
        print("")
        log = logging.getLogger(logger_name(self))
        log.debug("API Key: {key}".format(key=API_KEY))

        data = make_request(GET_SENSORS, API_KEY)

        log.debug("data: {}".format(data))

        self.assertEqual(data.get('message'), 'get sensors')

    def test_get_sensors(self):
        print("")
        log = logging.getLogger(logger_name(self))
        sensors = TempStickSensor.get_sensors(API_KEY)
        if len(sensors) > 0:
            print("{} | First sensor id: {}".format(log.name, sensors[0].sensor_id))
            print("{} | Last Checkin: {}".format(log.name, sensors[0].last_checkin))
            log.debug("First sensor: {}".format(sensors[0]))
        else:
            print("{} | No sensors found.".format(log.name))
            log.debug("No sensors found.")

        self.assertEqual(sensors[0].sensor_id, SENSOR_ID)

    def test_get_readings(self):
        print("")
        # log = logging.getLogger(logger_name(self))
        # log.debug("sensor_id: {}".format(SENSOR_ID))
        print("sensor_id: {}".format(SENSOR_ID))

        response = make_request(GET_READINGS, API_KEY, SENSOR_ID)
        response_b = benedict(response)
        readings = response_b.get_list("data.readings")

        first_reading_sensor_time = readings[0].get("sensor_time")

        print("{} | First reading sensor time: {}".format(logger_name(self), first_reading_sensor_time))
        logging.info("First reading sensor time: {}".format(first_reading_sensor_time))

        self.assertEqual(first_reading_sensor_time, "2022-09-04 07:00:36Z")

    def test_get_readings_class(self):
        print("")

        logger = {'log_name': logger_name(self)}
        log_print(('sensor_id', self.simple_sensor.sensor_id), **logger)

        readings = self.simple_sensor.get_readings(API_KEY)

        log_print(('readings[0]', readings[0]), **logger)

        self.assertEqual(readings[0].get("temperature"), 24.72)

    def test_get_readings_filter(self):
        print("")

        logger = {'log_name': logger_name(self)}

        # split range which goes from 2022-09-04 07:00:00Z - 2022-09-05 06:59:59Z
        filter_cutoff = format_datetime('2022-09-04 19:00:00Z')

        log_print(('filter_cutoff', filter_cutoff), **logger)

        readings = self.simple_sensor.get_readings(API_KEY, filter_cutoff)

        log_print(('readings[0]', readings[0]), **logger)

        self.assertGreater(format_datetime(readings[0].get('sensor_time')), filter_cutoff)

    def test_get_readings_filter_all(self):
        print("")

        logger = {'log_name': logger_name(self)}

        # current range goes from 2022-09-04 07:00:00Z - 2022-09-05 06:59:59Z
        filter_cutoff = format_datetime('2022-09-06 07:00:00Z')

        log_print(('filter_cutoff', filter_cutoff), **logger)

        self.assertRaises(FilterRemovesRange, self.simple_sensor.get_readings, API_KEY, filter_cutoff)

    def test_invalid_api_key(self):
        print("")

        logger = {'log_name': logger_name(self)}

        # sensors = TempStickSensor.get_sensors('invalid_api_key')

        # log_print(('sensors[0].get("last_checkin")', sensors[0].get("last_checkin")), **logger)

        self.assertRaises(InvalidApiKeyError, TempStickSensor.get_sensors, 'invalid_api_key')

def logger_name(test):
    logger_name = "{function}".format(class_name=test.__class__.__name__, function=test)
    return logger_name

def log_print(variable:dict, obj = None, log_name = None):
    logger = log_name if log_name else logger_name(obj)
    name, value = variable
    value = "{log_name} | {variable_name}: {value}".format(log_name=logger, variable_name=name, value=value)
    print(value)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # log = logging.getLogger(__name__)
    # print("hello")
    # logging.getLogger("TestSensorApi.test_make_request_get_sensors").setLevel(logging.DEBUG)
    # logging.getLogger("TestSensorApi.test_simple").setLevel(logging.DEBUG)
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)