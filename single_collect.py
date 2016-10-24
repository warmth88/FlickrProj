from collect import *
import time
import sys

# conduct a single collect with the sys argument provided

group_name = sys.argv[2]
group_id = sys.argv[3]
num = sys.argv[4]
api_key = sys.argv[1]

f = flickrapi.FlickrAPI(api_key)
get_group(f, group_name, group_id, num)

print 'subprocess %s successful!' % num

