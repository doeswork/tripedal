import asyncio
from bleak import BleakClient
import keyboard

async def send_command(client, command):
    await client.write_gatt_char('0000ffe1-0000-1000-8000-00805f9b34fb', bytearray(command, 'utf-8'))

async def connect_and_send_commands(address):
    async with BleakClient(address) as client:
        print(f'Connected: {client.is_connected}')

        while True:
            await asyncio.sleep(0.1)

            if keyboard.is_pressed('left'):
                await send_command(client, 'l')
                await asyncio.sleep(0.1)

            if keyboard.is_pressed('right'):
                await send_command(client, 'r')
                await asyncio.sleep(0.1)

try:
    address = '98:DA:60:07:D9:C7'  # Replace with the address of your HC-06
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect_and_send_commands(address))
except KeyboardInterrupt:
    print("\nProgram exited")

