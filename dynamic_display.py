import geocoder
import overpy
import folium
from geopy.distance import geodesic
from flask import Flask, render_template_string

app=Flask(__name__)

@app.route('/')
def map_view():
    g=geocoder.ip('me')
    user_lat, user_lon=g.latlng
    bbox=(user_lat - 0.02, user_lon - 0.02, user_lat + 0.02, user_lon + 0.02)
    api=overpy.Overpass()
    query=f"""(
      node["amenity"="school"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      node["amenity"="hospital"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      node["highway"="dangerous_intersection"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    );
    out center;
    """
    result=api.query(query)
    in_school_zone=False
    in_hospital_zone=False
    in_accident_zone=False
    zone_radius=500
    mymap=folium.Map(location=[user_lat, user_lon], zoom_start=14)
    folium.Marker(
        location=[user_lat, user_lon],
        popup=f"User Location",
        icon=folium.Icon(color="green", icon="user", prefix="fa")
    ).add_to(mymap)
    for node in result.nodes:
        location=(node.lat, node.lon)
        distance_to_user=geodesic((user_lat, user_lon), location).meters
        if 'amenity' in node.tags and node.tags['amenity'] == 'school':
            folium.Marker(
                location=[node.lat, node.lon],
                popup="School",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(mymap)
            if distance_to_user <= zone_radius:
                in_school_zone=True
        elif 'amenity' in node.tags and node.tags['amenity'] == 'hospital':
            folium.Marker(
                location=[node.lat, node.lon],
                popup="Hospital",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(mymap)
            if distance_to_user <= zone_radius:
                in_hospital_zone=True
        elif 'highway' in node.tags and node.tags['highway'] == 'dangerous_intersection':
            folium.Marker(
                location=[node.lat, node.lon],
                popup="Accident-Prone Area",
                icon=folium.Icon(color="orange", icon="exclamation-sign")
            ).add_to(mymap)
            if distance_to_user <= zone_radius:
                in_accident_zone=True
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
    if in_school_zone and in_hospital_zone and in_accident_zone:
        zone_status='000'
    elif in_school_zone and not in_hospital_zone and not in_accident_zone:
        zone_status='001'
    elif in_hospital_zone and not in_school_zone and not in_accident_zone:
        zone_status='010'
    elif in_accident_zone and not in_school_zone and not in_hospital_zone:
        zone_status='011'
    elif in_school_zone and in_hospital_zone and not in_accident_zone:
        zone_status='100'
    elif in_school_zone and in_accident_zone and not in_hospital_zone:
        zone_status='101'
    elif in_hospital_zone and in_accident_zone and not in_school_zone:
        zone_status='110'
    else:
        zone_status='111'

    map_html=mymap._repr_html_()

    html_template=f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Live Map View</title>
    </head>
    <body>
        <h1>User Location: {zone_status}</h1>
        {map_html}
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == "__main__":
    app.run(debug=True)