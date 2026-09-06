# Generative AI use disclosure
#
# An initial version of this monitoring interface was generated with AI  assistance (Claude), based on specifications for the required data 
# fields, layout, and colour-coding logic. This AI-generated version was used as a reference during development of the final interface 
# below. All code has been reviewed, adapted, and is fully understood by the researcher. See Appendix F (Generative AI Statement) for full disclosure.

import tkinter as tk
import json
import os

# Setting up colours and fonts suitable for Linux
bg_colour = "#2b2b2b"  
box_colour = "#3b3b3b" 
main_text_colour = "#ffffff" 
header_text_colour = "#88ccff" 

font_title = ("Liberation Sans", -36, "bold") # The minus tells the program to make the font 36 points tall (not pixels)
font_subtitle = ("Liberation Sans", -24, "bold")
font_text = ("Liberation Sans", -20)

window = tk.Tk() # Creating main blank window on screen, main application on screen
window.title("Empathetic Fitting Room - Live Monitor")
window.geometry("1000x800") # Setting window size to 1000x800 pixels
window.configure(bg=bg_colour) # Painting background of main window grey


# Creating the Status frame
status_frame = tk.Frame(window, bg=bg_colour) # Placing frame in window; container within the window
status_frame.pack(pady=20, fill="both", expand=True) # Placing window on screen, adding vertical padding, extending and stretching to whole screen

heading_label = tk.Label(status_frame, text="Waiting for system...", font=font_title, bg=bg_colour, fg="#ffb84d") # Creating text to place inside frame
heading_label.pack(expand=True)


# Creating the Physiology frame
physio_frame = tk.Frame(window, bg=box_colour, bd=2, relief="ridge") # Ridge makes box stand from the background, border with set to 2 pixels
physio_frame.pack(pady=10, padx=30, fill="both", expand=True)

tk.Label(physio_frame, text="Physiology Data", font=font_subtitle, bg=box_colour, fg=header_text_colour).pack(pady=10)
bpm_label = tk.Label(physio_frame, text="Heart rate: -- bpm", font=font_text, bg=box_colour, fg=main_text_colour) # Creating placeholder text for body metrics
bpm_label.pack(expand=True) # Spacing all four lines evenly inside the box
rr_label = tk.Label(physio_frame, text="RR average: -- ms", font=font_text, bg=box_colour, fg=main_text_colour)
rr_label.pack(expand=True)
baseline_label = tk.Label(physio_frame, text="Baseline RR: -- ms", font=font_text, bg=box_colour, fg=main_text_colour)
baseline_label.pack(expand=True)
deviation_label = tk.Label(physio_frame, text="Deviation: -- ms", font=font_text, bg=box_colour, fg=main_text_colour)
deviation_label.pack(expand=True)


# Creating the Controller frame
pid_frame = tk.Frame(window, bg=box_colour, bd=2, relief="ridge")
pid_frame.pack(pady=10, padx=30, fill="both", expand=True)

tk.Label(pid_frame, text="PID Controller", font=font_subtitle, bg=box_colour, fg=header_text_colour).pack(pady=10) 
pid_label = tk.Label(pid_frame, text="P: -- | I: -- | D: --", font=font_text, bg=box_colour, fg=main_text_colour) # Placeholders for PID values
pid_label.pack(expand=True)
score_label = tk.Label(pid_frame, text="Reaction score: --", font=font_title, bg=box_colour, fg=main_text_colour)
score_label.pack(pady=10)


# Creating the progress bar
meter_canvas = tk.Canvas(pid_frame, width=400, height=25, bg="#1a1a1a", highlightthickness=0) # Creating dark grey canvas for progress bar, placing in PID frame, setting size and background colour and removing border around bar
meter_canvas.pack(pady=10)
meter_bar = meter_canvas.create_rectangle(0, 0, 200, 25, fill="#ffb84d") # Drawing progress bar inside the canvas; 0, 0 implies to start drawing at top left of canva, until 200 pixels (mid-canva), 25 pixels down


# Creating the Output frame
output_frame = tk.Frame(window, bg=box_colour, bd=2, relief="ridge")
output_frame.pack(pady=10, padx=30, fill="both", expand=True)

tk.Label(output_frame, text="Environment Output", font=font_subtitle, bg=box_colour, fg=header_text_colour).pack(pady=10)
brightness_label = tk.Label(output_frame, text="Brightness: --", font=font_text, bg=box_colour, fg=main_text_colour)
brightness_label.pack(expand=True)

colour_temp_label = tk.Label(output_frame, text="Colour Temp: -- mireds", font=font_text, bg=box_colour, fg=main_text_colour)
colour_temp_label.pack(expand=True)

audio_stems_frame = tk.Frame(output_frame, bg=box_colour) # Creating a smaller box inside the output frame just to hold the audio labels together
audio_stems_frame.pack(expand=True, pady=10)

drone_label = tk.Label(audio_stems_frame, text="Drone: --%", font=font_text, bg=box_colour, fg=main_text_colour)
drone_label.pack(side="left", padx=15) # Using side="left" places label to the left edge of the frame, and other labels next to each other horizontally

chords_label = tk.Label(audio_stems_frame, text="Chords: --%", font=font_text, bg=box_colour, fg=main_text_colour)
chords_label.pack(side="left", padx=15)

rhythm_label = tk.Label(audio_stems_frame, text="Rhythm: --%", font=font_text, bg=box_colour, fg=main_text_colour)
rhythm_label.pack(side="left", padx=15)

melody_label = tk.Label(audio_stems_frame, text="Melody: --%", font=font_text, bg=box_colour, fg=main_text_colour)
melody_label.pack(side="left", padx=15)


# Handing number to these functions to retrieve colour
def pick_color(score):
    if score < -33: 
        return "#ff5555" # Red (Stressed)
    elif score < 33: 
        return "#ffb84d" # Orange (Transition)
    else: 
        return "#55ff55" # Green (Calm)

def get_audio_color(volume):
    if volume == 0: 
        return "#ff5555" # Red if it is off
    else: 
        return "#55ff55" # Green if it is actively playing

def get_light_color(brightness): # Based on 60-254 mapping range
    if brightness < 120: 
        return "#ff5555" # Red (Dim/Stressed)
    elif brightness < 200: 
        return "#ffb84d" # Orange 
    else: 
        return "#55ff55" # Green (Bright/Calm)

def get_temp_color(temp): # Based on 500-153 mireds mapping range
    if temp > 380: 
        return "#ff5555" # Red (Warm/Stressed)
    elif temp > 250: 
        return "#ffb84d" # Orange (Transition)
    else: 
        return "#55ff55" # Green (Cool/Calm)


# Refresh loop
def refresh_screen():
    if not os.path.exists("monitor_data.json"): # Checks if JSON file exists in storage
        window.after(500, refresh_screen) # If not, waits 0.5s and then re-runs refresh_screen until I close the program/file appears
        return 

    try:
        with open("monitor_data.json", "r") as f: # Opens file in read mode
            data = json.load(f) 
    except: # If anything crashes when opening/reading the file
        window.after(500, refresh_screen) # If anythng goes wrong with opening/reading the file, it waits 0.5s and then tries again
        return

    is_calibrated = data["calibrated"] 
    if is_calibrated == True: # Changing text/colour depending on whether calibration is completed; .config overwrites placeholders
        heading_label.config(text="Session Running", fg="#55ff55") 
    else:
        heading_label.config(text="Calibrating...", fg="#ffb84d") 

    bpm = round(data["bpm"]) 
    rr = round(data["rr_avg"])
    baseline = round(data["baseline_rr"])
    deviation = round(data["deviation"])
    p_val = round(data["p_value"], 2)
    i_val = round(data["i_value"], 2)
    d_val = round(data["d_value"], 2)
    score = round(data["reaction_score"], 1)

    bpm_label.config(text=f"Heart rate: {bpm} bpm")
    rr_label.config(text=f"RR average: {rr} ms")
    baseline_label.config(text=f"Baseline RR: {baseline} ms")
    deviation_label.config(text=f"Deviation: {deviation} ms")
    pid_label.config(text=f"P: {p_val} | I: {i_val} | D: {d_val}")
    
    score_color = pick_color(score)
    score_label.config(text=f"Reaction score: {score}", fg=score_color)
    
    # Updating the stress bar
    bar_width = int(((score + 100) / 200) * 400) # Converting PID score into pixel width
    bar_width = max(0, min(400, bar_width)) # Ensure bar never draws outside the box
    meter_canvas.coords(meter_bar, 0, 0, bar_width, 25) # Updates bar (meter_bar) to new width
    meter_canvas.itemconfig(meter_bar, fill=score_color) # Updates bar colour; .itemconfig lets you update properties of an item without touching size/position

    brightness_val = data['brightness'] # Updating brigthness text and colour
    brightness_label.config(text=f"Brightness: {brightness_val} / 254", fg=get_light_color(brightness_val))

    temp_val = data['colour_temp'] 
    colour_temp_label.config(text=f"Colour Temp: {temp_val} mireds", fg=get_temp_color(temp_val))

    # Updating audio texts and colours
    drone = int(data["vol_drone"] * 100)  
    chords = int(data["vol_chords"] * 100)
    rhythm = int(data["vol_rhythm"] * 100)
    melody = int(data["vol_melody"] * 100) 
    
    drone_label.config(text=f"Drone: {drone}%", fg=get_audio_color(drone))
    chords_label.config(text=f"Chords: {chords}%", fg=get_audio_color(chords))
    rhythm_label.config(text=f"Rhythm: {rhythm}%", fg=get_audio_color(rhythm))
    melody_label.config(text=f"Melody: {melody}%", fg=get_audio_color(melody))

    window.after(500, refresh_screen) # You can't use a standard while True loop in Tkinter: this waits 0.5s then starts the loop again


window.after(500, refresh_screen) # Starts the loop for the first time: after window opens it sets a timer for 0.5s and then it starts
window.mainloop() # Starts Tkinter GUI