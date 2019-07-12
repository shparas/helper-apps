# for listener
from sys import byteorder
from array import array
from struct import pack
import pyaudio

class Listener:
    THRESHOLD_START = 25000
    THRESHOLD = 3000
    CHUNK_SIZE = 1024
    FORMAT = pyaudio.paInt16
    RATE = 44100
    TIME = 1
    CHANNELS = 1
    MAXIMUM_VOLUME = 16384
    UP_TIME = 5

    def __init__(self,
                 up_time=UP_TIME,
                 threshold_start=THRESHOLD_START,
                 threshold=THRESHOLD,
                 chunk_size=CHUNK_SIZE,
                 audio_format=FORMAT,
                 rate=RATE,
                 time=TIME,
                 channels=CHANNELS,
                 maximum_volume=MAXIMUM_VOLUME):
        self.UP_TIME=up_time
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

    # Change the volume according to MAXIMUM and maximum of chunk
    def average_volume(self, snd_data, maximum_volume=MAXIMUM_VOLUME):
        if len(snd_data) == 0:
            return snd_data

        r = array('h')
        times = float(maximum_volume) / max(abs(i) for i in snd_data)
        for i in snd_data:
            r.append(int(i * times))
        return r

    # Removes silence before and after
    def remove_silence(self, snd_data):
        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i) > self.THRESHOLD:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        # Trim to the left
        snd_data = _trim(snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data

    # Add silence of X seconds before and after
    def add_silence(self, snd_data, seconds):
        r = array('h', [0 for i in xrange(int(seconds * RATE))])
        r.extend(snd_data)
        r.extend([0 for i in xrange(int(seconds * RATE))])
        return r

    def listen(self, audio_queue):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, output=True, frames_per_buffer=self.CHUNK_SIZE)

        startL = 0      # startListening = 1 or 0
        silentS = 0     # number of seconds the recording has been silent
        total_rec = array('h')  # collected chunk before it sends it to translate queue
        file_seq = 1    # number we are appending to filename, to make them unique, that we store our recordings at.
        temp_threshold = self.THRESHOLD_START

        while True:  # loop for every seconds
            one_rec = array('h')    # array of recording of every second
            time_elapsed = 0
            while time_elapsed < self.TIME * self.RATE:
                inst_rec = stream.read(self.CHUNK_SIZE)
                time_elapsed += self.CHUNK_SIZE

                tmp_data = array('h', inst_rec)
                if byteorder == 'big':
                    tmp_data.byteswap()  # tmp_data is now little endian, signed short array
                one_rec.extend(tmp_data)
            # one_rec is now available with the last second recording

            # Here, if it was listening earlier and now its silent, it increases and compares the silentS wrt UP_TIME
            # to see if it exceeds the wait time. If it does, it increases the threshold before it starts to listen again
            # ie it goes to sleep and you've to yell to wake it up. And, if it doesn't, just finalizes the last recording
            # and puts it in the queue with new (+1) file sequence.
            # If it wasn't listening before then doesn't effect anything.
            #
            # Also, if its not silent, it sees if it was listening earlier. If it was, it just extends the data at the
            # end of earlier recording. If it wasn't, starts listening and decreases the threshold so that you don't have
            # to yell anymore.

            if self.is_silent(one_rec, temp_threshold):
                if startL == 1:                                     # means it was listening before, it wasn't sleeping
                    silentS += 1                                    # since its silence, increases the sillentS count
                    print("Silent")                                 # hint to use
                    if silentS >=self.UP_TIME:                      # if it exceeds the wait time
                        temp_threshold = self.THRESHOLD_START          # increases the threshold so that you've to yell next time.
                        print("  Not Listening Anymore")               # Hint to uer.
                        startL = 0                                     # note that it wasn't listening.

                    if len(total_rec) > 100:                        # if we have something in total_rec, process it, put it
                        total_rec = self.average_volume(total_rec)         # into queue and then clear the total_rec for new data
                        data = pack('<' + ('h' * len(total_rec)), *total_rec)
                        sample_width = p.get_sample_size(self.FORMAT)
                        # record_to_file(sample_width, data, "G:/hello" + str(file_seq))    # in case you want into file
                        audio_queue.put([str(file_seq), sample_width, data])
                        file_seq += 1
                        del total_rec[:]
                        # END HERE

            else:  # not silent                                     # it is not silent, and there is data
                if startL != 1:                                     # if it wasn't listening earlier, start now.
                    print("Started listening.")
                    startL = 1                                        # Decreases the threshold and puts a note for future
                    temp_threshold = self.THRESHOLD
                total_rec.extend(one_rec)                           # Adds the recorded part to one_rec
                silentS = 0                                         # resets the silentS

        stream.stop_stream()
        stream.close()
        p.terminate()
