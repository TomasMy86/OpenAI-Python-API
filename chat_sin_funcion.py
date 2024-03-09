import openai

openai.api_key = open("openai_api_key.txt", "r").read()

def callGPT(model, messages):
    
    response = openai.chat.completions.create(
        model=model,
        messages=messages
    )
#model-->version-->gpt 4 preview
#message-->lo que recibe el chat

    return  response


while True:
    print("\n")
    user_input = input("You: ")
    print("\n")

    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Bye!")
        break

#lista de msg, dos atributos rol, contenido
#system tiene prioridad sobre el usuario
    messages = [
        {"role": "system", "content": "give short answers"}, #msg sist
        {"role": "user", "content": user_input} #msg usuario
    ]

    answer = callGPT("gpt-4-1106-preview", messages)
    #vble que guarda rta de chat gpt

    print("Chat:", answer.choices[0].message.content, "\n")
    #imprimo rta