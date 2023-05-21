from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.agents import initialize_agent, Tool, AgentType

from tools.tools import get_profile_url_serp


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    template = """given the full name {name_of_person} I want you to get it me a link to their 
    twitter profile page and extract from there the 
    Twitter username. Your answer should contain the person's username"""

    tools_for_agent = [
        Tool(
            name="Crawl Google for Twitter profile page url",
            func=get_profile_url_serp,
            description="Useful for when you need get the Twitter profile page URL",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    return agent.run(
        prompt_template.format_prompt(name_of_person=name)
    )
