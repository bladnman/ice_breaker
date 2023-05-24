from langchain import PromptTemplate, GoogleSearchAPIWrapper
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.tools import Tool

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from output_parsers import person_intel_parser, PersonIntel
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets

from tools.tools import get_profile_url_google

from langchain.tools.file_management import ReadFileTool

name = "Kendall Gelner"


# "@kendalldevdiary"
def ice_break(name: str) -> PersonIntel:
  # LINKED IN

  ## FILE MODE
  if "Kendall" in name:
    linkedin_data = ReadFileTool().run(
      "./files/linkedin_kendallgelner_small.json"
    )

  ## NETWORK MODE
  else:
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
      linkedin_profile_url=linkedin_profile_url
    )

  # TWITTER
  twitter_username = twitter_lookup_agent(name=name)
  tweets = scrape_user_tweets(username=twitter_username, num_tweets=10)

  summary_template = """
        You are a highly enthusiastic match maker that wants to connect people.
        I will provide you with the following information about a person: 
            1. Linkedin information {linkedin_information} 
            2. Twitter information {twitter_information} 
        I want you to provide me with the following information about them:
            1. A short summary
            2. 2 interesting facts about them
            3. A topic that may interest them
            4. 2 creative ice breakers to start a conversation with them
        \n{format_instructions}
     """

  summary_prompt_template = PromptTemplate(
    input_variables=["linkedin_information", "twitter_information"],
    template=summary_template,
    partial_variables={
      "format_instructions": person_intel_parser.get_format_instructions()}
  )

  llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

  chain = LLMChain(llm=llm, prompt=summary_prompt_template)

  summary = chain.run(
    linkedin_information=linkedin_data, twitter_information=tweets
  )
  print(summary)
  return person_intel_parser.parse(summary)


def test_tool():
  tool = Tool(
    name="Google Search",
    description="Search Google for recent results.",
    func=GoogleSearchAPIWrapper().run
  )
  result = tool.run("Obama's first name?")
  print(result)


def test_tool2():
  res = ReadFileTool().run("./files/linkedin_kendallgelner.json")
  print(res)


if __name__ == "__main__":
  person_intel = ice_break(name)
  print(person_intel)
  # test_tool()
  # test_tool2()
