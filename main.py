import os
import json
import csv
import time
import re
from openai import OpenAI

# Read API key safely from environment variable
api_key = os.getenv("OPENROUTER_API_KEY", "").strip()

if not api_key:
    raise ValueError("OPENROUTER_API_KEY is not set")

# Connect to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# Three free models selected from OpenRouter
MODELS = [
    "qwen/qwen3.8-27b:free",
    "z-ai/glm-5.2:free",
    "inclusionai/ling-3.0-flash-sante:free"
]

SYSTEM_PROMPT = """Classify the user's prompt into exactly one category:
simple, coding, or reasoning.
Reply with only the category word."""

# Load the 15 prompts and ground-truth labels
with open("prompts.json", "r", encoding="utf-8") as file:
    prompts = json.load(file)


def normalize_answer(text):
    """Convert model output into simple, coding, reasoning, or unknown."""

    if not text:
        return "unknown"

    text = text.lower().strip()

    for category in ["simple", "coding", "reasoning"]:
        if re.search(rf"\b{category}\b", text):
            return category

    return "unknown"


results = []

for model in MODELS:

    print("\n================================")
    print("MODEL:", model)
    print("================================")

    correct_count = 0

    for item in prompts:

        prompt_id = item["id"]
        prompt = item["prompt"]
        expected = item["label"]

        print(f"\nPrompt {prompt_id}/15")

        start_time = time.perf_counter()

        prediction = "error"
        raw_answer = ""
        error_message = ""
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=20
            )

            raw_answer = response.choices[0].message.content or ""
            prediction = normalize_answer(raw_answer)

            if response.usage:
                prompt_tokens = response.usage.prompt_tokens or 0
                completion_tokens = response.usage.completion_tokens or 0
                total_tokens = response.usage.total_tokens or 0

        except Exception as error:
            error_message = f"{type(error).__name__}: {str(error)}"

        latency = round(time.perf_counter() - start_time, 3)

        is_correct = prediction == expected

        if is_correct:
            correct_count += 1

        results.append({
            "prompt_id": prompt_id,
            "prompt": prompt,
            "expected_label": expected,
            "model": model,
            "raw_answer": raw_answer,
            "prediction": prediction,
            "correct": is_correct,
            "latency_seconds": latency,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "error": error_message
        })

        print("Expected:", expected)
        print("Prediction:", prediction)
        print("Latency:", latency, "seconds")

        if error_message:
          print("Error:", error_message)

        # Delay because free models can be rate-limited
        time.sleep(2)

    accuracy = (correct_count / len(prompts)) * 100

    print("\nAccuracy:", round(accuracy, 2), "%")


# Save experiment results
with open("results.csv", "w", newline="", encoding="utf-8") as file:

    fieldnames = [
        "prompt_id",
        "prompt",
        "expected_label",
        "model",
        "raw_answer",
        "prediction",
        "correct",
        "latency_seconds",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "error"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(results)


print("\nExperiment finished.")
print("Results saved to results.csv")