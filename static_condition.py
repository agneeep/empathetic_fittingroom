# This file is run in the evaluation, when participants experience the static control session
# In the static condition, light and audio are fixed; the Polar sensor is connected only to log heartbeat data for comparison with the adaptive condition

import asyncio
import pygame
import csv
import time
from bleak import BleakClient, BleakScanner
from bleakheart import HeartRate
from HueBLE import HueBleLight

sensor_address = "D4:8A:91:AC:B1:E9"
light_address = "DE:0F:02:B0:58:1D"

static_brightness = 254
static_colour_temp = 153

vol_drone = 1.0
vol_chords = 0.8
vol_rhythm = 0.8
vol_melody = 0.9

log_file = "session_log_static.csv" # Separate file so it does not overwrite adaptive log


def start_log():
    """Creates a new CSV log file at the start of each session."""
    with open(log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time_seconds", "rr_interval", "bpm"])
    print("Session log started.\n") # Saved in session_log_static.csv


def write_log_row(time_s, rr_interval):
    """Saves one heartbeat to the CSV."""
    bpm = 60000 / rr_interval if rr_interval > 0 else 0 # Dividing 1 min (60,000 ms) by length of each RR interval to calculate bpm
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([round(time_s, 2), round(rr_interval, 1), round(bpm, 1)])


def check_heartbeat_is_realistic(rr_value):
    """Filters out noise, same as adaptive condition."""
    if rr_value < 300:
        return False
    if rr_value > 1500:
        return False
    return True


async def log_heartbeats(queue, session_start_time):
    """Reads heartbeats from the sensor queue and logs them to CSV, not changing the environment."""
    beat_count = 0

    while True:
        heartbeat_data = await queue.get() # Waiting for new data and getting next heartbeat from sensor
        rr_interval = heartbeat_data[2][1] # Obtaining RR interval from heartbeat data

        if check_heartbeat_is_realistic(rr_interval): # Only saving data if it is a realistic heartbeat
        
            elapsed = time.monotonic() - session_start_time # putting timestamp on specific heartbeat
            write_log_row(elapsed, rr_interval)

            beat_count += 1
            bpm = 60000 / rr_interval
            print(f"  Beat {beat_count}: RR {round(rr_interval)}ms ({round(bpm)} bpm): logged")

        queue.task_done() # Telling queue we are finished with current heartbeat


async def run_static_condition():

    pygame.mixer.init() # Initialising music
    print("Loading audio files...")
    
    drone = pygame.mixer.Sound("stem_1_drone.wav")
    chords = pygame.mixer.Sound("chords_24s.wav")
    rhythm = pygame.mixer.Sound("rhythm_24s.wav")
    melody = pygame.mixer.Sound("stem_4_melody.wav")

    drone.play(-1).set_volume(vol_drone) # Playing music on loop and setting volumes
    chords.play(-1).set_volume(vol_chords)
    rhythm.play(-1).set_volume(vol_rhythm)
    melody.play(-1).set_volume(vol_melody)
    print("Music is playing.")

    print("Connecting to the Hue lights...")
    light_device = await BleakScanner.find_device_by_address(light_address) # Scanning for lights
    hue_light = HueBleLight(light_device) # Wrapping device in a HueBleLight object
    
    await hue_light.set_power(True) # Turning light on if not on already
    await hue_light.set_colour_temp(static_colour_temp)
    await hue_light.set_brightness(static_brightness)
    print("Light is set to fixed mode.")

    print("Connecting to Polar sensor...") 
    async with BleakClient(sensor_address) as client: # Establishing connection with sensor, with ensures sensor disconnects once program terminates
        print("Sensor connected.")
        
        heartbeat_queue = asyncio.Queue() # Creates queue for heartbeats until program is ready to save them
        start_log()
        start_time = time.monotonic() 

        monitor = HeartRate(
            client=client, 
            queue=heartbeat_queue, 
            unpack=True
        ) # Configuring heart rate monitor, linking Bluetooth connection (client) to queue
        
        await monitor.start_notify() # Telling sensor to start sending data to computer

        print("Static condition running.")
        
        asyncio.create_task(log_heartbeats(heartbeat_queue, start_time)) # Starts saving the heartbeats in the background; program can move to other things, e.g. listening for Ctrl+C

        # Keeping program alive until Ctrl+C is pressed
        try:
            while True:
                await asyncio.sleep(1) # Keeping the system alive: sleep for 1 sec and then go again
        except:
            pygame.mixer.stop() # When the user stops the program, it turns off the music
            print("Done! Data saved to file.")


if __name__ == "__main__":
    asyncio.run(run_static_condition())