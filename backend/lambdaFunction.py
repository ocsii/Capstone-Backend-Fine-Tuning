import json
import os
from openai import OpenAI
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


""" This is not used in the Local code, it is hosted on AWS Lambda, for reference only"""

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
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


    # Call OpenAI GPT API
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": (
                "You are a helpful assistant. Your goal is to answer the user's query using information from the provided sections. "
                "Step 1: Follow these guidelines for answering:"
                "\n1. First, check **Section 1** for the main answer. If it fully addresses the query, respond based primarily on this section."
                "\n2. If **Sections 2** or **3** contain additional relevant information to the answer, incorporate them briefly to enhance the answer."
                "\n3. If none of the sections fully address the query, synthesize a response from all sections, but ensure the answer is as **factual and concise** as possible."
                "\n\n Step 2: Please follow these formatting guidelines strictly:"
                "\n1. Use **bold** for key words or phrases that should stand out."
                "\n2. Use <b></b> HTML tags for bold text."
                "\n3. Use <ul><li></li></ul> for lists and number the items (e.g., <ul><li>1. Item one</li></ul>)."
                "\n4. Add a <br> tag after each paragraph or list to separate them visually."
                "\n5. If there is a numbered list, use the following format: *1. First point*."
                "\n6. If no relevant information is found, return 'The three sections provided to debugging'"
                "\n7. If information from multiple sections is required, ensure the response is concise and fact-based."
                "\n8. Ensure the answer is short and direct, avoid unnecessary details."
            )},
            {"role": "user", "content": f"Query: {query}\n"},
            {"role": "user", "content": f"Section 1: {section1}\n"},
            {"role": "user", "content": f"Section 2: {section2}\n"},
            {"role": "user", "content": f"Section 3: {section3}\n"}
        ],
        model="gpt-4o",
    )

    # Extract the answer from the response
    answer_content = chat_completion.choices[0].message.content

    return {
        "statusCode": 200,
        "body": json.dumps({"answer": answer_content})
    }
