from gtts import gTTS
import vlc
import Jobs

class Executer:
	AUDIO_FILE = "core/temp/out.mp3"

	def __init__(self, audio_file=AUDIO_FILE):
		self.AUDIO_FILE = audio_file

	def get_job_list(self):
		return Jobs.__all__

	def get_jobs(self):
		job_list = Jobs.__all__
		jobs = []
		for i in range(len(job_list)):
			module = __import__("Jobs." + job_list[i])
			jobs.append(getattr(module, job_list[i]))
		return jobs

	def speak(self, text):
		tts = gTTS(text)
		tts.save(self.AUDIO_FILE)
		vlc.MediaPlayer(self.AUDIO_FILE).play()

	def execute(self, conv_queue):
		jobs = self.get_jobs()
		while True:
			action = conv_queue.get().lower()
			print(action)
			success = 0
			for job in jobs:
				status, data, misc = job.execute(action)
				if status == 1:
					success = 1
					break
			if success == 0:
				print("Sorry! I didn't understand!")
		