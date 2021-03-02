# ha-ruuvitags
Run two docker containers: [Home Assistant Core](https://www.home-assistant.io/) and a
HTTP server for [RuuviTag](https://ruuvi.com/) weather station data.

### Description

Sets up RuuviTag temperature and humidity data via RESTful API for Home Assistant Core's
sensor platform. Instructions for Home Assistant configuration are 
[here](https://www.home-assistant.io/integrations/rest/).

Based on [ruuvitag-sensor](https://github.com/ttu/ruuvitag-sensor) code and RuuviTags with
the latest weather station firmware. Uses docker engine and docker compose on host. Tested 
only on Ubuntu 20.04.

- use Ruuvi Station app in phone to set up tags and collects MAC addresses
- edit tags in `ruuvi_server.py` and change port if needed (default=5150)
- `docker-compose up -d`
- verify data is available: `http://localhost:5150/ruuvitags` or `http://localhost:5150/ruuvitag/<mac>`
- visit `http://<host>:8123` to complete Home Assistant onboarding
- edit `~/.homeassistant/configuration.yaml` to add sensors for RuuviTags

<details>
<summary>example config</summary>
<p>

```yaml
sensor:
  - platform: rest
    name: ruuvitags
    resource: http://localhost:5150/ruuvitags
    json_attributes:
      - E6:E7:17:AA:BB:CC
      - D9:64:A3:DD:EE:FF
    value_template: OK
  - platform: template
    sensors:
      living_room_temperature:
        value_template: '{{ states.sensor.ruuvitags.attributes["E6:E7:17:AA:BB:CC"]["temperature"] }}'
        device_class: temperature
        unit_of_measurement: "C"
      living_room_humidity:
        value_template: '{{ states.sensor.ruuvitags.attributes["E6:E7:17:AA:BB:CC"]["humidity"] }}'
        device_class: humidity
        unit_of_measurement: "%"
      bedroom_temperature:
        value_template: '{{ states.sensor.ruuvitags.attributes["D9:64:A3:DD:EE:FF"]["temperature"] }}'
        device_class: temperature
        unit_of_measurement: "C"
      bedroom_humidity:
        value_template: '{{ states.sensor.ruuvitags.attributes["D9:64:A3:DD:EE:FF"]["humidity"] }}'
        device_class: humidity
        unit_of_measurement: "%"
```

</p>
</details>

### Improvements
- TODO: A way to run ruuviserver docker using host BLE driver *without* having to use network mode "host"
- TODO: Find more devices to add in Home Assistant
