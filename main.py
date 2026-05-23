import tkinter as tk
from tkinter import messagebox
import tkintermapview
import requests


class RoutePlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Route Planner")
        self.root.geometry("800x600")

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(input_frame, text="Start Position:").grid(row=0, column=0, padx=5, pady=5)
        self.start_entry = tk.Entry(input_frame, width=30)
        self.start_entry.grid(row=0, column=1, padx=5, pady=5)
        self.start_entry.insert(0, "UASLP Ingenieria")

        tk.Label(input_frame, text="End Position:").grid(row=0, column=2, padx=5, pady=5)
        self.end_entry = tk.Entry(input_frame, width=30)
        self.end_entry.grid(row=0, column=3, padx=5, pady=5)
        self.end_entry.insert(0, "Cineteca Alameda")

        search_button = tk.Button(input_frame, text="Find Route", command=self.calculate_route, bg="#4CAF50",
                                  fg="white")
        search_button.grid(row=0, column=4, padx=10)

        self.map_widget = tkintermapview.TkinterMapView(self.root, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)

        self.map_widget.set_position(22.1831, -100.9383)
        self.map_widget.set_zoom(13)

        self.current_path = None
        self.markers = []

    def get_coordinates(self, address):
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': address,
            'format': 'json',
            'limit': 1
        }

        headers = {
            'User-Agent': 'TiaraRoutePlannerApp/1.0'
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            data = response.json()

            if data:
                return float(data[0]['lat']), float(data[0]['lon'])

        except Exception as e:
            print(f"Geocoding error: {e}")

        return None

    def calculate_route(self):
        start_address = self.start_entry.get()
        end_address = self.end_entry.get()

        if not start_address or not end_address:
            messagebox.showwarning("Input Error", "Please enter both a start and end position.")
            return

        start_coords = self.get_coordinates(start_address)
        end_coords = self.get_coordinates(end_address)

        if not start_coords:
            messagebox.showerror("Error", f"Could not find coordinates for: {start_address}")
            return
        if not end_coords:
            messagebox.showerror("Error", f"Could not find coordinates for: {end_address}")
            return

        if self.current_path:
            self.current_path.delete()
        for marker in self.markers:
            marker.delete()
        self.markers.clear()

        self.markers.append(self.map_widget.set_marker(start_coords[0], start_coords[1], text="Start"))
        self.markers.append(self.map_widget.set_marker(end_coords[0], end_coords[1], text="End"))


        url = f"http://router.project-osrm.org/route/v1/driving/{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}?overview=full&geometries=geojson"

        try:
            response = requests.get(url)
            data = response.json()

            if data["code"] != "Ok":
                messagebox.showerror("API Error", "Could not calculate a route between these locations.")
                return

            route_geometry = data["routes"][0]["geometry"]["coordinates"]

            path_coords = [(lat, lon) for lon, lat in route_geometry]

            self.current_path = self.map_widget.set_path(path_coords, color="#2196F3", width=4)

            self.map_widget.fit_bounding_box(
                (min(c[0] for c in path_coords), min(c[1] for c in path_coords)),
                (max(c[0] for c in path_coords), max(c[1] for c in path_coords))
            )

        except Exception as e:
            messagebox.showerror("Network Error", f"Failed to connect to the routing API.\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RoutePlannerApp(root)
    root.mainloop()