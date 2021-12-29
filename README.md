# Nestalarm
### A script to monitor an EnvisaLink alarm module running Honeywell firmware, and set a Nest device to Home/Away depending on whether the alarm is Disarmed/Away.

## Setup
* Install the `requests` library according to `requirements.txt`
* Setup a `config.py` file
* Generate the Nest API protobuf python bindings
### Example Config
```python
ALARM_IP = "168.178.46.43"
ALARM_PORT = 4025
ALARM_PASSWORD = "user"

NEST_ENDPOINT = "https://grpc-web.production.nest.com/nestlabs.gateway.v1.ResourceApi/SendCommand"
NEST_USER_ID = "2760334"
NEST_STRUCTURE_ID = "015FB2C46740F660"
NEST_ACCESS_TOKEN = "g.0.eyJraWQiOiIyMzhiNTU..."
NEST_USER_AGENT = "Mozilla/5.0..."
```
Your Nest userid and access_token can be obtained by logging into the Nest webapp and then visting https://home.nest.com/session. You will have to manually change the config when the token becomes invalidated.

Your Nest structure id can be obtained by running the program with an invalid structure id.

### Generating Nest Protobuf Python Bindings
Copy the nest-protobuf folder from this git repo https://github.com/derek-miller/nest-protobuf, and then run `generate-nestapi.sh`.

## References
* https://github.com/emilburzo/nest-rest
* https://github.com/derek-miller/nest-protobuf
* http://forum.eyez-on.com/FORUM/viewtopic.php?t=301
