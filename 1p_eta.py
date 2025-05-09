# use shotsim for each individual stop along track,
# compare it to an average speed accrued and,
#give estimate of  arrival time at hole presuming 9 holes
#assume app asks for what user wants on 6th hole
#take normal distribution into account

import ShotSim

handicap  = 18

# DistanceLists are meant to track the distance walked on each hole for the user
# as a means of tracking time spent on the course


#implement first     in database
realHoleDistanceList = []
simulatedholeDistanceList = []


holeDistance = 150  #TODO insert per shot



par = 4             #TODO insert per hole
strokeCount =ShotSim.simulatePlayerHole(holeDistance, handicap)









