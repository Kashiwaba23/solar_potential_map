import requests
from PIL import Image
import numpy as np
from io import BytesIO
from utils.params import MAPS_API_KEY
import maxflow

def get_gmaps_image(lat,lon,zoom,size="572x594"):
    #Returns Google Maps image with watermark removed
    #Create Google Maps API call
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom={zoom}&size={size}&maptype=satellite&key={MAPS_API_KEY}"

    #Gets the Google Maps API Image and returns it without the watermark
    im = Image.open(requests.get(url,stream=True).raw).convert("RGB")
    return im.crop((0,0,572,572))

def rooftop_area_calculator(zoom,lat, mask:np.array):
    #Given a zoom level and lattitude, returns area of a pixel
    #Based on the assumption earth's radius = 6378137m

    #Get pixel length
    pixel_length = 156543.03392 * np.cos(lat * np.pi / 180) / (2 ** zoom)
    pixel_area = pixel_length ** 2
    white_pixel_count = np.count_nonzero(mask)
    #Return pixel area
    return pixel_area * white_pixel_count

def solar_panel_energy_output(area, location="tokyo", setback=0.75, efficiency=0.20):
    #Returns annual solar panel output energy taking panel efficiency, setback, and average annual solar radiation into account
    #Annual Solar Radiation based on 5 year average values from https://www.data.jma.go.jp/obd/stats/etrn/view/monthly_s3_en.php?block_no=47662&view=11
    location = location.lower().strip()
    radiation_dict = {"tokyo":13.64,"osaka":14.72,"nagoya":14.64,"fukuoka":14.1,"sapporo":13.04}
    sunshine_dict = {"tokyo":2035.28,"osaka":2214.84,"nagoya":2227.46,"fukuoka":2051.74,"sapporo":1907.68}
    sunshine_hours = sunshine_dict[location]

    #Convert radiation from MJ/m2 to KWh/m2
    radiation = (radiation_dict[location] * 1000000) / 3600000

    return ((area * setback) * radiation * sunshine_hours) * efficiency

def co2_calculator(solar_panel_output, solar_carbon_intensity=0.041, coal_carbon_intensity=1.043, gas_carbon_intensity=0.440):
    #Returns dictionary estimate of how much kg of carbon is offset by a given power amount produced by solar panels for gas and coal
    #Carbon intensity taken from https://www.eia.gov/tools/faqs/faq.php?id=74&t=11
    carbon_dict = {"Coal Offset":solar_panel_output * (coal_carbon_intensity - solar_carbon_intensity),
                   "Gas Offset": solar_panel_output * (gas_carbon_intensity - solar_carbon_intensity)}

    return carbon_dict

def car_equivalent(carbon, car_co2_year = 4200):
    #Returns equivalent number of cars per years for co2 output

    return carbon / car_co2_year

def home_electricity(solar_kw, home_yearly = 12154):
    #Returns number of homes that could be supplied for a year

    return solar_kw / home_yearly

def smooth_image(input_array:np.array, smoothing_factor:int)-> np.array:
    """Takes a black and white mask generated by SAM and smoothes it,
    i.e. gets rid of some of the noise. Returns a smoothed image in numpy array
    format. Black and white input images, when values are
    between 0 and 1, must be multiplied by 255 for this function to work!"""
    # Important parameter
    # Higher values means making the image smoother
    smoothing = smoothing_factor

    # Create the graph.
    g = maxflow.Graph[int]()
    # Add the nodes. nodeids has the identifiers of the nodes in the grid.
    nodeids = g.add_grid_nodes(input_array.shape)
    # Add non-terminal edges with the same capacity.
    g.add_grid_edges(nodeids, smoothing)
    # Add the terminal edges. The image pixels are the capacities
    # of the edges from the source node. The inverted image pixels
    # are the capacities of the edges to the sink node.
    g.add_grid_tedges(nodeids, input_array, 255-input_array)

    # Find the maximum flow.
    g.maxflow()
    # Get the segments of the nodes in the grid.
    sgm = g.get_grid_segments(nodeids)

    # The labels should be 1 where sgm is False and 0 otherwise.
    img_denoised = np.logical_not(sgm).astype(np.uint8) * 255

    # return the denoised image
    return img_denoised
