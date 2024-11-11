import json
import os
from openai import OpenAI
import logging

""" This is the code used in the Lambda Function. Not used Locally, just for reference """

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    logger.info(f"Received event: {event}")

    # Parse the JSON body
    body = json.loads(event['body'])

    # Extract query and retrieved sections from the parsed body
    query = body.get("query")
    retrieved_sections = body.get("retrieved_sections", [])

    # Prepare the top three sections
    section1 = retrieved_sections[0] if len(retrieved_sections) > 0 else ""
    section2 = retrieved_sections[1] if len(retrieved_sections) > 1 else ""
    section3 = retrieved_sections[2] if len(retrieved_sections) > 2 else ""

    # Set up the OpenAI client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY")) # This is stored in Lambda function environment variables

    # Call OpenAI GPT API
    chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": (
            "You are a helpful assistant. Your goal is to answer the user's query using information from the provided sections, focusing on clarity, conciseness, and accuracy. "
            "Follow these guidelines for answering and formatting:"
            "\n1. First, check **Section 1** for the main answer. If it fully addresses the query, respond based primarily on this section."
            "\n2. If **Sections 2** or **3** contain additional relevant information to the answer, incorporate them briefly to enhance the answer."
            "\n3. If no section fully answers the query, synthesize the closest match using relevant information from any of the sections."
            "\n- Focus strictly on information that directly addresses the query. Avoid unrelated details or tangential topics."
            "\n- Use **bold** for key words or phrases that should stand out in the answer."
            "\n- Every time you start a numbered list, bullet list, or point, add a single asterisk (*) immediately before the list to indicate a new line."
            "\n- Keep the response concise and as short as possible, avoid adding unnecessary details."
            "\n- Clarify any abbreviations or technical terms briefly."
            "\n- The beginning of a response can never have a bullet point"
        )},
        {"role": "user", "content": f"Query: {query}\n"},
        {"role": "user", "content": f"Section 1: {section1}\n"},
        {"role": "user", "content": f"Section 2: {section2}\n"},
        {"role": "user", "content": f"Section 3: {section3}\n"}
    ],
    model="gpt-4o",
)

    # Extract content only
    answer_content = chat_completion.choices[0].message.content

    return {
        "statusCode": 200,
        "body": json.dumps({"answer": answer_content})
    }
