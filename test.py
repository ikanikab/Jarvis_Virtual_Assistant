import google.generativeai as genai

genai.configure(api_key="AIzaSyAIAySqvZmPZRZ7ry-U5MCNlSJR0vGUWkg")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("say hello")
print(response.text)