import sys
import subprocess
import os

proc = subprocess.Popen(['ffprobe', sys.argv[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
_, stde = proc.communicate()
stde = stde.decode('utf-8').replace("      ", "").replace("  ", "")
stde = stde.split("\r\n")
channel = None
try:
    os.mkdir('output')
except FileExistsError:
    pass
try:
    os.mkdir('workinginputs')
except FileExistsError:
    pass
for x in stde:
    if 'Stream' in x and 'Audio' in x and '5.1' in x:
        channel = x.split(" ")[1].replace("#", "").split("(")[0]
        break
if channel is None:
    print("No 5.1 Surround sound stream found!")
    sys.exit(0)

subprocess.call(['ffmpeg', '-i', sys.argv[1],
                 '-filter_complex', f'[{channel}]channelsplit=channel_layout=5.1[FL][FR][FC][LFE][BL][BR]', '-ac', '1',
                 '-map', "[FL]", os.path.join(os.getcwd(), 'workinginputs', 'front_left.wav'), '-ac', '1',
                 '-map', "[FR]", os.path.join(os.getcwd(), 'workinginputs', 'front_right.wav'), '-ac', '1',
                 '-map', "[FC]", os.path.join(os.getcwd(), 'workinginputs', 'front_center.wav'), '-ac', '1',
                 '-map', "[LFE]", os.path.join(os.getcwd(), 'workinginputs', 'lfe.wav'), '-ac', '1',
                 '-map', "[BL]", os.path.join(os.getcwd(), 'workinginputs', 'back_left.wav'), '-ac', '1',
                 '-map', "[BR]", os.path.join(os.getcwd(), 'workinginputs', 'back_right.wav')])
for x in os.listdir('workinginputs'):
    subprocess.call(['java', '-jar', 'LionRay.jar',
                     os.path.join(os.getcwd(), 'workinginputs', x),
                     os.path.join(os.getcwd(), 'output', f'{x}.dfpwm')])
for x in os.listdir('workinginputs'):
    os.remove(os.path.join('workinginputs', x))
print("Finished. check output folder.")