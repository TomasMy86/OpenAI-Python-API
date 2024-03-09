import openai
import json
import requests

openai.api_key = open("openai_api_key.txt", "r").read()

weather_url = "https://api.openweathermap.org/data/2.5/weather?"
weather_api = open("clima_api_key.txt", "r").read()

tools = [
    {
        "type": "function",
        "function": {
            "name": "weather",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, US",
                    },
                },
                "required": ["location"],
            },
        }
    }
]

def weather(location):
    return requests.get(weather_url + "appid=" + weather_api + "&q="+ location).json()

def callGPT(model, messages):
    
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        tools= tools,
        tool_choice= "auto",
    )

    toolCalls = response.choices[0].message.tool_calls

    if toolCalls:
        for call in toolCalls:
            args = json.loads(call.function.arguments)

            if call.function.name == "weather":
                returnValue = json.dumps(weather(args['location']))

                print(returnValue, "\n")

                messages.append({"role":"function", "name":"weather", "content":returnValue})
        
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            tools= tools,
            tool_choice= "none",
        )

    return  response


while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Bye!")
        break

    messages = [
        {"role": "system", "content": "give short answers, if the user ask for the weather, Infer the temperature unit to use from the users location and convert from kelvin"},
        {"role": "user", "content": user_input}
    ]

    answer = callGPT("gpt-4-1106-preview", messages)

    print("Chat:", answer.choices[0].message.content)