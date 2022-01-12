# -*- coding: utf-8 -*-
"""

ip type check script
ip is valid if it contain 4 nums (not letter or other symbols)
   - item split with '.'
   - every item in range from 0 to 256

if ip not valid - print: 'Not valid IP'

print must execute just for one time, even if few cases is not done

for ip check type:

   'unicast' - if 1st byte in range 1-223
   'multicast' - if 1st byte in range 224-239
   'local broadcast' - if ip equal 255.255.255.255
   'unassigned' - if ip equal 0.0.0.0
   'unused' - in other cases

"""

ip_address = input("Enter ip address: ")
octets = ip_address.split(".")

correct_ip = len(octets) == 4
for octet in octets:
    correct_ip = correct_ip and octet.isdigit() and int(octet) in range(256)

if not correct_ip:
    print("Not valid IP")
else:
    octets_num = [int(i) for i in octets]

    if octets_num[0] in range(1, 224):
        print("unicast")
    elif octets_num[0] in range(224, 240):
        print("multicast")
    elif ip_address == "255.255.255.255":
        print("local broadcast")
    elif ip_address == "0.0.0.0":
        print("unassigned")
    else:
        print("unused")
