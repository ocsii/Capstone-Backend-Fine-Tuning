# import json
# import os
# from openai import OpenAI
# import logging

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# def lambda_handler(event, context):

#     logger.info(f"Received event: {event}")


#     # Parse the JSON body
#     body = json.loads(event['body'])

#     # Extract query and retrieved sections from the parsed body
#     query = body.get("query")
#     retrieved_sections = body.get("retrieved_sections", [])

   

#     # Prepare the top three sections
#     section1 = retrieved_sections[0] if len(retrieved_sections) > 0 else ""
#     section2 = retrieved_sections[1] if len(retrieved_sections) > 1 else ""
#     section3 = retrieved_sections[2] if len(retrieved_sections) > 2 else ""

#     # Set up the OpenAI client
#     client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

#     # Call OpenAI GPT API
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {"role": "system", "content": (
#                 "You are a helpful assistant. Your job is to answer the query using the provided sections. "
#                 "Focus on clear, very concise, and well-structured answers as short as possible in sentence form. Make sure not not stray from the query"
#                 "Always search for the answer in **Section 1** first. If the answer is not found there, then refer to Section 2. "
#                 "If still not found, refer to Section 3. If the answer cannot be found in any section, answer based on closest match from the text."
#                 "If you use abbreviations give context"
#                 "To separate each line, use an asterisk (*), I want responses in pure text paragraph format"
#             )},
#             {"role": "user", "content": f"Query: {query}\n"},
#             {"role": "user", "content": f"Section 1: {section1}\n"},
#             {"role": "user", "content": f"Section 2: {section2}\n"},
#             {"role": "user", "content": f"Section 3: {section3}\n"}
#         ],
#         model="gpt-3.5-turbo",
#     )

#     # Extract the answer from the response
#     answer_content = chat_completion.choices[0].message.content

#     return {
#         "statusCode": 200,
#         "body": json.dumps({"answer": answer_content})
#     }
