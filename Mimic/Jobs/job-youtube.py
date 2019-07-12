# Requires selenium and adblocker
# Voice Controlled YouTube Player
# Under Construction

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import time
from threading import Thread

class Youtube:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_extension('C:/Python/ublock_2_0_4.crx')
        # chrome_options.add_extension('C:/Python/adblock_1.13.2.crx')
        self.driver = webdriver.Chrome(executable_path='C:/Python/chromedriver.exe', chrome_options=self.chrome_options)
        self.driver.set_window_size(0, 0)
        self.driver.set_window_position(-300, -300)

        self.worker = Thread(target=self.start, args=())
        self.worker_update = 0
        self.worker_exit = 0

        self.play_list = []
        self.playing = 0
        self.now_playing = -1
        self.current_length = -1

    def play_name(self, name):
        page = "https://www.youtube.com/results?search_query=" + name
        source = requests.get(page).text

        start = source.find("data-context-item-id=\"") + len("data-context-item-id=\"")
        end = source.find("\"", start)
        t_start = source.find("<span class=\"video-time\" aria-hidden=\"true\">", end) + len("<span class=\"video-time\" aria-hidden=\"true\">")
        t_end = source.find("</span>", t_start)
        length_array = source[t_start:t_end].split(":")
        self.play_id(source[start:end], int(length_array[0])*60+int(length_array[1]))

    def play_id(self, video, length=0):
        self.driver.get("https://www.youtube.com/watch?v=" + video)
        print("Playing: ", video, "\nLength: ", length/60, ":",length%60)
        self.playing = 1
        self.now_playing += 1
        self.current_length = length

        if not self.worker.is_alive():
            self.worker = Thread(target=self.start, args=())
            self.worker.start()

    def add_next(self, name, immediate = 0):
        self.play_list.insert(self.playing + 1, name)
        if self.playing == 0 and immediate == 0:
            self.play_name(name)

    def add_last(self, name):
        self.play_list.append(name)
        if self.playing == 0:
            self.play_name(name)

    def play_next(self, name):
        self.add_next(name, 1)
        self.play_name(name)
        self.worker_update = 1

    def stop(self):
        self.play_list = []
        self.playing = 0
        self.now_playing = -1
        self.current_length = -1
        self.worker_update = 1
        self.worker_exit = 1
        self.driver.get("https://www.youtube.com")

    def quit(self):
        self.driver.close()
        self.driver.quit()

    def start(self):
        while True:
            time.sleep(1)
            if self.worker_exit == 1:
                self.worker_exit = 0
                return

            t = 0
            t2 = self.current_length                    # SO THAT WE CAN WORK ON IMMEDIATE UPDATE AND STUFFS
            while t < t2-4:                                # replace 2 by t2
                time.sleep(1)
                t += 1
                if self.worker_update == 1:
                    break
            if self.worker_update == 1:     # when someone calls for stop or play immediate next or something, UC
                self.worker_update = 0
                continue
            print("not continued")
            if self.playing == len(self.play_list) - 1:     # Played all, quits thread
                self.stop()
                break
            else:                                           # Playing next, loops on thread
                name = self.play_list[self.now_playing + 1]
                self.play_name(name)

def execute(action):
    player=Youtube()
		# fix the ACTION to run as follows
		"""
		player.play_next("Animals")
    time.sleep(50)
    player.play_next("Applause by gaga")
    player.play_next("Bad romance by gaga")
    time.sleep(3)
    player.stop()
    time.sleep(3)
    player.add_next("Bad romance by gaga")
    time.sleep(3)
    player.add_next("Bad romance by gaga")
    player.play_next("love story by taylor")
    # player.play_immediate_next("poker face by gaga")
		"""
		return 0, "", None
