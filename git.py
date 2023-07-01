import requests
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import os
smtp_user = os.environ.get("SMTP_USER")
smtp_pass = os.environ.get("SMTP_PASS")
receiver_email = os.environ.get("MANAGER_EMAIL")
#github api url
URL = "https://api.github.com"
#repository
OWNER = "aws"
NAME = "eks-anywhere"
# Date Range specifications
start_date = (datetime.now() - timedelta(weeks=1)).strftime("%Y-%m-%d")
# Query to search for all open pull requests which are created before start_date
query_open = f"repo:{OWNER}/{NAME} is:pr is:open created:>{start_date}"
# Query to search for all draft/in-progress pull requests which are created before start_date
query_in_progress = f"repo:{OWNER}/{NAME} is:pr is:draft created:>{start_date}"
# Query to search for all closed pull requests which are created before start_date
query_closed = f"repo:{OWNER}/{NAME} is:pr is:closed created:>{start_date}"
# Extra parameter specifications
search_url = f"{URL}/search/issues"
search_open = {"q": query_open}
search_in_progress = {"q": query_in_progress}
search_closed = {"q": query_closed}
headers = {"Accept": "application/vnd.github.v3+json"}
# API call for open Pull requests
response_open = requests.get(search_url, params=search_open, headers=headers).json()
# API call for Draft/In progress pull requests
response_in_progress = requests.get(search_url, params=search_in_progress, headers=headers).json()
# API call for closed pull requests
response_closed = requests.get(search_url, params=search_closed, headers=headers).json()
# Initialize the array
opened_prs = []
closed_prs = []
inprogress_prs = []

for item in response_open.get("items"):
    pr = item.get("pull_request")
    if pr:
        pr_info = {
            "URL": pr.get("html_url"),
        }
        opened_prs.append(pr_info)
for item in response_in_progress.get("items"):
    pr = item.get("pull_request")
    if pr:
        pr_info = {
            "URL": pr.get("html_url"),
        }
        inprogress_prs.append(pr_info)
for item in response_closed.get("items"):
    pr = item.get("pull_request")
    if pr:
        pr_info = {
            "URL": pr.get("html_url"),
        }
        closed_prs.append(pr_info)

# Generate the email summary report
report = f"Dear Manager,\n\nHere is the summary of Pull Requests for {OWNER}/{NAME} in the last week:\n\n"
report += f"- Opened Pull Requests ({len(opened_prs)}):\n"
for pr in opened_prs:
    report += f"  - {pr['URL']}\n"
report += f"\n- Inprogress Pull Requests ({len(inprogress_prs)}):\n"
for pr in inprogress_prs:
    report += f"  - {pr['URL']}\n"
report += f"\n- Closed Pull Requests ({len(closed_prs)}):\n"
for pr in closed_prs:
    report += f"  - {pr['URL']}\n"

# Send the report via email (Example: using the 'smtplib' library)
# Provide your email sending logic here
# SES SMTP configurations
smtp_server = "email-smtp.us-west-2.amazonaws.com"
smtp_port = 587
sender_email = "rjoseph@binaryfountain.com"
email_subject = "Pull Requests Summary"

# Create the email message
message = MIMEText(report)
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = email_subject
print("From:"+message["From"])
print("To:"+message["To"])
print("Subject:"+message["Subject"])
print("Body:\n"+report)
# Send the email using SES SMTP
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email. Error: {e}")
