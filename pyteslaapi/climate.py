import logging

_LOGGER = logging.getLogger(__name__)

class Climate:
    def __init__(self, vehicle):
        self.vehicle = vehicle

    def start_climate(self):
        return self.vehicle.send_command(
            'auto_conditioning_start'
        )

    def stop_climate(self):
        return self.vehicle.send_command(
            'auto_conditioning_stop'
        )

    def set_temperature(self, driver_temperature, passenger_temperature = None):
        return self.vehicle.send_command(
            'set_temps',
            {'driver_temp': driver_temperature,
             'passenger_temp': passenger_temperature or driver_temperature}
        )

    @property
    def attributes(self):
        return self.vehicle._climate_data

    @property
    def is_climate_on(self):
        return self.vehicle._climate_data.get('is_climate_on')

    @property
    def is_preconditioning(self):
        return self.vehicle._climate_data.get('is_preconditioning')

    @property
    def battery_heater_no_power(self):
        return self.vehicle._climate_data.get('battery_heater_no_power')

    @property
    def battery_heater(self):
        return self.vehicle._climate_data.get('battery_heater')

    @property
    def side_mirror_heaters(self):
        return self.vehicle._climate_data.get('side_mirror_heaters')

    @property
    def left_temp_direction(self):
        return self.vehicle._climate_data.get('left_temp_direction')

    @property
    def right_temp_direction(self):
        return self.vehicle._climate_data.get('right_temp_direction')

    @property
    def max_avail_temp(self):
        return self.vehicle._climate_data.get('max_avail_temp')

    @property
    def min_avail_temp(self):
        return self.vehicle._climate_data.get('min_avail_temp')

    @property
    def inside_temp(self):
        return self.vehicle._climate_data.get('inside_temp')

    @property
    def outside_temp(self):
        return self.vehicle._climate_data.get('outside_temp')

    @property
    def driver_temp_setting(self):
        return self.vehicle._climate_data.get('driver_temp_setting')

    @property
    def passenger_temp_setting(self):
        return self.vehicle._climate_data.get('passenger_temp_setting')

    @property
    def is_auto_conditioning_on(self):
        return self.vehicle._climate_data.get('is_auto_conditioning_on')

    @property
    def is_front_defroster_on(self):
        return self.vehicle._climate_data.get('is_front_defroster_on')

    @property
    def is_rear_defroster_on(self):
        return self.vehicle._climate_data.get('is_rear_defroster_on')

    @property
    def fan_status(self):
        return self.vehicle._climate_data.get('fan_status')

    @property
    def seat_heater_left(self):
        return self.vehicle._climate_data.get('seat_heater_left')

    @property
    def seat_heater_right(self):
        return self.vehicle._climate_data.get('seat_heater_right')

    @property
    def seat_heater_rear_left(self):
        return self.vehicle._climate_data.get('seat_heater_rear_left')

    @property
    def seat_heater_rear_right(self):
        return self.vehicle._climate_data.get('seat_heater_rear_right')

    @property
    def seat_heater_rear_center(self):
        return self.vehicle._climate_data.get('seat_heater_rear_center')

    @property
    def seat_heater_rear_right_back(self):
        return self.vehicle._climate_data.get('seat_heater_rear_right_back')

    @property
    def seat_heater_rear_left_back(self):
        return self.vehicle._climate_data.get('seat_heater_rear_left_back')

    @property
    def smart_preconditioning(self):
        return self.vehicle._climate_data.get('smart_preconditioning')
