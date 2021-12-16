import asyncio
from bluetooth_helper import send_coordinates, address, parse_string_list

f = open("coordinates.txt", "r")
coordinates = parse_string_list(f.read())

loop = asyncio.get_event_loop()
loop.run_until_complete(send_coordinates(address,coordinates))
