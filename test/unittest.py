import json
import sys
import unittest

from benedict import benedict

import responses
from responses import matchers

import logging

from src.tempstick_py.tempstick import (
    UPDATE_SENSOR_SETTINGS,
    TempStickSensor,
    make_request,
    GET_SENSORS,
    GET_SENSOR,
    GET_READINGS,
    REQUEST_TYPES,
    normalize_settings,
)
from src.tempstick_py._helpers import format_mac, format_datetime
from src.tempstick_py.exceptions import FilterRemovesRange, InvalidApiKeyError

from .data import (
    INVALID_KEY_RESPONSE,
    SENSOR,
    GENERATED_API_KEY,
    GET_SENSORS_DICT,
    GET_SENSOR_READING_DICT,
    GET_SENSORS_MULTIPLE,
    SENSOR_3_CHANGES,
    UPDATED_SETTINGS,
)

GET_SENSORS_JSON = json.dumps(GET_SENSORS_DICT)
GET_SENSOR_READINGS_JSON = json.dumps(GET_SENSOR_READING_DICT)
INVALID_KEY_RESPONSE_JSON = json.dumps(INVALID_KEY_RESPONSE)
GET_SENSORS_MULTIPLE_JSON = json.dumps(GET_SENSORS_MULTIPLE)

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

        self.headers = {"X-API-KEY": API_KEY}

        # valid for get_sensors
        self.r_mock.get(
            url="https://tempstickapi.com/api/v1/sensors/all",
            headers=self.headers,
            json=GET_SENSORS_JSON,
            match=[matchers.header_matcher({"X-API-KEY": API_KEY})],
        )
        # valid for get_sensors, multiple sensors
        self.r_mock.get(
            url="https://tempstickapi.com/api/v1/sensors/all",
            headers=self.headers,
            json=GET_SENSORS_MULTIPLE_JSON,
            match=[matchers.header_matcher({"X-API-KEY": API_KEY.replace("P", "a")})],
        )
        # valid for get_sensor_readings
        self.r_mock.get(
            url="https://tempstickapi.com/api/v1/sensors/{sensor_id}/readings".format(
                sensor_id=SENSOR_ID
            ),
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
        # valid for get_sensor (singular)
        self.r_mock.get(
            url="https://tempstickapi.com/api/v1/sensors/{}".format(SENSOR_ID),
            headers=self.headers,
            json=SENSOR,
            match=[matchers.header_matcher({"X-API-KEY": API_KEY})],
        )
        # valid for update_sensor POST
        self.r_mock.post(
            url="https://tempstickapi.com/api/v1/sensor/{}".format(SENSOR_ID),
            json=UPDATED_SETTINGS,
        )

        sensor = TempStickSensor(SENSOR.get("id"), SENSOR_ID, SENSOR.get("sensor_name"))
        self.simple_sensor = sensor

        print("{} | setup -> id: {}".format(logger_name(self), sensor.id))
        print("")
        # print("GET_SENSORS_MULTIPLE_JSON:\n{}".format(GET_SENSORS_MULTIPLE_JSON))
        # responses.add(
        #     method='GET',
        #     url='https://tempstickapi.com/api/v1/sensors/all',
        #     headers={'X-API-KEY': API_KEY},
        #     json=GET_SENSORS_JSON,
        # )

    def tearDown(self) -> None:
        self.r_mock.stop()
        self.r_mock.reset()

    # @responses.activate
    def test_make_request_get_sensors(self):
        print("")
        log = logging.getLogger(logger_name(self))
        log.debug("API Key: {key}".format(key=API_KEY))

        data = make_request(GET_SENSORS, API_KEY)

        log.debug("data: {}".format(data))

        self.assertEqual(data.get("message"), "get sensors")

    def test_get_sensors_multiple(self):
        print("")
        log = logging.getLogger(logger_name(self))
        sensors = TempStickSensor.get_sensors(API_KEY.replace("P", "a"))

        self.assertEqual(sensors[-1].sensor_id, SENSOR_3_CHANGES.get("sensor_id"))

    def test_get_readings(self):
        print("")
        print("sensor_id: {}".format(SENSOR_ID))

        response = make_request(GET_READINGS, API_KEY, SENSOR_ID)
        response_b = benedict(response)
        readings = response_b.get_list("data.readings")

        first_reading_sensor_time = readings[0].get("sensor_time")

        print(
            "{} | First reading sensor time: {}".format(
                logger_name(self), first_reading_sensor_time
            )
        )
        logging.info("First reading sensor time: {}".format(first_reading_sensor_time))

        self.assertEqual(first_reading_sensor_time, "2022-09-04 07:00:36Z")

    def test_get_readings_class(self):
        print("")

        logger = {"log_name": logger_name(self)}
        log_print(("sensor_id", self.simple_sensor.sensor_id), **logger)

        readings = self.simple_sensor.get_readings(API_KEY)

        log_print(("readings[0]", readings[0]), **logger)

        self.assertEqual(readings[0].get("temperature"), 24.72)

    def test_get_readings_filter(self):
        print("")

        logger = {"log_name": logger_name(self)}

        # split range which goes from 2022-09-04 07:00:00Z - 2022-09-05 06:59:59Z
        filter_cutoff = format_datetime("2022-09-04 19:00:00Z")

        log_print(("filter_cutoff", filter_cutoff), **logger)

        readings = self.simple_sensor.get_readings(API_KEY, filter_cutoff)

        log_print(("readings[0]", readings[0]), **logger)

        self.assertGreater(
            format_datetime(readings[0].get("sensor_time")), filter_cutoff
        )

    def test_get_readings_filter_all(self):
        print("")

        logger = logging.getLogger(__name__)
        log_print(("log_name", logger.name), logger_name(self))

        # logger = {'log_name': logger_name(self)}

        # current range goes from 2022-09-04 07:00:00Z - 2022-09-05 06:59:59Z
        filter_cutoff = format_datetime("2022-09-06 07:00:00Z")

        logger.debug("{}: {}".format("filter_cutoff", filter_cutoff))

        # log_print(('filter_cutoff', filter_cutoff), **logger)

        self.assertRaises(
            FilterRemovesRange, self.simple_sensor.get_readings, API_KEY, filter_cutoff
        )

    def test_invalid_api_key(self):
        print("")

        logger = {"log_name": logger_name(self)}

        self.assertRaises(
            InvalidApiKeyError, TempStickSensor.get_sensors, "invalid_api_key"
        )

    def test_get_sensor(self):
        print("")

        logger = logging.getLogger(__name__)
        log_print(("log_name", logger.name), logger_name(self))

        sensor = self.simple_sensor

        sensor = sensor.get_sensor(API_KEY)

        self.assertEqual(sensor.last_temp, SENSOR.get("last_temp"))

    def test_invalid_mac_address(self):
        print("")

        sensor_test = TempStickSensor(
            "654981", "981656", "invalid mac test", "ig:e8:4:90:!i:99"
        )

        self.assertIsNone(sensor_test.sensor_mac_address)
        # self.assertEqual(sensor.sensor_mac_address, None)

    def test_empty_mac_address(self):
        print("")

        sensor = self.simple_sensor

        self.assertIsNone(sensor.sensor_mac_address)

    def test_normalize_settings(self):
        print("")

        sensor = self.simple_sensor

        settings_in = {
            "sensor_name": "test name",
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

        settings_new = normalize_settings(sensor, settings_in)

        self.assertEqual(settings_new.get("sensor_name"), "test name")

    def test_update_settings(self):
        print("")

        logger = logging.getLogger(__name__)
        log_print(("log_name", logger.name), logger_name(self))

        sensor = self.simple_sensor

        settings_in = {
            "sensor_name": "test name",
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

        update = sensor.update_sensor_settings(API_KEY, settings_in)

        log_print({"name": "update", "value": update}, sensor, logger.name)

        self.assertEqual(sensor.sensor_name, "test name")


def logger_name(test):
    logger_name = "{function}".format(class_name=test.__class__.__name__, function=test)
    return logger_name


def log_print(variable: dict, obj=None, log_name=None):
    logger = log_name if log_name else logger_name(obj)
    name, value = variable
    value = "{log_name} | {variable_name}: {value}".format(
        log_name=logger, variable_name=name, value=value
    )
    print(value)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
