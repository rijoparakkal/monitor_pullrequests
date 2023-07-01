
# Monitor Pullrequests
 - git.py is useful to create a report on all pull
   requests(Open, In-progress and closed) in last 1 week
- It is also sending the report to manager using smtp
- We are using three env variables for this script
		- SMTP_USER - Since we are using SES for sending mail we need to specify the SMTP username which is generated from AWS
		- SMTP_PASS - Smtp password
		- MANAGER_EMAIL - Manager email

## Setting environment variables in Linux

 - Command we can use `export SMTP_USER="XXXXX"`

## Docker file and creating containers

- We have containerized the script using docker and we need to pass 3 env variables while running the containers
- Commands we need run
- `docker build -t gitapp .`
- `docker run -e SMTP_USER="*******" -e SMTP_PASS="****" -e "MANAGER_EMAIL=rijoparakkal@gmail.com" gitapp`
