import json
import yaml



def conv(filejson):
	with open(filejson, 'r') as f:
       		sample = json.load(f)
	
	json_obj = json.dumps(sample)
	#print 'json_obj =',json_obj

	ff = open('data.yaml', 'wb')
	yaml.safe_dump(sample, ff, allow_unicode=True)

	ydump = yaml.safe_dump(sample, default_flow_style=False)
#print 'ydump=',ydump


