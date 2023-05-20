import os
import requests


# https://nubela.co/proxycurl/linkedin

def scrape_linkedin_profile(url: str):
    """Scrape information from LinkedIn profiles.
    Manually scrape the information from the LinkedIn profile page."""

    header_dic = {"Authorization": f"Bearer {os.environ.get('PROXYCURL_API_KEY')}"}

    # api_endpoint = "https://api.proxycurl.com/linkedin"
    # response = requests.get(api_endpoint, headers=header_dic, params={"url": url})

    # READ FROM OUR GIST
    api_endpoint = "https://gist.githubusercontent.com/bladnman/62f1b4e8bcb9af9639c9eff781112fcb/raw/b5e12cfd4abba268595942a3db9286505b2f59db/musk_linkedin.json"
    response = requests.get(api_endpoint)
    data_json = response.json()

    cleaned_json = {
        k: v
        for k, v in data_json.items()
        if v not in ([], "", None)
           and k not in ["people_also_viewed", "certifications"]
    }
    if cleaned_json.get("groups"):
        for group_dict in cleaned_json.get("groups"):
            group_dict.pop("profile_pic_url")

    return cleaned_json
