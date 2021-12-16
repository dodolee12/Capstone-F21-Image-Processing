import asyncio
import bleak
import re
import time

address = "A0:E6:F8:BD:DA:81"
MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"
DATA_STRING_STORAGE_UUID = "F0001131-0451-4000-B000-000000000000"
string = "Finish"
coords = ["Start"]

async def send_coordinates(address,coords):
    client = bleak.BleakClient(address)
    try:
        print("Connecting to MSP...")
        await client.connect()
        ready = await client.read_gatt_char(MODEL_NBR_UUID)
        print(str(ready.decode("UTF-8")) + " is ready.")
        for coord in coords:
            print("Sending command " + coord);
            await client.write_gatt_char(DATA_STRING_STORAGE_UUID, coord.encode())
            ready = await client.read_gatt_char(DATA_STRING_STORAGE_UUID)
            print("String " + str(coord) + " successfully written. MSP state is " + str(ready.decode("UTF-8")))
    except Exception as e:
        print(e)
    finally:
        await client.disconnect()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(send_coordinates(address,string))
loop = asyncio.get_event_loop()
loop.run_until_complete(send_coordinates(address, coords))