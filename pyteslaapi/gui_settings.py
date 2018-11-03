
class GuiSettings:
    def __init__(self, vehicle):
        self.vehicle = vehicle

    @property
    def attributes(self):
        return self.vehicle._gui_settings_data

    @property
    def distance_units(self):
        return self.vehicle._gui_settings_data['gui_distance_units']

    @property
    def temperature_units(self):
        return self.vehicle._gui_settings_data['gui_temperature_units']

    @property
    def charge_rate_units(self):
        return self.vehicle._gui_settings_data['gui_charge_rate_units']

    @property
    def gui_24_hour_time(self):
        return self.vehicle._gui_settings_data['gui_24_hour_time']

    @property
    def range_display(self):
        return self.vehicle._gui_settings_data['gui_range_display']
