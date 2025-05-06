Airplane Tracking Script – Help & Usage Guide
Created by Patrick Elliott

Overview
This Python script allows you to:

Fetch real-time airplane data from the OpenSky Network

Filter airplanes by callsign prefix (e.g., airline code)

View a detailed, numbered list of currently tracked airplanes

Export airplane data to CSV

Visualize airplane positions on a world map (HTML)

Select an airplane to track in real time (position, altitude, velocity, etc.)

Requirements
Python 3.7+

OpenSky Network account

The following Python packages:

python_opensky or pyopensky

folium

Installation
Install required packages using pip:

bash
pip install python_opensky folium
If you prefer pyopensky, use:

bash
pip install pyopensky folium
Configuration
Edit the script
Replace the following lines with your OpenSky Network username and password:

python
USERNAME = "your_opensky_username"
PASSWORD = "your_opensky_password"
Usage
Run the script:

bash
python airplane_tracker.py
Script Flow
Filter by Callsign Prefix:

You can enter a prefix (e.g., "UAL" for United Airlines) to filter the list.

Press Enter to list all airplanes.

View Airplane List:

The script displays a numbered list of airplanes with details (callsign, ICAO24, position, altitude, etc.).

CSV Export:

The list is saved as airplanes.csv in the script directory.

Map Visualization:

The script creates an interactive map (airplanes_map.html) showing airplane positions.

Select an Airplane to Track:

Enter the number corresponding to the airplane you want to track.

Live Tracking:

The script prints the selected airplane’s position, altitude, velocity, and ground status every 10 seconds.

Press Ctrl+C to stop tracking.

Troubleshooting
No module named opensky_api error:
Install python_opensky or pyopensky as shown above.

No airplanes found:
Try removing the callsign prefix filter or check your network connection.

Map not displaying:
Open airplanes_map.html in a web browser.

API errors:
Check your OpenSky credentials and/or try again later.

Customization
Change update interval:
Edit the time.sleep(10) line to set a different refresh rate.

Change output filenames:
Modify the export_to_csv() and plot_on_map() function calls.

Credits
OpenSky Network

Folium

For further help or feature requests, contact the script author or refer to the OpenSky API documentation.

Let me know if you need this in another format or want to include command-line argument support!
