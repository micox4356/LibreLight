set -e
killall screen | echo  ""
killall SCREEN | echo  ""
path="/opt/LibreLight"
cd "$path"
screen -d -m -S ASP sh $path/ASP/start_ASP.sh 
cd $path/Xdesk/
screen -d -m -S console python3 $path/Xdesk/console.py 
screen -d -m -S Editor python3 $path/Xdesk/LibreLightDesk.py 

sleep 2
screen -ls
echo "BOOT END"
sleep 10;
