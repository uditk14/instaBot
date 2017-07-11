from paralleldots.config import  set_api_key,get_api_key
import requests
import json

# Parallel Dots Usage
def get_keywords(text,api_key):
    # Checking the text  and type of text that is received
    print text
    print type(text)
    # Setting the API key
    set_api_key("rnaQPDGNt7ZmD8wFa1e3qlDu9SQnEf52ZGdhAJXB8Q0")
    # Checking for api-key
    if not api_key == None:
        # Checking that
        if type(text) != str:
            return "Input must be a string."
        elif text == "":
            return "Input string cannot be empty."
            exit()
        else:

            #Base URL for parallel dots
            url = 'http://apis.paralleldots.com/keywords'
            # Calling the POST
            response = requests.post(url, params={"apikey": api_key, "q": text})

            # Checking the status code of returned response from POST request
            if response.status_code != 200:
                return ""
            response = {"keywords": json.loads(response.content)}
            # Returning the keywords
            return response['keywords']
    else:
        return "API key does not exist"
