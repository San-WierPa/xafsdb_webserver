docker build -t registry.hzdr.de/daphne4nfdi/xafsdb .
docker push registry.hzdr.de/daphne4nfdi/xafsdb

ssh -i /home/sepa/.ssh/google_cloud_ssh_key paripsa_uni_wuppertal_de@35.233.84.253