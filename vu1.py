from os.path import join as joinpath
import json
import colorsys
import requests

API_BASE = "api/v0/dial"

class DialServer():
    def __init__(self, url, key):
        self.url = url
        self._base = joinpath(self.url, API_BASE)
        self.key = key
        self._dials = []
        pass

    @property
    def dials(self):
        dial_data = self._req("list")
        for d in dial_data:
            dial = Dial(self, d["uid"])
            if not dial in self._dials:
                self._dials.append(dial)
        return self._dials

    @property
    def color(self):
        return None

    @color.setter
    def color(self, color):
        for dial in self._dials:
            dial.color = color

    def _req(self, endpoint, params={}, post=False):
        data_dict_base = {
            "key": self.key
        }
        data_dict = {**data_dict_base, **params}

        req = requests.post(joinpath(self._base, endpoint), data=data_dict_base, files=data_dict) if post else requests.get(joinpath(self._base, endpoint), data=data_dict)

        try:
            result = req.json()
            if result["status"] == "ok":
                return result["data"]
            else:
                raise Exception
        except KeyError as e:
            raise e

class Dial():
    def __init__(self, server, uid):
        self._server = server
        self.uid = uid
        pass

    def __eq__(self, other):
        try:
            return self.uid.lower() == other.uid.lower() #if other is another dial instance
        except AttributeError:
            return self.uid.lower() == other.lower() #fall back to uid string comparision

    def __repr__(self):
        return f"{super().__repr__()} - {self.name}, {self.uid}"

    def _get_status(self):
        s = self._server._req(f"{self.uid}/status")
        self._index = int(s["index"])
        self._name  = s["dial_name"]
        self._value = int(s["value"])
        self._fw_hash = s["fw_hash"]
        self._fw_version = s["fw_version"]
        self._hw_version = s["hw_version"]
        self._protocol_version = s["protocol_version"]
        self._color = Color(*s["backlight"].values())
        self._image = s["image_file"]

    @property
    def index(self):
        self._get_status()
        return self._index

    @property
    def name(self):
        self._get_status()
        return self._name

    @name.setter
    def name(self, new_name):
        self._server._req(f"{self.uid}/name", {"name": new_name})

    @property
    def value(self):
        self._get_status()
        return self._value

    @value.setter
    def value(self, new_value):
        self._server._req(f"{self.uid}/set", {"value": max(0, min(100, int(new_value)))})

    @property
    def fw_hash(self):
        self._get_status()
        return self._fw_hash

    @property
    def fw_version(self):
        self._get_status()
        return self._fw_version

    @property
    def hw_version(self):
        self._get_status()
        return self._hw_version

    @property
    def protocol_version(self):
        self._get_status()
        return self._protocol_version

    @property
    def color(self):
        self._get_status()
        return self._color

    @color.setter
    def color(self, new_color):
        self._server._req(f"{self.uid}/backlight", dict(new_color))

    @property
    def image(self):
        self._get_status()
        return self._image

    @image.setter
    def image(self, new_image):
        file = {'imgfile': (open(new_image, 'rb'))}
        self._server._req(f"{self.uid}/image/set", file, post=True)

class Color():
    def __init__(self, red, green, blue):
        self.red = max(0, min(100, red))
        self.green = max(0, min(100, green))
        self.blue = max(0, min(100, blue))

    def hsv(self):
        return colorsys.rgb_to_hsv(self.red, self.green, self.blue)

    def __iter__(self):
        for attr in ["red", "green", "blue"]:
            yield (attr, self.__dict__[attr])
