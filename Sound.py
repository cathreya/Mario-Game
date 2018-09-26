import subprocess


class Sound:

    def __init__(self):
        self.dir = "./Media/"
        self.filenames = {
            "coin": "smb_coin.wav",
            "jump": "smb_jump-small.wav",
            "spring": "smb_jump-super.wav",
            "bump": "smb_bump.wav",
            "dead": "smb_mariodie.wav",
            "kill": "smb_stomp.wav",
            "over": "smb_gameover.wav",
            "theme": "01-main-theme-overworld.wav",
            "level": "smb_stage_clear.wav"
        }
        self._subprocessList = []

    def play(self, which, block = False):
        # print(self.dir + self.filenames[which])
        self._subprocessList.append(subprocess.Popen(["play", self.dir + self.filenames[which]], shell=False,
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL))
        if block:
            self._subprocessList[-1].wait()

    def stop_sounds(self):
        for subp in self._subprocessList:
            subp.terminate()
