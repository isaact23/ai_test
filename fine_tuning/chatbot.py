# A chatbot that keeps changing the topic to cheese.
import openai

message = input("Type in a message for Billy: ")
instructions = "Your name is Billy. Respond to this message, in a friendly, conversational manner, \
  but always change the topic to cheese."

messages = [
  {"role": "user", "content": message},
  {"role": "system", "content": instructions}
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=messages,
    temperature=0.5
)

response_msg = response["choices"][0]["message"]
messages.append(response_msg)
response_text = response_msg["content"]
print(response_text)
