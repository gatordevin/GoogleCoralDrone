from DroneController import droneCont
drone = droneCont("172.16.0.32")
while(True):
    drone.move(0,0,0,0)