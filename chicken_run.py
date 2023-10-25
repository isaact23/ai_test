import openai, json

LINE_LENGTH = 60

FUNCTIONS = [
    {
        "name": "chickens_escape",
        "description": "The function to call if the plan meets all criteria.",
        "parameters": {
            "type": "object",
            "properties": {
                "critique": {
                    "type": "string",
                    "description": "Explain why the plan succeeds and how each criterion is met."
                }
            }
        }
    },
    {
        "name": "chickens_fail",
        "description": "The function to call if the plan does not meet all criteria.",
        "parameters": {
            "type": "object",
            "properties": {
                "realistic": {
                    "type": "number",
                    "description": "On a scale of 1 to 10, how realistic is the plan?"
                },
                "allChickensEscape": {
                    "type": "number",
                    "description": "On a scale of 1 to 10, how likely is it for every single chicken to escape?"
                },
                "underFiveMinutes": {
                    "type": "number",
                    "description": "On a scale of 1 to 10, how likely is it for the plan to be executed in under five minutes?"
                },
                "nobodyNotices": {
                    "type": "number",
                    "description": "On a scale of 1 to 10, how likely is it for neither Mr Tweedy, Mrs Tweedy nor the dogs to notice the escape?"
                },
                "longTermSuccess": {
                    "type": "number",
                    "description": "On a scale of 1 to 10, how prosperous will the chickens be in the long term?"
                },
                "nickAndFetcher": {
                    "type": "number",
                    "description": "On a scale of 1 to 10, how likely is it for Nick and Fetcher to escape as well?"
                },
                "critique": {
                    "type": "string",
                    "description": "Explain why the plan is a failure by explaining which criteria fail and why they failed."
                }
            }
        }
    }
]

# Print a bar in the terminal
def bar():
    print("-" * LINE_LENGTH)

# Function to call if the plan allows the chickens to escape.
def chickens_escape(critique):
    bar()
    print(critique)
    print("")
    print("THE CHICKENS ESCAPED.")
    bar()

# Function to call if the plan fails.
def chickens_fail(realistic, allChickensEscape, underFiveMinutes,
                  nobodyNotices, longTermSuccess, nickAndFetcher,
                  critique):

    bar()
    print(critique)
    print("")

    print("Plan realistic? "                                    .ljust(LINE_LENGTH) + str(realistic)         + "/10")
    print("Did all chickens escape? "                           .ljust(LINE_LENGTH) + str(allChickensEscape) + "/10")
    print("Plan executed under five minutes? "                  .ljust(LINE_LENGTH) + str(underFiveMinutes)  + "/10")
    print("Nobody noticed? "                                    .ljust(LINE_LENGTH) + str(nobodyNotices)     + "/10")
    print("Long term success and prosperity for the chickens? " .ljust(LINE_LENGTH) + str(longTermSuccess)   + "/10")
    print("Nick and Fetcher made it too? "                      .ljust(LINE_LENGTH) + str(nickAndFetcher)    + "/10")

    print("")
    print("THE CHICKENS DIED.")
    bar()

# Send a query to OpenAI with a message chain.
def query(messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=FUNCTIONS,
        function_call="auto"
    )

# Process a response from OpenAI. Return True if processing was successful, else False.
def process(response_message):

    # Determine if OpenAI wants to call a function
    if response_message.get("function_call"):

        # Determine which function OpenAI wants to call
        function_name = response_message["function_call"]["name"]
        function_args = json.loads(response_message["function_call"]["arguments"])

        # Handle plan approval
        if function_name == "chickens_escape":
            chickens_escape(function_args.get("critique"))

        # Handle plan rejection
        elif function_name == "chickens_fail":
            chickens_fail(function_args.get("realistic"),
                        function_args.get("allChickensEscape"),
                        function_args.get("underFiveMinutes"),
                        function_args.get("nobodyNotices"),
                        function_args.get("longTermSuccess"),
                        function_args.get("nickAndFetcher"),
                        function_args.get("critique"))
        
        else:
            print("Tried to call a function that doesn't exist.")
            return False
    
    # If OpenAI doesn't want to call a function,
    else:
        print("Could not make a determination. Sorry about that.")
        return False
    
    return True

# Run the program loop.
def run():

    bar()
    print("Give me an escape plan for the chickens from chicken run.")
    plan = input()
    print("Give me a moment to think over your plan.")

    # Generate request for OpenAI based on user-input plan
    first_message = "\
        Below is a proposed escape plan for the chickens from Chicken Run: \n" + plan + "\n" + \
        \
        "If the plan meets all criteria, call chickens_escape, explaining why the plan is successful. \
        If any criteria are unmet, call chickens_fail with parameters indicating whether or not each \
        criterion is met or unmet, and expose any fundamental flaws in the plan via the critique parameter. \
        If the plan is especially bad, make fun of it."
    
    first_message = first_message.strip()

    # Start message chain
    messages = [{"role": "user", "content": first_message}]

    while True:
    
        # Generate and send query
        responses = query(messages)

        # Interpret and handle the response
        response_message = responses["choices"][0]["message"]
        processed = process(response_message)
        if not processed:
            return
            
        # Ask user for follow-up
        print("Enter a response for this report, or press enter to quit.")
        response = input()
        if (len(response) == 0):
            return
        
        # Generate follow-up inquiry for OpenAI
        followup_content = "\
            The user has made the response: \n\n " + response + "\n\n" + \
        \
        "Respond to the user's response and re-evaluate the escape plan, \
        either calling chickens_escape or chickens_fail with parameters set \
        indicating whether each criterion is met."
        
        # Add user response and previous OpenAI response to message chain
        followup_message = {"role": "user", "content": followup_content}
        messages.append(response_message)
        messages.append(followup_message)
        print("Give me a moment to re-think my evaluation.")


if __name__ == "__main__":
    run()
