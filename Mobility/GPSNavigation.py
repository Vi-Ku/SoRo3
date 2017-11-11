import math
# things for GPS comunication
# make sure to run pip install sbp
from sbp.client.drivers.network_drivers import TCPDriver
from sbp.client import Handler, Framer
from sbp.navigation import SBP_MSG_POS_LLH, MsgPosLLH

""" This code provides the rover with autonomous GPS navigation capabilites.
    There will be two ways of inputting the destination coordinates:
        - User input from keyboard (Prone to user error, e.g. Being of by +/-.0004 longitude would result
            in an approximate positional error of +/-30 meters.
        - Read Lat/Lon decimal values from a file. (Will remove human error (double/triple check values before running the code)
    This code then takes the Lat/Lon values and uses the Haversine formula to calculate distance to destination and also calculates
        Theta, which is the closest angle to the destination, offset from North. (e.g. +/-180 degrees from North)"""
#TODO: move some variables to global variables to improve readability

def main():
    args = getArgs()
    driver = TCPDriver('192.168.1.222', '55555')
    #Location of rover, from the top.
    #driver.read is the literal output from the tcp driver
    #framer turns bytes into SBP messages (swift binary protocol)
    #handler is an itterable to read the messages
    with Handler(Framer(driver.read, None, verbose=True)) as source:
        #reeds all the messages in a loop as they are recieved
        for msg, metadata in source.filter(SBP_MSG_POS_LLH):
            #Shouldnt We need an elivation?.. that's msg.height
            #int of acuracy is [h/v]_acuracy also there is n_sats
            roverLat = math.radians(msg.lat)
            roverLong = math.radians(msg.lon)

            #Get longitude, latitude, (not yet...height, and number of satellites) - need it in degrees
            longitude = math.radians(args.longitude[0])
            latitude = math.radians(args.latitude[0])

            distance = getDistance(longitude, latitude, roverLat, roverLong)
            theta = getBearing(longitude, latitude, roverLat, roverLong)

            #TODO: turn(bearing) # somthing like: if math.abs(bearing) > tolerence then turn else drive(distance)
            #TODO: drive(distance)

            #Need to fix this to output the proper value of theta
            print("Bearing: ", 360 + math.degrees(theta), ", Distance: ", d)

            # If we're within 2 meters of the destination
            if (distance <= 2):
                print("Distance is within 2 meters of the destination.")
                #TODO: put a break to say we are finnished
def getArgs():
    """
    Get and parse arguments.
    """
    import argparse
    parser = argparse.ArgumentParser(
        description="Swift Navigation SBP Example.")
    parser.add_argument(
        "--longitude",
        default=0,
        nargs=1,
        help="specify the longitude in decimal.")
    parser.add_argument(
        "--latitude",
        default=0,
        nargs=1,
        help="specify the latitude in decimal.")
    return parser.parse_args()

def getDistance(longitude, latitude, roverLat, roverLong):
    # Radius of the Earth
    RADIUS_OF_EARTH = 6371 * (1000)
    # Haversine Formula: a = sin((lat2-lat1)/2) * sin((lat2-lat1)/2) + cos(lat1) * cos(lat2) * sin((lon2-lon1)/2) * sin((lon2-lon1)/2)
    # Calulate change in Latitude
    deltaLat = latitude - roverLat
    # Calculate change in Longitude
    deltaLon = longitude - roverLong
    # Haversine formula for distance
    a = math.sin(deltaLat/2) * math.sin(deltaLat/2) + math.cos(roverLat) * math.cos(latitude) * math.sin(deltaLon/2) * math.sin(deltaLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = RADIUS_OF_EARTH * c
    return d

def getBearing(longitude, latitude, roverLat, roverLong):
    # Calulate change in Latitude
    deltaLat = latitude - roverLat
    # Calculate change in Longitude
    deltaLon = longitude - roverLong
    # Bearing, represented as nearest offset from North. (+/-180 degrees from North)
    theta = math.atan2(math.sin(deltaLon) * math.cos(latitude), math.cos(roverLat) * math.sin(latitude) - math.sin(roverLat) * math.cos(latitude) * math.cos(deltaLon))
    return theta

def drive(distance):
    #TODO: Make a drive method
    return 0
def turn(bearing):
    #TODO: Make a turning method
    """if (bearingDiff >= 90):
        turnInPlace(bearingDiff)
    else:
        turnInArc(bearingDiff)"""
    return 0
def turnInPlace(bearing):
    #TODO: finnish this
    return 0
def turnInArc(bearing):
    #TODO: finnish this
    return 0


if(__name__=="__main__"):
    main()
