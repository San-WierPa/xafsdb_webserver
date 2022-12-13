## Docker

+ Check requirements (imports) and add them if necessary to
  `requirements.txt`

+ Login to docker (atm via hzdr gitlab):
```shell
docker login registry.hzdr.de
```

+ Build the image:
```shell
docker build -t registry.hzdr.de/daphne4nfdi/xafsdb .
```

+ Check output, cp image-id
```shell
$ Successfully built <image-id>
$ Successfully tagged registry.hzdr.de/daphne4nfdi/xafsdb:latest
```

### Testing

+ Testing via docker registry:
```shell
docker run registry.hzdr.de/daphne4nfdi/xafsdb
```

+ Purely locally (mainly for debugging after local changes):
```shell
docker run -p 8000:8000 <image-id>
```

### Pre-deploy to gitlab -> atm hzdr

+ Push the image:
```shell
docker push registry.hzdr.de/daphne4nfdi/xafsdb
```

## Google-vm

**NOTE:**  It is not required to use `sudo` on this machine!

+ Connect to google-vm:
```shell
ssh -i /home/sepa/.ssh/google_cloud_ssh_key paripsa_uni_wuppertal_de@35.233.84.253
```
+ Out: `paripsa_uni_wuppertal_de@wupp-1:~$`

+ Execute script:
```shell
sh deploy.sh
```

### Docker

+ Login (You only need to login once per machine, the credentials are cached.)
```shell
docker login registry.hzdr.de
```

+ Run the image (only to check if the image works. The server cannot be accessed and needs
  all from xafsdb_deployment in order to function!)
```shell
docker run registry.hzdr.de/daphne4nfdi/xafsdb
```

### Docker-compose

+ Check what is running:
```shell
docker-compose ps
```
+ Out:
```shell
$               Name                             Command               State                 Ports
--------------------------------------------------------------------------------------------------------------
xafsdb_deployment_mongo-express_1   tini -- /docker-entrypoint ...   Exit 1
xafsdb_deployment_mongodb_1         /opt/bitnami/scripts/mongo ...   Up       27017/tcp
xafsdb_deployment_reverse-proxy_1   /entrypoint.sh --api.insec ...   Up       0.0.0.0:80->80/tcp,:::80->80/tcp
xafsdb_deployment_scicat_1          docker-entrypoint.sh node  ...   Up       3000/tcp
xafsdb_deployment_xafsdb_1          uvicorn --host 0.0.0.0 web ...   Up       8000/tcp
```

+ Stop all docker-compose processes:
```shell
docker-compose down
```

+ Start all services depicted in the docker-compose:
```shell
docker-compose up
```
+ Respectively:
```shell
docker-compose up -d
```

**TODO**
+ Add/connect `db.sqlite3` to `docker-compose.yml`
+ Add/connect `.env` to `docker-compose.yml` or `Dockerfile` (?)

### Dataset upload to google-vm

+ xafsdb_deployment/config/xafsdb/_auth_constants.py
```python
import scicat_py

USERNAME = env("USERNAME_AUTH")
# OLD -> PASSWORD = "2jf70TPNZsS"
PASSWORD = env("PASSWORD_AUTH")

CONFIGURATION = scicat_py.Configuration(
    host="http://35.233.84.253",
)
```

**TODO**
+ `USERNAME` and `PASSWORD` must be used in .env (as it is already on branch `master`) and overwritten by `docker-compose.yml`
+ `CONFIGURATION`: host can be public (also overwritten by `docker-compose.yml`) and `_auth_constants.py` can be deleted

## Databases

### Sqlite3

+ Contains entries for object storage

+ Deleting datasets is easy:
```shell
python manage.py flush
python manage.py makemigrations # optional?
python manage.py migrate
```

### MongoDB

+ Access mongodb-express (browser) via (use admin and password out of `_auth_constants.py`):
```
http://35.233.84.253/mongodb/db/scicat/
```

+ For deleting (flush) datasets, do not forget to delete ALL relational entries in the database (e.g. attachment with the same datasetId)
**NOTE** Deleting atm only manually, since the db is persistent and the vm does not have a mongosh!



## PIPELINE

**TODO**
+ Following steps ought to be automated (see also gitlab CI):

+ Change in vscode (locally):
  - `commit` AND `push` to gitlab
  - `docker build` AND `docker push registry.hzdr.de/daphne4nfdi/xafsdb`
+ Google-vm -> in `paripsa_uni_wuppertal_de@wupp-1:/sebastian/xafsdb/`:
  - `git pull` AND `docker pull registry.hzdr.de/daphne4nfdi/xafsdb`
  - Then `cd xafsdb_deployment` AND `docker-compose up -d`
