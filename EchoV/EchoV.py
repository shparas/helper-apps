from sys import byteorder
from array import array
from struct import pack
import pyaudio

class Listener:
	THRESHOLD_START = 1000
	THRESHOLD = 1000
	CHUNK_SIZE = 1024
	FORMAT = pyaudio.paInt16
	RATE = 44100
	TIME = 1
	CHANNELS = 1
	MAXIMUM_VOLUME = 16384
	UP_TIME = 5

	def __init__(self,
				 up_time = UP_TIME,
				 threshold_start = THRESHOLD_START,
				 threshold = THRESHOLD,
				 chunk_size = CHUNK_SIZE,
				 audio_format = FORMAT,
				 rate = RATE,
				 time = TIME,
				 channels =C HANNELS,
				 maximum_volume = MAXIMUM_VOLUME):
		self.UP_TIME = up_time
		self.RATE = rate
		self.THRESHOLD = threshold
		self.THRESHOLD_START = threshold_start
		self.CHUNK_SIZE = chunk_size
		self.FORMAT = audio_format
		self.TIME = time
		self.CHANNELS = channels
		self.MAXIMUM_VOLUME = maximum_volume

	# 'True' if max of the collected data is below the threshold
	def is_silent(self, snd_data, threshold=THRESHOLD):
		return max(snd_data) < threshold

	def listen(self):
		p = pyaudio.PyAudio()
		streamI = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, output=True, frames_per_buffer=self.CHUNK_SIZE)
		
		startL = 0	  # startListening = 1 or 0
		silentS = 0	 # number of seconds the recording has been silent
		total_rec = array('h')  # collected chunk before it sends it to translate queue
		temp_threshold = self.THRESHOLD_START

		while True:  # loop for every seconds
			one_rec = array('h')	# array of recording of every second
			time_elapsed = 0
			while time_elapsed < self.TIME * self.RATE:
				inst_rec = streamI.read(self.CHUNK_SIZE)
				time_elapsed += self.CHUNK_SIZE

				tmp_data = array('h', inst_rec)
				if byteorder == 'big':
					tmp_data.byteswap()  # tmp_data is now little endian, signed short array
				one_rec.extend(tmp_data)
			# one_rec is now available with the last second recording

			if self.is_silent(one_rec, temp_threshold):
				if startL == 1:									 # means it was listening before, it wasn't sleeping
					silentS += 1									# since its silence, increases the sillentS count
					if silentS == 1:
						print("Silent.", end='')
					else:
						print(".", end="")
					if silentS >=self.UP_TIME:					  # if it exceeds the wait time
						temp_threshold = self.THRESHOLD_START		  # increases the threshold so that you've to yell next time.
						print("  Not Listening Anymore")			   # Hint to user.
						startL = 0									 # note that it wasn't listening.

					if len(total_rec) > 100:						# if we have something in total_rec, process it, put it
						# total_rec = self.remove_silence(self.average_volume(total_rec))		 # into queue and then clear the total_rec for new data
						data = pack('<' + ('h' * len(total_rec)), *total_rec)
						del total_rec[:]
						streamI.write(data)
			else:  # not silent									 # it is not silent, and there is data
				if startL != 1:									 # if it wasn't listening earlier, start now.
					print("Started listening.")
					startL = 1										# Decreases the threshold and puts a note for future
					temp_threshold = self.THRESHOLD
				total_rec.extend(one_rec)						   # Adds the recorded part to one_rec
				silentS = 0										 # resets the silentS

		streamI.stop_stream()
		p.terminate()

if __name__=='__main__':
    lis = Listener()
    lis.listen()
