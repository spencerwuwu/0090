"""two c220g5 client nodes and one server running ubuntu 20.04

Instructions:
su sudo for root access"""

#
# NOTE: This code was machine converted. An actual human would not
#       write code like this!
#

import os
# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal object,
pc = portal.Context()
# urn:publicid:IDN+utah.cloudlab.us:super-fuzzing-pg0+ltdataset+DataStorage
pc.defineParameter("DATASET", "URN of your dataset",
                   portal.ParameterType.STRING,
                   "urn:publicid:IDN+utah.cloudlab.us:wildharness-pg0+ltdataset+wildharness-data")

pc.defineParameter("MPOINT", "Mountpoint for file system",
                   portal.ParameterType.STRING, "/data")

params = pc.bindParameters()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

USER = os.environ["USER"]
OQINSTALL = "sudo bash /local/repository/install-docker.sh"
SINEPY = "sudo -u {} nohup python3 /local/repository/sine.py > /dev/null &"
SINEPY = SINEPY.format(USER)
ADDGRP = "sudo usermod -aG docker {}"
ADDGRP = ADDGRP.format(USER)
CHOWN_DATA = "sudo chown -R {} /mydata"
CHOWN_DATA = CHOWN_DATA.format(USER)
MKDIR_DATA = "sudo -u {} mkdir /mydata/data"
MKDIR_DATA = MKDIR_DATA.format(USER)
URN2204 = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD"

HARDWARE_TYPE = 'c6420'
NODE_COUNT = 5

# Link link-0
link_0 = request.Link('link-0')
link_0.Site('undefined')

for node_id in range(NODE_COUNT):
    node = request.RawPC('n{}'.format(node_id))
    node.hardware_type = HARDWARE_TYPE
    node.disk_image = URN2204
    iface = node.addInterface('interface-{}'.format(node_id))
    bs0 = node.Blockstore('bs{}'.format(node_id), '/mydata')
    node.addService(pg.Execute(shell="bash", command=OQINSTALL))
    #node.addService(pg.Execute(shell="bash", command=SINEPY))
    node.addService(pg.Execute(shell="bash", command=ADDGRP))
    link_0.addInterface(iface)


# Print the generated rspec
pc.printRequestRSpec(request)
