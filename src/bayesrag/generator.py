from openai import OpenAI
from bayesrag.config import OPENAI_BASE_URL, OPENAI_API_KEY
from bayesrag.utils import ClassificationResult

import json

client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)


def generate_response(user_query, context):
    prompt_template = f""" You are a Lawyer. Response only related Law Question. do not use your knowledge use below context to get information

    Here is the question: {user_query}

    Additional context to support the answer: {context}
    """

    system_prompt = "You are a helpful assistant that handles user queries and provides answers using the given context without external information."

    completion = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_template},
        ],
        temperature=0.7,
        stream=True
    )

    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


def classify_query(user_query) -> ClassificationResult:
    """
    Classifies a user query related to law and returns a ClassificationResult enum.

    Args:
        user_query: The user's question.

    Returns:
        ClassificationResult.YES if the query is classified as a law-related question, 
        ClassificationResult.NO if it's not a law-related question, 
        ClassificationResult.ERROR if there's an error parsing the response.
    """

    system_prompt = f"""
    You are a Lawyer. Classify the following question related to Law and always give response  in json format as "results":"yes/no" and not give any reason in reponse
    """

    completion = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
        ],
        temperature=1,
    )

    # Parse the response into JSON
    response_json = completion.choices[0].message.content
    try:
        response_dict = json.loads(response_json)
        result = response_dict["results"].lower()
        if result == "yes":
            print("Yes it related to law")
            return ClassificationResult.YES
        elif result == "no":
            print("No it not related to law")
            return ClassificationResult.NO
        else:
            print("Unexpected result in classification")
            return ClassificationResult.ERROR  # Handle unexpected results
    except json.JSONDecodeError:
        print(f"Error parsing JSON response: {response_json}")
        return ClassificationResult.ERROR

    

if __name__ == "__main__":
    
    user_query = "hey how are you"
    
    result=classify_query(user_query)

    if result ==ClassificationResult.NO:
        for text in generate_response(user_query,None):
            print(text,end="")
    else:
        print("Find from vector Database")