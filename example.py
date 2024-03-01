import vu1

API = vu1.DialServer("http://localhost:5340", "my_secret_api_key")
dials = API.dials

# set image and value of specific dial by uid
dial = dials[dials.index("my_dial_uid")]
dial.image = "image_pack/gpu-load.png"
dial.value = 50

# set backlight to white on all available dials
for dial in dials:
    dial.color = vu1.Color(100, 100, 100) #full white

