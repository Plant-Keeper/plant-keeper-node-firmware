"""
KeyStudio circuit board helpers collection

Author: Shanmugathas Vigneswaran
email: vigneswaran.shanmugathas@outlook.fr
"""

from utils import fit


class KS0429TdsMeterV1:
    """
    TDS meter V1
    https://wiki.keyestudio.com/KS0429_keyestudio_TDS_Meter_V1.0
    """
    @staticmethod
    def raw_adc_to_ppm(raw_adc, temperature=25):
        """
        ADC to PPM conversion
        Based on Arduino/C++ code, from doc : https://wiki.keyestudio.com/KS0429_keyestudio_TDS_Meter_V1.0
        :param temperature:
        :param raw_adc:
        :return:
        """
        # convert ADC to voltage
        adc_to_voltage = fit(
            [0, 4095],
            [0, 3.6]
        )
        voltage = adc_to_voltage(raw_adc)
        # temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.02*(fTP-25.0));
        compensation_voltage = voltage / (1.0 + 0.02 * (temperature - 25.0))
        # tds value in PPM
        tds_value = (
                            133.42 * compensation_voltage * compensation_voltage * compensation_voltage
                            -
                            255.86 * compensation_voltage * compensation_voltage + 857.39 * compensation_voltage
                    ) * 0.5
        return int(tds_value)
