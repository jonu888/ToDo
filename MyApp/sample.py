import google.generativeai as genai
genai.configure(api_key='AIzaSyD4KzSvbunVkd1TKpmvO83ivvRXk9P0P6E')
model=genai.GenerativeModel("gemini-pro")
while True:
    prompt=input('Ask bot : ')
    if prompt.lower() not in ['quit', 'exit']:
        response=model.generate_content(prompt)
        print(response.text)
    else:
        break