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

    count = len(jobs)
    message["Subject"] = f"💻 New SWE Internship{'s' if count > 1 else ''}"

    # Text fallback
    message_content = f"New internship posting{'s' if count > 1 else ''} found! Apply ASAP to give yourself the best chances😊\n\n"
    for job in jobs:
        message_content += (
            f"{job["title"]}\n"
            f"{job["company"]}\n"
            f"{job["city"]}, {job["country"]}\n"
            f"Posting Date: {job["posting_date"]}\n"
            f"Apply Here: {job["link"]}\n\n"
        )
    message.set_content(message_content)

    # HTML version
    job_cards = ""

    for job in jobs:
        job_cards += f"""
        <div style="
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 18px;
            margin-bottom: 16px;
        ">
            <h2 style="margin: 0 0 6px 0; font-size: 18px;">
                {job["title"]}
            </h2>

            <p style="margin: 0 0 12px 0; color: #555;">
                <strong>{job["company"]}</strong><br>
                📍 {job["city"]}, {job["country"]}<br>
                📅 Posted {job["posting_date"]}
            </p>

            <a href="{job["link"]}"
               style="
                   display: inline-block;
                   padding: 10px 16px;
                   background: #111;
                   color: white;
                   text-decoration: none;
                   border-radius: 6px;
                   font-weight: bold;
               ">
                Apply →
            </a>
        </div>
        """
    
    html_content = f"""
    <html>
        <body style="
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: auto;
            padding: 20px;
            color: #111;
        ">
            <p style="color: #555; margin-top: 0; margin-bottom: 25px;">
                Found <strong>{count}</strong> new
                internship posting{'s' if count != 1 else ''}.
                Apply ASAP to give yourself the best chances 😊
            </p>

            {job_cards}

            <p style="
                color: #999;
                font-size: 12px;
                margin-top: 30px;
            ">
                Internship Monitor
            </p>
        </body>
    </html>
    """

    message.add_alternative(html_content, subtype="html")


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