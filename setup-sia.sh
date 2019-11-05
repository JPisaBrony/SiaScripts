apt-get update

cd /SiaScripts

mkdir s3backer
cd s3backer
apt-get install libcurl4-openssl-dev libfuse-dev libexpat1-dev libssl-dev zlib1g-dev pkg-config autoconf automake -y
wget https://github.com/archiecobbs/s3backer/archive/1.5.4.tar.gz
tar -xzf 1.5.4.tar.gz
cd s3backer-1.5.4
./autogen.sh
./configure
make dist
make install

cd /SiaScripts

mkdir blk
mkdir mount
s3backer --size=75G --listBlocks main --region=fr-par --baseURL=https://s3.fr-par.scw.cloud/ blk
mount -o loop blk/file mount/

docker run \
  --detach \
  --volume /SiaScripts/mount/sia-node:/sia-data \
  --publish 127.0.0.1:9980:9980 \
  --publish 9981:9981 \
  --publish 9982:9982 \
  --name sia-container \
   mtlynch/sia
