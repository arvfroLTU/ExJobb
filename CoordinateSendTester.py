import time
import SimCoordFeeder
import threading

SimCoordFeeder.start_observer_threads()
SimCoordFeeder.start_active_thread(100,200)
time.sleep(5)  # Simulate a delay for the player to get ready
SimCoordFeeder.start_active_thread(200,200)  # Simulate player moving to a coordinate
time.sleep(5)  # Simulate a delay for the player to get ready
SimCoordFeeder.start_active_thread(100,300)  # Simulate player moving to a coordinate
time.sleep(5)  # Simulate a delay for the player to get ready
SimCoordFeeder.start_active_thread(100,50)  # Simulate player moving to a coordinate
time.sleep(5)  # Simulate a delay for the player to get ready
SimCoordFeeder.coordSubmission(100, 2)  # Simulate player moving to a coordinate