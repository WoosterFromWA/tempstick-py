import http.client
from decimal import Decimal
import json

from benedict import benedict

import logging

logger = logging.getLogger(__name__)


class TempStickSensor:
    def __init__(
        self,
        id,
        version,
        sensor_id,
        sensor_name,
        sensor_mac_address,
        owner_id,
        type,
        alert_interval,
        send_interval,
        last_temp:Decimal,
        last_humidity:Decimal,
        last_voltage,
        wifi_connect_time,
        rssi,
        last_checkin,
        next_checkin,
        ssid,
        offline,
        alerts,
        use_sensor_settings,
        temp_offset,
        humidity_offset,
        alert_temp_below:Decimal,
        alert_temp_above:Decimal,
        alert_humidity_below:Decimal,
        alert_humidity_above:Decimal,
        connection_sensivity,
        use_alert_interval,
        use_offset,
        battery_pct,
        last_messages
    ) -> None:
        self.id = id
        self.version = version
        self.sensor_id = sensor_id
        self.sensor_name = sensor_name
        self.sensor_mac_address = sensor_mac_address
        self.owner_id = owner_id
        self.type = type
        self.intervals = {
            "alert_interval": alert_interval,
            "send_interval": send_interval
        }
        self.last_sensor_values = {
            "temperature": last_temp,
            "humidity": last_humidity,
            "voltage": last_voltage
        }
        self.wifi_connect_time = wifi_connect_time
        self.rssi = rssi
        self.checkins = {
            "last": last_checkin,
            "next": next_checkin
        }
        self.ssid = ssid
        self.offline = offline
        self.alerts = alerts
        self.use_sensor_settings = use_sensor_settings
        self.offsets = {
            "temperature": temp_offset,
            "humidity": humidity_offset
        }
        self.alert_ranges = {
            "temperature": (alert_temp_below, alert_temp_above),
            "humidity": (alert_humidity_below, alert_humidity_above)
        }
        self.connection_sensitivity = connection_sensivity
        self.use_alert_interval = use_alert_interval
        self.use_offset = use_offset
        self.battery_percent = battery_pct
        self.last_messages = last_messages

        @classmethod
        def from_get_sensor(cls, response:dict):
            response_b = benedict(response)

            last_messages_raw = response_b.get_list("data.last_messages")
            last_messages = Message.fromsensor(last_messages_raw)

            response_b.remove("data.last_messages")

            # kwargs = {
            #     "id": response_b.get_str("data.id"),
            #     "version": response_b.get_str("data.version"),
            #     "sensor_id": 
            # }

            return cls(response_b.get_dict("data"))


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

def get_sensors(api_key:str) -> list[TempStickSensor]:
    logger.warning("key: {}".format(api_key))
    print(api_key)
    data = make_request(GET_SENSORS, api_key)

    logger.info("data: {}".format(data))

    data_b = benedict(data)

    sensors_list = []
    for sensor in data_b.get_list("data.items"):
        sensor_obj = TempStickSensor(**sensor)
        sensors_list.append(sensor_obj)

    return sensors_list

GET_SENSORS = "api/v1/sensors/all"
GET_SENSOR = "api/v1/sensors/{}"
GET_READINGS = "api/v1/sesnosrs/{}/readings"
REQUEST_TYPES = [
    GET_SENSORS,
    GET_SENSOR,
    GET_READINGS,
]

def make_request(request_type:REQUEST_TYPES, api_key:str, sensor_id:str = None):
    print(request_type)
    conn = http.client.HTTPSConnection("tempstickapi.com")

    headers = {"Content-Type": "application/json", "X-KEY-API": api_key}

    conn.request("GET", request_type.format(sensor_id), headers = headers)

    res = conn.getresponse()
    print("res: {}".format(res))
    data_bytes = res.read()

    logger.info("data_bytes: {}".format(data_bytes))

    data_json = json.loads(data_bytes.decode("utf-8"))

    return data_json