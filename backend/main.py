import ollama
import pdfplumber

client = ollama.Client()

def ollama_agent():
    response = client.chat(model="deepseek-r1:8b", messages=[
        {"role": "system", "content": "You are a concise assistant. Keep responses brief and to the point."},
        {"role": "user", "content": "Say hello!"}
    ])
    print("Assistant response:", response['message']['content'])
    return response['message']['content']

def main():
    ollama_agent()
    
if __name__ == "__main__":
    main()