from DroneController import droneCont
import pygame
import time
drone = droneCont("10.0.0.17")
pygame.init()
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
leftBump = False
rightBump = False
if joystick_count != 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    pygame.quit()
drone.arming()
drone.enableAlignment()
while True:
    # get every event in the events list
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.send('client terminate')
            pygame.quit()
            quit()

    # number of inputs
    name = joystick.get_name()
    axes = joystick.get_numaxes()
    buttons = joystick.get_numbuttons()
    hats = joystick.get_numhats()

    # get the input types value
    x1_axis = joystick.get_axis(0)
    y1_axis = joystick.get_axis(1)

    x2_axis = joystick.get_axis(4)
    y2_axis = joystick.get_axis(3)

    a_button = joystick.get_button(0)
    b_button = joystick.get_button(1)
    if(abs(x1_axis) < 0.1):
        x1_axis = 0
    if (abs(x2_axis) < 0.1):
        x2_axis = 0
    if (abs(y1_axis) < 0.1):
        y1_axis = 0
    if (abs(y2_axis) < 0.1):
        y2_axis = 0
    if(a_button):
        drone.arming()
    elif(b_button):
        drone.disarm()

    if(joystick.get_button(4)):
        drone.updateDead(-2.0)

    if(joystick.get_button(5)):
        drone.updateDead(2.0)

    drone.move(0.1*x1_axis,0.25*x2_axis,-0.25*y2_axis,-y1_axis)
    time.sleep(0.05)
