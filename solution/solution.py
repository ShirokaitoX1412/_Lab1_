import os
import time
from typing import Any, Callable
from openai import OpenAI

# ---------------------------------------------------------------------------
# Estimated costs per 1K OUTPUT tokens (USD)
# ---------------------------------------------------------------------------
COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}

OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"

# Khởi tạo client (Lấy từ biến môi trường hệ thống)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------------------------------------------------------
# Task 1 — Call GPT-4o
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 1.5,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    start_time = time.time()
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )
    
    latency = time.time() - start_time
    return response.choices[0].message.content, latency


# ---------------------------------------------------------------------------
# Task 2 — Call GPT-4o-mini
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    return call_openai(prompt, model=OPENAI_MINI_MODEL, temperature=temperature, top_p=top_p, max_tokens=max_tokens)


# ---------------------------------------------------------------------------
# Task 3 — Compare GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    res_4o, lat_4o = call_openai(prompt)
    res_mini, lat_mini = call_openai_mini(prompt)
    
    # Ước tính cost: (số từ / 0.75) / 1000 * đơn giá
    words = len(res_4o.split())
    tokens_est = words / 0.75
    cost_est = (tokens_est / 1000) * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
    
    return {
        "gpt4o_response": res_4o,
        "mini_response": res_mini,
        "gpt4o_latency": lat_4o,
        "mini_latency": lat_mini,
        "gpt4o_cost_estimate": cost_est
    }


# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot with conversation history
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    history = []
    print("Chatbot started. Type 'quit' or 'exit' to stop.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit"]:
            break
            
        history.append({"role": "user", "content": user_input})
        
        # Chỉ giữ 3 lượt hội thoại gần nhất (3 user + 3 assistant = 6 tin nhắn)
        current_messages = history[-6:]
        
        stream = client.chat.completions.create(
            model=OPENAI_MINI_MODEL,
            messages=current_messages,
            stream=True
        )
        
        print("Assistant: ", end="", flush=True)
        full_response = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            full_response += delta
            
        history.append({"role": "assistant", "content": full_response})


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    attempt = 0
    while attempt <= max_retries:
        try:
            return fn()
        except Exception as e:
            if attempt == max_retries:
                raise e
            delay = base_delay * (2 ** attempt)
            print(f"Error occurred. Retrying in {delay:.2f}s...")
            time.sleep(delay)
            attempt += 1


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    results = []
    for p in prompts:
        res = compare_models(p)
        res["prompt"] = p
        results.append(res)
    return results


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    header = f"{'Prompt':<40} | {'GPT-4o Res':<40} | {'Mini Res':<40} | {'4o Lat':<8} | {'Mini Lat':<8}"
    separator = "-" * len(header)
    lines = [header, separator]
    
    for r in results:
        p = (r['prompt'][:37] + '..') if len(r['prompt']) > 40 else r['prompt']
        res4 = (r['gpt4o_response'][:37] + '..') if len(r['gpt4o_response']) > 40 else r['gpt4o_response']
        resm = (r['mini_response'][:37] + '..') if len(r['mini_response']) > 40 else r['mini_response']
        
        line = f"{p:<40} | {res4:<40} | {resm:<40} | {r['gpt4o_latency']:<8.2f} | {r['mini_latency']:<8.2f}"
        lines.append(line)
        
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Lưu ý: Cần set API Key trước khi chạy lệnh dưới
    try:
        test_prompt = "Explain the difference between temperature and top_p in one sentence."
        print("=== Comparing models ===")
        result = compare_models(test_prompt)
        for key, value in result.items():
            print(f"{key}: {value}")

        print("\n=== Starting chatbot (type 'quit' to exit) ===")
        streaming_chatbot()
    except Exception as e:
        print(f"\n[!] Error: {e}")
        print("Please check your API Key and Credit balance.")