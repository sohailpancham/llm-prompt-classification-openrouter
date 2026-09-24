# LLM Prompt Classification Evaluation using OpenRouter

## Overview

This project evaluates how different Large Language Models (LLMs) classify user prompts into three categories:

- Simple
- Coding
- Reasoning

The experiment uses the OpenRouter API and Python.

A total of 15 prompts were created manually, with 5 prompts for each category. These manually assigned labels are used as the ground truth for evaluating the model predictions.

## Models Used

The following free OpenRouter models were selected:

1. `qwen/qwen3.8-27b:free`
2. `z-ai/glm-5.2:free`
3. `inclusionai/ling-3.0-flash-sante:free`

The available free models were discovered using the OpenRouter `/api/v1/models` endpoint by filtering model IDs ending with `:free`.

## Prompt Categories

The dataset contains:

| Category | Number of Prompts |
|---|---:|
| Simple | 5 |
| Coding | 5 |
| Reasoning | 5 |
| Total | 15 |

The prompts and their ground-truth labels are stored in `prompts.json`.

## System Prompt

The following instruction was given to the models:

> Classify the user's prompt into exactly one category: simple, coding, or reasoning. Reply with only the category word.

## How the Program Works

The Python program:

1. Loads the 15 prompts from `prompts.json`.
2. Sends each prompt to three free OpenRouter models.
3. Measures the latency of each API request.
4. Records token usage when available.
5. Normalizes model responses into `simple`, `coding`, or `reasoning`.
6. Compares the prediction with the ground-truth label.
7. Handles API errors without stopping the complete experiment.
8. Adds a delay between requests because free models may be rate-limited.
9. Saves all experiment data to `results.csv`.
10. Calculates accuracy for each model.

## Results

| Model | Accuracy | Observation |
|---|---:|---|
| Qwen 3.8 27B Free | 0.00% | Requests were blocked by temporary rate limits during the experiment |
| GLM 5.2 Free | 13.33% | Some classifications succeeded, while several requests were rate-limited or produced responses that normalized to unknown |
| Ling 3.0 Flash Sante Free | 0.00% | Requests completed, but responses did not produce usable category text and were normalized to unknown |

Accuracy was calculated as:

`Accuracy = (Correct classifications / 15) × 100`

API errors were therefore not counted as correct classifications.

## Observations

### Qwen

During the experiment, the Qwen free endpoint was temporarily rate-limited. The program correctly caught these API errors and continued processing instead of terminating.

Therefore, the reported 0% should not be interpreted as the model incorrectly classifying every prompt. The experiment did not receive usable classifications for those rate-limited requests.

### GLM

GLM returned some usable classifications. For example, it correctly classified a simple prompt and a coding prompt during the run.

However, several requests were affected by free-provider rate limits, while some responses could not be normalized into one of the three expected category words.

Under the experiment's accuracy calculation, GLM achieved 13.33%.

### Ling

The Ling endpoint returned responses without usable classification text under the tested configuration. These responses were normalized to `unknown`, resulting in 0% accuracy in this run.

## Error Handling

Free OpenRouter models can be temporarily unavailable or rate-limited.

The program uses exception handling so that one failed API request does not terminate the entire experiment. Errors are recorded in `results.csv` together with the corresponding model and prompt.

A delay is also added between API requests to reduce rapid requests to free endpoints.

## Normalization

Model responses are converted to lowercase and checked for the expected category words:

- `simple`
- `coding`
- `reasoning`

For example:

- `Coding.` becomes `coding`
- `This is coding` becomes `coding`
- A response without any valid category becomes `unknown`

## Improvements

The experiment could be improved by:

1. Adding retry logic with exponential backoff for HTTP 429 rate-limit errors.
2. Increasing the delay between free-model requests.
3. Repeating the experiment at different times to reduce temporary provider congestion.
4. Testing additional free models when provider availability changes.
5. Separately reporting classification accuracy on successful responses and API availability/failure rate.
6. Testing different prompt wording and output constraints.

## Project Files

- `main.py` - Runs the classification experiment.
- `prompts.json` - Contains the 15 prompts and ground-truth labels.
- `results.csv` - Contains predictions, correctness, latency, token usage, and API errors.
- `requirements.txt` - Contains Python package dependencies.
- `.gitignore` - Prevents local environments and secret files from being committed.

## Setup

Create and activate a Python virtual environment.

Install the required packages:

```bash
pip install -r requirements.txt