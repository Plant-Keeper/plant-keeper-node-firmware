try:
    import urequests as requests
except ImportError:
    import requests
from node_type import (
    NODE_TYPES,
    ENCLOSURE,
    COOLER,
    HEATER,
    HUMIDIFIER,
    SPRINKLER,
    WATER_PUMP
)
from validate_dict import (
    ValidateEnclosurePOST,
    ValidatedCoolerPOST,
    ValidateHeaterPOST,
    ValidateHumidifierPOST,
    ValidateSprinklerPOST,
    ValidateWaterPumpPOST,
)


class Client:

    def __init__(
            self,
            host='10.3.141.1',
            port=8001,
            user='',
            password=''
    ):

        assert isinstance(host, str)
        assert isinstance(port, int)
        assert isinstance(user, str)
        assert isinstance(password, str)

        self.node_type = False
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.header = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.power = False
        self.validator = self.__get_post_validator()

    @property
    def api(self):
        return (
                'http://'
                + self.host
                + ':'
                + str(self.port)
                + '/'
                + str(self.node_type)
                + '/'
        )

    def __get_post_validator(self):
        if self.node_type == ENCLOSURE:
            return ValidateEnclosurePOST()
        elif self.node_type == COOLER:
            return ValidatedCoolerPOST()
        elif self.node_type == HEATER:
            return ValidateHeaterPOST()
        elif self.node_type == HUMIDIFIER:
            return ValidateHumidifierPOST()
        elif self.node_type == SPRINKLER:
            return ValidateSprinklerPOST()
        elif self.node_type == WATER_PUMP:
            return ValidateWaterPumpPOST()

    def set_node_type(self, node_type):
        assert isinstance(node_type, str)
        if node_type not in NODE_TYPES:
            raise ValueError(
                'Node type=' + node_type
                + ' not in ' + str(NODE_TYPES)
            )
        self.node_type = node_type

    def post(self, _dict):
        assert isinstance(_dict, dict)
        try:
            self.validator.validate(_dict)
        except ValueError:
            print('Post dict not valid')
        else:
            r = requests.post(
                self.api,
                json=_dict,
                headers=self.header
            )

            if r.status_code in [200, 201]:
                self.power = r.json()['power']
