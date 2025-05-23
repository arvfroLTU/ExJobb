
import Group_session
import math



holeLength = 440  #TODO fetch hole length from DB
Players = ["Player1", "Player2", "Player3", "Player4"] #TODO  fetch userID from DB here and for all players
Hcp1, Hcp2, Hcp3, Hcp4 = 34, 20, 15, 10 #TODO fetch from DB
P_Hcp = {Players[0]: Hcp1, Players[1]: Hcp2, Players[2]: Hcp3, Players[3]: Hcp4} #TODO fetch from DB
TurnOrder = Players    #TODO decide based on handicap
#PlayerTurnsTaken = {Players[0]: 0, Players[1]: 0, Players[2]: 0, Players[3]: 0}

Distances = {Players[0]: holeLength, Players[1]: holeLength, Players[2]: holeLength, Players[3]: holeLength}


#keeps track of players while approaching their ball during other players turns [0] for x, [1] for y, [2] for most recent theta angle
PlayerPositions = {Players[0]: [0, holeLength], Players[1]: [0, holeLength], Players[2]: [0, holeLength], Players[3]: [0, holeLength]} #TODO fetch from DB
BallPositions = {Players[0]: [0, holeLength, 0], Players[1]: [0, holeLength, 0], Players[2]: [0, holeLength, 0], Players[3]: [0, holeLength, 0]} #TODO fetch from DB




Group_session.TeeTimeEstimation(TurnOrder, Distances, P_Hcp, holeLength, PlayerPositions, BallPositions, Players)