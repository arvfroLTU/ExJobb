
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



coord = (0, 0)  # Placeholder for the coordinate of the tracked player
coord_ready =threading.Event()





"Beginning skeleton for real time implementation of the simulation"


coordWait = True
bad = False


def goodCoordWait():
    global coord
    time.sleep(10)  # simulate delay before device gives coordinate
    coord = (59.3293, 18.0686)  
    bad =True
    print("[device] Coordinate set.")


def wait_for_player_movement():
    global coordinate
    while coordWait is bad:
        time.sleep(0.5)
    coord_ready.set()
    print("Coordinate received:", coord)
    bad = False
    

threading.Thread(target=goodCoordWait, daemon=True).start()
threading.Thread(target=wait_for_player_movement, daemon=True).start()

input_thread = threading.Thread(target=wait_for_input)
input_thread.start()





#TODO Store this somewhere
# 1st  run stored
BallPositions, PlayerPositions, Distances = Group_session.TeeToTimeEstimation(TurnOrder, Distances, P_Hcp, holeLength, PlayerPositions, BallPositions, Players)




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


#The model of the golf course should be able to be simplified to a straight 2d plane