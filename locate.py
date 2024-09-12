import folium
import overpy
import geocoder
from geopy.distance import geodesic
g=geocoder.ip('me')

user_lat,user_lon=g.latlng  
bbox=(user_lat - 0.02,user_lon - 0.02,user_lat+0.02,user_lon+0.02)
api=overpy.Overpass()

query=f"""(
  node["amenity"="school"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  way["amenity"="school"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  node["amenity"="hospital"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  way["amenity"="hospital"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  node["highway"="dangerous_intersection"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  way["highway"="dangerous_intersection"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
);
out center;
"""

result=api.query(query)
mymap=folium.Map(location=[user_lat,user_lon],zoom_start=14)
school_zones=[]
hospital_zones=[]
accident_zones=[]
for node in result.nodes:
    if 'amenity' in node.tags:
        if node.tags['amenity'] == 'school':
            school_zones.append((node.lat,node.lon))
            folium.Marker(
                location=[node.lat,node.lon],
                popup="School Zone",
                icon=folium.Icon(color="blue",icon="graduation-cap",prefix="fa"),
            ).add_to(mymap)
        elif node.tags['amenity'] == 'hospital':
            hospital_zones.append((node.lat,node.lon))
            folium.Marker(
                location=[node.lat,node.lon],
                popup="Hospital Zone",
                icon=folium.Icon(color="red",icon="plus-square",prefix="fa"),
            ).add_to(mymap)
for way in result.ways:
    if 'amenity' in way.tags:
        if way.tags['amenity'] == 'school':
            school_zones.append((way.center_lat,way.center_lon))
            folium.Marker(
                location=[way.center_lat,way.center_lon],
                popup="School Zone",
                icon=folium.Icon(color="blue",icon="graduation-cap",prefix="fa"),
            ).add_to(mymap)
        elif way.tags['amenity'] == 'hospital':
            hospital_zones.append((way.center_lat,way.center_lon))
            folium.Marker(
                location=[way.center_lat,way.center_lon],
                popup="Hospital Zone",
                icon=folium.Icon(color="red",icon="plus-square",prefix="fa"),
            ).add_to(mymap)
accident_location=(user_lat+0.01,user_lon+0.01)  
folium.Marker(
    location=accident_location,
    popup="Accident Prone Area",
    icon=folium.Icon(color="orange",icon="warning",prefix="fa"),
).add_to(mymap)

for school in school_zones:
    folium.Circle(
        location=school,
        radius=500,
        color="blue",
        fill=True,
        fill_opacity=0.3,
        popup="School Zone (500m)",
    ).add_to(mymap)

for hospital in hospital_zones:
    folium.Circle(
        location=hospital,
        radius=500,
        color="red",
        fill=True,
        fill_opacity=0.3,
        popup="Hospital Zone (500m)",
    ).add_to(mymap)
mymap.save("zones_map.html")
print(f"Map saved as 'zones_map.html'. Centered around user's location: {user_lat},{user_lon}")
