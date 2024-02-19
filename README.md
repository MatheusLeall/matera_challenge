## Matera challenge

#### Loan API Project

##### This project uses [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) to run it on your machine. To run it, you'll need to install them. If you already have them on your machine, you'll now need to set the values of the `DJANGO_SECRET_KEY` and `DJANGO_DEBUG` variables in the project's `.env` file. Remember, these values are secret and should not be exposed in the repository for security reasons.

##### You may need to give execute permission to the files inside the script folder. To do this, run the following command:

```bash
sudo chmod +x scripts/file_name.sh
```

##### After completing the steps above, run the following command inside the folder where the docker-compose.yaml file is located:

```bash
docker-compose up app
```

##### If it's the first time running the project, it will be built and executed.

> **Warning:** If any issues occur during the project execution, simply run the command **_docker-compose up --build app_**, and the project will be rebuilt, resolving the issue.

##### Before starting to use the API, you'll need to create a user. This can be done by running the command below. Enter the username, email (optional), and password when prompted.

```bash
python manage.py createsuperuser
```

> **Warning:** Since sqlite3 was used in the project (to be as lightweight as possible), you may encounter an error when creating a user for the first time. If this happens, run **_sudo chmod 777 db.sqlite3_** in the project folder to grant read and write permissions to everyone on the database file. After doing this, run the above step again, and the user should be created.

##### After creating the user, you'll need to create a token for them. In the admin panel (localhost:8000/admin), access the Tokens resource. In the upper right part of the screen, click on ADD TOKEN +, select the user you created, and click SAVE.

##### With your user and token properly created, access the API (localhost:8000/api/v1/swagger) and click on the token endpoint. By clicking Try it out, you'll need to enter the username and password of the user you created in the previous step. After clicking execute, your authentication token will be returned.

##### Copy the returned token, click Authorize at the top right of the screen, then type Token and paste the token you copied (your input should be Token copied_token), and click Authorize to authenticate yourself to the API.

##### Now you can use the API freely through its documentation.

##### Oh, if you want to run the project's tests, you can also use docker-compose. There's a service for that:

```bash
docker-compose up integration-tests
```