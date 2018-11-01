class VehicleDevice:
    def __init__(self, data, controller):
        self._id = data['id']
        self.type = None
        self._vehicle_id = data['vehicle_id']
        self._vin = data['vin']
        self._state = data['state']
        self.__name = data['display_name']
        self._controller = controller
        self.should_poll = True
        self._attributes = {}
        self._attributes['vin'] = self._vin
        self._attributes['display_name'] = self.__name
        self._attributes['id'] = self._id
        self._attributes['state'] = self._state

    def _name(self):
        if self.__name:
            return '{} {}'.format(self.__name, self.type)
        return 'Tesla Model {} {}'.format(
            str(self._vin[3]).upper(), self.type)

    def _uniq_name(self):
        if self.__name:
            return 'Tesla Model {} {} {}'.format(
            str(self._vin[3]).upper(), self.__name, self.type)
        return 'Tesla Model {} {} {}'.format(
            str(self._vin[3]).upper(), self._vin, self.type)

    @staticmethod
    def is_armable():
        return False

    @staticmethod
    def is_armed():
        return False

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        return self._attributes
