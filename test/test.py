import requests
import concurrent.futures

def send_request(session, url, params):
    try:
        response = session.get(url, params=params)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def load_test(num_requests, num_workers):
    url = 'http://localhost:5000/home'
    with requests.Session() as session:
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(send_request, session, url, {'id': i}) for i in range(num_requests)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
            return results

if __name__ == '_main_':
    num_requests = 10
    num_workers = 5
    results = load_test(num_requests, num_workers)
    
    # Print results
    for i, result in enumerate(results):
        if result:
            print(f"Response {i+1}: {result['message']}")
        else:
            print(f"Response {i+1}: No response received")