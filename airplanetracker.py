import time
import csv
import folium
from opensky_api import OpenSkyApi

# --- CONFIGURATION ---
USERNAME = "username"  # Replace with your OpenSky credentials
PASSWORD = "password"

# --- FETCH AIRPLANE DATA ---
def fetch_airplanes(api, callsign_prefix=None):
    try:
        states = api.get_states()
        aircraft_list = []
        for s in states.states:
            callsign = s.callsign.strip() if s.callsign else "N/A"
            if callsign_prefix and not callsign.startswith(callsign_prefix):
                continue
            aircraft_list.append({
                'icao24': s.icao24,
                'callsign': callsign,
                'latitude': s.latitude,
                'longitude': s.longitude,
                'altitude': s.geo_altitude,
                'velocity': s.velocity,
                'on_ground': s.on_ground
            })
        return aircraft_list
    except Exception as e:
        print("Failed to fetch data:", e)
        return []

# --- EXPORT TO CSV ---
def export_to_csv(aircraft_list, filename='airplanes.csv'):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ICAO24', 'Callsign', 'Latitude', 'Longitude', 'Altitude', 'Velocity', 'On Ground'])
        for ac in aircraft_list:
            writer.writerow([ac['icao24'], ac['callsign'], ac['latitude'], ac['longitude'], ac['altitude'], ac['velocity'], ac['on_ground']])
    print(f"Exported {len(aircraft_list)} airplanes to {filename}")

# --- PLOT ON MAP ---
def plot_on_map(aircraft_list, filename='airplanes_map.html'):
    m = folium.Map(location=[20, 0], zoom_start=2)
    for ac in aircraft_list:
        if ac['latitude'] and ac['longitude']:
            folium.Marker(
                [ac['latitude'], ac['longitude']],
                popup=f"{ac['callsign']} (ICAO24: {ac['icao24']})"
            ).add_to(m)
    m.save(filename)
    print(f"Map saved to {filename}")

# --- MAIN SCRIPT ---
def main():
    api = OpenSkyApi(USERNAME, PASSWORD)

    # Optional: Filter by callsign prefix (e.g., airline code)
    callsign_prefix = input("Enter callsign prefix to filter (or press Enter for all): ").strip().upper() or None

    # Fetch and display airplanes
    aircraft_list = fetch_airplanes(api, callsign_prefix)
    if not aircraft_list:
        print("No airplanes found.")
        return

    print("\nAvailable airplanes:")
    for idx, ac in enumerate(aircraft_list):
        print(f"{idx}: {ac['callsign']} | ICAO24: {ac['icao24']} | Lat: {ac['latitude']} | Lon: {ac['longitude']} | Alt: {ac['altitude']} | On Ground: {ac['on_ground']}")

    # Export to CSV
    export_to_csv(aircraft_list)

    # Plot on map
    plot_on_map(aircraft_list)

    # Select airplane to track
    while True:
        try:
            choice = int(input("\nEnter the number of the airplane to track: "))
            if 0 <= choice < len(aircraft_list):
                selected = aircraft_list[choice]
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")

    print(f"\nTracking {selected['callsign']} (ICAO24: {selected['icao24']}) in real time. Press Ctrl+C to stop.\n")

    # Live tracking loop
    try:
        while True:
            updated_list = fetch_airplanes(api)
            tracked = next((ac for ac in updated_list if ac['icao24'] == selected['icao24']), None)
            if tracked:
                print(f"Lat: {tracked['latitude']}, Lon: {tracked['longitude']}, Alt: {tracked['altitude']}, Vel: {tracked['velocity']}, On Ground: {tracked['on_ground']}")
            else:
                print("Airplane not found in current data.")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nTracking stopped.")

if __name__ == "__main__":
    main()
