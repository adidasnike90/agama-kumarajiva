# LoRA / SFT (later phase)

Do **not** fine-tune until you have a human-reviewed golden set
(`data/golden/`) of at least dozens of sutras.

Suggested stack when ready:

- Base: Qwen2.5 / DeepSeek distill instruct
- Method: LoRA via Axolotl or LLaMA-Factory
- Train pairs: `chinese_text` (+ optional EN) → `kumarajiva_style_text`
- Hold out 10% for style + doctrine eval (forbidden-term scan + spot checks)

`prepare_lora_dataset.py` converts reviewed JSONL once gold files exist.
