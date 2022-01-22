killall screen

cd /opt/ASP/
screen -d -m -S ASP sh /opt/ASP/start_ASP.sh 
cd /opt/Xdesk/
screen -d -m -S console python3 /opt/Xdesk/console.py 
screen -d -m -S Editor python3 /opt/Xdesk/Editor.py 

sleep 2
screen -ls
echo "BOOT END"
sleep 10;
