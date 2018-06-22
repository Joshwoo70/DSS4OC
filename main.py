import sys
import subprocess
import os
"""
Audio modes:
0: Mono [Not used]
1: Stereo
2:
"""
proc = subprocess.Popen(['ffprobe', sys.argv[1]], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
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
audiomode = None
for x in stde:
    if '5.1' in x:
        channel = x.split(" ")[1].replace("#", "").split("(")[0]
        audiomode = 0
        break
    elif '2 channels' in x or 'stereo' in x:
        channel = x.split(" ")[1].replace("#", "").split("(")[0]
        print("File is in Stereo Mode!")
        audiomode = 1
        break

if channel is None:
    print("No Dual Soundable Streams!")
    sys.exit(1)
if audiomode == 1:
    subprocess.call(['ffmpeg', '-i', sys.argv[1], '-filter_complex',
                     f"[{channel}]channelsplit=channel_layout=stereo[L][R]", '-ac', '1', '-map', "[L]",
                     os.path.join(os.getcwd(), 'workinginputs', 'left.wav'), '-ac', '1', '-map', "[R]",
                     os.path.join(os.getcwd(), 'workinginputs', 'right.wav'), '-ac', '1'],
                    stdout=subprocess.DEVNULL)
elif audiomode == 0:
    subprocess.call(['ffmpeg', '-i', sys.argv[1],
                     '-filter_complex', f'[{channel}]channelsplit=channel_layout=5.1[FL][FR][FC][LFE][BL][BR]', '-ac',
                     '1',
                     '-map', "[FL]", os.path.join(os.getcwd(), 'workinginputs', 'front_left.wav'), '-ac', '1',
                     '-map', "[FR]", os.path.join(os.getcwd(), 'workinginputs', 'front_right.wav'), '-ac', '1',
                     '-map', "[FC]", os.path.join(os.getcwd(), 'workinginputs', 'front_center.wav'), '-ac', '1',
                     '-map', "[LFE]", os.path.join(os.getcwd(), 'workinginputs', 'lfe.wav'), '-ac', '1',
                     '-map', "[BL]", os.path.join(os.getcwd(), 'workinginputs', 'back_left.wav'), '-ac', '1',
                     '-map', "[BR]", os.path.join(os.getcwd(), 'workinginputs', 'back_right.wav')],
                    stdout=subprocess.DEVNULL)
else:
    print("Cannot find a suitable audio mode...")
    sys.exit(1)
for x in os.listdir('workinginputs'):
    subprocess.call(['java', '-jar', 'LionRay.jar',
                     os.path.join(os.getcwd(), 'workinginputs', x),
                     os.path.join(os.getcwd(), 'output', f'{x}.dfpwm')],
                    stdout=subprocess.DEVNULL)
for x in os.listdir('workinginputs'):
    os.remove(os.path.join('workinginputs', x))
files = []
for file in os.listdir('output'):
    size = os.stat(os.path.join('output',file)).st_size
    files.append(size)
    pass  # TODO: combine files.
print("Writing DFPWMX...")
with open(os.path.join('output',os.path.split(sys.argv[1])[-1])+'.dfpwmx','wb') as f:
    f.write(b"\x00DFPWMX"+b"\xff")
    f.write(str(len(files)).zfill(2).encode()+b"\xff")
    for fsize in files:
        f.write(str(fsize).encode()+b"\xff")
    f.write(b"\xff")
    folderlist = os.listdir('output')
    for file in folderlist:
        with open(os.path.join('output', file), 'rb') as f2:
            while True:
                data = f2.read(2048)
                if not data:
                    break
                f.write(data)

print("Finished. check output folder.")
