screen -ls
set -e
screen -XS ASP quit | echo ""
screen -XS console quit | echo ""
screen -XS Editor quit | echo ""
#killall screen | echo  ""
#killall SCREEN | echo  ""
path="/opt/LibreLight"
cd "$path"
screen -d -m -S ASP sh $path/ASP/start_ASP.sh 
cd $path/Xdesk/
screen -d -m -S console python3 $path/Xdesk/console.py 
sleep 3;
#xterm -e 'screen -r DMX'
xfce4-terminal -e 'screen -r DMX' --hide-menubar --zoom=-2 --geometry=90x35+800+520
sleep 2
screen -d -m -S Editor python3 $path/Xdesk/LibreLightDesk.py 

screen -ls
echo "BOOT END"
sleep 3;
