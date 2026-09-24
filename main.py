import requests
from database import (
    initialize_database,
    insert_job,
    job_exists,
    get_all_jobs
)
import json
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

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

def get_amazon_jobs():
    amazon_jobs = []

    res = requests.post(
        "https://www.amazon.jobs/api/jobs/search?is_als=true",
        json={
            "accessLevel": "EXTERNAL",
            "contentFilterFacets": [{
                "name": "primarySearchLabel",
                "requestedFacetCount": 9999,
                "values": [{"name": "studentprograms.team-internships-for-students"}]
            }],
            "excludeFacets": [
                {"name": "isConfidential", "values": [{"name": "1"}]},
                {"name": "businessCategory", "values": [{"name": "a-confidential-job"}]}
            ],
            "filterFacets": [{"name": "category", "requestedFacetCount": 9999, "values": [{"name": "Software Development"}]}],
            "includeFacets": [],
            "jobTypeFacets": [{"name": "employeeClass", "values": [{"name": "Intern"}]}],
            "locationFacets": [
                [
                    {"name": "country", "requestedFacetCount": 9999, "values": [{"name": "US"}]},
                    {"name": "normalizedStateName", "requestedFacetCount": 9999},
                    {"name": "normalizedCityName", "requestedFacetCount": 9999}
                ],
                [
                    {"name": "country", "requestedFacetCount": 9999, "values": [{"name": "CA"}]},
                    {"name": "normalizedStateName", "requestedFacetCount": 9999},
                    {"name": "normalizedCityName", "requestedFacetCount": 9999}
                ]
            ],
            "query": "",
            "size": 999,
            "sort": {"sortOrder": "DESCENDING", "sortType": "SCORE"},
            "start": 0,
            "treatment": "OM"
        },
        timeout=10
    )
    print("Response status code:", res.status_code)
    json_data = res.json()
    job_list = json_data["searchHits"]

    for job in job_list:
        fields = job["fields"]
        amazon_jobs.append({
            "id": fields["icimsJobId"][0],
            "company": "Amazon",
            "posting_date": fields["createdDate"][0],
            "title": fields["title"][0],
            "link": fields["urlNextStep"][0],
            "city": fields["city"][0],
            "country": fields["country"][0]
        })
    return amazon_jobs


def send_email(jobs):
    message = EmailMessage()
    message["From"] = os.getenv("EMAIL_ADDRESS")
    message["To"] = os.getenv("RECIPIENT_EMAIL_ADDRESS")
    message["Subject"] = f"💻 New SWE Internships! 🎉"
    message_content = """
        New internship postings found! Apply ASAP to give yourself the best chances.

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
    # new_jobs = []
    # initialize_database()
    # amazon_jobs = get_amazon_jobs()
    
    # for job in amazon_jobs:
    #     if not job_exists(job["id"], job["company"]):
    #         # Add job to alert list and then add to db
    #         new_jobs.append(job)
    #         insert_job(job["id"], job["company"], job["title"])
    
    # if len(amazon_jobs) > 0:
    #     send_email(amazon_jobs)
    send_email(
        [
            {
                "id": "123456",
                "company": "Amazon",
                "posting_date": "April 21, 2026",
                "title": "Software Engineer Intern",
                "link": "https://account.amazon.jobs/jobs/10552937/apply",
                "city": "Seattle",
                "country": "USA"
            },
            {
                "id": "123456",
                "company": "RBC",
                "posting_date": "April 29, 2026",
                "title": "Software Developer Intern",
                "link": "https://account.amazon.jobs/jobs/10552937/apply",
                "city": "Toronto",
                "country": "CAN"
            }
        ]
    )
