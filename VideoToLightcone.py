import cv2
# Var

print('HONKAI STAR RAIL MOD SCRIPT - VIDEO TO LIGHTCONE')
print('This Scripts Converts Video into pictures and config file for lightcone mods in honkai star rail')

modName = input('Enter Mod Name : ')
while modName == '':
	modName = input('Mod name cannot be empty. \n\
	Enter Mod Name(needs to be unique than other mods.... i think) : ')

videofilename = input('Enter file name e.g. sample.mp4 : ') 
while videofilename == '':
	modName = input('File cannot be empty. \n\
	Enter file name e.g. sample.mp4 : ') 

FRAME_COUNT = int(input('How many frame do you want (more the animation will be less choppy but take more space) : '))
use_resize = int(input('do you want to use resize, may cause distortion? (1 - yes, 0 - no, use original resolution) '))

lightconeimagehash = input ("Enter Lightcone hash e.g. 89881665 for A Secret Vow (you can look up the hash in txt file in this folder) :")
while lightconeimagehash == '':
	lightconeimagehash = input('Hash cannot be empty. \n\
	Enter Lightcone hash e.g. 89881665 for A Secret Vow (you can look up the hash in txt file in this folder) :') 

# Param
MIN_FRAMES = 15
BORDER_COLOR = [178, 190, 181] # grey
BORDER_WIDTH = 10
top, bottom, left, right = [BORDER_WIDTH]*4

vidcap = cv2.VideoCapture(videofilename)
success,image = vidcap.read()
total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = vidcap.get(cv2.CAP_PROP_FPS)
print('total_frames', total_frames)

count = 0
frame_count = 0
inc = min(int(total_frames / FRAME_COUNT), MIN_FRAMES)

# make images
while success and count < FRAME_COUNT:
    if frame_count % inc == 0:
        if use_resize:
        	image_resized = cv2.resize(image, (710, 980))
        else :
            image_resized = image
        image_rotated = cv2.rotate(image_resized, cv2.ROTATE_180)
        image_rotated_border = cv2.copyMakeBorder(image_rotated, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BORDER_COLOR)
        
        filename = modName+ str(count) + ".jpg" 
        # path = './'+modName+'/'+filename
        path = filename
        cv2.imwrite(path, image_rotated_border)     # save frame as JPEG file      
        print('Write image: ',path )
        count += 1

    success,image = vidcap.read()
    frame_count += 1


# make config file
f = open(modName + ".ini", "w")
print('Writing config file')
configfilecontent = \
"\
[Constants] \n\
global $framevar = 0  \n\
global $active \n\
global $fpsvar = 0 \n\
 \n\
[Present] \n\
post $active = 0 \n\
 \n\
if $active == 1 && $fpsvar < 60 \n\
	$fpsvar = $fpsvar + 15 \n\
endif \n\
 \n\
if $fpsvar >= 60 \n\
	$fpsvar = $fpsvar - 60 \n\
	$framevar = $framevar + 1 \n\
endif \n\
 \n\
if $framevar > "+ str(FRAME_COUNT-1) + "\n\
	$framevar = 0 \n\
endif \n\
 \n\
[TextureOverride{modname}] \n\
hash = {hash} \n\
run = CommandlistFrame \n\
$active = 1 \n\
 \n\
[CommandlistFrame] \n\
if $framevar == 0 \n\
	ps-t0 = Resource{modname}0 \n"

for i in range(FRAME_COUNT-1):
	configfilecontent += \
"\
else if $framevar == " + str(i+1) +" \n\
	ps-t0 = Resource{modname}"+ str(i+1) +" \n"

configfilecontent += \
"endif \n\
 \n"

for i in range(FRAME_COUNT):
	configfilecontent += \
"\
[Resource{modname}"+ str(i) +"] \n\
filename = {modname}"+ str(i) +".jpg \n\
\n"

f.write(configfilecontent.format(modname = modName, hash = lightconeimagehash))
f.close()
print('Done!')
