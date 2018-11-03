from exceptions import TeslaException
from climate import Climate
from drive import Drive
from charge import Charge
from gui_settings import GuiSettings
import logging
import time

_LOGGER = logging.getLogger(__name__)

class Vehicle:
    UPDATES = ['vehicle_state', 'drive_state', 'charge_state', 'climate_state', 'gui_settings']
    STATE_VENT = 'vent'
    STATE_CLOSE = 'close'
    def __init__(self, client, data):
        self.__id = data['id']
        self._vehicle_id = data['vehicle_id']
        self.__vin = data['vin']
        self.__state = data['state']
        self.__name = data['display_name']
        self.__client = client
        self.__vehicle_data = None
        self._drive_data = None
        self._charge_data = None
        self._climate_data = None
        self._gui_settings_data = None
        self.__climate = Climate(self)
        self.__drive = Drive(self)
        self.__charge = Charge(self)
        self.__gui_settings = GuiSettings(self)

    def __update_state(self, data):
        self.__state = data['state']
        self.__name = data['display_name']

    def update_vehicle(self):
        vehicles = self.__client.get('vehicles')
        for v in vehicles:
            if v['id'] == self.__id:
                self.__update_state(v)

    def update(self):
        for update in self.UPDATES:
            try:
                data = self.__client.get('vehicles/{}/data_request/{}'.format(self.id, update))
                if update == 'vehicle_state':
                    _LOGGER.debug(data)
                    self.__vehicle_data = data
                elif update == 'drive_state':
                    self._drive_data = data
                elif update == 'charge_state':
                    self._charge_data = data
                elif update == 'climate_state':
                    self._climate_data = data
                elif update == 'gui_settings':
                    self._gui_settings_data = data
                else:
                    _LOGGER.debug("Unknown update of {} found".format(update))
            except TeslaException as ex:
                _LOGGER.error('Updating Tesla {} resulted in an error {} - {}'.format(update, ex.code, ex.message))

    def __set_sunroof_state(self, state):
        return self.__client.command(
            self.id,
            'sun_roof_control',
            {'state': state}
        )
    def send_command(self, command_name, data={}):
        return self.__client.command(
            self.id,
            command_name,
            data
        )
    def vent_sunroof(self):
        return self.__set_sunroof_state(self.STATE_VENT)

    def close_sunroof(self):
        return self.__set_sunroof_state(self.STATE_CLOSE)

    def open_sunroof(self, percentage):
        return self.send_command(
            'sun_roof_control',
            {'percent': percentage}
        )

    def flash_lights(self):
        return self.send_command(
            'flash_lights'
        )

    def honk_horn(self):
        return self.send_command(
            'honk_horn'
        )

    def unlock_doors(self):
        return self.send_command(
            'door_unlock'
        )

    def lock_doors(self):
        return self.send_command(
            'door_lock'
        )

    def valet_mode_off(self, pin=None):
        return self.send_command(
            'set_valet_mode',
            {'on': False, 'pin': pin}
        )

    def valet_mode_on(self, pin=None):
        return self.send_command(
            'set_valet_mode',
            {'on': True, 'pin': pin}
        )

    def reset_valet_pin(self, pin=None):
        return self.send_command(
            'reset_valet_pin'
        )

    def open_trunk(self, pin=None):
        return self.send_command(
            'trunk_open',
            {'which_trunk': 'rear'}
        )

    def open_frunk(self, pin=None):
        return self.send_command(
            'trunk_open',
            {'which_trunk': 'front'}
        )

    def remote_state(self, pin=None):
        return self.send_command(
            'remote_start_drive',
            {'password': self.__client._password}
        )

    @property
    def climate(self):
        return self.__climate

    @property
    def drive(self):
        return self.__drive

    @property
    def charge(self):
        return self.__charge

    @property
    def gui_settings(self):
        return self.__gui_settings

    def wake_up(self):
        data = self.__client.post('vehicles/{}/wake_up'.format(self.id))
        retry = 0
        while data['state'] == 'offline' and retry <= 5:
            _LOGGER.debug("Vehicle still not awake trying again")
            retry += 1
            time.sleep(retry * 2.5)
            data = self.__client.post('vehicles/{}/wake_up'.format(self.id))
        if retry == 6:
            return False
        return data

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        if self.__name:
            return self.__name
        return 'Tesla Model {} {}'.format(
            str(self.__vin[3]).upper(), str(self.__vin))

    @property
    def vin(self):
        return self.__vin

    @property
    def state(self):
        return self.__state

    @property
    def api_version(self):
        return self.__vehicle_data['api_version']

    @property
    def autopark_state_v2(self):
        return self.__vehicle_data['autopark_state_v2']

    @property
    def autopark_style(self):
        return self.__vehicle_data['autopark_style']

    @property
    def calendar_supported(self):
        return self.__vehicle_data['calendar_supported']

    @property
    def car_version(self):
        return self.__vehicle_data['car_version']

    @property
    def center_display_state(self):
        return self.__vehicle_data['center_display_state']

    @property
    def df(self):
        return self.__vehicle_data['df']

    @property
    def dr(self):
        return self.__vehicle_data['dr']

    @property
    def ft(self):
        return self.__vehicle_data['ft']

    @property
    def homelink_nearby(self):
        return self.__vehicle_data['homelink_nearby']

    @property
    def is_user_present(self):
        return self.__vehicle_data['is_user_present']

    @property
    def last_autopark_eror(self):
        return self.__vehicle_data['last_autopark_eror']

    @property
    def locked(self):
        return self.__vehicle_data['locked']

    @property
    def media_state(self):
        return self.__vehicle_data['media_state']

    @property
    def notifications_supported(self):
        return self.__vehicle_data['notifications_supported']

    @property
    def odometer(self):
        return self.__vehicle_data['odometer']

    @property
    def parsed_calendar_supported(self):
        return self.__vehicle_data['parsed_calendar_supported']

    @property
    def pf(self):
        return self.__vehicle_data['pf']

    @property
    def pr(self):
        return self.__vehicle_data['pr']

    @property
    def remote_start(self):
        return self.__vehicle_data['remote_start']

    @property
    def remote_start_supported(self):
        return self.__vehicle_data['remote_start_supported']

    @property
    def rt(self):
        return self.__vehicle_data['rt']

    @property
    def software_update(self):
        return self.__vehicle_data['software_update']

    @property
    def speed_limit_mode(self):
        return self.__vehicle_data['speed_limit_mode']

    @property
    def sun_roof_percent_open(self):
        return self.__vehicle_data['sun_roof_percent_open']

    @property
    def sun_roof_state(self):
        return self.__vehicle_data['sun_roof_state']

    @property
    def timestamp(self):
        return self.__vehicle_data['timestamp']

    @property
    def valet_mode(self):
        return self.__vehicle_data['valet_mode']

    @property
    def vehicle_name(self):
        return self.__vehicle_data['vehicle_name']


