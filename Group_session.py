import ShotSim
import math


holeLength  = 440
Players = ["Player1", "Player2", "Player3", "Player4"]
P_Hcp = {Players[0]: 34, Players[1]: 20, Players[2]: 15, Players[3]: 10} #TODO fetch from DB
TurnOrder = [Players[0], Players[1], Players[2], Players[3]]    #TODO decide based on handicap
PlayerTurnsTaken = {Players[0]: 0, Players[1]: 0, Players[2]: 0, Players[3]: 0}

Distances = {"Player1": holeLength, "Player2": holeLength, "Player3": holeLength, "Player4": holeLength}


#keeps track of players while approaching their ball during other players turns [0] for x, [1] for y, [2] for most recent theta angle
PlayerPositions = {Players[0]: [0, holeLength], Players[1]: [0, holeLength], Players[2]: [0, holeLength], Players[3]: [0, holeLength]} #TODO fetch from DB
BallPositions = {Players[0]: [0, holeLength, 0], Players[1]: [0, holeLength, 0], Players[2]: [0, holeLength, 0], Players[3]: [0, holeLength, 0]} #TODO fetch from DB
#TODO fetch from DB

def ChangeTurnOrder(turnOrder, player):
    turnOrder.remove(player)
    turnOrder.insert(0, player)
    return turnOrder

def update_other_players_positions(excluded_player, yAxisGroup, TurnOrder, PlayerPositions, BallPositions, PlayerMovements):
    
    for player in TurnOrder:

        if player == excluded_player and PlayerPositions[player][1] > math.fabs(yAxisGroup): #only move players who are not the furthest or the active player
            
            #Using trigonometry to track non last-place players 
            yMovement= yAxisGroup - PlayerPositions[player][1]
            angle = BallPositions[player][2]
            hypotenuse= (yMovement)/math.cos(angle) #length travelled


            NonActivePlayer_X =math.sqrt((hypotenuse**2) - (yMovement**2)) #xAxis distance player moves while approaching ball
            PlayerPositions[player][0] = PlayerPositions[player][0] + NonActivePlayer_X #update xAxis distance to hole for player
            PlayerPositions[player][1] = PlayerPositions[player][1] + yMovement #update yAxis distance for player
            if abs(hypotenuse) > 0.01:
                print( player, " moved to: ", PlayerPositions[player][0], PlayerPositions[player][1], " a distance of ", hypotenuse)
                PlayerMovements[player].append(math.fabs(hypotenuse))



def TeeTimeEstimation(TurnOrder, Distances, P_Hcp, holeLength, PlayerPositions, BallPositions, Players):
   
   
    tempY = 0           #these three hold the positions of the player to shoot first after moving away from tee
    tempX = 0           # it's for an edge case. time calculation doesn't work without it
    cacheFlag = 0
    TrackedPlayer = TurnOrder[0]
    yAxisGroup= 0
    totalShots = 0
    TimedWalks = []  # since players normally move concurrently, only the walkups to the worst shots should count for the amount of time 
    NoWalkUp =4     #since no player walks up to staring tee, this cant amount for travel time.
    TurnNumber= 0
    
    activePlayer =  TurnOrder[0] 
    PlayerTurnsTaken = {Players[0]: 0, Players[1]: 0, Players[2]: 0, Players[3]: 0}
    PlayerMovements = {Players[0]: [], Players[1]: [], Players[2]: [], Players[3]: []} 
    
    # Simulation of single player doing one shot
    while any(value != 0 for value in Distances.values()):
        
        print("player is", activePlayer, "with handicap", P_Hcp[activePlayer])
        
        #keeping track of movements that occur during a shot 
        
        Shot = ShotSim.NextShotSetup(P_Hcp[activePlayer], Distances[activePlayer])
        PlayerTurnsTaken[activePlayer] += 1
        D_walked, D_ToHole, yAxisLeft, xAxisDisc, theta = Shot
        
        
        #keep track of last player's distance to Hole
        Distances[activePlayer] = D_ToHole # update distance left to hole for active player after shot
        
        #store ball position
        BallPositions[activePlayer][0] = BallPositions[activePlayer][0] +xAxisDisc 
        BallPositions[activePlayer][1] = yAxisLeft
        BallPositions[activePlayer][2] = theta #angle in respect to player and ball in x-y plane
        
        
        
        
        furthestPlayer = max(Distances, key=Distances.get)
        
        #euclidean distance formula for last place player approaching ball
        Groupwalk = math.sqrt((BallPositions[furthestPlayer][0]-PlayerPositions[furthestPlayer][0])**2 + (BallPositions[furthestPlayer][1]-PlayerPositions[furthestPlayer][1])**2) #distance walked to the furthest player
        
        
        
        if NoWalkUp  <= 0:  # cases after players have left starting tee 
            TurnNumber += 1
            print("Turn number is now: ", TurnNumber)
            
            yAxisGroup = BallPositions[furthestPlayer][1] #yAxis distance that the group moves to current last player
            print("Y Axis distance left to hole for furthest player is: ", yAxisGroup)
            
            flag= 0
            
            if NoWalkUp == 0: #walk up for first player to leave starting tee
                print( activePlayer, " is first to bat")
                flag = 1
                print(" HEY", str(math.sqrt((tempY)**2  + (tempX - 0)**2)))
                PlayerMovements[activePlayer].append(math.sqrt((holeLength  - tempY)**2  + (tempX - 0)**2))  #add distance walked for new player furthest from hole
                PlayerPositions[activePlayer][0] = tempX #update xAxis distance to hole for player
                PlayerPositions[activePlayer][1] = tempY #update yAxis distance for player
                
                TimedWalks.append(D_walked)
                TimedWalks.append("1st walkup " +str(activePlayer))
                TimedWalks.append(math.sqrt((tempY)**2  + (tempX - 0)**2))
                TimedWalks.append("1st shot " +str(activePlayer))
                print("CHECK")
                
                for player in TurnOrder:
                    
                    if player != activePlayer and PlayerPositions[player][1] > math.fabs(yAxisGroup): #only move players who are not the furthest or the active player
                        
                        #Using trigonometry to track non last-place players 
                        yMovement= yAxisGroup - PlayerPositions[player][1]
                        angle = BallPositions[player][2]
                        hypotenuse= (yMovement)/math.cos(angle) #length travelled


                        NonActivePlayer_X =math.sqrt((hypotenuse**2) - (yMovement**2)) #xAxis distance player moves while approaching ball
                        PlayerPositions[player][0] = PlayerPositions[player][0] + NonActivePlayer_X #update xAxis distance to hole for player
                        PlayerPositions[player][1] = PlayerPositions[player][1] + yMovement #update yAxis distance for player
                        if abs(hypotenuse) > 0.01:
                            print(" 124X Player ", player, " moved to: ", PlayerPositions[player][0], PlayerPositions[player][1], " a distance of ", hypotenuse)
                            PlayerMovements[player].append(math.fabs(hypotenuse))
                
                
                
            if furthestPlayer != activePlayer and flag == 0: #this means the current player has shot themself out of last place
                
                
                #TODO Fix so that it is the individual walk of the furthest player
                
                TimedWalks.append(Groupwalk) #add distance walked for new player furthest from hole 
                TimedWalks.append("Player Switch Groupwalk")
                
                #MOVE OTHER PLAYERS TO Y AXIS OF FURTHEST PLAYER BUT TOWARDS THEIR OWN BALL
                
                for player in TurnOrder:
                    
                    if player != furthestPlayer and PlayerPositions[player][1] > math.fabs(yAxisGroup): #only move players who are not the furthest or the active player
                        
                        #Using trigonometry to track non last-place players 
                        yMovement= yAxisGroup - PlayerPositions[player][1]
                        angle = BallPositions[player][2]
                        hypotenuse= (yMovement)/math.cos(angle) #length travelled


                        NonActivePlayer_X =math.sqrt((hypotenuse**2) - (yMovement**2)) #xAxis distance player moves while approaching ball
                        PlayerPositions[player][0] = PlayerPositions[player][0] + NonActivePlayer_X #update xAxis distance to hole for player
                        PlayerPositions[player][1] = PlayerPositions[player][1] + yMovement #update yAxis distance for player
                        if abs(hypotenuse) > 0.01:
                            print(" 153X Player ", player, " moved to: ", PlayerPositions[player][0], PlayerPositions[player][1], " a distance of ", hypotenuse)
                            PlayerMovements[player].append(math.fabs(hypotenuse))
                
                
            else : #furthest player remains the active player
                if flag == 0:
                    
                    
                    #logging
                    TimedWalks.append(D_walked)
                    TimedWalks.append("Player stays D " +str(activePlayer))
                    PlayerMovements[activePlayer].append(math.fabs(D_walked))
                    PlayerPositions[activePlayer][0] = BallPositions[activePlayer][0] 
                    PlayerPositions[activePlayer][1] = BallPositions[activePlayer][1] #update xAxis distance to hole for active player
                    print(" 167X Player ", activePlayer, " moved to: ", PlayerPositions[activePlayer][0], PlayerPositions[activePlayer][1], " a distance of ", hypotenuse)
                    
                    for player in TurnOrder:
                    
                        if player != activePlayer and PlayerPositions[player][1] > math.fabs(yAxisGroup): #only move players who are not the furthest or the active player
                            
                            #Using trigonometry to track non last-place players 
                            yMovement= yAxisGroup - PlayerPositions[player][1]
                            angle = BallPositions[player][2]
                            hypotenuse= (yMovement)/math.cos(angle) #length travelled


                            NonActivePlayer_X =math.sqrt((hypotenuse**2) - (yMovement**2)) #xAxis distance player moves while approaching ball
                            PlayerPositions[player][0] = PlayerPositions[player][0] + NonActivePlayer_X #update xAxis distance to hole for player
                            PlayerPositions[player][1] = PlayerPositions[player][1] + yMovement #update yAxis distance for player
                            
                            if abs(hypotenuse) > 0.01:
                                print(" 164X Player ", player, " moved to: ", PlayerPositions[player][0], PlayerPositions[player][1])
                                PlayerMovements[player].append(math.fabs(hypotenuse))
                        
        else: #All the cases before group leaves starting tee
            
            if TimedWalks == []:
                TimedWalks.append(D_walked)
                TimedWalks.append("1st Player walking up stays  " + str(activePlayer)) 
                tempX, tempY, tempTheta = xAxisDisc, yAxisLeft, theta
            else:
                if TimedWalks[0] > D_walked:
                    TimedWalks[0] = D_walked
                    TimedWalks[1] = "1st walkup switches " + str(activePlayer)
                    tempX, tempY, tempTheta = xAxisDisc, yAxisLeft, theta 
            
            
            
            
        #Ordering and logging for next player up to bat 
            
        ChangeTurnOrder(TurnOrder, furthestPlayer) # change turn order to the player who is furthest from the hole
        
        if TimedWalks[-1] == "1st player switches" or TimedWalks[-1] == "Player Switch":
            TimedWalks[-1] += (" " + TurnOrder[0]) #add the name of the player who is furthest from the hole to the list of distances walked
        print("Turn order is now: ", TurnOrder)
        
        activePlayer =  TurnOrder[0]
        if activePlayer== TrackedPlayer and cacheFlag ==0:
            cacheFlag +=1
            cachedBallPos = BallPositions
            cachedPlayerPos = PlayerPositions
            cachedDistances = Distances
            print("Cached ball position: ", cachedBallPos)
            print("Cached player position: ", cachedPlayerPos)
            print("Cached distances: ", cachedDistances)
        
        #after the first four shots, the players walk up to the furthest player
        NoWalkUp-= 1
    
    for i in range(0, len(TimedWalks), 2):
        print(TimedWalks[i:i+2])
        
        
        
    result = sum(TimedWalks[0::2])
    print("Total distance walked is: ", result, "meters")
  
    for player, distances in PlayerMovements.items():
        for i, d in enumerate(distances, 1):
            print(f"{player} - Movement {i}: {d:.2f} meters")
            
      
    for player, distances in PlayerMovements.items():
        total_distance = sum(distances) 
        print(f"{player} traveled a total of {total_distance:.2f} meters")
    
    for player, turns in PlayerTurnsTaken.items():
        print(f"{player} has taken  {turns} Shots on the current hole ")
    
    
    #totTime = (40* totalShots) + (sum(TimedWalks)*1.4) #40 seconds per shot + time spent walking up to the furthest player and ball
    print("################################################")
    #print(totalShots, " shots taken", sum(TimedWalks), "meters walked", "total time spent: ", totTime/60, "minutes")
    print("################################################")
    
    return cachedBallPos, cachedPlayerPos, cachedDistances
    
     
 
def startingMidRoundSim(TurnOrder, Distances, P_Hcp, PlayerPositions, BallPositions, Players):
       
    cacheFlag = 0
    TrackedPlayer = TurnOrder[0]
    yAxisGroup = max(PlayerPositions.values(), key=lambda x: x[1])[1]
    totalShots = 0
    TimedWalks = []  # since players normally move concurrently, only the walkups to the worst shots should count for the amount of time 
    
    activePlayer =  TurnOrder[0] 
    PlayerTurnsTaken = {Players[0]: 0, Players[1]: 0, Players[2]: 0, Players[3]: 0}
    PlayerMovements = {Players[0]: [], Players[1]: [], Players[2]: [], Players[3]: []} 
    
    # Simulation of single player doing one shot
    while any(value != 0 for value in Distances.values()):
        
        PlayerTurnsTaken[activePlayer] += 1
        print("player is", activePlayer, "with handicap", P_Hcp[activePlayer])
        
        #keeping track of movements that occur during a shot 
        Shot = ShotSim.NextShotSetup(P_Hcp[activePlayer], Distances[activePlayer])
        D_walked, D_ToHole, yAxisLeft, xAxisDisc, theta = Shot
        Distances[activePlayer] = D_ToHole # update distance left to hole for active player after shot
        
        #store ball position
        BallPositions[activePlayer][0] = BallPositions[activePlayer][0] +xAxisDisc 
        BallPositions[activePlayer][1] = yAxisLeft
        BallPositions[activePlayer][2] = theta #angle in respect to player and ball in x-y plane
        
        #euclidean distance formula for last place player approaching ball
        furthestPlayer = max(Distances, key=Distances.get)
        Groupwalk = math.sqrt((BallPositions[furthestPlayer][0]-PlayerPositions[furthestPlayer][0])**2 + (BallPositions[furthestPlayer][1]-PlayerPositions[furthestPlayer][1])**2) #distance walked to the furthest player
        yAxisGroup = BallPositions[furthestPlayer][1] #yAxis distance that the group moves to current last player
        print("Y Axis distance left to hole for furthest player is: ", yAxisGroup)
    
        for player in TurnOrder:
            
            if player != activePlayer and PlayerPositions[player][1] > math.fabs(yAxisGroup): #only move players who are not the furthest or the active player
                
                #Using trigonometry to track non last-place players 
                yMovement= yAxisGroup - PlayerPositions[player][1]
                angle = BallPositions[player][2]
                hypotenuse= (yMovement)/math.cos(angle) #length travelled


                NonActivePlayer_X =math.sqrt((hypotenuse**2) - (yMovement**2)) #xAxis distance player moves while approaching ball
                PlayerPositions[player][0] = PlayerPositions[player][0] + NonActivePlayer_X #update xAxis distance to hole for player
                PlayerPositions[player][1] = PlayerPositions[player][1] + yMovement #update yAxis distance for player
                if abs(hypotenuse) > 0.01:
                    print(" 124X Player ", player, " moved to: ", PlayerPositions[player][0], PlayerPositions[player][1], " a distance of ", hypotenuse)
                    PlayerMovements[player].append(math.fabs(hypotenuse))
            
            
            
        if furthestPlayer != activePlayer: #this means the current player has shot themself out of last place
            
            
            #TODO Fix so that it is the individual walk of the furthest player
            
            TimedWalks.append(Groupwalk) #add distance walked for new player furthest from hole 
            TimedWalks.append("Player Switch Groupwalk")
            
            #MOVE OTHER PLAYERS TO Y AXIS OF FURTHEST PLAYER BUT TOWARDS THEIR OWN BALL
            
            for player in TurnOrder:
                
                if player != furthestPlayer and PlayerPositions[player][1] > math.fabs(yAxisGroup): #only move players who are not the furthest or the active player
                    
                    #Using trigonometry to track non last-place players 
                    yMovement= yAxisGroup - PlayerPositions[player][1]
                    angle = BallPositions[player][2]
                    hypotenuse= (yMovement)/math.cos(angle) #length travelled


                    NonActivePlayer_X =math.sqrt((hypotenuse**2) - (yMovement**2)) #xAxis distance player moves while approaching ball
                    PlayerPositions[player][0] = PlayerPositions[player][0] + NonActivePlayer_X #update xAxis distance to hole for player
                    PlayerPositions[player][1] = PlayerPositions[player][1] + yMovement #update yAxis distance for player
                    if abs(hypotenuse) > 0.01:
                        print(" 153X Player ", player, " moved to: ", PlayerPositions[player][0], PlayerPositions[player][1], " a distance of ", hypotenuse)
                        PlayerMovements[player].append(math.fabs(hypotenuse))
                
                
            else : #furthest player remains the active player
                    
                    
                    #logging
                    TimedWalks.append(D_walked)
                    TimedWalks.append("Player stays D " +str(activePlayer))
                    PlayerMovements[activePlayer].append(math.fabs(D_walked))
                    PlayerPositions[activePlayer][0] = BallPositions[activePlayer][0] 
                    PlayerPositions[activePlayer][1] = BallPositions[activePlayer][1] #update xAxis distance to hole for active player
                    print(" 167X Player ", activePlayer, " moved to: ", PlayerPositions[activePlayer][0], PlayerPositions[activePlayer][1], " a distance of ", hypotenuse)
                    
                    for player in TurnOrder:
                    
                        if player != activePlayer and PlayerPositions[player][1] > math.fabs(yAxisGroup): #only move players who are not the furthest or the active player
                            
                            #Using trigonometry to track non last-place players 
                            yMovement= yAxisGroup - PlayerPositions[player][1]
                            angle = BallPositions[player][2]
                            hypotenuse= (yMovement)/math.cos(angle) #length travelled


                            NonActivePlayer_X =math.sqrt((hypotenuse**2) - (yMovement**2)) #xAxis distance player moves while approaching ball
                            PlayerPositions[player][0] = PlayerPositions[player][0] + NonActivePlayer_X #update xAxis distance to hole for player
                            PlayerPositions[player][1] = PlayerPositions[player][1] + yMovement #update yAxis distance for player
                            
                            if abs(hypotenuse) > 0.01:
                                print(" 164X Player ", player, " moved to: ", PlayerPositions[player][0], PlayerPositions[player][1])
                                PlayerMovements[player].append(math.fabs(hypotenuse))

            
        #Ordering and logging for next player up to bat 
            
        ChangeTurnOrder(TurnOrder, furthestPlayer) # change turn order to the player who is furthest from the hole
        
        if TimedWalks[-1] == "1st player switches" or TimedWalks[-1] == "Player Switch":
            TimedWalks[-1] += (" " + TurnOrder[0]) #add the name of the player who is furthest from the hole to the list of distances walked
        print("Turn order is now: ", TurnOrder)
        
        activePlayer =  TurnOrder[0]
        if activePlayer== TrackedPlayer and cacheFlag ==0:
            cacheFlag +=1
            cachedBallPos = BallPositions
            cachedPlayerPos = PlayerPositions
            cachedDistances = Distances
        totalShots += 1
        print ("Player: ", activePlayer, "Distance to hole: ", Distances[activePlayer])  
        
    for i in range(0, len(TimedWalks), 2):
        print(TimedWalks[i:i+2])
        
    result = sum(TimedWalks[0::2])
    print("Total distance walked is: ", result, "meters")
  
    for player, distances in PlayerMovements.items():
        for i, d in enumerate(distances, 1):
            print(f"{player} - Movement {i}: {d:.2f} meters")
            
      
    for player, distances in PlayerMovements.items():
        total_distance = sum(distances) 
        print(f"{player} traveled a total of {total_distance:.2f} meters")
    
    for player, turns in PlayerTurnsTaken.items():
        print(f"{player} has taken  {turns} Shots on the current hole ")
    
    return cachedBallPos, cachedPlayerPos, cachedDistances
  
  

TeeTimeEstimation(TurnOrder, Distances, P_Hcp, holeLength, PlayerPositions, BallPositions, Players)



