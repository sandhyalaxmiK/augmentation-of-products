import json
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from os import listdir
import os
import sys
'''
obj=json.load(open(sys.argv[1]))
#print obj
xml = dicttoxml(obj,root=False,attr_type=False)
#print xml
dom = parseString(xml)
dom.toprettyxml()
with open(sys.argv[1].split('.')[0]+'.xml','w') as f:
	f.write(dom.toprettyxml())'''


for json_file in listdir(sys.argv[1]+'/'):
		
	obj=json.load(open(os.path.join(sys.argv[1],json_file)))
	#print obj
	xml = dicttoxml(obj,root=False,attr_type=False)
	#print xml
	dom = parseString(xml)
	dom.toprettyxml()
	with open(sys.argv[2]+'/'+json_file.split('.')[0]+'.xml','w') as f:
		f.write(dom.toprettyxml())


