from threading import Thread
from queue import Queue
from core import *

# use after recording. Put here data array to be processed into file. After making file, put file name into following queue
audio_queue = Queue()		 
# use after file name is ready. Recognize the text and fill the text_queue. delete the file after the conversion
conversion_queue = Queue()	
# use after recognition. Put the recognized text.
text_queue = Queue()		  

if __name__=='__main__':
	lis = Listener()
	tra = Translator()
	exe = Executer()

	lis_proc = Thread(target=lis.listen, args=(audio_queue,))
	tra_proc = Thread(target=tra.translate, args=(audio_queue, conversion_queue))
	exe_proc = Thread(target=exe.execute, args=(conversion_queue,))

	lis_proc.start()
	tra_proc.start()
	exe_proc.start()

	lis_proc.join()
	tra_proc.join()
	exe_proc.join()
