import os
import requests


def scrape_linkedin_profile(linkedin_profile_url: str):
  """
  Scrape information from LinkedIn profiles
  """
  api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
  header_dic = {
    "Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}

  response = requests.get(
    api_endpoint, params={"url": linkedin_profile_url}, headers=header_dic
  )

  if response.status_code != 200:
    raise ValueError(f"Got error from Proxycurl: {response.text}")

  data = response.json()
  data = {
    k: v
    for k, v in data.items()
    if v not in ([], "", "", None)
       and k not in ["people_also_viewed", "certifications",
                     "social_networking_services", "accomplishment_patents"]
  }
  if data.get("groups"):
    for group_dict in data.get("groups"):
      group_dict.pop("profile_pic_url")

  return data
