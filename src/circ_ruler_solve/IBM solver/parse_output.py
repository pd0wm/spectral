import xml.etree.ElementTree as ET

N = 30
tree = ET.parse('output.xml')
variables = tree.getroot()[3]

ruler = []
for i in range(N):
    if int(variables[i].get('value')) == 1:
        ruler.append(i)

print ruler
