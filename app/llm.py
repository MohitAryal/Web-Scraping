from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model='llama-3.1-8b-instant', 
    temperature=2,
    max_tokens=100
)

# The prompt to pass to the model
prompt = ChatPromptTemplate.from_messages(
    [
        ('system', '''You are given a user's intent and a list of webpages.
Return a webpage URL that best matches the user's intent.
Quote the link exactly while providing the output.
Use semantic matching and chain of thought to determine where the required content maybe present.
Do not add any explanation, text, or formatting.
        ```User's intent```
        "{intent}"

        ```Webpages list```
        "{pages}"


        ###OUTPUT FORMAT
        Only provide the mathced link as output.
        Keep the output format exactly as below:
        [link]
        ''')
    ]
)

# Chain the model's components
chain = prompt | llm | StrOutputParser()


def call_llm(intent: str, top_links: list[str]) -> str:
    
    # Invoke the chain to get model's response
    response = chain.invoke({"intent": intent, "pages":top_links})

    # Return the response
    return response