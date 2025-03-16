import logging
import asyncio
import sys
sys.path.insert(0, "..")
 # importing the Library opcua from FreeOPC-UA.
from asyncua import uamethod, Server

@uamethod
def methodScript(parent, x):
    return 5*x 

# For multiple inputs and outputs defined as single properties
# Where x and y are the inputs
# Where (y+x) and (x+y) are the outputs

# @uamethod
# def methodScript(parent, x,y):
#     return y*x, x+y

async def main():
    _logger = logging.getLogger('asyncua')
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://XXX.XXX.XXX.XXX:4840/') # Setting the IP and port
    server.set_security_policy( # We add the security policies in order to be able to edit nodes
        [
            ua.SecurityPolicyType.NoSecurity,
#            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
#            ua.SecurityPolicyType.Basic256Sha256_Sign,
        ]
    )
    await server.import_xml("AASmodel.xml") # Importing the OPCUA ML model generated on the AASX tool.
    # Creating the variables based on the nodes defined in the OPCUA ML model.
    testProperty1=server.get_node("ns=3;i=119")
    testProperty2=server.get_node("ns=3;i=126")
    # We have now to set up the varibales to editable if we want to overwrite its values. 
    # This will also allows to edit the variables from different connected clients (Variable.set_writable())
    testProperty1.set_writable()
    testProperty1.set_writable()
    # We can associate a method in OPC UA with an Operation of the AAS.
    # The following lines will link such operation with the defined method "methodScript"
    methodXML = server.get_node("ns=3;i=148")
    server.link_method(methodXML,methodScript)   
    async with server:
        while True: # Infinite loop to overwrite the variables Temperature and Volume
            await asyncio.sleep(3)
            new_testProperty1 = await testProperty1.get_value() + 0.1
            new_testProperty2 = await testProperty2.get_value() + 1
            await testProperty1.write_value(new_testProperty1)
            await testProperty2.write_value(new_testProperty2)
            print("New testProperty1: " + str(new_testProperty1) + ", New testProperty2: " + str(new_testProperty2))          
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)
