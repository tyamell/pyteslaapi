
class Charge:
    def __init__(self, vehicle):
        self.vehicle = vehicle

    def start_charging(self):
        return self.vehicle.send_command(
            'charge_start'
        )

    def open_charge_port(self):
        return self.vehicle.send_command(
            'charge_port_door_open'
        )

    def stop_charging(self):
         return self.vehicle.send_command(
            'charge_stop'
        )

    def set_charge_standard(self):
         return self.vehicle.send_command(
            'charge_standard'
        )

    def set_charge_max_range(self):
         return self.vehicle.send_command(
            'charge_max_range'
        )

    def set_charge_limit(self, percentage):
        percentage = round(percentage)

        if percentage < 50 or percentage > 100:
            raise ValueError('Percentage should be between 50 and 100')

        return self.vehicle.send_command(
            'set_charge_limit',
            {'limit_value': percentage}
        )

    @property
    def attributes(self):
        return self.vehicle._charge_data

    @property
    def is_charging(self):
        return self.charging_state == 'Charging'

    @property
    def charging_state(self):
        return self.vehicle._charge_data.get('charging_state')

    @property
    def charge_limit_soc(self):
        return self.vehicle._charge_data.get('charge_limit_soc')

    @property
    def charge_limit_soc_std(self):
        return self.vehicle._charge_data.get('charge_limit_soc_std')

    @property
    def charge_limit_soc_min(self):
        return self.vehicle._charge_data.get('charge_limit_soc_min')

    @property
    def charge_limit_soc_max(self):
        return self.vehicle._charge_data.get('charge_limit_soc_max')

    @property
    def charge_to_max_range(self):
        return self.vehicle._charge_data.get('charge_to_max_range')

    @property
    def battery_heater_on(self):
        return self.vehicle._charge_data.get('battery_heater_on')

    @property
    def not_enough_power_to_heat(self):
        return self.vehicle._charge_data.get('not_enough_power_to_heat')

    @property
    def max_range_charge_counter(self):
        return self.vehicle._charge_data.get('max_range_charge_counter')

    @property
    def fast_charger_present(self):
        return self.vehicle._charge_data.get('fast_charger_present')

    @property
    def fast_charger_type(self):
        return self.vehicle._charge_data.get('fast_charger_type')

    @property
    def battery_range(self):
        return self.vehicle._charge_data.get('battery_range')

    @property
    def est_battery_range(self):
        return self.vehicle._charge_data.get('est_battery_range')

    @property
    def ideal_battery_range(self):
        return self.vehicle._charge_data.get('ideal_battery_range')

    @property
    def battery_level(self):
        return self.vehicle._charge_data.get('battery_level')

    @property
    def usable_battery_level(self):
        return self.vehicle._charge_data.get('usable_battery_level')

    @property
    def battery_current(self):
        return self.vehicle._charge_data.get('battery_current')

    @property
    def charge_energy_added(self):
        return self.vehicle._charge_data.get('charge_energy_added')

    @property
    def charge_miles_added_rated(self):
        return self.vehicle._charge_data.get('charge_miles_added_rated')

    @property
    def charge_miles_added_ideal(self):
        return self.vehicle._charge_data.get('charge_miles_added_ideal')

    @property
    def charger_voltage(self):
        return self.vehicle._charge_data.get('charger_voltage')

    @property
    def charger_pilot_current(self):
        return self.vehicle._charge_data.get('charger_pilot_current')

    @property
    def charger_actual_current(self):
        return self.vehicle._charge_data.get('charger_actual_current')

    @property
    def charger_power(self):
        return self.vehicle._charge_data.get('charger_power')

    @property
    def time_to_full_charge(self):
        return self.vehicle._charge_data.get('time_to_full_charge')

    @property
    def trip_charging(self):
        return self.vehicle._charge_data.get('trip_charging')

    @property
    def charge_rate(self):
        return self.vehicle._charge_data.get('charge_rate')

    @property
    def charge_port_door_open(self):
        return self.vehicle._charge_data.get('charge_port_door_open')

    @property
    def motorized_charge_port(self):
        return self.vehicle._charge_data.get('motorized_charge_port')

    @property
    def scheduled_charging_start_time(self):
        return self.vehicle._charge_data.get('scheduled_charging_start_time')

    @property
    def scheduled_charging_pending(self):
        return self.vehicle._charge_data.get('scheduled_charging_pending')

    @property
    def user_charge_enable_request(self):
        return self.vehicle._charge_data.get('user_charge_enable_request')

    @property
    def eu_vehicle(self):
        return self.vehicle._charge_data.get('eu_vehicle')

    @property
    def charger_phases(self):
        return self.vehicle._charge_data.get('charger_phases')

    @property
    def charge_port_latch(self):
        return self.vehicle._charge_data.get('charge_port_latch')

    @property
    def charge_current_request(self):
        return self.vehicle._charge_data.get('charge_current_request')

    @property
    def charge_current_request_max(self):
        return self.vehicle._charge_data.get('charge_current_request_max')

    @property
    def managed_charging_active(self):
        return self.vehicle._charge_data.get('managed_charging_active')

    @property
    def managed_charging_user_canceled(self):
        return self.vehicle._charge_data.get('managed_charging_user_canceled')

    @property
    def managed_charging_start_time(self):
        return self.vehicle._charge_data.get('managed_charging_start_time')
