class Task:
	__TASKDESC = "TEST"
	def __init__(self):
		pass
		
	def get_task_description(self):
		return self.__TASKDESC

	def execute(self, action="NA", state = None):
		print(self.get_task_description())

def execute(action):
	return 0, "", None
	
if __name__ == "__main__":
	task = Task()
	print(task.__TASKDESC)
	task.execute("Hello")