
import Group_session
import threading
import time
import signal
import sys
from geopy.distance import geodesic


################## STARTING VARIABLES FOR SIM #########################

holeLength = 440  #TODO fetch hole length from DB
Players = ["Player1", "Player2", "Player3", "Player4"] #TODO  fetch userID from DB here and for all players
Hcp1, Hcp2, Hcp3, Hcp4 = 34, 20, 15, 10 #TODO fetch from DB
P_Hcp = {Players[0]: Hcp1, Players[1]: Hcp2, Players[2]: Hcp3, Players[3]: Hcp4} #TODO fetch from DB
TurnOrder = Players    #TODO decide based on handicap

ActivePlayerPosition = {Players[0]: (0, holeLength)}
ActivePlayerDistance = {Players[0]: holeLength}  #TODO fetch from DB

Distances = {Players[0]: holeLength, Players[1]: holeLength, Players[2]: holeLength, Players[3]: holeLength}

#keeps track of players while approaching their ball during other players turns [0] for x, [1] for y, [2] for most recent theta angle
PlayerPositions = {Players[0]: [0, holeLength], Players[1]: [0, holeLength], Players[2]: [0, holeLength], Players[3]: [0, holeLength]} #TODO fetch from DB
BallPositions = {Players[0]: [0, holeLength, 0], Players[1]: [0, holeLength, 0], Players[2]: [0, holeLength, 0], Players[3]: [0, holeLength, 0]} #TODO fetch from DB


###########################################################################33











"Beginning skeleton for real time implementation of the simulation"

coordWait = True
RecieverReady = False
coord = (0, 0)  # Placeholder for the coordinate of the tracked player
coord_ready =threading.Event()
stop_thread = threading.Event()

###################### Base observer pattern ###############################


def start_observer_threads():
    t1 = threading.Thread(target=wait_for_player_movement)
    t1.start()
    return t1

def start_active_thread(x, y):
    t1 = threading.Thread(target=coordSubmission, args=(x, y), daemon=True)
    t1.start()
    return t1


"Sets observed variable to a coordinate"
def coordSubmission(coordX, coordY):
    global coord
    global RecieverReady
    coord = (coordX, coordY)  
    RecieverReady =True
    coord_ready.set()
    print(" coordSubmission[device] Coordinate set. to " + str(coordX) + ' ' + str(coordY))



" Test observing architecure by observing the variable coordWait"

def wait_for_player_movement():
    global coord
    global RecieverReady
    global coordWait
    global stop_thread
    global BallPositions
    global PlayerPositions  
    global Distances
    
    while not stop_thread.is_set():
     # Wait until a coordinate is ready or stop requested
        triggered = coord_ready.wait(timeout=3)  
        if stop_thread.is_set():
            print("Break reached")
            break
        if triggered:
            print("Coordinate received:", coord)
            
            
            #intended to return the total amount of space travelled by the active player
            
            BallPositions, PlayerPositions, Distances = midRoundSim(Players[0], holeLength, P_Hcp[Players[0]], PlayerPositions, BallPositions, coord)
            
            
            
            
            RecieverReady = False
            coord_ready.clear()  # Go back to waiting
            
            
            
            
        

def signal_handler(sig, frame):
    print("\nStopping threads...")
    stop_thread.set()
    coord_ready.set()  # Wake any waiting threads so they can exit
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)



#TODO Store this somewhere
# 1st  run stored
BallPositions, PlayerPositions, Distances = Group_session.TeeTimeEstimation(TurnOrder, Distances, P_Hcp, holeLength, PlayerPositions, BallPositions, Players)




"takes user position as indata and runs next round of simulation for tracked player"
def UpdateUserPosition(TrackedPlayerPosition):
    
    global Distances
    global PlayerPositions
    
    
    #Distance to which hole? Let's decide on the blue hole
    Distances[Players[0]] = geodesic(TrackedPlayerPosition, (63.715154, 20.399921)).meters  #Set to blue hole
    PlayerPositions[Players[0]] = TrackedPlayerPosition
    
    



#Can take coordinates of single player in respect to hole, and start a simulation from there   
def midRoundSim(Player, holeLength, P_Hcp, PlayerPositions, BallPositions, PPos):
    
    #TODO Take Tracked player into account, only when tracked player is last will this occur
    #TODO tracked player will also be first in turn order
    
    #BallPosition assumed correct from previous sim and fetched here
    
    
    BallPositions, PlayerPositions, Distances = Group_session.startingMidRoundSim(Players, Distances, P_Hcp, PlayerPositions, BallPositions, Players)
    UpdateUserPosition(PPos) # overwrites sim data with actual data
    
    Group_session.startingMidRoundSim(Players, Distances, P_Hcp, holeLength, PlayerPositions, BallPositions, Players)
    
    pass


def entered_9th_hole_check():

    def check_nearby_course_color(coord):
        starts = {
            "Red": (63.714834, 20.408835),
            "Blue": (63.713914, 20.400604),
            "Yellow": (63.715103, 20.396621)
        }

        for color, start_coord in starts.items():
            distance = geodesic(coord, start_coord).meters
            if distance <= 10:
                return True, color

        return False, None
    



input_thread = threading.Thread(target=wait_for_player_movement, daemon=True)
input_thread.start()


