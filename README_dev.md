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

+ Testing via docker registry (via gitlab):
```shell
docker run registry.hzdr.de/daphne4nfdi/xafsdb
```

+ Purely locally (mainly for debugging after local changes):
```shell
docker run -p 8000:8000 <image-id>
```

+ Testing via `uvicorn` (in root -> `manage.py`) (`reload` only under linux):
```shell
uvicorn webserver.asgi:application --port 8001 --reload
```
**NOTE**: First do(!!!)
```shell
pip install -r requirements.txt
```
and
```shell
pip install -r requirements_create.txt
```

## Testing via feature- and dev-branch

  - Before starting any new work, make sure you are on the development branch by running git checkout dev in your terminal.
  - Create a new feature branch for your work by running git checkout -b my-feature where "my-feature" is a descriptive name for your branch.
  - Make changes to the code, commit frequently, and push your feature branch to the remote repository with git push -u origin my-feature.
  - Once your work is complete and tested, it's time to merge it back into the development branch. First, switch to the dev branch with git checkout dev.
  - Merge your feature branch into the development branch with git merge my-feature.
  - Resolve any merge conflicts that arise. These can often be resolved automatically by Git, but sometimes manual intervention is required.
  - Once the conflicts are resolved, run your tests on the dev branch to make sure everything is still working as expected.
  - If all tests pass, push the changes to the remote dev branch with git push.
  - After pushing the changes to the development branch, it's time to deploy to production. Depending on your deployment process, this might involve creating a new build, running tests in a production-like environment, and deploying the new build to your production servers.
  - Once the new build is deployed, monitor your production environment closely for any issues that may arise. If you do discover issues, you may need to roll back the changes to the previous version of your code.
  - Repeat this process as necessary, always working on feature branches and merging them into the development branch before deploying to production.

### 'git fetch' and 'git pull'

Both commands that are used to update the local repository with changes from a remote repository. However, they work in slightly different ways.
- `git fetch` retrieves the latest changes from the remote repository and stores them in the local repository, but it does not automatically merge the changes with the local code. This means that 'git fetch' only updates the local repository's view of the remote repository, but it does not modify your local code or any of your local branches. You can use 'git fetch' to preview changes made by other developers without making any changes to your local code.
- 'git pull', on the other hand, does two things: it retrieves the latest changes from the remote repository and automatically merges them with your local code. This means that 'git pull' updates both your local repository's view of the remote repository and your local code or branch. This can be useful if you want to quickly update your code with the latest changes from the remote repository and don't need to preview the changes before merging them.
- In summary, 'git fetch' updates your local repository's view of the remote repository without modifying your local code or branch, while 'git pull' updates both your local repository's view of the remote repository and your local code or branch by merging the changes automatically.

### 'git stash'

- `git stash` is a Git command that allows you to temporarily save and set aside changes that you have made to your working directory, without committing them to your Git repository. This can be useful if you need to switch to a different branch or work on a different task, but are not ready to commit your current changes yet.
- When you run 'git stash', Git will take all of the changes in your working directory that have not yet been committed and save them to a special area called the "stash". This area is separate from your Git repository, and allows you to store your changes without creating a new commit. Once your changes have been stashed, your working directory will revert to the state it was in at the last commit.
- You can then switch to a different branch, or work on a different task, and come back to your stashed changes later. To retrieve your stashed changes, you can use the `git stash apply` command, which will apply the most recent stash to your working directory. You can also use the `git stash pop` command, which will apply the most recent stash and remove it from the stash list.

Here's an example of how to use git stash:

  - Make some changes to your working directory that you don't want to commit yet.
  - Run `git stash` to stash your changes.
  - Switch to a different branch or work on a different task.
  - When you're ready to retrieve your stashed changes, run `git stash apply` or `git stash pop`.

Note that if you have multiple stashes, you can specify which stash you want to apply by using the `git stash apply <stash>` or `git stash pop <stash>` command, where '<stash>' is the name or index of the stash you want to apply. You can also list all of your stashes by running 'git stash list'.

## Python tests

+ In Django, the python manage.py test command is used to run all of the tests for the project. This command uses the built-in unittest module to discover and run the test cases in the project.

Using python manage.py test has a few advantages over using unittest directly:

    - It automatically sets up the Django environment for the     tests, which includes configuring the database and loading the project's settings.

    - It provides a consistent interface for running tests across different Django projects.

    - It allows for more fine-grained control over the tests, such as running only specific tests or excluding tests with certain tags.

    - It integrates with other Django features, such as test fixtures, which can make it easier to set up test data.

That being said, it is still possible to use unittest directly to run tests in a Django project. However, in most cases, using python manage.py test is the recommended approach.

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

+ To kill and delete container (basically clean):
```shell
docker ps -aq | xargs docker stop | xargs docker rm
```

+ To clean up, that is to remove all unused containers, volumes, networks and images (both dangling and unreferenced):
```shell
docker system prune
```
And
```shell
docker image prune -a
```
**Warning**
When using first `system prune` and then `image prune`, the cleansing is much deeper. Also working scicat-images might disappear!

+ With more control than the above, we can limit the pruning down to a single part, like the images, by issuing something like:
```shell
docker image prune
```


+ To build using custom Dockerfile:
```shell
docker build -t xafsdb_create:0.0.1 -f Dockerfile.dev .
```

+ Run with parameters and input:
```shell
docker run -e USERNAME_AUTH=admin -e PASSWORD_AUTH=mypwd -i -t xafsdb_create:0.0.1
```

respectively for running in the background (and specific Container `ca...`):
```shell
docker run --detach --name ca98108987de -e USERNAME_AUTH=admin -e PASSWORD_AUTH=mypwd xafsdb_create:0.0.1
```

+ In order to create a dataset of a file from OUTSIDE of the container, the user need to run (atm):
```shell
docker run -e USERNAME_AUTH=admin -e PASSWORD_AUTH=mypwd --mount type=bind,source=/home/sepa/Desktop/test.dat,target="/opt/app/quality_control/example data/LABORATORY/test.dat" -i -t xafsdb_create:0.0.1
```
**NOTE**: `--mount` is clear. `-v` (volume) cannot be used, since it is always creating a directory as a target inside the container!
**NOTE**: Mounting source requires `absolut path`!
**TODO**: Possible to use os.environ('FILE') and docker run with `-e FILE=test.dat`?

**NOTE**: https://www.howtogeek.com/devops/how-to-share-docker-images-with-others/

To share the docker with other, use (atm):
```shell
docker save xafsdb_create:0.0.1 > xafsdb_create.tar
```
Load it on the new host computer via
```shell
docker load < xafsdb_create.tar
```

**TODO**: Better solution would be to use docker repository.

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

+ `Flush` under `docker-compose`:
  - First, make sure that your Docker Compose setup is running `docker-compose up -d`
  - Once your Docker Compose setup is running, open a new terminal window and navigate to the directory where your Django project is located.
  - Run the command:
  ```shell
  docker-compose exec web python manage.py flush
  ```
  This command will execute the flush command inside the web container. The web container is the container that runs your Django project.
  - The flush command will clear the database and reset all the tables. Once the command finishes executing, you can exit the terminal window.

+ Enter the db.sqlite3 via command line:
```shell
python manage.py dbshell
```

### MongoDB

+ Access mongodb-express (browser) via (use admin and password out of `_auth_constants.py`):
```
http://35.233.84.253/mongodb/db/scicat/
```

+ For deleting (flush) datasets, do not forget to delete ALL relational entries in the database (e.g. attachment with the same datasetId)
**NOTE** Deleting atm only manually, since the db is persistent and the vm does not have a mongosh!

**TODO**
```shell
mongo-express_1    | Mongo Express server listening at http://0.0.0.0:8081
mongo-express_1    | Server is open to allow connections from anyone (0.0.0.0)
mongo-express_1    | basicAuth credentials are "admin:pass", it is recommended you change this in your config.js!
```


## PIPELINE

**TODO**
+ Following steps ought to be automated (see also gitlab CI):

+ Change in vscode (locally):
  - `commit` AND `push` to gitlab
  - `docker build` AND `docker push registry.hzdr.de/daphne4nfdi/xafsdb`
+ Google-vm -> in `paripsa_uni_wuppertal_de@wupp-1:/sebastian/xafsdb/`:
  - `git pull` AND `docker pull registry.hzdr.de/daphne4nfdi/xafsdb`
  - Then `cd xafsdb_deployment` AND `docker-compose up -d`


## Backup of both databases

+ Start docker-compose with
```shell
docker-compose --env-file .env up -d
```

### Static

+ Locally:
```shell
python manage.py collectstatic
```

+ GVM:
```shell
docker-compose exec web python manage.py collectstatic
```