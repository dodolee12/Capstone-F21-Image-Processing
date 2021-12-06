import asyncio
import bleak
import re
import time

address = "A0:E6:F8:BD:DA:81"
MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"
DATA_STRING_STORAGE_UUID = "F0001131-0451-4000-B000-000000000000"

async def send_coordinates(address,coordinates):
    client = bleak.BleakClient(address)
    try:
        print("Connecting to MSP...")
        await client.connect()
        print("Connection established")
        await client.write_gatt_char(DATA_STRING_STORAGE_UUID, "Start".encode())
        print("Starting")
        i = 0
        for coordinate in coordinates:
            await client.write_gatt_char(DATA_STRING_STORAGE_UUID, coordinate.encode())
            ready = await client.read_gatt_char(DATA_STRING_STORAGE_UUID)
            print("Coordinate (" + str(i) + ") " + str(coordinate) + " successfully written. MSP state is " + str(ready.decode("UTF-8")))
            i += 1
    except Exception as e:
        print(e)
    finally:
        await client.disconnect()

def parse_string_list(string):
    listOfElements = []

    for element in re.findall('\(.*?\)|Lift Pen', string):
        listOfElements.append(element)

    return listOfElements


f = open("coordinates.txt", "r")
coordinates = parse_string_list(f.read())


loop = asyncio.get_event_loop()
loop.run_until_complete(send_coordinates(address,coordinates))
