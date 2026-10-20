"""CLI.

  python -m gobr contexto <dir_ou_arquivo_gobr> <dir_saida>     pacote JSON completo por arquivo
  python -m gobr entrada <dir_contexto> <dir_saida>             visão do pacote que o redator lê
  python -m gobr consolidar <dir_candidatos> <dir_saida> --contexto <dir> [<dir>...] --prompt <arquivo>
        valida os candidatos <dir_candidatos>/<arquivo>/*.json, escolhe o de maior concordância e
        grava <arquivo>.json (com _meta) e <arquivo>.md
  python -m gobr pendentes <dir_candidatos> <dir_entrada> --contexto <dir> [<dir>...]
        estratégia adaptativa: imprime "<arquivo> <n>" para cada arquivo que ainda precisa de n réplicas
        (completa até --base; vai até --maximo quando a concordância fica abaixo de --limiar)
  python -m gobr cobertura <dir_gobr>                            lista trechos não reconhecidos
"""
import argparse
import json
import sys
from pathlib import Path

from gobr import consensus, redator
from gobr.context import build
from gobr.parser import parse_file, unrecognized

MODEL = "claude-sonnet-5-5"


def gobr_files(target: Path) -> list[Path]:
    files = [target] if target.is_file() else sorted(target.glob("*.gobr"))
    if not files:
        raise SystemExit(f"nenhum .gobr encontrado em {target}")
    return files


def write_json(path: Path, data: dict, indent: int | None = 2) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=indent), encoding="utf-8")


def write_packages(target: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = gobr_files(target)
    for path in paths:
        write_json(out_dir / f"{path.stem}.json", build(path))
    print(f"{len(paths)} pacotes gravados em {out_dir}")


def write_views(context_dir: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    packages = sorted(context_dir.glob("*.json"))
    for path in packages:
        write_json(out_dir / path.name, redator.view(json.loads(path.read_text(encoding="utf-8"))), indent=1)
    print(f"{len(packages)} entradas do redator gravadas em {out_dir}")


def load_package(name: str, context_dirs: list[Path]) -> dict:
    for directory in context_dirs:
        path = directory / f"{name}.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    raise SystemExit(f"{name}: pacote de contexto não encontrado em {context_dirs}")


def evaluate(file_dir: Path, package: dict) -> tuple[list[consensus.Candidate], consensus.Candidate | None, float]:
    candidates = [consensus.load(p, package) for p in sorted(file_dir.glob("*.json"))]
    chosen, agreement = consensus.choose(candidates)
    return candidates, chosen, agreement


def consolidate(candidates_dir: Path, out_dir: Path, context_dirs: list[Path], prompt: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for file_dir in sorted(p for p in candidates_dir.iterdir() if p.is_dir()):
        package = load_package(file_dir.name, context_dirs)
        candidates, chosen, agreement = evaluate(file_dir, package)
        meta = consensus.provenance(package, candidates, chosen, agreement, prompt, MODEL)
        valid = sum(c.report.ok for c in candidates)
        shown = "sem medida" if agreement is None else f"{agreement:.2f}"
        print(f"{file_dir.name}: {valid}/{len(candidates)} válidos, concordância {shown}, escolhido {meta['escolhido']}")
        if chosen is None:
            write_json(out_dir / f"{file_dir.name}.falha.json", {"_meta": meta})
            continue
        write_json(out_dir / f"{file_dir.name}.json", {**chosen.answer, "_meta": meta})
        (out_dir / f"{file_dir.name}.md").write_text(redator.render_markdown(chosen.answer, package), encoding="utf-8")


def report_pending(candidates_dir: Path, inputs_dir: Path, context_dirs: list[Path],
                   base: int, maximum: int, threshold: float) -> None:
    total = 0
    for input_path in sorted(inputs_dir.glob("*.json")):
        file_dir = candidates_dir / input_path.stem
        existing = sorted(file_dir.glob("*.json")) if file_dir.exists() else []
        missing = base - len(existing)
        if missing <= 0 and len(existing) < maximum:
            candidates, _, agreement = evaluate(file_dir, load_package(input_path.stem, context_dirs))
            if agreement is None or agreement < threshold:
                missing = maximum - len(existing)
        if missing > 0:
            print(f"{input_path.stem} {missing}")
            total += missing
    print(f"{total} réplicas pendentes", file=sys.stderr)


def report_coverage(target: Path) -> None:
    total = 0
    for path in gobr_files(target):
        file = parse_file(path)
        total += sum(len(b.all_clauses()) + len(b.unclassified) for b in file.blocks)
        for block_id, item in unrecognized(file):
            print(f"{path.name}\t{block_id}\t{getattr(item, 'text', item)}")
    print(f"{total} cláusulas analisadas", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m gobr")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("contexto", "entrada"):
        cmd = commands.add_parser(name)
        cmd.add_argument("entrada", type=Path)
        cmd.add_argument("saida", type=Path)
    consolidate_cmd = commands.add_parser("consolidar")
    consolidate_cmd.add_argument("candidatos", type=Path)
    consolidate_cmd.add_argument("saida", type=Path)
    consolidate_cmd.add_argument("--contexto", type=Path, nargs="+", required=True)
    consolidate_cmd.add_argument("--prompt", type=Path, required=True)
    pending_cmd = commands.add_parser("pendentes")
    pending_cmd.add_argument("candidatos", type=Path)
    pending_cmd.add_argument("entrada", type=Path)
    pending_cmd.add_argument("--contexto", type=Path, nargs="+", required=True)
    pending_cmd.add_argument("--base", type=int, default=3)
    pending_cmd.add_argument("--maximo", type=int, default=5)
    pending_cmd.add_argument("--limiar", type=float, default=0.8)
    coverage_cmd = commands.add_parser("cobertura")
    coverage_cmd.add_argument("entrada", type=Path)
    args = parser.parse_args()
    if args.command == "contexto":
        write_packages(args.entrada, args.saida)
    elif args.command == "entrada":
        write_views(args.entrada, args.saida)
    elif args.command == "consolidar":
        consolidate(args.candidatos, args.saida, args.contexto, args.prompt)
    elif args.command == "pendentes":
        report_pending(args.candidatos, args.entrada, args.contexto, args.base, args.maximo, args.limiar)
    else:
        report_coverage(args.entrada)


if __name__ == "__main__":
    main()
