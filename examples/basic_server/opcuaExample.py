import logging
import asyncio
import sys
sys.path.insert(0, "..")
from asyncua import Server

async def main():
    _logger = logging.getLogger('asyncua')
    server = Server() # setup our server
    await server.init()
    server.set_endpoint('opc.tcp://XXX.XXX.XXX.XXX:4840/') # Setting the IP and port
    await server.import_xml("AASmodelV2.xml") # Importing the OPCUA ML model generated with the AASX tool. (In this case AASmodelV2.xml will the imported)
    # Creating the variables based on the nodes of the OPCUA ML model. 
    # Use the UaModeler or opcua-modeler to verify the number of the nodes.
    Temperature=server.get_node("ns=3;i=119")
    Volume=server.get_node("ns=3;i=126")
    # Setting up the variables in order to overwrite their values
    Temperature.set_writable()
    Volume.set_writable()
    async with server:
        while True: # Infinite loop to overwrite the variables Temperature and Volume
            await asyncio.sleep(3)
            new_temp = await Temperature.get_value() + 0.1
            await Temperature.write_value(new_temp)
            new_vol = await Volume.get_value() + 0.5
            await Volume.write_value(new_vol)       
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)
