
import Group_session
import threading
import time


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

"Beginning skeleton for real time implementation of the simulation"

coordWait = True
bad = False
coord = (0, 0)  # Placeholder for the coordinate of the tracked player
coord_ready =threading.Event()



"Tests Setting observed variable to a coordinate"
def coordSubmission(coordX, coordY):
    global coord
    global bad
    coord = (coordX, coordY)  
    bad =True
    print(" coordSubmission[device] Coordinate set. to" + str(coordX) + ' ' + str(coordY))

" Test observing architecure by observing the variable coordWait"
def wait_for_player_movement():
    global coordinate
    global bad
    global coordWait
    while coordWait is bad:
        time.sleep(0.5)
    coord_ready.set()
    print("Coordinate received:", coord)
    
    
    Blah= Group_session.coordinateToDistanceStart(coord)
    
    
    #TODO Write coord into user database while running TeeTimeEstimation or midRoundSim 
    
    bad = False


#TODO Store this somewhere
# 1st  run stored
BallPositions, PlayerPositions, Distances = Group_session.TeeTimeEstimation(TurnOrder, Distances, P_Hcp, holeLength, PlayerPositions, BallPositions, Players)




"takes user position as indata and runs next round of simulation"
def UpdateUserPosition(TrackedPlayerPosition, Distance):
    
    Distances[Players[0]] = Distance
    PlayerPositions[Players[0]] = TrackedPlayerPosition
    
    



#Can take coordinates of single player in respect to hole, and start a simulation from there   
def midRoundSim(Player, holeLength, P_Hcp, PPositions, BallPositions, PPos, APDist):
    
    #TODO Take Tracked player into account, only when tracked player is last will this occur
    #TODO tracked player will also be first in turn order
    
    #BallPosition assumed correct from previous sim and fetched here
    
    UpdateUserPosition(PPos, APDist)
    BallPositions, PlayerPositions, Distances = Group_session.startingMidRoundSim(Players, Distances, P_Hcp, PlayerPositions, BallPositions, Players)
    Group_session.startingMidRoundSim(Players, Distances, P_Hcp, holeLength, PlayerPositions, BallPositions, Players)
    #TODO
    pass


def entered_9th_hole_check():
    
    from geopy.distance import geodesic

    def check_nearby_course_color(coord):
        # Define start coordinates with colors
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
    
    
def start_observer_threads():
    t1 = threading.Thread(target=wait_for_player_movement)
    t1.start()
    return t1

def start_active_thread(x, y):
    t1 = threading.Thread(target=coordSubmission, args=(x, y), daemon=True)
    t1.start()
    return t1
    
threading.Thread(target=coordSubmission, args = (1337, 7331), daemon=True).start()
threading.Thread(target=wait_for_player_movement, daemon=True).start()

input_thread = threading.Thread(target=wait_for_player_movement)
input_thread.start()


