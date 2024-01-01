from yeelight import Bulb
from yeelight import discover_bulbs


print(discover_bulbs())

bulb = Bulb("172.30.1.7")

# Turn the bulb on.
bulb.turn_on()

# Turn the bulb off.
bulb.turn_off()

# Set the bulb color.
bulb.set_rgb(255, 0, 0)