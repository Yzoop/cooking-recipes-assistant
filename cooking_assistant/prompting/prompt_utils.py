from pathlib import Path


def read_prompt(prompt_name: str) -> str:
    if (prompt_path := Path(__file__).parent / "textual_prompts" / prompt_name).exists():
        with open(prompt_path) as prompt_file:
            return prompt_file.read()
    else:
        raise FileNotFoundError(f"Prompt {prompt_path} does not exist!")
