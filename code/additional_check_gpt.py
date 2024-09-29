import requests


# The endpoint for ChatGPT API (GPT-4)
url = "https://api.openai.com/v1/chat/completions"

# The headers, including the API key
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer "
}

prompt = "can you return only names from below keeping them line after line? And names in the same line must be kept in the same line separated by commas. Again, it will be just names. And if name is just one word ignore it. It must be full name \n\n"

with open("additional_check.txt", 'r') as input_file:
    with open("passed_2.txt", 'w') as output_file:
        while True:
            lines = ''
            for _ in range(300):
                try:
                    line = next(input_file).strip()
                    lines += line + "\n"  # Concatenate lines with newline
                except StopIteration:
                    break  # Stop if there are no more lines
            
            if not lines:  # Break the loop if there are no more lines
                break
            
            data = {
                "model": "gpt-4",  # You can use "gpt-3.5-turbo" if you're using GPT-3.5
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt + lines }
                ]
            }
            response = requests.post(url, headers=headers, json=data)

            # Print the response from the API
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                print(content)  # Output the first completion
                output_file.write(content + "\n")
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
