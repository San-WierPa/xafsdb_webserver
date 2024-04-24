## Regarding scicat testing / production!
+ Production: only use `host="http://34.29.91.220"`, i.e. this and only this VM-instance
  is consistenly running, hence the webserver -and website are accessible.
+ Development: In order to work locally, i.e. on `http://127.0.0.1:8001/`, please:
  + Turn on dev-google VM-instance,
  + Copy / paste the dev-host-url into: `auto_bl_create.py`, `auto_dataset_create.py`
    and (IMPORTANT) in `_auth_constants.py`!
    (and optional: `README_dev.md`) and comment out the production-host-url.
  + Now, datasets that are uploaded should appear locally (but are not stored in production),
    BLs as well.
  + When testing finished: uncomment production-host-url
    (not that the webserver-docker-image would by mistake have the dev-host-url)
+ Most amazingly, now possible to upload a dataset locally and it is visible locally as well,
  but not in production.
  **NOTE**: Dataset can only be visible after setting `is_published` to `true`.

## Docker

+ Check requirements (imports) and add them if necessary to
  `requirements.txt`

+ Login to docker (atm via hzdr gitlab):
```shell
docker login registry.hzdr.de
```
**NOTE**: `username`: paripsa, `password`: (see gitlab.hzdr.de credentials)

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

+ Regarding `unit_test`:
  - Remember importing relative to root, e.g.
  ```shell
  from ..xafsdb_web.utils import term_checker
  ```
  - Change to correct directory:
  ```shell
  cd /home/sepa/Desktop/xafs-db/xafsdb/
  ```
  - Finally, run the test from this directory:
  ```shell
  python -m unittest webserver.test.test_utils
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
ssh -i /home/sepa/.ssh/google_cloud_ssh_key paripsa_uni_wuppertal_de@35.233.73.213
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

+ To clean up, that is, to remove all unused containers, volumes, networks and images (both dangling and unreferenced):
```shell
docker system prune
```
**WARNING**: Never ever do `system prune`. Only in an apocalyptic scenario maybe (deletes also scicat image and stuff)!
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
PASSWORD = env("PASSWORD_AUTH")

CONFIGURATION = scicat_py.Configuration(
    # production
    host="http://34.29.91.220",
    # dev (varies due to shut-down/restart of vm - every restart changes ip)
    # host="http://35.232.106.48",
)
```
**NOTE**: AFTER TESTING ON DEV-HOST ON GOOGLE VM, BUT BEFORE DOCKER-COMPOSE ON PRODUCTION-HOST, FIRST TEST LOCAL WITH PRODUCTION-HOST URL!!!

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
http://34.29.91.220/mongodb/db/scicat/
```

+ For deleting (flush) datasets, do not forget to delete ALL relational entries in the database (e.g. attachment with the same datasetId)
**NOTE** Deleting atm only manually, since the db is persistent and the vm does not have a mongosh!

**TODO**
```shell
mongo-express_1    | Mongo Express server listening at http://0.0.0.0:8081
mongo-express_1    | Server is open to allow connections from anyone (0.0.0.0)
mongo-express_1    | basicAuth credentials are "admin:pass", it is recommended you change this in your config.js!
```

### Google & mongodb

In order to have `auto_bl_create.py` working, i.e. no 500 appearing while trying to upload $>1$ beamline, the `Instrument` entry in mongodb needs to be adjusted this way:

+ Access to the mongodb shell via ssh only via docker (since its all about images):
  + Check the image via `docker ps`
  + Log "into" docker: `sudo docker exec -it 074b69e456cc bash`
  + Log into the mongodb shell: `mongo`
  + Now you're good to go and mess things up (be careful!)!
+ A few steps:
  + `show dbs`, `use scicat`
  + For example, if some nasty identifier is not doing what it "supposed" to do:
    `db.Instrument.dropIndex("datasets.pid_1")` and then
    `db.Instrument.createIndex({"datasets.pid": 1}, {unique: false, background: true})`

### Google & pip

If already have a running container and just want to execute a single command without starting a Bash session, use the `docker exec` command.
+ Check installed python packages inside container:
  `docker exec -it my_container pip list`

## PIPELINE

**TODO**
+ Following steps ought to be automated (see also gitlab CI):

+ Change in vscode (locally):
  - `commit` AND `push` to gitlab
  - `docker build` AND `docker push registry.hzdr.de/daphne4nfdi/xafsdb`
+ Google-vm -> in `paripsa_uni_wuppertal_de@wupp-1:/sebastian/xafsdb/`:
  - `git pull` AND `docker pull registry.hzdr.de/daphne4nfdi/xafsdb`
    (for dev: `docker pull registry.hzdr.de/daphne4nfdi/xafsdb/xafsdb_devenv:latest`)
    (or `docker pull registry.hzdr.de/daphne4nfdi/xafsdb/refxas_beta_test:latest`)
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

## Misc

+ Footer: Either `<span id="date"></span>` or simply `start-year to end-year`?
+ Automatic email: at the moment via `gmail`. Please see<hr>
  `https://dev.to/abderrahmanemustapha/how-to-send-email-with-django-and-gmail-in-production-the-right-way-24ab`<hr>
  for more info (and for resetting).

## Benchmarking

+ Use siege (command-line-tool) in order to execute test on websites via
`siege -c200 -d10 -t30s http://xafsdb.ddns.net/`
This command simulates 200 concurrent users, each delayed by up to 10 seconds between requests,
for a total test time of 30 seconds.
Output:
```shell
Transactions:                   7884 hits
Availability:                 100.00 %
Elapsed time:                  30.04 secs
Data transferred:             132.40 MB
Response time:                  0.28 secs
Transaction rate:             262.45 trans/sec
Throughput:                     4.41 MB/sec
Concurrency:                   74.60
Successful transactions:        7132
Failed transactions:               0
Longest transaction:            5.56
Shortest transaction:           0.06
```

## Docs

### Sphinx

+ First, start the venv with
```shell
source /home/sepa/Desktop/xafs-db/xafsdb/webserver/docs/venv/bin/activate
```
and Sphinx can be used inside the `cd/venv` only with the full path:
```shell
/home/sepa/Desktop/xafs-db/xafsdb/webserver/docs/venv/bin/sphinx-quickstart
```

+ Start Documenting:<br>
  Begin creating or editing your .rst (reStructuredText) or .md (Markdown, if configured) files.<br>
  The index.rst file is your documentation's root, from which you can link to other documentation files.

+ Build Your Documentation:<br>
  To generate your documentation, run the following command from the directory containing the Makefile<br>
  (typically the root of your docs directory):
```shell
make html
```

+ View Your Documentation:<br>
  Open the generated HTML files in your web browser. For example, you can open `build/html/index.html`<br>
  to view the root page of your documentation.
<!--<div>
            <a href="https://github.com/SciCatProject" target="_blank">
                <img class="responsive_coll" src="{% static 'img/SciCatLogo.png' %}" alt="scicat" style="object-fit:contain; background-color: white;" ></a>
        </div>

        <div>
            <a href="https://www.daphne4nfdi.de/english/index.php" target="_blank">
                <img class="responsive_daph" src="{% static 'img/daphne.png' %}" alt="daphne" style="object-fit:contain; background-color: white;" ></a>
        </div>-->

# Outreach

In order to have badges and proper formatting, please use `isort` and `black`, e.g.:
  ```shell
  python -m isort test/test_utils.py
  ```
  and
  ```shell
  python -m black test/test_utils.py
  ```
**NOTE**: Firstly `black`and secondly `isort`!

## Linter / Formatting django

For the django.htmls: use `python -m pip install djlint` via e.g.
  ```shell
  python -m djlint login.html --profile django
  ```
and formatting via:
  ```shell
  python -m djlint login.html --profile django --reformat
  ```
**NOTE**: Reformatting django-htmls may cause syntax errors...