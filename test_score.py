import json
from score import init, run

init()

sample = {
    "text": "Breaking news about world politics and economy"
}

result = run(json.dumps(sample))

print(result)