import cv2
# Var

print('HONKAI STAR RAIL MOD SCRIPT - VIDEO TO LIGHTCONE')
print('This Scripts Converts Video into pictures and config file for lightcone mods in honkai star rail')

modName = input('Enter Mod Name(needs to be unique than other mods.... i think.... ) : ')
while modName == '':
	modName = input('Mod name cannot be empty. \n\
	Enter Mod Name(needs to be unique than other mods.... i think) : ')

videofilename = input('Enter file name e.g. sample.mp4 : ') 
while videofilename == '':
	modName = input('File cannot be empty. \n\
	Enter file name e.g. sample.mp4 : ') 

lightconeimagehash = input ("Enter Lightcone hash e.g. 89881665 for A Secret Vow (you can look up the hash in txt file in this folder) :")
while lightconeimagehash == '':
	lightconeimagehash = input('Hash cannot be empty. \n\
	Enter Lightcone hash e.g. 89881665 for A Secret Vow (you can look up the hash in txt file in this folder) :') 

# Param
MIN_FRAMES = 15
FRAME_COUNT = 15
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
while success and count < 15:
    if frame_count % inc == 0:
        image_rotated = cv2.rotate(image, cv2.ROTATE_180)
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
if $framevar > 14 \n\
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
	ps-t0 = Resource{modname}00 \n\
else if $framevar == 1 \n\
	ps-t0 = Resource{modname}01 \n\
else if $framevar == 2 \n\
	ps-t0 = Resource{modname}02 \n\
else if $framevar == 3 \n\
	ps-t0 = Resource{modname}03 \n\
else if $framevar == 4 \n\
	ps-t0 = Resource{modname}04 \n\
else if $framevar == 5 \n\
	ps-t0 = Resource{modname}05 \n\
else if $framevar == 6 \n\
	ps-t0 = Resource{modname}06 \n\
else if $framevar == 7 \n\
	ps-t0 = Resource{modname}07 \n\
else if $framevar == 8 \n\
	ps-t0 = Resource{modname}08 \n\
else if $framevar == 9 \n\
	ps-t0 = Resource{modname}09 \n\
else if $framevar == 10 \n\
	ps-t0 = Resource{modname}10 \n\
else if $framevar == 11 \n\
	ps-t0 = Resource{modname}11 \n\
else if $framevar == 12 \n\
	ps-t0 = Resource{modname}12 \n\
else if $framevar == 13 \n\
	ps-t0 = Resource{modname}13 \n\
else if $framevar == 14 \n\
	ps-t0 = Resource{modname}14 \n\
endif \n\
 \n\
[Resource{modname}00] \n\
filename = {modname}0.jpg \n\
 \n\
[Resource{modname}01] \n\
filename = {modname}1.jpg \n\
 \n\
[Resource{modname}02] \n\
filename = {modname}2.jpg \n\
 \n\
[Resource{modname}03] \n\
filename = {modname}3.jpg \n\
 \n\
[Resource{modname}04] \n\
filename = {modname}4.jpg \n\
 \n\
[Resource{modname}05] \n\
filename = {modname}5.jpg \n\
 \n\
[Resource{modname}06] \n\
filename = {modname}6.jpg \n\
 \n\
[Resource{modname}07] \n\
filename = {modname}7.jpg \n\
 \n\
[Resource{modname}08] \n\
filename = {modname}8.jpg \n\
 \n\
[Resource{modname}09] \n\
filename = {modname}9.jpg \n\
 \n\
[Resource{modname}10] \n\
filename = {modname}10.jpg \n\
 \n\
[Resource{modname}11] \n\
filename = {modname}11.jpg \n\
 \n\
[Resource{modname}12] \n\
filename = {modname}12.jpg \n\
 \n\
[Resource{modname}13] \n\
filename = {modname}13.jpg \n\
 \n\
[Resource{modname}14] \n\
filename = {modname}14.jpg \n\
"
f.write(configfilecontent.format(modname = modName, hash = lightconeimagehash))
f.close()
print('Done!')