import flickrapi
import json 
import time
import csv

def photo_otherinfo(f, id):
	otherinfo=f.photos_getinfo(photo_id=id,format='json')
	otherinfo=json.loads('['+otherinfo[14:-1]+']')[0]['photo']
	faves=f.photos_getFavorites(photo_id=id,format='json')	
	faves=json.loads('['+faves[14:-1]+']')[0]['photo']
	date_uploaded	=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(otherinfo['dates']['posted'])))
	tags=otherinfo['tags']['tag']
	first_4tags=[]
	if tags!=[]:
		count=0
		for i in tags:
			first_4tags.append(unicode(i['_content']).encode('utf-8'))
			count+=1
			if count==4: break
	return date_uploaded,otherinfo['views'],faves['total'],first_4tags

def get_comments(f, id):
	comments=f.photos_comments_getlist(photo_id=id,format='json')
	comments=json.loads('['+comments[14:-1]+']')[0]['comments']
	count=1
	comment_list = []
	try:
		for i in comments['comment']:
			commenting_user=i['authorname']
			user_id = i['author']
			time_comment=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(i['datecreate'])))
			full_text=i['_content']
			order_of_comments=count
			count +=1
			comment_list.append([commenting_user, user_id, time_comment, full_text, order_of_comments])
		return comment_list
	except:
		return comment_list
	
def get_users(f, id):
	users = f.people_getinfo(user_id = id, format = 'json')
	users = json.loads('['+users[14:-1]+']')[0]['person']
	total_num_photos = users['photos']['count']['_content']
	pro_membership = users['ispro']
	earliest_activity = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(users['photos']['firstdate']['_content'])))
	date_joined = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(users['datecreate'])))
	try:
		location = users['location']['_content']
	except:
		location = ''
	
	contacts = f.contacts_getPublicList(user_id = id, page = 1, per_page = 1, format = 'json')
	contacts = json.loads('['+contacts[14:-1]+']')[0]['contacts']
	total_contacts = contacts['total']
	
	return [id,total_num_photos, pro_membership, earliest_activity, date_joined, total_contacts, location]


def get_group(f, group_name, group_ID, group_order):
	
	recent = f.groups_pools_getPhotos(group_id = group_ID, extras='last_update',per_page=500,format='json')
	recent2 = f.groups_pools_getPhotos(group_id= group_ID, extras='last_update',page = 2, per_page=500,format='json')
	
	
	# open csv files for write
	current_time = time.strftime("%Y-%m-%d", time.gmtime())
	photo_file = open('./tmp/photo_'+current_time+'_'+group_order+'.csv','w')
	comments_file = open('./tmp/comments_'+current_time+'_'+group_order+'.csv','w')
	wr_photo = csv.writer(photo_file, dialect='excel')
	wr_comments = csv.writer(comments_file, dialect='excel')
	
	photo_header = ['Group Name', 'Group ID', 'Photo ID', 'Order in Group', 'Photo Title', 'Username', 'Time Uploaded to Flickr', 'Time Added to Group', 'First Four Tags', 'Number of Views', 'Number of Faves', 'User ID', 'User Total Number of Photos', 'Pro Membership', 'Earliest Activity on Flickr', 'Date Joined Flickr', 'Number of Contacts', 'Location']
	wr_photo.writerow(photo_header)
	comments_header = ['Group Name', 'Group ID', 'Photo ID', 'Commenting User', 'User ID', 'Commenting time', 'Full Text of Comment', 'Order of Comment']
	wr_comments.writerow(comments_header)
		
	# start collection
	for run in range(2):
		page=run+1
	
		if run == 1: recent = recent2
		recent=json.loads('['+recent[14:-1]+']')
		total=recent[0]['photos']['total']
		recent=(recent[0]['photos']['photo'])
		
		for i in xrange(len(recent)):
			photo_ID	=recent[i]['id']
			order_in_group	=str(i+(page-1)*500+1)
			title		=recent[i]['title']
			username	=recent[i]['ownername']
			user_ID		=recent[i]['owner']
			date_added	=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(recent[i]['dateadded'])))
			date_uploaded,views,faves,tags=photo_otherinfo(f, photo_ID)
		
			photo_all=[photo_ID,order_in_group,title,username,date_uploaded,date_added,tags,views,faves]
		        
		        comments_all = get_comments(f, photo_ID)
		
			user_all = get_users(f, user_ID)
		
			photo_print = []
			comments_print = []
			for j in [group_name, group_ID]+photo_all+user_all:
				photo_print.append(unicode(j).encode('utf-8'))
			photo_print[8] = photo_print[8].replace("'", "")
			
			for j in comments_all:
				tmp = [group_name, group_ID, photo_ID]
				for k in j:
					tmp.append(unicode(k).encode('utf-8'))
				if len(tmp) != 8: print "extra!!!"
				comments_print.append(tmp)
				
			
		
			wr_photo.writerow(photo_print)
			for j in comments_print:
				wr_comments.writerow(j)
			if i%50 == 0:
				print 'subprocess ' + group_order + '   '+str((i+500*run)/10.)[:3]+'%'
	#		if i==500:
	#			break
	


	

# from photo info get <uploaded date, views, # of comments, tags>

# photos_getFavorites  <# of faves>

# photos_comments_getlist <all the info we want for comments>

# people_getinfo <most of the info of users>

# contacts_getPublicList <# of contacts>




# cannot find if listed in other groups

