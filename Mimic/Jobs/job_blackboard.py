class Blackboard:
	DOOR = "******"		# UTA NetID
	KEY = "*******"		# UTA Password

	def __init__(self, door=DOOR, key=KEY):
		self.DOOR = door
		self.KEY = key
		pass

	def output(self):
		n, g = self.update()
		if n > -1 or g > -1:
			if int(n) == 0:
				n = "no"
			if int(g) == 0:
				g = "no"
			return "You have " + n + " new notifications and " + g + " new grades update."
		return "Error logging in!"

	def update(self):
		import requests

		header = {
			'Host': 'elearn.uta.edu:443',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, sdch, br',
			'Accept-Language': 'en-US,en;q=0.8',
			'Origin': 'https://elearn.uta.edu/',
			'Referer': 'https://elearn.uta.edu/',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
		}
		headerX = {
			'Host': 'elearn.uta.edu',
			'Connection': 'keep-alive',
			'Content-Length': '267',
			'undefined': 'true',
			'Origin': 'https://elearn.uta.edu',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
			'Content-Type': 'text/plain',
			'Accept': '*/*',
			'Referer': 'https://elearn.uta.edu/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_50_1',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'en-US,en;q=0.8'
		}

		postTo = 'https://elearn.uta.edu/webapps/login/'
		postToX = 'https://elearn.uta.edu/webapps/portal/dwr_open/call/plaincall/ToolActivityService.getActivityForAllTools.dwr'

		start = requests.Session()
		start.headers.update(header)

		# to get authCode at the end
		postData = {"user_id": self.DOOR, "password": self.KEY, "login": "Login", "action": "login", "new_loc": ""}
		requestForLogin = start.post(postTo, data=postData)

		loginOutput = requestForLogin.text
		if loginOutput.find("loginPageContainer") > -1:
			print("Sorry, we couldn't log into your account!")
			return -1, -1

		########################## FOR XHR, ie X or headerX and postToX used ###########
		start.headers.update(headerX)
		postDataX = {
			"callCount": "1",
			"page": "/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_50_1",
			"httpSessionId": "",
			"scriptSessionId": "",
			"c0-scriptName": "ToolActivityService",
			"c0-methodName": "getActivityForAllTools",
			"c0-id": "0",
			"batchId": "0"
		}

		requestForData = start.post(postToX, data=postDataX).text
		if requestForData.find("AlertsOnMyBb_____AlertsTool") < 0:
			return 0, 0
		startP = requestForData.find("AlertsOnMyBb_____AlertsTool") + len("AlertsOnMyBb_____AlertsTool")
		startP = requestForData.find(":", startP) + 1
		endP = requestForData.find(",", startP)

		startP2 = requestForData.find("MyGradesOnMyBb_____MyGradesTool") + len("MyGradesOnMyBb_____MyGradesTool")
		startP2 = requestForData.find(":", startP2) + 1
		endP2 = requestForData.find(",", startP2)

		return requestForData[startP:endP], requestForData[startP2:endP2]

def execute(action):
	bb = Blackboard()
	return 1, bb.output(), None