import os, subprocess, re

# determine the local ip

a = subprocess.Popen("hostname -I", shell=True, stdout=subprocess.PIPE)
out, err = a.communicate()

if err != None:
	print(err)

ip = out.strip()
print("the local ip is: " + out.strip())

# edit these files to have the correct local ip

files_to_edit = [
	"/usr/local/nginx/conf/nginx.conf",
	os.getcwd() + "/server/server/settings.py",
	# os.getcwd() + "/server/apps/home_app/templates/home_app/watch.html"
]

for filename in files_to_edit:
	with open(filename) as file:
		txt = file.read()
		file.close()
		ips = set(re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', txt))
		try:
			# don't overwrite this one!
			ips.remove("127.0.0.1")
		except KeyError:
			pass
		try:
			ip_to_replace = list(ips)[0]
			newtxt = txt.replace(list(ips)[0], ip)
			with open(filename, 'w+') as file:
				file.write(newtxt)
				file.close()
		except KeyError:
			print("nothing to replace in: " + filename)

# start the nginx server

print("starting nginx")
b = subprocess.Popen("systemctl start nginx.service", shell=True, stdout=subprocess.PIPE)
out, err = b.communicate()
if err != None:
	print(err)

# check for virtualenv

if 'venv' not in os.listdir(os.getcwd()):
	os.system("virtualenv venv")
	os.system("source venv/bin/activate")
	os.system("pip install -r requirments.txt")
else:
	os.system("source venv/bin/activate")

# run the django server

os.chdir("server")
print("starting the server")
os.system("python manage.py runserver 0.0.0.0:8000")
