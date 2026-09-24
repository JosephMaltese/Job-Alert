from database import (
    initialize_database,
    insert_job,
    job_exists,
)
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from find_postings import find_all_jobs

# Jobs will be represented as a dictionary containing the following keys:
# id
# company
# posting_date
# title
# link
# city
# country
# Note: Some keys may have to be optional depending on other apis

load_dotenv()

def send_email(jobs):
    message = EmailMessage()
    message["From"] = os.getenv("EMAIL_ADDRESS")
    message["To"] = os.getenv("RECIPIENT_EMAIL_ADDRESS")
    message["Subject"] = f"💻 New SWE Internships! 🎉"
    message_content = """
        New internship postings found! Apply ASAP to give yourself the best chances 😊

        """
    for job in jobs:
        message_content += f"""
        {job["title"]}
        {job["company"]}
        {job["city"]}, {job["country"]}
        Posting Date: {job["posting_date"]}
        Apply Here: {job["link"]}

        """
    message.set_content(
        message_content
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(
            os.getenv("EMAIL_ADDRESS"),
            os.getenv("EMAIL_APP_PASSWORD")
        )

        smtp.send_message(message)

if __name__ == '__main__':
    new_jobs = []
    initialize_database()
    all_jobs = find_all_jobs()
    
    for job in all_jobs:
        if not job_exists(job["id"], job["company"]):
            # Add job to alert list and then add to db
            new_jobs.append(job)
            insert_job(job["id"], job["company"], job["title"])
    
    if len(new_jobs) > 0:
        send_email(new_jobs)
    else:
        print("No email sent")