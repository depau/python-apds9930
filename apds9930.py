#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ("APDS9930")

import smbus
from apds9930_regs import *

class APDS9930_I2C_Base(object):
    def __init__(self, bus, address):
        self._bus = smbus.SMBus()
        self._bus.open(bus)
        self.address = address

    def write_byte(self, data):
        self._bus.write_byte(self.address, data)

    def write_byte_data(self, reg, data, mode=AUTO_INCREMENT):
        self._bus.write_byte_data(self.address, reg | mode, data)

    def write_block_data(self, reg, data, mode=AUTO_INCREMENT):
        self._bus.write_i2c_block_data(self.address, reg | mode, data)

    def read_byte(self):
        return self._bus.read_byte(self.address)

    def read_byte_data(self, reg, mode=AUTO_INCREMENT):
        return self._bus.read_byte_data(self.address, reg | mode)

    def read_block_data(self, reg, len, mode=AUTO_INCREMENT):
        return self._bus.read_i2c_block_data(self.address, reg | mode, len)

    def close(self):
        self._bus.close()

class APDS9930(APDS9930_I2C_Base):
    def __init__(self, bus, address=APDS9930_I2C_ADDR):
        super(APDS9930, self).__init__(bus, address)

        self.address = HexInt(self.address) # For aesthetic purposes only

        # Check device ID against preset values
        if self.id not in APDS9930_IDs:
            raise SensorError("Device ID not recognized: {0}".format(hex(self.id)))
        
        # Turn off all features (set ENABLE to 0x00)
        self.set_mode(ALL, OFF)

        # Set default values for ambient light and proximity registers
        self.write_byte_data(APDS9930_ATIME, DEFAULT_ATIME)
        self.write_byte_data(APDS9930_WTIME, DEFAULT_WTIME)
        self.write_byte_data(APDS9930_PPULSE, DEFAULT_PPULSE)
        self.write_byte_data(APDS9930_POFFSET, DEFAULT_POFFSET)
        self.write_byte_data(APDS9930_CONFIG, DEFAULT_CONFIG)

        self.led_drive = DEFAULT_PDRIVE
        self.proximity_gain = DEFAULT_PGAIN
        self.ambient_light_gain = DEFAULT_AGAIN
        self.proximity_diode = DEFAULT_PDIODE
        self.proximity_int_low_threshold = DEFAULT_PILT
        self.proximity_int_high_threshold = DEFAULT_PIHT
        self.light_int_low_threshold = DEFAULT_AILT
        self.light_int_high_threshold = DEFAULT_AIHT

        self.write_byte_data(APDS9930_PERS, DEFAULT_PERS)

    @property
    def id(self):
        """The ID of the device, stored in the APDS9930_ID register.
        """
        return HexInt(self.read_byte_data(APDS9930_ID))
    
    @property
    def mode(self):
        """The value of the APDS9930_ENABLE register, which stores
        the enabled features of the sensor. You should not set this
        property directly unless you know what you're doing. Use set_mode
        and/or the specific feature methods instead.
        """
        return BinInt(self.read_byte_data(APDS9930_ENABLE))
    @mode.setter
    def mode(self, value):
        self.write_byte_data(APDS9930_ENABLE, value)

    def get_mode(self, mode):
        """Gets the state of a specific feature in the APDS9930_ENABLE
        register. Good values for mode are:

            POWER                 = 0
            AMBIENT_LIGHT         = 1
            PROXIMITY             = 2
            WAIT                  = 3
            AMBIENT_LIGHT_INT     = 4
            PROXIMITY_INT         = 5
            SLEEP_AFTER_INT       = 6

        The specified feature is either enabled or disabled depending
        on whether the method returns True or False
        """
        return bool((self.mode & (1 << mode)) >> mode)

    def set_mode(self, mode, enable):
        """Like get_mode, but changes the mode instead. The enable argument
        determines whether the feature specified by mode will be enabled or
        disabled. The method accepts one additional argument as mode,

        ALL                   = 7

        which enables or disables all features at once.

        The specified feature will either be enabled or disabled depending
        on whether enable is True or False
        """
        reg_val = self.mode

        if mode >= 0 and mode <= 6:
            if enable:
                reg_val |= 1 << mode
            else:
                reg_val &= -(1 << mode)
        elif mode == ALL:
            reg_val = 0x7F if enable else 0x00

        self.mode = reg_val

    @property
    def power(self):
        """Turn on or off the internal oscillator (mode, boolean).
        """
        return self.get_mode(POWER)
    @power.setter
    def power(self, value):
        self.set_mode(POWER, value)

    @property
    def ambient_light_sensor(self):
        """Enable or disable the ambient light sensor (mode, boolean).
        """
        return self.get_mode(AMBIENT_LIGHT)
    @ambient_light_sensor.setter
    def ambient_light_sensor(self, value):
        self.set_mode(AMBIENT_LIGHT, value)
        
    @property
    def proximity_sensor(self):
        """Enable or disable the proximity sensor (mode, boolean).
        """
        return self.get_mode(PROXIMITY)
    @proximity_sensor.setter
    def proximity_sensor(self, value):
        self.set_mode(PROXIMITY, value)
        
    @property
    def wait(self):
        """Enable or disable the wait feature (mode, boolean).
        """
        return self.get_mode(WAIT)
    @wait.setter
    def wait(self, value):
        self.set_mode(WAIT, value)
        
    @property
    def enable_ambient_light_interrupt(self):
        """Enable or disable the ambient light interrupt (mode, boolean).
        """
        return self.get_mode(AMBIENT_LIGHT_INT)
    @enable_ambient_light_interrupt.setter
    def enable_ambient_light_interrupt(self, value):
        self.set_mode(AMBIENT_LIGHT_INT, value)
        
    @property
    def enable_proximity_interrupt(self):
        """Enable or disable the proximity interrupt (mode, boolean).
        """
        return self.get_mode(PROXIMITY_INT)
    @enable_proximity_interrupt.setter
    def enable_proximity_interrupt(self, value):
        self.set_mode(PROXIMITY_INT, value)
        
    @property
    def sleep_after_interrupt(self):
        """Enable or disable the sleep after interrupt feature. If True,
        the device will power down after an interrupt has been generated
        (mode, boolean).
        """
        return self.get_mode(SLEEP_AFTER_INT)
    @sleep_after_interrupt.setter
    def sleep_after_interrupt(self, value):
        self.set_mode(SLEEP_AFTER_INT, value)

    def enable_ambient_light_sensor(self, interrupt=False):
        """Set all the needed values to turn on the ambient light
        sensor and turn it on.
        If interrupt is True, ALS interrupts will also be enabled.
        """

        self.ambient_light_gain = DEFAULT_AGAIN
        self.ambient_light_interrupt = interrupt
        self.power = True
        self.ambient_light_sensor = True

    def enable_proximity_sensor(self, interrupt=False):
        """Set all the needed values to turn on the proximity
        sensor and turn it on.
        If interrupt is True, proximity interrupts will also
        be enabled.
        """

        self.proximity_gain = DEFAULT_PGAIN
        self.led_drive = DEFAULT_PDRIVE
        self.proximity_diode = DEFAULT_PDIODE
        self.proximity_interrupt = interrupt
        self.power = True
        self.proximity_sensor = True


    @property
    def ch0_light(self):
        """Light data from channel 0. Read-only.
        """
        l = self.read_byte_data(APDS9930_Ch0DATAL)
        h = self.read_byte_data(APDS9930_Ch0DATAH)

        return l + (h << 8)

    @property
    def ch1_light(self):
        """Light data from channel 1. Read-only.
        """
        l = self.read_byte_data(APDS9930_Ch1DATAL)
        h = self.read_byte_data(APDS9930_Ch1DATAH)

        return l + (h << 8)

    @property
    def ambient_light(self):
        """Ambient light value in lux (read-only).
        """
        ch0, ch1 = self.ch0_light, self.ch1_light
        return self.ambient_to_lux(ch0, ch1)

    def ambient_to_lux(self, ch0, ch1):
        """Accepts data from both channels and returns a value
        in lux (according to the datasheet).
        """

        ALSIT = 2.73 * (256 - DEFAULT_ATIME)
        iac = max(ch0 - B * ch1, C * ch0 - D * ch1)
        lpc = GA * DF / (ALSIT * self.ambient_light_gain)
        return iac * lpc

    @property
    def proximity(self):
        """Proximity data. Read-only.
        """
        l = self.read_byte_data(APDS9930_PDATAL)
        h = self.read_byte_data(APDS9930_PDATAH)

        return l + (h << 8)

    @property
    def proximity_int_low_threshold(self):
        """Proximity interrupt low threshold.
        """
        l = self.read_byte_data(APDS9930_PILTL)
        h = self.read_byte_data(APDS9930_PILTH)

        return l + (h << 8)
    @proximity_int_low_threshold.setter
    def proximity_int_low_threshold(self, value):
        h = value >> 8
        l = value & 0x00FF

        self.write_byte_data(APDS9930_PILTL, l)
        self.write_byte_data(APDS9930_PILTH, h)

    @property
    def proximity_int_high_threshold(self):
        """Proximity interrupt high threshold.
        """
        l = self.read_byte_data(APDS9930_PIHTL)
        h = self.read_byte_data(APDS9930_PIHTH)

        return l + (h << 8)
    @proximity_int_high_threshold.setter
    def proximity_int_high_threshold(self, value):
        h = value >> 8
        l = value & 0x00FF

        self.write_byte_data(APDS9930_PIHTL, l)
        self.write_byte_data(APDS9930_PIHTH, h)

    @property
    def led_drive(self):
        """LED drive strength for proximity and ALS. Good values
        are:

            Value    LED Current
              0        100 mA       (LED_DRIVE_100MA)
              1         50 mA       (LED_DRIVE_50MA)
              2         25 mA       (LED_DRIVE_25MA)
              3        12.5 mA     (LED_DRIVE_12_5MA)
        """
        reg_val = self.read_byte_data(APDS9930_CONTROL)
        v =  (reg_val >> 6) & 3     # 3 = 00000011

        return DictReprInt(v, mapping={0: "LED_DRIVE_100MA",
                                       1: "LED_DRIVE_50MA",
                                       2: "LED_DRIVE_25MA",
                                       3: "LED_DRIVE_12_5MA"})

    @led_drive.setter
    def led_drive(self, value):
        reg_val = self.read_byte_data(APDS9930_CONTROL)

        value &= 3                # 3 = 00000011
        value = value << 6
        reg_val &= int("00111111", 2)
        reg_val |= value

        self.write_byte_data(APDS9930_CONTROL, reg_val)

    @property
    def proximity_gain(self):
        """Receiver gain for proximity detection. Good values are:

            Value    Gain
              0       1x        (PGAIN_1X)
              1       2x        (PGAIN_2X)
              2       4x        (PGAIN_4X)
              3       8x        (PGAIN_8X)
        """
        reg_val = self.read_byte_data(APDS9930_CONTROL)
        v = (reg_val >> 2) & 3     # 3 = 00000011

        return DictReprInt(v, mapping={0: "PGAIN_1X",
                                       1: "PGAIN_2X",
                                       2: "PGAIN_4X",
                                       3: "PGAIN_8X"})

    @proximity_gain.setter
    def proximity_gain(self, value):
        reg_val = self.read_byte_data(APDS9930_CONTROL)

        value &= 3                # 3 = 00000011
        value = value << 2
        reg_val &= int("11110011", 2)
        reg_val |= value

        self.write_byte_data(APDS9930_CONTROL, reg_val)

    @property
    def proximity_diode(self):
        """Diode used for proximity sensor. Good values are:

            Value    Diode selection
              0       Reserved
              1       Reserved
              2       Use Ch1 diode
              3       Reserved
        """
        reg_val = self.read_byte_data(APDS9930_CONTROL)
        v = (reg_val >> 4) & 3     # 3 = 00000011

        return DictReprInt(v, mapping={3: "Ch1 diode"})

    @proximity_diode.setter
    def proximity_diode(self, value):
        reg_val = self.read_byte_data(APDS9930_CONTROL)

        value &= 3                # 3 = 00000011
        value = value << 4
        reg_val &= int("11001111", 2)
        reg_val |= value

        self.write_byte_data(APDS9930_CONTROL, reg_val)

    @property
    def ambient_light_gain(self):
        """Receiver gain for ambient light sensor. Good values are:

            Value    Gain       
              0        1x       AGAIN_1X
              1        4x       AGAIN_8X
              2       16x       AGAIN_16X
              3       64x       AGAIN_120X
        """
        reg_val = self.read_byte_data(APDS9930_CONTROL)
        v = reg_val & 3     # 3 = 00000011

        return DictReprInt(v, mapping={0: "AGAIN_1X",
                                       1: "AGAIN_8X",
                                       2: "AGAIN_16X",
                                       3: "AGAIN_120X"})

    @ambient_light_gain.setter
    def ambient_light_gain(self, value):
        reg_val = self.read_byte_data(APDS9930_CONTROL)

        value &= 3                # 3 = 00000011
        reg_val &= int("11111100", 2)
        reg_val |= value

        self.write_byte_data(APDS9930_CONTROL, reg_val)

    @property
    def ambient_light_int_low_threshold(self):
        """Ambient light interrupt low threshold.
        """
        l = self.read_byte_data(APDS9930_AILTL)
        h = self.read_byte_data(APDS9930_AILTH)

        return l + (h << 8)
    @ambient_light_int_low_threshold.setter
    def ambient_light_int_low_threshold(self, value):
        h = value >> 8
        l = value & 0x00FF

        self.write_byte_data(APDS9930_AILTL, l)
        self.write_byte_data(APDS9930_AILTH, h)

    @property
    def ambient_light_int_high_threshold(self):
        """Ambient light interrupt high threshold.
        """
        l = self.read_byte_data(APDS9930_AIHTL)
        h = self.read_byte_data(APDS9930_AIHTH)

        return l + (h << 8)
    @ambient_light_int_high_threshold.setter
    def ambient_light_int_high_threshold(self, value):
        h = value >> 8
        l = value & 0x00FF

        self.write_byte_data(APDS9930_AIHTL, l)
        self.write_byte_data(APDS9930_AIHTH, h)

    @property
    def ambient_light_interrupt(self):
        """If True, the device is asserting an ambient light interrupt.
        Set it to None to clear it.
        """
        val = self.read_byte_data(APDS9930_STATUS)
        return bool((val >> 4) & 1)
    @ambient_light_interrupt.setter
    def ambient_light_interrupt(self, value):
        if not value:
            self.write_byte(CLEAR_ALS_INT)

    @property
    def proximity_interrupt(self):
        """If True, the device is asserting a proximity interrupt.
        Set it to None to clear it.
        """
        val = self.read_byte_data(APDS9930_STATUS)
        return bool((val >> 5) & 1)
    @proximity_interrupt.setter
    def proximity_interrupt(self, value):
        if not value:
            self.write_byte(CLEAR_PROX_INT)
    
    def clear_all_interrupts(self):
        """Clear all interrupts.
        """
        self.write_byte(CLEAR_ALL_INTS)

    def _dump_registers(self):
        """Debug: read all the registers from the device and
        **print** them.
        """
        reg = 0
        while reg <= 0x19:
            val = self.read_byte_data(reg)
            print "{:<8} dec {:<3}   hex {:<4}   bin {:08d}".format(hex(reg) + ":", str(int(val)), hex(val), int(bin(val)[2:]))
            reg += 1
        val = self.read_byte_data(0x1E)
        print "{:<8} dec {:<3}   hex {:<4}   bin {:08d}".format(hex(reg) + ":", str(int(val)), hex(val), int(bin(val)[2:]))


class HexInt(int):
    """Integer that represents itself as a hex number.
    """
    def __repr__(self):
        return hex(self)

class BinInt(int):
    """Integer that represents itself as a binary number.
    """
    def __repr__(self):
        return bin(self)

class DictReprInt(int):
    """Integer that represents itself with a name rather than
    a value. Specify the name mappings in the "mapping" argument.
    """
    mapping = {}

    def __init__(self, n, base=10, mapping={}):
        self.mapping = mapping
        if type(n) == int:
            return super(DictReprInt, self).__init__(n)
        else:
            return super(DictReprInt, self).__init__(n, base)

    def __new__(cls, n, base=10, mapping={}):
        if type(n) == int:
            obj = int.__new__(cls, n)
        else:
            obj = int.__new__(cls, n, base)
        obj.mapping = mapping
        return obj

    def __repr__(self):
        if int(self) in self.mapping:
            return super(DictReprInt, self).__repr__() + " = " + self.mapping[self]
        else:
            return super(DictReprInt, self).__repr__()

class SensorError(EnvironmentError):
    pass
