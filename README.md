# LLM Prompt Classification Evaluation using OpenRouter

## Overview

This project evaluates how different Large Language Models (LLMs) classify user prompts into three categories:

- Simple
- Coding
- Reasoning

The experiment uses the OpenRouter API and Python.

A total of 15 prompts were created manually, with 5 prompts for each category. These manually assigned labels are used as the ground truth for evaluating the model predictions.

## Models Used

The final experiment used the following three OpenRouter models:

1. `google/gemini-2.5-flash-lite`
2. `openai/gpt-4.1-nano`
3. `mistralai/mistral-small-3.2-24b-instruct`

Initially, free OpenRouter models were tested. However, some free endpoints were affected by rate limits, provider restrictions, or unusable responses. Since API credit was available, the final experiment used low-cost working models so that complete classification results could be collected.

## Prompt Categories

| Category | Number of Prompts |
|---|---:|
| Simple | 5 |
| Coding | 5 |
| Reasoning | 5 |
| Total | 15 |

The prompts and their ground-truth labels are stored in `prompts.json`.

## System Prompt

The following instruction was given to each model:

> Classify the user's prompt into exactly one category: simple, coding, or reasoning. Reply with only the category word.

## How the Program Works

The Python program:

1. Loads the 15 prompts from `prompts.json`.
2. Sends every prompt to each of the three models.
3. Measures the latency of each API request.
4. Records prompt, completion, and total token usage.
5. Normalizes model responses into `simple`, `coding`, or `reasoning`.
6. Compares each prediction with the ground-truth label.
7. Records errors without terminating the complete experiment.
8. Adds a delay between API requests.
9. Saves all experiment data to `results.csv`.
10. Calculates accuracy for each model.

A total of 45 classifications were performed:

`15 prompts × 3 models = 45 classifications`

## Results

| Model | Correct | Total | Accuracy |
|---|---:|---:|---:|
| Gemini 2.5 Flash Lite | 15 | 15 | 100% |
| GPT-4.1 Nano | 13 | 15 | 86.67% |
| Mistral Small 3.2 24B Instruct | 13 | 15 | 86.67% |

Accuracy was calculated as:

`Accuracy = (Correct classifications / Total prompts) × 100`

In this experiment, Gemini 2.5 Flash Lite classified all 15 prompts correctly.

## Misclassified Prompts

### GPT-4.1 Nano

**Prompt 8**

Prompt:

`Why does my React useEffect run twice in development?`

Ground truth:

`coding`

Model prediction:

`reasoning`

This prompt can be interpreted as reasoning because it asks "why" something happens, even though the subject is a programming problem.

**Prompt 9**

Prompt:

`Write a SQL query to select all students whose marks are greater than 80.`

Ground truth:

`coding`

Raw model response:

`codeing`

Normalized prediction:

`unknown`

The model intended to return the coding category but misspelled `coding` as `codeing`. Since the normalization function only accepts the expected category words, the response was recorded as `unknown`.

### Mistral Small 3.2 24B Instruct

**Prompt 2**

Prompt:

`Who invented the telephone?`

Ground truth:

`simple`

Model prediction:

`reasoning`

The model classified this factual question as reasoning instead of simple.

**Prompt 8**

Prompt:

`Why does my React useEffect run twice in development?`

Ground truth:

`coding`

Model prediction:

`reasoning`

Like GPT-4.1 Nano, Mistral interpreted the explanatory nature of the question as reasoning rather than coding.

## Cost and Budget

The task budget was limited to $0.50.

OpenRouter usage after the experiment was:

`$0.000250582`

This is well below the $0.50 budget.

The experiment used short prompts, a small output-token limit, and low-cost models to keep API usage minimal.

## Error Handling

The program uses exception handling so that an API failure for one request does not terminate the entire experiment.

If an API request fails:

- The error is recorded.
- The prediction is treated appropriately.
- The program continues with the remaining prompts.

This was especially useful during initial testing of free OpenRouter endpoints, where rate limits and provider restrictions were encountered.

## Normalization

Model responses are converted to lowercase and checked for the expected category words:

- `simple`
- `coding`
- `reasoning`

Examples:

- `Coding.` → `coding`
- `This is coding` → `coding`
- A response without a valid category → `unknown`

This makes the evaluation more robust to small formatting differences while still requiring one of the expected category names.

## Observations

Gemini 2.5 Flash Lite achieved 100% accuracy in this experiment.

GPT-4.1 Nano achieved 86.67%. One prompt was classified as reasoning instead of coding, while another response contained the misspelling `codeing`, which was normalized to `unknown`.

Mistral Small 3.2 24B Instruct achieved 86.67%. It misclassified one simple factual question and one coding-related explanatory question as reasoning.

Prompt 8 was particularly interesting because both GPT-4.1 Nano and Mistral classified it as reasoning. This shows that prompts containing programming topics can still be interpreted differently when they ask for an explanation rather than explicitly asking for code.

## Improvements

The experiment could be improved by:

1. Adding retry logic with exponential backoff for temporary API failures.
2. Making category definitions more explicit in the system prompt.
3. Improving normalization to optionally handle minor spelling mistakes such as `codeing`.
4. Repeating the experiment multiple times to test consistency.
5. Using a larger and more diverse prompt dataset.
6. Separately measuring API reliability and classification accuracy.

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
```

Set the OpenRouter API key as an environment variable.

Example in PowerShell:

```powershell
$env:OPENROUTER_API_KEY="YOUR_API_KEY"
```

The actual API key is not stored in the source code or committed to GitHub.

Run the experiment:

```bash
python main.py
```

The program will generate the experiment results in:

```text
results.csv
```