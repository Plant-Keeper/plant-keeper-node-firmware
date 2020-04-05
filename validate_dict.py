from .node_type import NODE_TYPES


class BaseValidatePOST:
    required_keys = None

    def validate(self, _dict):
        for r in self.required_keys:
            if r not in _dict:
                raise ValueError(
                    'Mandatory key=' + r + ' not provided'
                )
        else:
            return True


class ValidateEnclosurePOST(BaseValidatePOST):
    required_keys = [
        'temperature',
        'humidity',
        'uv_index',
        'co2_ppm',
        'cov_ppm'
    ]


class ValidatedCoolerPOST(BaseValidatePOST):
    required_keys = [
        ''
    ]


class ValidateHeaterPOST(BaseValidatePOST):
    required_keys = [
        ''
    ]


class ValidateWaterPumpPOST(BaseValidatePOST):
    required_keys = [
        'level'
    ]


class ValidateHumidifierPOST(BaseValidatePOST):
    required_keys = [
        ''
    ]


class ValidateSprinklerPOST(BaseValidatePOST):
    required_keys = [
        'tag',
        'soil_humidity'
    ]
