

#for ip in $(seq "%05g" 1 254); do
for ip in $(seq 1 254); do
    #echo $ip
    sh -c "ping -c 1 192.168.2.$ip | grep 'bytes from '" &
done

sleep 10
