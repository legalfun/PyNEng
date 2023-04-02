# import sys
from pprint import pprint
import textfsm
from tabulate import tabulate

# template = sys.argv[1]
# output_file = sys.argv[2]

def parse_output(template, output_file):
    with open(template) as f, open(output_file) as output:
        re_table = textfsm.TextFSM(f)
        header = re_table.header
        result = re_table.ParseText(output.read())
        # result = re_table.ParseTextToDicts(output.read())
        pprint(result, width=150)
        return tabulate(result, headers=header)

if __name__ == '__main__':
    print(parse_output('templates/show_ip_route_ospf.txt', 'output/sh_ip_route_ospf.txt'))

