import time
import SimCoordFeeder
import threading


SimCoordFeeder.coordSubmission(200,200)  # Simulate player moving to a coordinate
time.sleep(2)  # Simulate a delay for the player to get ready
SimCoordFeeder.coordSubmission(100,300)  # Simulate player moving to a coordinate
time.sleep(3)  # Simulate a delay for the player to get ready
SimCoordFeeder.coordSubmission(100,50)  # Simulate player moving to a coordinate
time.sleep(4)  # Simulate a delay for the player to get ready
SimCoordFeeder.coordSubmission(100, 2)  # Simulate player moving to a coordinate