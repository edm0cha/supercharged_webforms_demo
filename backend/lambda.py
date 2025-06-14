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

DEFAULT_PROMPT_TEMPLATE = """You are a master branding consultant who specializes in naming brands.\n

You come up with a catchy and memorable brand names.

Take the brand description below and use it to create the name for a brand.

<brand-description>{brand_description}</brand-description>

then based on the description and you hot new brand name give the brand a score 1-10 for how likely it is to succeed.

{format_instructions}
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

    parser = PydanticOutputParser(pydantic_object=BrandInfo)

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["brand_description"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    qa = LLMChain(llm=llm, prompt=prompt)
    return qa

def run_chain(chain, question: str):
    return chain.invoke({"brand_description": question})

def run_chatbot_request(question):
    try:
        llm_chain = build_chain(DEFAULT_PROMPT_TEMPLATE)
    except Exception as e:
        return {"error building chain": str(e), "trace": traceback.format_exc()}
    try:
        result = run_chain(llm_chain, question)
    except Exception as e:
        return {"error running chain": str(e), "trace": traceback.format_exc()}
    # Return answer which is result, and then document list as sources
    return result


def get_an_answer(question):
    try:
        return run_chatbot_request(question)
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}


def lambda_handler(event, _):
    response = {}

    request_body = json.loads(event["body"])
    question = request_body.get("question", "")

    try:
        response["statusCode"] = 200
        response["headers"] = {
            "Access-Control-Allow-Origin": "*",
            "content-type": "application/json",
        }
        resp = get_an_answer(question)
        parser = PydanticOutputParser(pydantic_object=BrandInfo)
        parsed = parser.parse(response['text'])

        response["body"] = json.dumps(parsed)

    except Exception as e:
        response["statusCode"] = 500
        response["body"] = str(e)
    return response

if __name__ == "__main__":
    query = "a cool hip new hosting website brand aimed at developers and startups"
    response = get_an_answer(question=query)
    parser = PydanticOutputParser(pydantic_object=BrandInfo)
    parsed = parser.parse(response['text'])
    print(parsed)