import bcolors
from modules.functions import imreadgray
from modules.functions import flip

print(bcolors.HEADER, "  _____       _            _        _____ _       ")
print("  / ____|     | |          (_)      / ____(_)      ")
print(" | (___   __ _| | __ _ _ __ _ _____| (___  _ _   _ ")
print("  \___ \ / _` | |/ _` | '__| |______\___ \| | | | |")
print("  ____) | (_| | | (_| | |  | |      ____) | | |_| |")
print(" |_____/ \__,_|_|\__,_|_|  |_|     |_____/|_|\__, |")
print("                                              __/ |")
print("                                             |___/ ", bcolors.ENDC)

# Beolvasás szürkeárnyalatos képként
picture = 'sima'

img = imreadgray('../pictures/' + picture + '.png')

# Értékek átkonvertálása 0-255
img = flip(img)

print(img)
