import vu1

API = vu1.DialServer("http://localhost:5340", "my_secret_api_key")
dials = API.dials

# set color, image and value of specific dial by uid
dial = dials[dials.index("my_dial_uid")]
dial.image = "image_pack/gpu-load.png"
dial.value = 50

dial.color = vu1.VUColor(100, 100, 0) # as expected by the API (color between 0-100)
dial.color = vu1.RGBColor(1.0, 1.0, 0.0) # can be used to have colors as float
dial.color = vu1.HSVColor(0.16666666666666669, 1.0, 1.0) # same color as above (yellow) but written in HSV color space - userful for e.g. gradients

# set backlight to white on all available dials
for dial in dials:
    dial.color = vu1.VUColor(100, 100, 100) # full white
