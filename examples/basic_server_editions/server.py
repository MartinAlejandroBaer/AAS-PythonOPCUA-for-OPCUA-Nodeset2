import logging
import asyncio
import sys
sys.path.insert(0, "..")
import operator
 # importing the Library opcua from FreeOPC-UA.
from asyncua import ua, uamethod, Server

async def main():
    _logger = logging.getLogger('asyncua')
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://XXX.XXX.XXX.XXX:4840/') # Setting the IP and port
    server.set_security_policy(
        [
            ua.SecurityPolicyType.NoSecurity,
#            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
#            ua.SecurityPolicyType.Basic256Sha256_Sign,
        ]
    )
    await server.import_xml("OPC UA Nodeset2.xml") # Importing the OPCUA ML model generated on the AASX tool.
    #await server.import_xml("instance.xml")
    # Creating the variables based on the nodes defined in the OPCUA ML model.
    StringVariable=server.get_node("ns=3;i=1203") # Note: The variable Node is a string
    # We have now to set up the varibales to editable if we want to overwrite its values.
    await StringVariable.set_writable()
    async with server:
        while True: # Infinite loop to overwrite the variables Temperature and Volume
            await asyncio.sleep(5)
            new_str = await StringVariable.get_value()
            await StringVariable.write_value("Test")
            print("New temperature: " + str(new_str))
          
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)
