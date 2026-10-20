"""Freeze the redator prompt: template + example (input, output) pairs -> prompt_redator.md.

Run from the project root: python redator/montar_prompt.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = [
    (ROOT / "data/entrada_redator/RegraMaxlub.json", ROOT / "redator/exemplos/RegraMaxlub.saida.json"),
    (ROOT / "data/entrada_redator/regra_001.json", ROOT / "redator/exemplos/regra_001.saida.json"),
]


def compact(path: Path) -> str:
    return json.dumps(json.loads(path.read_text(encoding="utf-8")), ensure_ascii=False)


def main() -> None:
    blocks = [f'<exemplo>\n<pacote>\n{compact(package)}\n</pacote>\n<saida>\n{compact(answer)}\n</saida>\n</exemplo>'
              for package, answer in EXAMPLES]
    template = (ROOT / "redator/prompt_redator.template.md").read_text(encoding="utf-8")
    (ROOT / "redator/prompt_redator.md").write_text(template.replace("{{EXEMPLOS}}", "\n".join(blocks)), encoding="utf-8")
    print("redator/prompt_redator.md gravado")


if __name__ == "__main__":
    main()
