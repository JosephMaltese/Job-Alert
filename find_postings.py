import requests
from datetime import date

today = date.today()

def find_td_jobs():
    root_job_path = "https://td.wd3.myworkdayjobs.com/en-US/TD_Bank_Careers"
    td_jobs = []
    res = requests.post(
        "https://td.wd3.myworkdayjobs.com/wday/cxs/td/TD_Bank_Careers/jobs",
        json={
            "appliedFacets":{"locationCountry":["a30a87ed25634629aa6c3958aa2b91ea"],"jobFamily":["de769652963501ab29a8b80c0704c3aa","de769652963501e60b293b0d070431ab"]},
            "limit":20,
            "offset":0,
            "searchText":""
        },
        timeout=10)
    if res.status_code != 200:
        print("Failed to fetch TD jobs.")
        return
    res_json = res.json()
    jobs = res_json["jobPostings"]
    filtered_jobs = filter(lambda x: "software" in x["title"].lower() or "developer" in x["title"].lower() or "machine learning" in x["title"].lower(), jobs)

    for job in filtered_jobs:
        location  = job["locationsText"]
        location_split = location.split(",")
        if len(location_split) > 1:
            city = location_split[0]
            country = location_split[1]
        else:
            city = location_split[0]
            country = ""
        td_jobs.append({
            "id": job["bulletFields"][0],
            "company": "TD",
            "posting_date": str(today),
            "title": job["title"],
            "link": root_job_path + job["externalPath"],
            "city": city,
            "country": country
        })
    return td_jobs

def find_ibm_jobs():
    ibm_jobs = []
    res = requests.post(
        "https://www-api.ibm.com/search/api/v2", 
        json={
            "appId":"careers",
            "scopes":["careers2"],
            "query":{"bool":{"must":[]}},
            "post_filter":{"bool":{"must":[{"term":{"field_keyword_08":"Software Engineering"}},{"term":{"field_keyword_18":"Internship"}},{"bool":{"should":[{"term":{"field_keyword_05":"Canada"}},{"term":{"field_keyword_05":"United States"}}]}}]}},
            "aggs":{"field_keyword_172":{"filter":{"bool":{"must":[{"term":{"field_keyword_08":"Software Engineering"}},{"term":{"field_keyword_18":"Internship"}},{"bool":{"should":[{"term":{"field_keyword_05":"Canada"}},{"term":{"field_keyword_05":"United States"}}]}}]}},"aggs":{"field_keyword_17":{"terms":{"field":"field_keyword_17","size":6}},"field_keyword_17_count":{"cardinality":{"field":"field_keyword_17"}}}},"field_keyword_083":{"filter":{"bool":{"must":[{"term":{"field_keyword_18":"Internship"}},{"bool":{"should":[{"term":{"field_keyword_05":"Canada"}},{"term":{"field_keyword_05":"United States"}}]}}]}},"aggs":{"field_keyword_08":{"terms":{"field":"field_keyword_08","size":6}},"field_keyword_08_count":{"cardinality":{"field":"field_keyword_08"}}}},"field_keyword_184":{"filter":{"bool":{"must":[{"term":{"field_keyword_08":"Software Engineering"}},{"bool":{"should":[{"term":{"field_keyword_05":"Canada"}},{"term":{"field_keyword_05":"United States"}}]}}]}},"aggs":{"field_keyword_18":{"terms":{"field":"field_keyword_18","size":6}},"field_keyword_18_count":{"cardinality":{"field":"field_keyword_18"}}}},"field_keyword_055":{"filter":{"bool":{"must":[{"term":{"field_keyword_08":"Software Engineering"}},{"term":{"field_keyword_18":"Internship"}}]}},"aggs":{"field_keyword_05":{"terms":{"field":"field_keyword_05","size":1000}},"field_keyword_05_count":{"cardinality":{"field":"field_keyword_05"}}}}},
            "size":100,
            "sort":[{"_score":"desc"},{"pageviews":"desc"}],
            "lang":"zz",
            "localeSelector":{},
            "sm":{"query":"","lang":"zz"},
            "_source":["_id","title","url","description","language","entitled","field_keyword_17","field_keyword_08","field_keyword_18","field_keyword_19"]
        },
        timeout=10)
    if res.status_code != 200:
        print("Failed to fetch IBM jobs")
        return
    res_json = res.json()
    jobs = res_json["hits"]["hits"]
    
    for job in jobs:
        location = job["_source"]["field_keyword_19"]
        location_split = location.split(",")

        if len(location_split) == 1:
            city = location_split[0]
            country = ""
        else:
            city = location_split[0]
            country = location_split[1]

        ibm_jobs.append({
            "id": job["_id"],
            "company": "IBM",
            "posting_date": str(today),
            "title": job["_source"]["title"],
            "link": job["_source"]["url"],
            "city": city,
            "country": country
        })
    return ibm_jobs

def find_rbc_jobs():
    rbc_jobs = []
    res = requests.post(
        "https://jobs.rbc.com/widgets",
        json={
            "lang":"en_ca",
            "deviceType":"mobile",
            "country":"ca",
            "pageName":"Student &amp; Early Talent",
            "ddoKey":"eagerLoadRefineSearch",
            "sortBy":"Most recent",
            "subsearch":"",
            "from": 0,
            "irs": "false",
            "jobs":"true",
            "counts":"true",
            "all_fields":["category","subCategory","platform","careerLevel","type","jobType","country","state","city"],
            "pageType":"landingPage",
            "size":50,
            "rk":"l-student-early-talent",
            "clearAll":"false",
            "jdsource":"facets",
            "isSliderEnable":"false",
            "pageId":"page118-ds",
            "siteType":"external",
            "keywords":"",
            "global":"true",
            "selected_fields":{},
            "sort":{"order":"desc","field":"postedDate"},
            "locationData":{},
            "rkstatus":"true",
            "s":"1"
        },
        timeout=10
    )
    
    if (res.status_code != 200):
        print("Failed to fetch RBC jobs")
        return
    res_json = res.json()

    jobs = res_json["eagerLoadRefineSearch"]["data"]["jobs"]

    relevant_jobs = filter(lambda x: "software" in x["title"].lower() or "developer" in x["title"].lower() or "amplify" in x["title"].lower(), jobs)

    for job in relevant_jobs:
        rbc_jobs.append({
            "id": job["jobId"],
            "company": "RBC",
            "posting_date": str(today),
            "title": job["title"],
            "link": job["applyUrl"],
            "city": job["cityState"],
            "country": job["country"]
        })
    return rbc_jobs

def find_wealthsimple_jobs():
    wealthsimple_jobs = []
    valid_teamIds = {"ec7a8bf2-6077-4567-9be4-80d84ab469be", "ba888bf4-d594-4282-bc08-ba76976777f5", "75086480-176b-4527-8647-141db967afb2"}
    res = requests.post(
        "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams",
        json={
            "operationName": "ApiJobBoardWithTeams",
            "query": "query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {\n  jobBoard: jobBoardWithTeams(\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\n  ) {\n    teams {\n      id\n      name\n      externalName\n      parentTeamId\n      __typename\n    }\n    jobPostings {\n      id\n      title\n      teamId\n      locationId\n      locationName\n      workplaceType\n      employmentType\n      secondaryLocations {\n        ...JobPostingSecondaryLocationParts\n        __typename\n      }\n      compensationTierSummary\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment JobPostingSecondaryLocationParts on JobPostingSecondaryLocation {\n  locationId\n  locationName\n  __typename\n}",
            "variables": {"organizationHostedJobsPageName": "wealthsimple"}
        },
        timeout=10
    )
    if res.status_code != 200:
        print("Failed to fetch Wealthsimple jobs")
        return
    json_data = res.json()

    job_postings = json_data["data"]["jobBoard"]["jobPostings"]

    tech_internship_postings = list(filter(lambda x: x["employmentType"] == "Intern" and x["teamId"] in valid_teamIds, job_postings))

    for job in tech_internship_postings:
        wealthsimple_jobs.append({
            "id": job["id"],
            "company": "Wealthsimple",
            "posting_date": str(today),
            "title": job["title"],
            "link": "https://jobs.ashbyhq.com/wealthsimple?departmentId=75086480-176b-4527-8647-141db967afb2&employmentType=Intern",
            "city": job["locationName"],
            "country": ""
        })
    return wealthsimple_jobs

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

    if res.status_code != 200:
        print("Failed to fetch Amazon jobs")
        return
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

    wealthsimple_jobs = find_wealthsimple_jobs()
    all_jobs += wealthsimple_jobs

    rbc_jobs = find_rbc_jobs()
    all_jobs += rbc_jobs

    ibm_jobs = find_ibm_jobs()
    all_jobs += ibm_jobs

    td_jobs = find_td_jobs()
    all_jobs += td_jobs

    return all_jobs