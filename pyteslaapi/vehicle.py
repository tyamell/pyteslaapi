from pyteslaapi.exceptions import TeslaException
from pyteslaapi.climate import Climate
from pyteslaapi.drive import Drive
from pyteslaapi.charge import Charge
from pyteslaapi.gui_settings import GuiSettings
import logging
import time
from multiprocessing import RLock

_LOGGER = logging.getLogger(__name__)

class Vehicle:
    UPDATES = ['vehicle_state', 'drive_state', 'charge_state', 'climate_state', 'gui_settings']
    STATE_VENT = 'vent'
    STATE_CLOSE = 'close'
    def __init__(self, client, data, wake=False,
                 update_interval=900,
                 drive_interval=45,
                 wake_interval=21800):
        self.__id = data['id']
        self._vehicle_id = data['vehicle_id']
        self.__vin = data['vin']
        self.__state = data['state']
        self.__name = data['display_name']
        self.__client = client
        self.__vehicle_data = {}
        self._drive_data = {}
        self._charge_data = {}
        self._climate_data = {}
        self._gui_settings_data = {}
        self.__climate = Climate(self)
        self.__drive = Drive(self)
        self.__charge = Charge(self)
        self.__gui_settings = GuiSettings(self)
        self.__wake = wake
        self.__wake_interval = wake_interval
        self.__update_interval = update_interval
        self.__drive_interval = drive_interval
        self.__lock = RLock()
        self.__last_update_time = None
        self.__first_update = True


    def __update_state(self, data):
        self.__state = data['state']
        self.__name = data['display_name']

    def update_vehicle(self):
        with self.__lock:
            vehicles = self.__client.get('vehicles')
            for v in vehicles:
                if v['id'] == self.__id:
                    self.__update_state(v)

    def __check_driving_interval(self):
        return (time.time() - self.__last_update_time > self.__drive_interval)

    def __check_update_interval(self):
        return (time.time() - self.__last_update_time > self.__update_interval)

    def __check_wake_interval(self):
        if self.__wake is False and self.__first_update is False:
            return (time.time() - self.__last_update_time > self.__wake_interval)
        return (time.time() - self.__last_update_time > self.__update_interval)

    def update(self):
        with self.__lock:
            should_update = False
            self.update_vehicle()
            if self.__first_update:
                should_update = True
                self.__first_update = False
                _LOGGER.debug("First update so getting data no matter what")
            elif (self.state == 'online' and
                self.drive.shift_state != "P"):
                should_update = self.__check_driving_interval()
                if should_update:
                    _LOGGER.debug("Tesla is driving getting updates at {}".format(self.__drive_interval))
            elif self.state == 'online':
                should_update = self.__check_update_interval()
                if should_update:
                    _LOGGER.debug("Tesla online getting updates at interval {}".format(self.__update_interval))
            else:
                should_update = self.__check_wake_interval()
                if should_update:
                    _LOGGER.debug("Tesla not awake but waking up. Wake interval is  {}".format(self.__wake_interval))

            if should_update:
                _LOGGER.debug("Getting updated data on tesla")
                self._update()
                self.__last_update_time = time.time()
                return True
            return False

    def _update(self):
        if self.state != "online":
            self.wake_up()
        for update in self.UPDATES:
            try:
                data = self.__client.get('vehicles/{}/data_request/{}'.format(self.id, update))
                if data:
                    if update == 'vehicle_state':
                        _LOGGER.debug("Got vehicle state update")
                        self.__vehicle_data = data
                    elif update == 'drive_state':
                        _LOGGER.debug("Got drive state update")
                        self._drive_data = data
                    elif update == 'charge_state':
                        _LOGGER.debug("Got charge state update")
                        self._charge_data = data
                    elif update == 'climate_state':
                        _LOGGER.debug("Got climate state update")
                        self._climate_data = data
                    elif update == 'gui_settings':
                        _LOGGER.debug("Got gui settings update")
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
        return self.__vehicle_data.get('api_version')

    @property
    def autopark_state_v2(self):
        return self.__vehicle_data.get('autopark_state_v2')

    @property
    def autopark_style(self):
        return self.__vehicle_data.get('autopark_style')

    @property
    def calendar_supported(self):
        return self.__vehicle_data.get('calendar_supported')

    @property
    def car_version(self):
        return self.__vehicle_data.get('car_version')

    @property
    def center_display_state(self):
        return self.__vehicle_data.get('center_display_state')

    @property
    def df(self):
        return self.__vehicle_data.get('df')

    @property
    def dr(self):
        return self.__vehicle_data.get('dr')

    @property
    def ft(self):
        return self.__vehicle_data.get('ft')

    @property
    def homelink_nearby(self):
        return self.__vehicle_data.get('homelink_nearby')

    @property
    def is_user_present(self):
        return self.__vehicle_data.get('is_user_present')

    @property
    def last_autopark_eror(self):
        return self.__vehicle_data.get('last_autopark_eror')

    @property
    def locked(self):
        return self.__vehicle_data.get('locked')

    @property
    def media_state(self):
        return self.__vehicle_data.get('media_state')

    @property
    def notifications_supported(self):
        return self.__vehicle_data.get('notifications_supported')

    @property
    def odometer(self):
        return self.__vehicle_data.get('odometer')

    @property
    def parsed_calendar_supported(self):
        return self.__vehicle_data.get('parsed_calendar_supported')

    @property
    def pf(self):
        return self.__vehicle_data.get('pf')

    @property
    def pr(self):
        return self.__vehicle_data.get('pr')

    @property
    def remote_start(self):
        return self.__vehicle_data.get('remote_start')

    @property
    def remote_start_supported(self):
        return self.__vehicle_data.get('remote_start_supported')

    @property
    def rt(self):
        return self.__vehicle_data.get('rt')

    @property
    def software_update(self):
        return self.__vehicle_data.get('software_update')

    @property
    def speed_limit_mode(self):
        return self.__vehicle_data.get('speed_limit_mode')

    @property
    def sun_roof_percent_open(self):
        return self.__vehicle_data.get('sun_roof_percent_open')

    @property
    def sun_roof_state(self):
        return self.__vehicle_data.get('sun_roof_state')

    @property
    def timestamp(self):
        return self.__vehicle_data.get('timestamp')

    @property
    def valet_mode(self):
        return self.__vehicle_data.get('valet_mode')

    @property
    def vehicle_name(self):
        return self.__vehicle_data.get('vehicle_name')


