
---

# Smart-Vehicle-Automation

The current status of this project is that it dynamically detects and visualizes school zones,hospital zones,and accident-prone areas using free map data from OpenStreetMap (via Overpass API). It leverages Python libraries to fetch real-time location data,query map data,and create an interactive map that is centered around the user’s location.

## Features
- Detects school zones,hospital zones,and accident-prone areas based on OpenStreetMap data.
- Visualizes zones with dynamic markers and radius circles on an interactive map.
- Automatically centers the map on the user's current location based on IP.
- Provides a customizable bounding box for the map query area.
- Generates an interactive HTML map that can be viewed in any browser.

## Requirements

The project requires Python 3.x and the following Python libraries:

- **folium**: For generating interactive maps
- **overpy**: For querying OpenStreetMap data using Overpass API
- **geocoder**: To get the user's current location via IP
- **geopy**: (Optional) For calculating distances if needed

Install the required libraries using the following command:
```bash
pip install folium overpy geocoder geopy
```

## How it Works

### 1. Get User Location:
The user's location is fetched using `geocoder` by querying the public IP address of the user. The latitude and longitude coordinates are used to center the map and create a bounding box around the user's location.

```python
import geocoder
g=geocoder.ip('me')
user_lat,user_lon=g.latlng
```

### 2. Query OpenStreetMap Data:
Using the **Overpass API**,we query OpenStreetMap data for amenities such as schools,hospitals,and accident-prone zones within the specified bounding box around the user's location.

```python
import overpy
api=overpy.Overpass()
query=f"""(
  node["amenity"="school"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  node["amenity"="hospital"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  node["highway"="dangerous_intersection"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
);
out center;
"""
result=api.query(query)
```

### 3. Create Interactive Map:
Using **folium**,an interactive map is generated centered on the user’s location. Markers are added for schools,hospitals,and accident-prone areas,with different colors and icons for each.

```python
import folium

mymap=folium.Map(location=[user_lat,user_lon],zoom_start=14)
folium.Marker(
    location=[lat,lon],
    popup="School Zone",
    icon=folium.Icon(color="blue",icon="graduation-cap",prefix="fa")
).add_to(mymap)
mymap.save("zones_map.html")
```

### 4. Visualizing Zones:
Markers with popup labels and circle overlays are added to highlight the areas. Each zone (school,hospital,etc.) can be visualized with a color-coded circle (e.g.,500-meter radius for school and hospital zones).

## Usage
1. Clone the repository and install the required Python libraries.
2. Run the Python script to fetch data from OpenStreetMap based on your location.
3. Open the generated `zones_map.html` in a browser to view the interactive map.

## Example Output
The map will show markers for:
- **Blue** markers and zones for schools.
- **Red** markers and zones for hospitals.
- **Orange** markers for accident-prone areas.

Each zone will have a corresponding circle (radius of 500 meters) to indicate its area of influence.

## Customization
- **Bounding Box**: You can customize the bounding box size to adjust the area of data retrieval around the user's location.
- **Markers and Colors**: You can modify the colors,icons,and popup information for different zone types.

## Future Enhancements
- Incorporate real-time accident data or dangerous intersections from traffic databases.
- Add additional map layers to show road conditions or traffic.
- Integrate a live data feed for continuous updates on school,hospital,or accident zones.

## Credits
- **OpenStreetMap** and the **Overpass API** for providing geographical data.
- **Folium** for creating interactive maps.
- **Geocoder** for fetching the user's location.
---
