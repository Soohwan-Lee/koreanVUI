from yeelight import Bulb
from yeelight import discover_bulbs

# Discover enable bulb
# print(discover_bulbs())

# Bulbs List (EXPC_Lab WIFI)
livingRoomBulb = Bulb("192.168.0.17")
bedRoomBulb = Bulb("192.168.0.18")

bedRoomBulb.turn_off()



# Funtion: Turn the bulb on.
def turnOn_livingRoomBulb():
    livingRoomBulb.turn_on()

def turnOn_bedRoomBulb():
    bedRoomBulb.turn_on()

# Function: Turn the bulb off.
def turnOff_livingRoomBulb():
    livingRoomBulb.turn_off()

def turnOff_bedRoomBulb():
    bedRoomBulb.turn_off()

# Set the bulb color.
def setRGB_livingRoomBulb(r, g, b):
    livingRoomBulb.set_rgb(r, g, b)

def setRGB_bedRoomBulb(r,g,b):
    bedRoomBulb.set_rgb(r,g,b)