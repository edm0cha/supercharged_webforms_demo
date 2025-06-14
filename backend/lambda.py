import json
import os
import traceback
import boto3
import langchain

from langchain.llms.bedrock import Bedrock
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.cache import InMemoryCache
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, field_validator

langchain.llm_cache = InMemoryCache()
langchain.debug = True
langchain.verbose = True

BEDROCK_CLIENT = boto3.client("bedrock-runtime")

MAX_TOKENS_TO_SAMPLE: int = 2048
TEMPERATURE: float = 0.9
TOP_K: int = 250
TOP_P: float = 0.99
STOP_SEQUENCES = ["\n\nHuman:"]

DEFAULT_PROMPT_TEMPLATE = """You are a trip planner manager and your goal is to design an amazing trip expirience based on the place your customers wants to travel, 
take in consideration the following information:.\n
Location, Date, time and number or people that are going the trip and how adventurousness the people is from a scale from 1 to 10
with that you need to generate a full itinerary agenda with places to go, important landmakrs, things to do

<arrive-date>{arrive_date}</arrive-date>
<departure-date>{arrive_date}</departure-date>
<place>{destination}</place>
<passengers>{tickets}</passengers>
<adventurousness>{adventurousness}</adventurousness>

We need the response as plain text
"""

class BrandInfo(BaseModel):
    brand_name: str = Field(description="This is the name of the brand")
    likelihood_of_success: int = Field(description="This is an integer between 1-10")
    reasoning: str = Field(description="This is the reasoning for the score")

    @field_validator("likelihood_of_success")
    def check_score(cls, v):
        if v < 1 or v > 10:
            raise ValueError("The score must be between 1 and 10")
        return v
    

def build_chain(prompt_template):
    llm = Bedrock(
        client=BEDROCK_CLIENT,
        model_id="anthropic.claude-v2",
        model_kwargs={
            "max_tokens_to_sample": MAX_TOKENS_TO_SAMPLE,
            "temperature": TEMPERATURE,
            "top_k": TOP_K,
            "top_p": TOP_P,
            "stop_sequences": STOP_SEQUENCES,
        },
    )

    #parser = PydanticOutputParser(pydantic_object=BrandInfo)

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["arrive_date", "departure_date", "destination", "tickets", "adventurousness"],
        #partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    qa = LLMChain(llm=llm, prompt=prompt)
    return qa

def run_chain(chain, startDate: str, endDate: str, destination, tickets, adventurousness):
    return chain.invoke({"arrive_date": startDate, "departure_date": endDate, "destination":destination, "tickets":tickets, "adventurousness":adventurousness})

def run_chatbot_request(startDate, endDate, destination, tickets, adventurousness):
    try:
        llm_chain = build_chain(DEFAULT_PROMPT_TEMPLATE)
    except Exception as e:
        return {"error building chain": str(e), "trace": traceback.format_exc()}
    try:
        result = run_chain(llm_chain, startDate, endDate, destination, tickets, adventurousness)
    except Exception as e:
        return {"error running chain": str(e), "trace": traceback.format_exc()}
    # Return answer which is result, and then document list as sources
    return result


def get_an_answer(startDate, endDate, destination, tickets, adventurousness):
    try:
        return run_chatbot_request(startDate, endDate, destination, tickets, adventurousness)
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}


def lambda_handler(event, _):
    response = {}

    request_body = json.loads(event["body"])
    startDate = request_body.get("startDate", "")
    endDate = request_body.get("endDate", "")
    destination = request_body.get("destination", "")
    tickets = request_body.get("tickets", "")
    adventurousness = request_body.get("adventurousness", "")

    try:
        response["statusCode"] = 200
        response["headers"] = {
            "Access-Control-Allow-Origin": "*",
            "content-type": "application/json",
        }
        resp = get_an_answer(startDate,endDate, destination, tickets, adventurousness)

        response["body"] = resp

    except Exception as e:
        response["statusCode"] = 500
        response["body"] = str(e)
    return response