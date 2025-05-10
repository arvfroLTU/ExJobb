""""
    Club | Average Distance (meters)
    Driver | 210 – 265
    3-Wood | 192 – 229
    5-Wood | 183 – 219
    3-Iron | 165 – 201
    4-Iron | 155 – 192
    5-Iron | 146 – 183
    6-Iron | 137 – 174
    7-Iron | 128 – 165
    8-Iron | 119 – 155
    9-Iron | 110 – 146
    Pitching Wedge | 101 – 137
    Sand Wedge | 82 – 119
    Lob Wedge | 73 – 110 
    """

import numpy as np
import random
import math


strokeCount = 0
holeDistance = 0

# made to adjust for Shotlength always being preferred by the simulator typically, a player on green would be expected to take 2 putts, so this is set to 2
putterCount = 2

clubs = {
        "Driver": [210, 280],
        "3-Wood": [192, 229],
        "5-Wood": [183, 219],
        "3-Iron": [165, 201],
        "4-Iron": [155, 192],
        "5-Iron": [146, 183],
        "6-Iron": [137, 174],
        "7-Iron": [128, 165],
        "8-Iron": [119, 155],
        "9-Iron": [110, 146],
        "Pitching Wedge": [101, 137],
        "Sand Wedge": [92, 129],
        "Lob Wedge": [82, 119],
        "Soft Pitching Wedge": [61, 80],
        "Soft Sand Wedge": [28, 60],
        "Soft Lob Wedge": [14, 27],
        "Putter": [0, 14],
        }

def setHoleDistance(distance):
    global holeDistance
    holeDistance = distance
    print( "hole distance set to: ", holeDistance)




def failureCheck(handicap):
        value = random.randint(0, 100) 
        
        if value > handicap:
            return False
        else:
            return True
        
def criticalHitRate(handicap):
    checkValue = random.randint(0, 100)
    
    #max percent for a criticalHit is 6% for scratchplayer  and 2 % for a 36 handicap player
    handicapRefValue = min(((36-handicap)/6), 2) 
    
    if checkValue <= handicapRefValue:
        return True
    else:
        return False
    
        
        

def Club_Selection(D_hole):
    # selects appropriate club based on distance to hole
        match D_hole:
            case s if 0 <= s <= 14:
                return "Putter"
            case s if 14 < s <= 40:
                return "Soft Lob Wedge"
            case s if 40 < s <= 60:
                return "Soft Sand Wedge"
            case s if 60 < s <= 82:
                return "Soft Pitching Wedge"
            case s if 82 < s <= 119:
                return "Lob Wedge"
            case s if 119 < s <= 137:
                return "Sand Wedge"
            case s if 137 < s <= 146:
                return "Pitching Wedge"
            case s if 146 < s <= 155:
                return "9-Iron"
            case s if 155 < s <= 165:
                return "8-Iron"
            case s if 165 < s <= 174:
                return "7-Iron"
            case s if 174 < s <= 183:
                return "6-Iron"
            case s if 183 < s <= 192:
                return "5-Iron"
            case s if 192 < s <= 201:
                return "4-Iron"
            case s if 201 < s <= 210:
                return "3-Iron"
            case s if 210 < s <= 219:
                return "5-Wood"
            case s if 219 < s <= 229:
                return "3-Wood"
            case s if 229 < s:
                return "Driver"
    
        
def ShotAngle(handicap, failure):

        min_theta, max_theta = -(math.pi/4), (math.pi/4) # 45 degrees as expressed in radians
        min_hcap, max_hcap = -18, 18 
        skillBias = ((1- (handicap/36))*100)
        HandicapGaussian =np.random.normal(0, handicap/2, 1)[0]
        hcap_percentpercent_along = (HandicapGaussian - min_hcap) / (max_hcap - min_hcap) 
        
        Angle_range = skillBias* (max_theta - min_theta)
        
        if failure == True:
            
            #failure occurs
            theta = np.random.uniform(min_theta, max_theta)
        else:
            #failure doesn't occur
            max_error = math.pi/4 * (1 - skillBias / 100)  # 35 degrees max error for worst player, 0 degrees for best
            theta = np.random.uniform(-max_error, max_error)
            
        return theta

def ShotDistance(handicap, D_hole):
        #global putterCount
        # calculates shot distance based on handicap and distance to hole
        
        #sets up range for chosen club
        Club = Club_Selection(D_hole)
        failure = failureCheck(handicap)
        Crit = criticalHitRate(handicap)
        
        print("club selected is: ", Club)
       

        
        
        if Club == "Putter":
            if failure == True:
                    print("putt failed, ball barely moved ")
                    return[0,0]
            elif Crit == True:
                    # Critical hit on putt, player can sink the ball in one shot
                    print("putt was a critical hit")
                    return [D_hole,0]
            else:   
                    # Normal putt, player is cautious
                    print("putt was normal, Distance to hole diminished by 2/3ds")
                    return [(2*D_hole)/3,0]
        
        
        
        
        
        min_dist, max_dist = clubs[Club]
        club_range = max_dist - min_dist
        
        theta = ShotAngle(handicap, failure)
        # Calculates where along the club range the player shot will land
        
        handicapSigma = handicap/2
         
        HandicapGaussDistPos1 =np.random.normal(0, handicap/2, 1)[0]
        
        
        #Since variance on the normal distribution is handicap/2  the max amount of variance is 36/2 so is 18,
        #making this a global variable makes sure that the percent_along variable represens relational skill levels
        playerHandicapRange = [-18, 18] 
        min_hcap, max_hcap = playerHandicapRange
        
        #can generate zany numbers since gaussian dist is unbounded
        percent_along = ((HandicapGaussDistPos1 - min_hcap) / (max_hcap - min_hcap))* 100
        print("current shot was valued at ", percent_along,  " out of 1 for the players skill level")
        
        #meant to move a skilled player from a final result of 49-51%  of a golf clubs range to 99 to 101%
        skillBias = ((1- (handicap/36))*100)*(5/10) # a percent value which moves the shot towards the higher end of the range based on handicap, base 0 peak 40
        print("skill bias is: ", skillBias, "percent")
        print("percent along is: ", percent_along, "percent")
        print("skill bias is and percent along is: ", skillBias + percent_along, "percent")

        finalShotLength = min_dist +  (min((max((percent_along +skillBias),20), 100))/100  * (club_range))
        
        if failure == True:
            #failure occurs
            finalShotLength = finalShotLength/2 # Shot fails and distance is cut in half
            print("Shot failed")
        else:
            print("Shot is successful")
        
        
        print ("shot distance is: ", finalShotLength, "meters")
        print ("shot angle is: ", theta, "degrees")
        
        return [finalShotLength, theta]




def NextShotSetup(handicap, D_hole):
        # assume straight shot to hole for all holes
        
        #assumes this is the shot that was just made, not the shot that will be made next
        D_travel, PreTheta = ShotDistance(handicap, D_hole) 
       # global strokeCount
       # strokeCount += 1
       
        holeDistance= D_hole
        
        #pythagorean theorem to the rescue, all in radians
        
        xAxisDistTravelled = D_travel* math.sin(PreTheta)
        yAxisDistTravelled = D_travel* math.cos(PreTheta)
        yAxisDistToHole = holeDistance - yAxisDistTravelled
        print("yAxisDistToHole is: ", yAxisDistToHole, "meters")
        xAxisDistToHole = - xAxisDistTravelled
        newHoleDistance = math.sqrt(((xAxisDistToHole**2)) + (yAxisDistToHole**2))
        
        if newHoleDistance <= 1:
            newHoleDistance = 0
            print("Ball will be sunk next shot!")
        
        print("D_travel is: ", D_travel, "meters")
        print("New hole distance is: ", newHoleDistance, "meters")
        setHoleDistance(newHoleDistance)
        print("################################################")
        
        return  [D_travel, newHoleDistance, yAxisDistToHole, xAxisDistToHole, PreTheta]
    
def simulatePlayerHole(HoleDistance, handicapArg):
        #global putterCount
        strokeCount = 0
        print("################################")
        print("Golf Simulation")
        print("################################")
        setHoleDistance(HoleDistance)  # Set the distance to the hole in meters
        print("hole distance is: ", holeDistance, "meters")
        handicap = handicapArg  # Example handicap value
        print("Player handicap is: ", handicap)
        D_hole = holeDistance  # Distance to the hole
        
        while D_hole > 0:
            NextShotSetup(handicap, D_hole)
            D_hole = holeDistance  # Update the distance to the hole after each shot
            strokeCount+= 1
            print
        print("Total strokes taken: ", strokeCount)
        #putterCount = 2
        return strokeCount
    
#simulatePlayerHole(440, 34)
#print("Total strokes taken: ", strokeCount)
#strokeCount = 0
#putterCount = 2