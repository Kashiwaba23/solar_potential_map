import streamlit as st
import googlemaps as gm
import requests
from PIL import Image
import gdown
from params import *



def watermark_remover(url):
    #Takes the GoogleMaps API Image and returns it without the watermark

    #Get the image
    im = Image.open(requests.get(url,stream=True).raw)

    #Return cropped image
    return im.crop((0,0,572,572))


def call_backend(lat,lng,zoom_level,size_h,size_v,API_key):
    #Calls the backend to get the solar potential

    #Get the image
    # url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom={zoom_level}&size={size_h}x{size_v}&maptype=satellite&key={API_key}"

    #Return the new image
    pass




def confirm_image(url):

    with st.spinner("Loading..."):
        # st.success("Modal loaded successfully!")

        st.write("Please confirm that the area is correct:")
        # Display the image hosted on a URL
        # f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom={zoom_level}&size=500x500&maptype=satellite&key={API_key}"
        # url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom={zoom_level}&size=500x500&maptype=satellite&key={API_key}"
        img = watermark_remover(url)
        st.image(img, caption="Area to be analyzed")
        # st.image(url, caption="Area")

        # Accept and Close buttons
        if st.button("Accept"):
            st.write("You clicked Accept!")


        st.write(" ")
        if st.button("Close"):
            st.write("You clicked Close!")


def main():

    st.set_page_config(layout="wide")

    # Set up the page title
    st.title("Solar Potential Map")

    margins_css = """
        <style>
            .main > div {
                padding-top: 2rem;
                padding-left: 5rem;
                padding-right: 5rem;
            }
        </style>
    """

    st.markdown(margins_css, unsafe_allow_html=True)

    API_key = MAPS_API_KEY

    # Initialize Google Maps API client
    gmaps = gm.Client(key=API_key)

    # Set up default location (Le Wagon Tokyo, Meguro)
    default_location = ( 35.633942, 139.708126)

    #ATTEMPTING TO MAKE INPUT HEADER BIGGER
    #color working, font not?
    tabs_font_css = """
        <style>
        div[class*="stTextInput"] label {
        font-size: 40px;
        color: black;
        }
        </style>
        """

    st.write(tabs_font_css, unsafe_allow_html=True)

    # Get user input for location
    with st.sidebar:
        location = st.text_input("Enter location:", 'Le Wagon Tokyo, Meguro')

    # Geocode location to get latitude and longitude
    geocode_result = gmaps.geocode(location)
    if geocode_result:
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        zipcode = geocode_result[0]['address_components'][0]['long_name']
        address = ""
        for component in geocode_result[0]['address_components']:
            address += component['long_name'] + " "
        address = address.strip()


    else:
        st.error("Error: Location not found.")
        st.stop()

    #     # setting up the header with its own row
    # r1_col1, _ = st.columns([6, 1])
    # with r1_col1:
    #     st.markdown(f"<p style='font-size: 20px;'><i>How much solar power can an area generate?</i></p>",
    #                 unsafe_allow_html=True)
    # # with r1_col3:
    # #     st.write('')

    # # main information line: includes map location
    # r2_col1, r2_col3, _ = st.columns([6, 4, 1])
    # with r2_col1:
    #     # info sidebar
    #     r2_col1.markdown('### Choose a location')
    #     text1, text2 = "Address", f'{address}'
    #     st.markdown(FACT_BACKGROUND.format(text1, img, 24, text2), unsafe_allow_html=True)
    #     st.markdown("""<div style="padding-top: 15px"></div>""", unsafe_allow_html=True)
    #     text1, text2 = "Latitude and Longitude", f"{lat}, {lng}"
    #     st.markdown(FACT_BACKGROUND.format(text1, img, 24, text2), unsafe_allow_html=True)

    #     # white space
    #     for _ in range(10):
    #         st.markdown("")


    # Set up zoom level
    # zoom_level = st.slider("Zoom level:", 1, 20, 19)
    zoom_level = 18.5

    # Get user input for radius
    # radius = st.slider("Radius (meters):", 10, 250, 62)
    radius = 62

    size_h= 572
    size_v= 594

    # Set parameters for the map
    # st.write(f"Map of {location}:")
    # st.write(f"Address: {address}")
    # st.write(f"Latitude: {lat}, Longitude: {lng}")
    # st.write(f"Zoom Level: {zoom_level}")

    # Build Html/JS code to visualize the map using Google Maps API:
    map_html = f"""
        <div id="map" style="width: 100%; height: 600px;"></div>
        <script>
            var lat = {lat};
            var lng = {lng};
            function initMap() {{
                var geocoder = new google.maps.Geocoder();
                var address = "{location}";
                geocoder.geocode({{ 'address': address }}, function(results, status) {{
                    if (status === 'OK') {{
                        var map = new google.maps.Map(document.getElementById('map'), {{
                            zoom: {zoom_level},
                            mapTypeId: 'satellite',
                            tilt: 0,
                            center: results[0].geometry.location
                        }});
                        // Enable the map type control
                        var mapTypeControlOptions = {{
                            style: google.maps.MapTypeControlStyle.DEFAULT,
                            position: google.maps.ControlPosition.TOP_RIGHT
                        }};
                        map.setOptions({{ mapTypeControl: true, mapTypeControlOptions: mapTypeControlOptions }});


                        // Draw square overlay
                        var center = results[0].geometry.location;
                        var north = center.lat() + ({radius} / 111000);
                        var south = center.lat() - ({radius} / 111000);
                        var east = center.lng() + ({radius} / (111000 * Math.cos(center.lat() * Math.PI / 180)));
                        var west = center.lng() - ({radius} / (111000 * Math.cos(center.lat() * Math.PI / 180)));
                        var squareCoords = [
                            {{ lat: north, lng: west }},
                            {{ lat: north, lng: east }},
                            {{ lat: south, lng: east }},
                            {{ lat: south, lng: west }},
                            {{ lat: north, lng: west }}
                        ];
                        var square = new google.maps.Polygon({{
                            paths: squareCoords,
                            strokeColor: '#FF0000',
                            strokeOpacity: 0.9,
                            strokeWeight: 2,
                            fillColor: '#FF0000',
                            fillOpacity: 0.20
                        }});
                        square.setMap(map);
                    }} else {{
                        alert('Geocode was not successful for the following reason: ' + status);
                    }}
                }});
            }}
            function updateLocation() {{
                var newUrl = window.location.href.split("?")[0] + "?location=" + lat + "," + lng;
                window.history.pushState('{{}}', '{{}}', newUrl);
                // Send message to parent with new location
                var newLocation = {{ lat: lat, lng: lng }};
                window.parent.postMessage({{ location: JSON.stringify(newLocation) }}, '*');
            }}


            setInterval(updateLocation, 10);
        </script>
        <script async defer src="https://maps.googleapis.com/maps/api/js?key={API_key}&callback=initMap"></script>
    """

    # Display the map:
    # with r2_col3:
    st.components.v1.html(map_html, width=650, height=400)


    # Temp: Button to open the link in a new tab
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom={zoom_level}&size={size_h}x{size_v}&maptype=satellite&key={API_key}"
    # st.link_button("Open Static Map", url)

    # if st.button("Calculate Solar Potential"):
    #     confirm_image(url)







if __name__ == "__main__":
    main()