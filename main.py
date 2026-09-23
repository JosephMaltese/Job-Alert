import requests


def get_data():
    # First, get Amazon jobs
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
    print(json_data["searchHits"])

if __name__ == '__main__':
    get_data()
