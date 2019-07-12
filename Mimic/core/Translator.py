import speech_recognition as sr
import wave

# from pydub import AudioSegment
# AudioSegment.ffmpeg="C:/ffmpeg/bins/ffmpeg.exe"
# AudioSegment.converter="C:/ffmpeg/bins/ffmpeg.exe"

class Translator:
    AUDIO_FILE="core/temp/hello"

    def __init__(self, audio_file=AUDIO_FILE):
        self.AUDIO_FILE=audio_file

    def translate(self, audio_queue, conversion_queue):
        while True:
            file_seq, width, data = audio_queue.get()

            self.write_to_file(width, data, self.AUDIO_FILE + str(file_seq))

            r = sr.Recognizer()
            with sr.AudioFile(self.AUDIO_FILE + str(file_seq) + ".wav") as source:
                audio = r.record(source)  # read the entire audio file

            try:
                conversion_queue.put(r.recognize_google(audio))
            except sr.UnknownValueError:
                conversion_queue.put("Sorry, couldn't get that!")
            except sr.RequestError as e:
                conversion_queue.put("Sorry, couldn't start service!")

    def write_to_file(self, sample_width, data, file):
        wf = wave.open(file+".wav", 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(44100)
        wf.writeframes(data)
        wf.close()
        return
        # pd = AudioSegment.from_wav(file + ".wav");
        # pd.export(file+".mp3", format="mp3")