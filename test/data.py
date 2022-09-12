GENERATED_API_KEY = 'VD*Xy2gI*7@P5uHSR0xjTD$RT0Hua2'

SENSOR = {
    "id": "211973",
    "version": "1104",
    "sensor_id": "348052",
    "sensor_name": "test sensor 1",
    "sensor_mac_addr": "6J:IX:3L:ML:WO:ZF",
    "owner_id": "68131",
    "type": "DHT",
    "alert_interval": "600",
    "send_interval": "1800",
    "last_temp": 24.53,
    "last_humidity": 36.59,
    "last_voltage": 3,
    "wifi_connect_time": 1,
    "rssi": -35,
    "last_checkin": "2022-09-05 06:21:19-00:00Z",
    "next_checkin": "2022-09-05 06:51:19-00:00Z",
    "ssid": "test_ssid",
    "offline": "0",
    "use_sensor_settings": "0",
    "temp_offset": "0",
    "humidity_offset": "0",
    "alert_temp_below": "21.11",
    "alert_temp_above": "25.00",
    "alert_humidity_above": "50",
    "connection_sensitivity": "2",
    "use_alert_interval": 1,
    "use_offset": "0",
    "battery_pct": 100,
}

SENSOR_2_CHANGES = {
    "id": "546987",
    "sensor_id": "898541",
    "sensor_name": "test sensor 2",
    "sensor_mac_addr": "6J:IX:3L:ML:WO:ZH",
}

SENSOR_2 = SENSOR.copy()

print("SENSOR_2 before update: {}".format(SENSOR_2))

SENSOR_2.update(SENSOR_2_CHANGES)

print("SENSOR after SENSOR_2 update: {}".format(SENSOR))
print("SENSOR_2 after update: {}".format(SENSOR_2))

SENSOR_3_CHANGES = {
    "id": "651651",
    "sensor_id": "981694",
    "sensor_name": "test sensor 3",
    "sensor_mac_addr": "6J:IX:3L:M1:WO:ZF",
}

SENSOR_3 = SENSOR.copy()

print("SENSOR after SENSOR_3 assignment: {}".format(SENSOR))
print("SENSOR_3 before update: {}".format(SENSOR_3))

SENSOR_3.update(SENSOR_3_CHANGES)

GET_SENSOR_DICT = {
    "type": "success",
    "message": "get sensor",
    "data": {
        "id": "211973",
        "version": "1104",
        "sensor_id": "348052",
        "sensor_name": "test sensor 1",
        "sensor_mac_addr": "6J:IX:3L:ML:WO:ZF",
        "owner_id": "68131",
        "type": "DHT",
        "alert_interval": "600",
        "send_interval": "1800",
        "last_temp": 24.53,
        "last_humidity": 36.59,
        "last_voltage": 3,
        "wifi_connect_time": 1,
        "rssi": -35,
        "last_checkin": "2022-09-05 06:21:19-00:00Z",
        "next_checkin": "2022-09-05 06:51:19-00:00Z",
        "ssid": "test_ssid",
        "offline": "0",
        "alerts": [],
        "use_sensor_settings": "0",
        "temp_offset": "0",
        "humidity_offset": "0",
        "alert_temp_below": "21.11",
        "alert_temp_above": "25.00",
        "alert_humidity_below": "",
        "alert_humidity_above": "50",
        "connection_sensitivity": "2",
        "use_alert_interval": 1,
        "use_offset": "0",
        "battery_pct": 100,
        "last_messages": [
            {
                "temperature": 24.53,
                "humidity": 36.59,
                "voltage": "3.00",
                "RSSI": "-35",
                "time_to_connect": "1.0",
                "sensor_time_utc": "2022-09-05 06:21:19"
            },
            {
                "temperature": 24.69,
                "humidity": 36.68,
                "voltage": "3.00",
                "RSSI": "-36",
                "time_to_connect": "1.0",
                "sensor_time_utc": "2022-09-05 05:52:02"
            },
            {
                "temperature": 24.88,
                "humidity": 36.3,
                "voltage": "3.00",
                "RSSI": "-39",
                "time_to_connect": "1.0",
                "sensor_time_utc": "2022-09-05 05:22:45"
            },
            {
                "temperature": 25.03,
                "humidity": 36.78,
                "voltage": "3.00",
                "RSSI": "-41",
                "time_to_connect": "1.0",
                "sensor_time_utc": "2022-09-05 04:53:28"
            },
            {
                "temperature": 25.06,
                "humidity": 36.99,
                "voltage": "3.00",
                "RSSI": "-39",
                "time_to_connect": "1.0",
                "sensor_time_utc": "2022-09-05 04:43:46"
            }
        ]
    }
}

GET_SENSORS_BASE = {
    "type": "success",
    "message": "get sensors",
    "data": {
        "groups": [],
        "items": [
            {
                "group": 0,
            }
        ]
    }
}

GET_SENSORS_DICT = GET_SENSORS_BASE.copy()

GET_SENSORS_DICT["data"]["items"][0].update(SENSOR)

# GET_SENSORS_DICT = GET_SENSORS_BASE

print("SENSOR_2: {}".format(SENSOR_2))

SENSORS_LIST = [
    SENSOR_2,
    SENSOR_3,
]

GET_SENSORS_MULTIPLE = GET_SENSORS_BASE.copy()

# GET_SENSORS_MULTIPLE["data"]["items"].clear()

GET_SENSORS_MULTIPLE["data"]["items"] = SENSORS_LIST

GET_SENSOR_READING_DICT = {
    "type": "success",
    "message": "get messages",
    "data": {
        "start": "2022-09-04 07:00:00Z",
        "end": "2022-09-05 06:59:59Z",
        "readings": [
            {
                "sensor_time": "2022-09-04 07:00:36Z",
                "temperature": 24.72,
                "humidity": 37.69,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 07:30:04Z",
                "temperature": 24.68,
                "humidity": 38.09,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 07:40:10Z",
                "temperature": 24.78,
                "humidity": 37.84,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 08:09:18Z",
                "temperature": 24.66,
                "humidity": 37.09,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 08:38:36Z",
                "temperature": 24.53,
                "humidity": 37.51,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 09:07:50Z",
                "temperature": 24.47,
                "humidity": 37.95,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 09:37:09Z",
                "temperature": 24.57,
                "humidity": 38.2,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 10:06:24Z",
                "temperature": 24.59,
                "humidity": 38.07,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 10:35:42Z",
                "temperature": 24.46,
                "humidity": 37.75,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 11:04:56Z",
                "temperature": 24.38,
                "humidity": 38.23,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 11:34:14Z",
                "temperature": 24.34,
                "humidity": 38.53,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 12:03:28Z",
                "temperature": 24.32,
                "humidity": 38.74,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 12:32:45Z",
                "temperature": 24.32,
                "humidity": 38.48,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 13:02:03Z",
                "temperature": 24.24,
                "humidity": 37.95,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 13:31:18Z",
                "temperature": 24.16,
                "humidity": 38.22,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 14:00:33Z",
                "temperature": 24.14,
                "humidity": 38.49,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 14:29:50Z",
                "temperature": 24.13,
                "humidity": 38.64,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 14:59:08Z",
                "temperature": 24.16,
                "humidity": 39.45,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 15:28:22Z",
                "temperature": 24.28,
                "humidity": 40.01,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 15:57:41Z",
                "temperature": 24.3,
                "humidity": 38.44,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 16:26:57Z",
                "temperature": 24.21,
                "humidity": 38.82,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 16:56:11Z",
                "temperature": 24.28,
                "humidity": 40.46,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 17:25:27Z",
                "temperature": 24.41,
                "humidity": 41.35,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 17:54:45Z",
                "temperature": 24.56,
                "humidity": 41.58,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 18:24:01Z",
                "temperature": 24.69,
                "humidity": 42.61,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 18:53:19Z",
                "temperature": 24.87,
                "humidity": 42.98,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 19:22:36Z",
                "temperature": 25.02,
                "humidity": 42.28,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 19:32:16Z",
                "temperature": 25.04,
                "humidity": 41.99,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 19:41:55Z",
                "temperature": 25.09,
                "humidity": 41.78,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 19:51:34Z",
                "temperature": 25.08,
                "humidity": 41.55,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 20:01:15Z",
                "temperature": 25.09,
                "humidity": 41.38,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 20:10:55Z",
                "temperature": 25.07,
                "humidity": 41.2,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 20:20:36Z",
                "temperature": 25.06,
                "humidity": 41.28,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 20:30:17Z",
                "temperature": 25.1,
                "humidity": 41.31,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 20:39:59Z",
                "temperature": 25.1,
                "humidity": 41.64,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 20:49:40Z",
                "temperature": 25.16,
                "humidity": 41.68,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 20:59:22Z",
                "temperature": 25.17,
                "humidity": 41.46,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 21:09:04Z",
                "temperature": 25.18,
                "humidity": 41.55,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 21:18:44Z",
                "temperature": 25.2,
                "humidity": 41.57,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 21:28:23Z",
                "temperature": 25.2,
                "humidity": 41.5,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 21:38:05Z",
                "temperature": 25.21,
                "humidity": 41.4,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 21:47:45Z",
                "temperature": 25.21,
                "humidity": 41.32,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 21:57:24Z",
                "temperature": 25.21,
                "humidity": 41.28,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 22:07:05Z",
                "temperature": 25.2,
                "humidity": 41.23,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 22:16:45Z",
                "temperature": 25.21,
                "humidity": 41.13,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 22:26:27Z",
                "temperature": 25.21,
                "humidity": 41.09,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 22:36:06Z",
                "temperature": 25.23,
                "humidity": 41.08,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 22:45:48Z",
                "temperature": 25.24,
                "humidity": 40.97,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 22:55:28Z",
                "temperature": 25.21,
                "humidity": 40.84,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 23:05:10Z",
                "temperature": 25.22,
                "humidity": 40.76,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 23:14:46Z",
                "temperature": 25.25,
                "humidity": 40.65,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 23:24:25Z",
                "temperature": 25.23,
                "humidity": 40.53,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 23:34:04Z",
                "temperature": 25.21,
                "humidity": 40.45,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 23:43:45Z",
                "temperature": 25.22,
                "humidity": 40.3,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-04 23:53:27Z",
                "temperature": 25.18,
                "humidity": 40.38,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 00:03:07Z",
                "temperature": 25.19,
                "humidity": 40.55,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 00:12:48Z",
                "temperature": 25.21,
                "humidity": 40.53,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 00:22:29Z",
                "temperature": 25.22,
                "humidity": 40.31,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 00:32:12Z",
                "temperature": 25.23,
                "humidity": 40.32,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 00:41:51Z",
                "temperature": 25.24,
                "humidity": 40.36,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 00:51:33Z",
                "temperature": 25.25,
                "humidity": 40.14,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 01:01:11Z",
                "temperature": 25.27,
                "humidity": 39.91,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 01:10:51Z",
                "temperature": 25.29,
                "humidity": 39.92,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 01:20:32Z",
                "temperature": 25.3,
                "humidity": 39.76,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 01:30:13Z",
                "temperature": 25.32,
                "humidity": 39.5,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 01:39:54Z",
                "temperature": 25.31,
                "humidity": 39.48,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 01:49:34Z",
                "temperature": 25.33,
                "humidity": 39.33,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 01:59:16Z",
                "temperature": 25.34,
                "humidity": 39.14,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 02:08:55Z",
                "temperature": 25.34,
                "humidity": 39.1,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 02:18:36Z",
                "temperature": 25.37,
                "humidity": 38.87,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 02:28:18Z",
                "temperature": 25.35,
                "humidity": 38.75,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 02:38:00Z",
                "temperature": 25.38,
                "humidity": 38.72,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 02:47:39Z",
                "temperature": 25.37,
                "humidity": 38.43,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 02:57:21Z",
                "temperature": 25.34,
                "humidity": 38.39,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 03:07:02Z",
                "temperature": 25.37,
                "humidity": 38.18,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 03:16:43Z",
                "temperature": 25.37,
                "humidity": 37.87,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 03:26:24Z",
                "temperature": 25.37,
                "humidity": 37.9,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 03:36:06Z",
                "temperature": 25.34,
                "humidity": 37.73,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 03:45:46Z",
                "temperature": 25.3,
                "humidity": 37.59,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 03:55:26Z",
                "temperature": 25.27,
                "humidity": 37.53,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 04:05:09Z",
                "temperature": 25.21,
                "humidity": 37.64,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 04:14:47Z",
                "temperature": 25.19,
                "humidity": 37.56,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 04:24:25Z",
                "temperature": 25.17,
                "humidity": 37.41,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 04:34:06Z",
                "temperature": 25.13,
                "humidity": 37.22,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 04:43:46Z",
                "temperature": 25.06,
                "humidity": 36.99,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 04:53:28Z",
                "temperature": 25.03,
                "humidity": 36.78,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 05:22:45Z",
                "temperature": 24.88,
                "humidity": 36.3,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 05:52:02Z",
                "temperature": 24.69,
                "humidity": 36.68,
                "offline": 0
            },
            {
                "sensor_time": "2022-09-05 06:21:19Z",
                "temperature": 24.53,
                "humidity": 36.59,
                "offline": 0
            }
        ]
    }
}

INVALID_KEY_RESPONSE = {
    "type": "error",
    "message": "Invalid X-API-KEY",
    "data": {
        "key": "invalid-api-key"
    }
}