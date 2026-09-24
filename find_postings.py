import requests

def find_amazon_jobs():
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

def find_all_jobs():
    all_jobs = []
    amazon_jobs = find_amazon_jobs()
    all_jobs += amazon_jobs

    return all_jobs