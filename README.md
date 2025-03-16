Example test of an OPC UA server provided to address the detected issue in the AASX Package Explorer tool [Link](https://github.com/eclipse-aaspe/aaspe/issues/187#issuecomment-2106367090) 

## Examples
The example requires the Asyncua library which can be easily installed via pip. [Link](https://pypi.org/project/asyncua/)

``` Python
pip install asyncua
```

``` Python
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
```
The following example allows to link between an Operation Submodel Element of the Asset Administration Shell and an OPC UA method

``` Python
import logging
import asyncio
import sys
sys.path.insert(0, "..")
 # importing the Library opcua from FreeOPC-UA.
from asyncua import uamethod, Server

@uamethod
def methodScript(parent, x):
    return 5*x 

# For multiple inputs and outputs defined as single Submodel Element Properties within the Submodel Element Operation
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
    await server.import_xml("AASmodel.xml") # Importing the OPCUA ML model generated on the AASX tool.
    # Creating the variables based on the nodes defined in the OPCUA ML model.
    testProperty1=server.get_node("ns=3;i=119")
    testProperty2=server.get_node("ns=3;i=126")
    # We have now to set up the varibales to editable if we want to overwrite its values
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
```
## Important notes
- The required files to execute the above mentioned codes are contained within the folder "examples"
- The variables exposed with two above presented codes are read-only. In order to be able to edit them from different clients check the "examples" folder
- The deployed **Asset Administration Shells** corresponds to **Version 2.0**

