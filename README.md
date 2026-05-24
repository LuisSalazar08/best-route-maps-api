# Python Desktop Route Planner

A lightweight, interactive desktop application built with Python and Tkinter that calculates and visualizes driving routes. The app operates completely independent of commercial mapping services (like Google Maps) by integrating open-source APIs.

## Features
* **Interactive Map UI:** Built with `tkintermapview` for a smooth, scrollable, and zoomable map interface.
* **Free Geocoding:** Converts human-readable addresses into latitude/longitude coordinates using the OpenStreetMap Nominatim API.
* **Dynamic Routing:** Calculates the driving path between two points using the OSRM (Open Source Routing Machine) API.
* **No API Keys Required:** Runs entirely on free, community-driven data services.

## Tech Stack
* Python 3.x
* `tkinter` (Standard GUI library)
* `tkintermapview` (Map widget)
* `requests` (HTTP requests for API calls)

## Installation

1. Clone the repository:
```bash
   git clone [https://github.com/yourusername/python-route-planner.git](https://github.com/yourusername/python-route-planner.git)
   cd python-route-planner
