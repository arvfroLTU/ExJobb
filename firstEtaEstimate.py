from getpass import getpass
from mysql.connector import connect, Error

user = input("Enter user e-mail: ")
course = input("Enter course id: ")

try:
    with connect(
        host="127.0.0.1",
        port= 3306,
        #user=input("foo"),
        #password=getpass("Enter password: "),
        user = "root",
        password = "hejhej",
        database = "golf_eta"
    ) as connection:
        print(connection)
        query= "SELECT * FROM golf_course WHERE id = " + course + ";"
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                course_id = row[0]
                course_name = row[1]
                golf_club_id = row[2]
                slope_rating = row[3]
                course_Rating = row[4]
                coursePar = row[5]
                courseLength = row[6]
                print(row)
except Error as e:
    print(e)
    
    
try:
    with connect(
        host="127.0.0.1",
        port= 3306,
        #user=input("foo"),
        #password=getpass("Enter password: "),
        user = "root",
        password = "hejhej",
        database = "golf_eta"
    ) as connection:
        print(connection)
        query= "SELECT * FROM Users WHERE email = '" + user + "';"
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                print(row)
                golfer_id = row[0]
                golfer_name = row[1]
                teleNr = row[2]
                email = row[3]
                handicap = row[4]
                avg_speed = row[5]
                
except Error as e:
    print(e)    
    




#course handicap is the formula to determine expected strokes for a player given 
# courses of different levels of difficulty, noted by slope rating, course rating and total par

Course_Handicap =handicap *(slope_rating/113) + (float(course_Rating) - coursePar)

print("Course handicap for " + golfer_name + " at " + course_name + " is ", Course_Handicap)

# we make an assumption that it takes 40 seconds per shot as per the rules of golf issued by the R&A and USGA
#On average, a typical walking speed is about 1.4 meters per second for a man
#The total course length is usually about 6000 metres (+- 500 metres) given a par 72 course
#splitting the length up into metres per point of par gives us around 83.33 metres per par point.
#(this variable tries to take into account a player who shoots in a zig-zagging motion)

#Crude_eta = (courseLength/avg_speed) + ((Course_Handicap + coursePar) * 40) #in seconds

Crude_eta = (Course_Handicap+coursePar)*(83.33+ 40) #(travel time + tee time) * amount of shots
Crude_eta_Hrs = Crude_eta/3600 #in hours

print(" Initial Estimated time to finish the course is ", Crude_eta_Hrs, " hours")


#Write average speed as a relation to expectation given from handicap
