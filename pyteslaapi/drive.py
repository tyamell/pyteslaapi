
class Drive:
    def __init__(self, vehicle):
        self.vehicle = vehicle

    @property
    def attributes(self):
        return self.vehicle._drive_data

    @property
    def shift_state(self):
        if not self.vehicle._drive_data['shift_state']:
            return 'P'
        return self.vehicle._drive_data['shift_state']

    @property
    def speed(self):
        return self.vehicle._drive_data['speed']

    @property
    def latitude(self):
        return self.vehicle._drive_data['latitude']

    @property
    def longitude(self):
        return self.vehicle._drive_data['longitude']

    @property
    def heading(self):
        return self.vehicle._drive_data['heading']

    @property
    def gps_as_of(self):
        return self.vehicle._drive_data['gps_as_of']