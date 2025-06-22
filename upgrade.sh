set -e

#sh -c 'cd /opt/LibreLight/Xdesk/; git status'
echo "upgrade LibreLight from git master ?"
echo " press enter to run"
read X

#echo $X
#read -p -t $Xa 
#x=read

cd /opt/LibreLight/git/
pwd
ls -l
rm -rf LibreLightASP
#!/usr/bin/dash

rm -rf ASP
#git clone https://github.com/micox4356/LibreLightASP.git
git clone https://gogs.librelight.de/librelight/ASP.git
#rsync -apv --delete /opt/LibreLight/git/LibreLightASP/ /opt/LibreLight/ASP/
rsync -apv --delete /opt/LibreLight/git/ASP/ /opt/LibreLight/ASP/
pwd
ls -l

echo
cd /opt/LibreLight/git/ASP
git remote -v
echo

# -----------------------------------------------------
cd /opt/LibreLight/git/
rm -rf LibreLight
rm -rf Xdesk
pwd
ls -l
#git clone https://github.com/micox4356/LibreLight.git
git clone https://gogs.librelight.de/librelight/Xdesk.git
cd /opt/LibreLight/git/
#rsync -apv --delete /opt/LibreLight/git/LibreLight/ /opt/LibreLight/Xdesk/
rsync -apv --delete /opt/LibreLight/git/Xdesk/ /opt/LibreLight/Xdesk/
pwd
ls -l

echo
cd /opt/LibreLight/git/ASP
git remote -v
echo ""
echo "ENDE"
read X 
#read -p -t 1 
