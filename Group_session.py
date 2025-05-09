import ShotSim

# Estimate time for a group of players to finish a hole, we need:
# distance left after one shot for each of 4 players
# handicap for each of 4 players

#fetch players from database

Dummy1 = "Player1" #TODO  fetch userID from DB here and for all players
#player2
#player3
#player4

holeLength = 440  #TODO fetch hole length from DB 
P_Hcp = {"Player1": 34, "Player2": 20, "Player3": 15, "Player4": 10} #TODO fetch from DB
TurnOrder = ["Player1", "Player2", "Player3", "Player4"]    #TODO decide based on handicap
activePlayer =  TurnOrder[0] 
print(activePlayer, "is first to play")
Distances = {"Player1": holeLength, "Player2": holeLength, "Player3": holeLength, "Player4": holeLength}

#tuple pos[0] = general distance,  tuple pos[1] = yAxis distance tuple pos[2] = xAxis distance
Distances2 = {"Player1": [holeLength, holeLength, 0], "Player2": [holeLength, holeLength, 0], "Player3": [holeLength, holeLength, 0], "Player4": [holeLength, holeLength, 0]}

#keeps track of players while approaching their ball during other players turns [0] for x, [1] for y
CurrentPositions = {"Player1": [0, holeLength], "Player2": [0, holeLength], "Player3": [0, holeLength], "Player4": [0, holeLength]} #TODO fetch from DB

def ChangeTurnOrder(turnOrder, player):
    turnOrder.remove(player)
    turnOrder.insert(0, player)
    return turnOrder




def TeeTimeEstimation():
    global activePlayer
    global TurnOrder
    global Distances
    global P_Hcp
    global holeLength
    print(P_Hcp[activePlayer], "is the handicap of the first player")
    yAxisSum= 0
    totalShots = 0
    TimedWalks = []  # since players normally move concurrently, only the walkups to the worst shots should count for the amount of time 
    timeKeeping  = []
    NoWalkUp =4     #since no player walks up to tee, this cant amount for travel time
    
    while all(value != 0 for value in Distances.values()):
        print("player is", activePlayer, "with handicap", P_Hcp[activePlayer])
        # Simulation of single player doing one shot
        
        #TODO add time calculation/logging for distance travelled and tee time
        #TODO in time logging, only calculate bottleneck
        
        
        #keeping track of movements that occur during a shot aswell as turn order.
        
        Shot = ShotSim.NextShotSetup(P_Hcp[activePlayer], Distances[activePlayer])
        D_walked, D_ToHole, yAxisLeft, xAxisDisc = Shot
        
        #store
        Active_X_StartDist = Distances2[activePlayer][2] #starting distance for active player during current shot
        Active_Y_StartDist = Distances2[activePlayer][1] #starting distance for active player during current shot
        ActiveStartDist = Distances[activePlayer] #starting distance for active player during current shot
        
        #update
        Distances2[activePlayer][2] = xAxisDisc #update xAxis distance to hole for active player
        Distances2[activePlayer][1] = yAxisLeft #update yAxis distance for active player
        Distances[activePlayer] = D_ToHole # updatedistance left to hole for active player after shot
        
        furthestPlayer = max(Distances, key=Distances.get)
        
        Groupwalk =ActiveStartDist - Distances2[furthestPlayer][1] #distance walked to the furthest player
        
        #after the first four shots, the players walk up to the furthest player
        NoWalkUp-= 1
        
        if NoWalkUp  <= 0:  # cases after players ahve left starting tee  
                if furthestPlayer != activePlayer:
                    #TODO not very precise but good enough for now
                    
                    yAxisSum += yAxisLeft #keeps track of how far along most players would be to keep up with the spearhead player
                    print("yAxisSum is: ", yAxisSum)
                    
                    #D_walked = (holeLength - Distances[furthestPlayer]) + yAxisSum #distance walked to the furthest player
                    TimedWalks.append(Groupwalk) #add distance walked for new player furthest from hole
                    TimedWalks.append("Player Switch")
                else:
                    TimedWalks.append(D_walked)
                    TimedWalks.append("Player stays")
                    
        else: #All the cases before group leaves starting tee
            if TimedWalks == []:
                TimedWalks.append(D_walked)
                TimedWalks.append("1st Player stays")
            else:
                if TimedWalks[0] > D_walked:
                    TimedWalks[0] = D_walked
                    TimedWalks[1] = "1st player switches"
            
        ChangeTurnOrder(TurnOrder, furthestPlayer) # change turn order to the player who is furthest from the hole
        
        if TimedWalks[-1] == "1st player switches" or TimedWalks[-1] == "Player Switch":
            TimedWalks[-1] += (" " + TurnOrder[0]) #add the name of the player who is furthest from the hole to the list of distances walked
        print("Turn order is now: ", TurnOrder)
        
        activePlayer =  TurnOrder[0]
        totalShots += 1
        print ("Player: ", activePlayer, "Distance to hole: ", Distances[activePlayer])  
    
    for i in range(0, len(TimedWalks), 2):
        print(TimedWalks[i:i+2])
        
    result = sum(TimedWalks[0::2])
    print("Total distance walked is: ", result, "meters")
    
    #totTime = (40* totalShots) + (sum(TimedWalks)*1.4) #40 seconds per shot + time spent walking up to the furthest player and ball
    print("################################################")
    #print(totalShots, " shots taken", sum(TimedWalks), "meters walked", "total time spent: ", totTime/60, "minutes")
    print("################################################")
TeeTimeEstimation()