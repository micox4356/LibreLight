set -e
echo "upgrade LibreLight from git master ?"
echo " press enter to run"
#read -p -t $Xa 
x=read
cd /opt/LibreLight/git/
pwd
ls -l
rm -rf LibreLightASP
#git clone https://github.com/micox4356/LibreLightASP.git
git clone https://gogs.librelight.de/librelight/ASP.git
#rsync -apv --delete /opt/LibreLight/git/LibreLightASP/ /opt/LibreLight/ASP/
rsync -apv --delete /opt/LibreLight/git/ASP/ /opt/LibreLight/ASP/
pwd
ls -l

cd /opt/LibreLight/git/
rm -rf LibreLight
pwd
ls -l
#git clone https://github.com/micox4356/LibreLight.git
git clone https://gogs.librelight.de/librelight/Xdesk.git
#rsync -apv --delete /opt/LibreLight/git/LibreLight/ /opt/LibreLight/Xdesk/
rsync -apv --delete /opt/LibreLight/git/Xdesk/ /opt/LibreLight/Xdesk/
pwd
ls -l
read -p -t 1 
