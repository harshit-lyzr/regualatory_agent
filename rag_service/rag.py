import requests

def train_rag_agent(rag_id, request_body):
    # Define the endpoint
    endpoint = f"https://rag-prod.studio.lyzr.ai/v3/rag/train/{rag_id}/"
    body = [request_body]
    # Make the POST request
    try:
        response = requests.post(endpoint, json=body)
        response.raise_for_status()  # Raise an error for HTTP codes >= 400
        # Return the parsed JSON response
        if response.status_code == 200:
            print("call successfull")
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def get_rag_docs(rag_id, access_token=None):
    url = f'https://rag-prod.studio.lyzr.ai/v3/rag/documents/{rag_id}/'

    # Set up headers if access_token is provided
    headers = {}
    if access_token:
        headers['Authorization'] = f'Bearer {access_token}'

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response:
        return response.json()
    else:
        return {"error": f"Failed to get documents. Status code: {response.status_code}"}


def delete_rag_docs(rag_id, request_data, access_token=None):
    url = f'https://rag-prod.studio.lyzr.ai/v3/rag/{rag_id}/docs/'

    # Set up headers if access_token is provided
    headers = {
        'Content-Type': 'application/json'  # Ensures that the body is sent as JSON
    }
    if access_token:
        headers['Authorization'] = f'Bearer {access_token}'

    # Make the DELETE request
    response = requests.delete(url, json=request_data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to delete documents. Status code: {response.status_code}"}