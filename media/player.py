# importing vlc module
import vlc
 
# importing time module
import time
import os

HOME = os.getenv('HOME')
 
media_path = HOME+"/LibreLight/music/"  
fname = "1.mp3"
def play(): 
    # creating vlc media player object
    media_player = vlc.MediaPlayer()
     
    # media object
    media = vlc.Media(media_path+fname)#death_note.mkv")
     
    # setting media to the media player
    media_player.set_media(media)
     
     
    # start playing video
    media_player.play()
    return media_player
# wait so the video can be played for 5 seconds
# irrespective for length of video
#time.sleep(5)
media_player = play()
#time.sleep(1)
#media_player1 = play()

#for i in dir(media_player):
#    print(i)
##input() 
while 1:
    t = media_player.get_time()
    print([t,media_player.get_length(),media_player.get_state()],end=" ")
    print( media_path,fname)
    if t > 1000:
        if vlc.State.Playing == media_player.get_state():
            media_player.pause()
        time.sleep(0.1)
#
#    #    media_player.set_time(1)
#    #    #break
## getting media
#value = media_player.get_media()
# 
## printing media
#print("Media : ")
#print(value)

