import bcolors
from Common.functions import imreadgray
from Common.functions import flip

print(bcolors.OK, " _  ___             _                  _____ _           _ ")
print(" | |/ (_)           | |                / ____| |         (_)")
print(" | ' / _ _ __ ___   | |     ___  ___  | |    | |__   ___  _ ")
print(" |  < | | '_ ` _ \  | |    / _ \/ _ \ | |    | '_ \ / _ \| |")
print(" | . \| | | | | | | | |___|  __/  __/ | |____| | | | (_) | |")
print(" |_|\_\_|_| |_| |_| |______\___|\___|  \_____|_| |_|\___/|_|", bcolors.ENDC)

# Beolvasás szürkeárnyalatos képként
picture = 'sima'

img = imreadgray('../Common/' + picture + '.png')

# Értékek átkonvertálása 0-255
img = flip(img)

print(img)
