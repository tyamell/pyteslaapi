from pytesla.vehicle import VehicleDevice
from datetime import datetime


class DriveSensor(VehicleDevice):
    def __init__(self, data, controller):
        super().__init__(data, controller)
        self.__state = {}
        self.__state['state'] = None
        self.type = 'driving sensor'
        self.hass_type = 'sensor'

        self.name = self._name()
        self.measurement = ''
        self.uniq_name = self._uniq_name()
        self.bin_type = 0x11
        self.update()

    def update(self):
        if self._controller.update(self._id) is False:
            return False
        data = self._controller.get_drive_params(self._id)
        return self.__update_data(data)

    def __update_data(self, data):
        if not data:
            return False
        if not data['shift_state'] or data['shift_state'] == 'P':
            self.__set_state(True)
        else:
             self.__set_state(False)
        self._attributes['speed'] = data['speed']
        self._attributes['latitude'] = data['latitude']
        self._attributes['longitude'] = data['longitude']
        directions = ["North", "North East", "East", "South East","South",
        "South West", "West", "North West", "North"]
        self._attributes['heading'] = directions[int((data['heading']%360)/45)]
        self._attributes['gps_as_of'] = datetime.utcfromtimestamp(int(data['gps_as_of']))
        self.__state['attributes'] = self._attributes
        self.__state['last_updated'] = datetime.now()
        return True

    def get_value(self):
        return self.__state

    def __set_state(self, state):
        if state != self.__state['state']:
            self._attributes['last_changed'] = datetime.now()
        self.__state['state'] = state

    @staticmethod
    def has_battery():
        return False
