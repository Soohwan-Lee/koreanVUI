from pydantic import BaseModel
from openai import OpenAI

# YOUR_API_KEY
client = OpenAI(api_key="YOUR_API_KEY")

class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
        {"role": "user", "content": "how can I solve 8x + 7 = -23"}
    ],
    response_format=MathReasoning,
)

math_reasoning = completion.choices[0].message.parsed

# Print each step with explanation and output
for step in math_reasoning.steps:
    print(f"Explanation: {step.explanation}")
    print(f"Output: {step.output}")
    print()  # Add a blank line for better readability

# Print the final answer
print(f"Final Answer: {math_reasoning.final_answer}")