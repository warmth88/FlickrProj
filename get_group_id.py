from urllib import * 
f = open('group_list.dat','r')
f2 = open('group_id.dat', 'w')

count = 0 
for i in f:
	flag = False
	page = urlopen('http://www.flickr.com/groups/'+str(i)[:-1]+'/').read()
	index = page.find('/buddyicons/') + 12
	print index
	for j in range(15):
		if page[index+j] == '.': 
			ID = page[index : index+j]
			print "name: "+ i[:-1]+"    ID: "+ID 
			f2.write(str(i)+ID+'\n')
			count += 1
			flag = True
	if flag == False:
		print "error for group: ", i[:-1]
		
print "total number of groups: ", count
f.close()
f2.close()
