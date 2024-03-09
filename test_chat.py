import openai
import json
import requests

#se conecta la api de openai a traves de la key
openai.api_key = open("openai_api_key.txt", "r").read()

#se establece la url con la api key que se usara para hacer los request a la pagina del clima
weather_url = "https://api.openweathermap.org/data/2.5/weather?"
weather_api = open("clima_api_key.txt", "r").read()

#se establecen la herramientas (hasta ahora solo se pueden usar funciones) que el modelo tendra a su disposición
tools = [
    {
        "type": "function",
        "function": {
            "name": "Weather",
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

#esta funcion hace un request a la pagina del clima con una ciudad y devuelve un json con toda la información
def weather(location):
    return requests.get(weather_url + "appid=" + weather_api + "&q="+ location).json()

#a esta funcion se le pasan el modelo y una lista de mensajes que se le daran al chat y te devuelve la respuesta
def callGPT(model, messages):
    
    response = openai.chat.completions.create(
        model=model, #modelo a usar (gpt-4)
        messages=messages, #lista de mensajes (mensaje del sistema y del usuario)
        tools= tools, #las herramientas que definimos arriba
        tool_choice= "auto", #esto significa que el modelo decidira si usar o no una funcion automaticamente
    )

    print(response.choices[0].message, "\n")

    toolCalls = response.choices[0].message.tool_calls #se guardan las solicitudes de llamado a funcion

    if toolCalls: #si hay alguna solicitud
        for call in toolCalls: #por cada solicitud
            args = json.loads(call.function.arguments) #se guardan los argumentos de la funcion que se debe llamar

            #si el nombre de la funcion es weather (en este caso siempre lo será)
            if call.function.name == "weather":
                print(f"Ejecutando funcion weather para {args['location']}...")

                #se llama a la funcion weather con los argumentos que guardamos anteriormente y se guarda el resultado
                returnValue = json.dumps(weather(args['location'])) 

                print(returnValue, "\n")

                #se agrega a la lista de mensajes un nuevo mensaje con el resultado de la funcion
                messages.append({"role":"function", "name":"weather", "content":returnValue})
        

        #se vuelve a llamar al modelo esta vez con el resultado de todas las funciones que se hayan ejecutado anteriormente
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            tools= tools,
            tool_choice= "none", #esto determina que no se usara ninguna funcion asegurando que te de una respuesta
        )
        print(response.choices[0].message, "\n")
    
    return  response


while True:
    print("\n")
    user_input = input("You: ")
    print("\n")

    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Bye!")
        break

    messages = [
        {"role": "system", "content": "if the user ask for the weather, convert the temperature unit to Celsius from Kelvin without telling the user"},
        {"role": "user", "content": user_input}
    ]

    answer = callGPT("gpt-4-1106-preview", messages)

    print("Chat:", answer.choices[0].message.content, "\n")