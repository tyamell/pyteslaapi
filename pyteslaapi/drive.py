
class Drive:
    def __init__(self, vehicle):
        self.vehicle = vehicle

    @property
    def attributes(self):
        return self.vehicle._drive_data

    @property
    def shift_state(self):
        shift = self.vehicle._drive_data.get('shift_state')
        if not shift:
            return 'P'
        return shift

    @property
    def speed(self):
        return self.vehicle._drive_data.get('speed')

    @property
    def latitude(self):
        return self.vehicle._drive_data.get('latitude')

    @property
    def longitude(self):
        return self.vehicle._drive_data.get('longitude')

    @property
    def heading(self):
        _heading = self.vehicle._drive_data.get('heading')
        if _heading:
            directions = [
            "North", "North East", "East", "South East",
            "South", "South West", "West", "North West", "North"
            ]
            return directions[int((_heading%360)/45)]
        return 'Unknown'

    @property
    def gps_as_of(self):
        return self.vehicle._drive_data.get('gps_as_of')