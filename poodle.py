import gamepad

from time import sleep
gamepad.init()

fart = gamepad.gamepad()
if fart.button_x == True:
    print('its connected')
    sleep(2)
else:
    print('standby, farting')
    sleep(5)
