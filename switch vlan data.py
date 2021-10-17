from napalm import get_network_driver
import logging

VLANS = []
data_name_list = []

#connecting to the devices using napalm with the ip 10.0.0.2 - 4 user cisco pass cisco
driver = get_network_driver('ios')
switch1 = driver('10.0.0.2', 'cisco', 'cisco')
switch2 = driver('10.0.0.3', 'cisco', 'cisco')
switch3 = driver('10.0.0.4', 'cisco', 'cisco')
switch1.open()
switch2.open()
switch3.open()
switches = [switch1, switch2, switch3]
for n in switches:
    logging.debug("connecting to " + str(n))
    switch_vlans = n.get_vlans()
    # geting vlan info
    lss = []
    name_ls = []
    for s in switch_vlans:
        lss.append(s)
    #geting vlans names
    for name in lss:
        vl_na = switch_vlans.get(name)['name']
        name_ls.append(vl_na)
    logging.debug("list of vlans in {} {}".format(n, lss))
    logging.debug("vlans name in {} {}".format(n, name_ls))
    name_ls = data_name_list
    # comparing vlans list
    VLANS.sort()
    lss.sort()
    if (VLANS == lss):
        logging.debug("Equal")
    else:
        list_difference = []
        for item in lss:
            if item not in VLANS:
                list_difference.append(item)
        VLANS += list_difference
        logging.debug("Vlans in the database {}".format(VLANS))
        logging.warning("Non equal")
        # adding missing vlans to the switch using netmiko
        for v in list_difference:
            commands = ['conf t', "vlan " + str(v)]
            res = n.cli(commands)
            logging.debug("added vlan {}".format(v))
switch1.close()
logging.debug("connection closed to {}".format(n))
switch2.close()
logging.debug("connection closed to {}".format(n))
switch3.close()
logging.debug("connection closed to {}".format(n))