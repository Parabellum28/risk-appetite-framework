import requests

times = []

for i in range(10):
    res = requests.post(
        "http://127.0.0.1:5000/query",
        json={"question": "What is risk appetite?"}
    )

    data = res.json()
    t = data["meta"]["response_time_ms"]

    print(f"Request {i+1}: {t} ms")

    times.append(t)

print("\nAll times:", times)