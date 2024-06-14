import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://localhost:80"
NUM_REQUESTS = 100
CONCURRENT_THREADS = 100  # Number of concurrent threads

def send_request(session, url):
    try:
        response = session.get(url)
        return response.status_code, response.json()
    except Exception as e:
        return None, str(e)

def main():
    with ThreadPoolExecutor(max_workers=CONCURRENT_THREADS) as executor:
        with requests.Session() as session:
            futures = [executor.submit(send_request, session, f"{BASE_URL}/home") for _ in range(NUM_REQUESTS)]
            responses = []
            for future in as_completed(futures):
                status_code, response = future.result()
                responses.append((status_code, response))
                if status_code == 200:
                    server = response.get("message", "").split()[-1]
                    print(f"Success: {response['message']} from {server}")
                else:
                    print(f"Failed: {response}")

    # Basic analysis of responses
    success_count = sum(1 for status, _ in responses if status == 200)
    failure_count = NUM_REQUESTS - success_count

    print(f"\nTotal Requests: {NUM_REQUESTS}")
    print(f"Successful Responses: {success_count}")
    print(f"Failed Responses: {failure_count}")

if __name__ == "__main__":
    main()
