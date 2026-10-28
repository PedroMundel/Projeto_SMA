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
  python -m gobr manual <manual.pdf> <dir_saida>                 seções e chunks do manual (exige pdfplumber)
  python -m gobr indexar-manual <dir_manual> <dir_indice> [--modelo M]   embute os chunks do manual
  python -m gobr buscar-manual <dir_indice> "<pergunta>" [-k 3] [--modo denso|bm25|hibrido]
  python -m gobr avaliar-manual <dir_indice> --consultas <arquivo.json> [-k 5]   Recall@1/@k e MRR por modo
  python -m gobr indexar <dir_descricoes> <dir_indice> --contexto <dir> [<dir>...] --gobr <dir> [<dir>...]
        embute os chunks (arquivo, regra, consulta hipotética) com --modelo e grava vetores e metadados
  python -m gobr buscar <dir_indice> "<descrição do usuário>" [-k 5]
        arquivos mais parecidos, um por assinatura estrutural, com o caminho do .gobr
  python -m gobr avaliar-indice <dir_indice> --consultas <arquivo.json> [<arquivo.json>...]
        Recall@1/@k e MRR por variante de índice (consultas: {arquivo esperado: texto})
"""
import argparse
import json
import sys
from pathlib import Path

from gobr import consensus, redator
from gobr.context import build
from gobr.parser import parse_file, unrecognized

MODEL = "claude-sonnet-5-5"
EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-0.6B"


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


def write_manual(pdf: Path, out_dir: Path) -> None:
    from gobr import manual

    sections = manual.extract(pdf)
    if not sections:
        raise SystemExit(f"{pdf}: nenhuma seção encontrada (o capítulo 1 precisa de um título em negrito)")
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "secoes.json", [
        {"secao": s.number, "titulo": s.title, "pagina": s.page, "caminho": s.path, "texto": manual.render(s)}
        for s in sections
    ], indent=1)
    found = manual.chunks(sections)
    (out_dir / "chunks.jsonl").write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in found),
                                          encoding="utf-8")
    print(f"{len(sections)} seções, {len(found)} chunks gravados em {out_dir}")


def build_manual_index(manual_dir: Path, out_dir: Path, model: str) -> None:
    from gobr import index, manual_search

    built, manifest = manual_search.build(manual_dir, index.Embedder(model))
    manual_search.save(built, manifest, out_dir)
    print(f"{len(built.chunks)} chunks do manual ({model}) gravados em {out_dir}")


def search_manual(index_dir: Path, text: str, k: int, mode: str) -> None:
    from gobr import index, manual_search

    loaded = manual_search.load(index_dir)
    vector = index.Embedder(loaded.model).queries([text])[0]
    for n, hit in enumerate(manual_search.search(loaded, text, vector, k, mode), 1):
        print(f"{n}. {hit['secao']} {hit['titulo']} (p. {hit['pagina']})  {hit['nota']:.4f}")
        preview = [line for line in hit["chunk"]["texto"].splitlines() if line.strip() and line != "```"][-1]
        print(f"   [{hit['chunk']['tipo']}] {preview[:160]}")


def evaluate_manual(index_dir: Path, query_file: Path, k: int) -> None:
    from gobr import index, manual_search

    loaded = manual_search.load(index_dir)
    queries = json.loads(query_file.read_text(encoding="utf-8"))["consultas"]
    table = manual_search.evaluate(loaded, index.Embedder(loaded.model), queries, k)
    print(f"modelo: {loaded.model}\n")
    print(f"| modo | consultas | n | recall@1 | recall@{k} | MRR |")
    print("|---|---|---|---|---|---|")
    for (mode, kind), row in table.items():
        print(f"| {mode} | {kind} | {row['n']} | {row['recall@1']:.3f} | {row[f'recall@{k}']:.3f} | {row['mrr']:.3f} |")


def report_coverage(target: Path) -> None:
    total = 0
    for path in gobr_files(target):
        file = parse_file(path)
        total += sum(len(b.all_clauses()) + len(b.unclassified) for b in file.blocks)
        for block_id, item in unrecognized(file):
            print(f"{path.name}\t{block_id}\t{getattr(item, 'text', item)}")
    print(f"{total} cláusulas analisadas", file=sys.stderr)


# gobr.index exige numpy e sentence-transformers; o resto da CLI roda só com a biblioteca padrão.
def build_index(descriptions_dir: Path, out_dir: Path, context_dirs: list[Path], gobr_dirs: list[Path], model: str) -> None:
    from gobr import index

    built = index.build(descriptions_dir, context_dirs, gobr_dirs, index.Embedder(model))
    index.save(built, out_dir)
    print(f"{len(built.files)} arquivos, {len(built.chunks)} chunks ({model}) gravados em {out_dir}")


def search(index_dir: Path, text: str, k: int) -> None:
    from gobr import index

    loaded = index.load(index_dir)
    query = index.Embedder(loaded.model).queries([text])[0]
    for n, hit in enumerate(index.search(loaded, query, index.numbers(text), k), 1):
        same = f" (+{len(hit['equivalentes'])} de mesma estrutura)" if hit["equivalentes"] else ""
        print(f"{n}. {hit['arquivo']}  {hit['nota']:.3f}{same}  {hit['gobr']}")
        if hit["regra_mais_parecida"]:
            print(f"   regra mais parecida: {hit['regra_mais_parecida']['texto'].splitlines()[-1]}")


def evaluate_index(index_dir: Path, query_files: list[Path], k: int) -> None:
    from gobr import index

    loaded = index.load(index_dir)
    labelled = {}
    for path in query_files:
        queries = json.loads(path.read_text(encoding="utf-8"))
        labelled[path.stem] = {name: text for name, text in queries.items() if not name.startswith("_")}
    table = index.evaluate(loaded, index.Embedder(loaded.model), labelled, k)
    print(f"modelo: {loaded.model}\n")
    print(f"| chunks | peso dos números | consultas | n | recall@1 | recall@{k} | MRR | posições |")
    print("|---|---|---|---|---|---|---|---|")
    for (variant, weight, group), row in table.items():
        positions = "" if row["posicoes"] is None else " ".join(str(p or "-") for p in row["posicoes"])
        print(f"| {variant} | {weight} | {group} | {row['n']} | {row['recall@1']:.3f} | {row[f'recall@{k}']:.3f} "
              f"| {row['mrr']:.3f} | {positions} |")


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
    manual_cmd = commands.add_parser("manual")
    manual_cmd.add_argument("pdf", type=Path)
    manual_cmd.add_argument("saida", type=Path)
    manual_index_cmd = commands.add_parser("indexar-manual")
    manual_index_cmd.add_argument("manual", type=Path)
    manual_index_cmd.add_argument("saida", type=Path)
    manual_index_cmd.add_argument("--modelo", default=EMBEDDING_MODEL)
    manual_search_cmd = commands.add_parser("buscar-manual")
    manual_search_cmd.add_argument("indice", type=Path)
    manual_search_cmd.add_argument("texto")
    manual_search_cmd.add_argument("-k", type=int, default=3)
    manual_search_cmd.add_argument("--modo", choices=("denso", "bm25", "hibrido"), default="hibrido")
    manual_eval_cmd = commands.add_parser("avaliar-manual")
    manual_eval_cmd.add_argument("indice", type=Path)
    manual_eval_cmd.add_argument("--consultas", type=Path, required=True)
    manual_eval_cmd.add_argument("-k", type=int, default=5)
    coverage_cmd = commands.add_parser("cobertura")
    coverage_cmd.add_argument("entrada", type=Path)
    index_cmd = commands.add_parser("indexar")
    index_cmd.add_argument("descricoes", type=Path)
    index_cmd.add_argument("saida", type=Path)
    index_cmd.add_argument("--contexto", type=Path, nargs="+", required=True)
    index_cmd.add_argument("--gobr", type=Path, nargs="+", required=True)
    index_cmd.add_argument("--modelo", default=EMBEDDING_MODEL)
    search_cmd = commands.add_parser("buscar")
    search_cmd.add_argument("indice", type=Path)
    search_cmd.add_argument("texto")
    search_cmd.add_argument("-k", type=int, default=5)
    eval_cmd = commands.add_parser("avaliar-indice")
    eval_cmd.add_argument("indice", type=Path)
    eval_cmd.add_argument("--consultas", type=Path, nargs="+", required=True)
    eval_cmd.add_argument("-k", type=int, default=5)
    args = parser.parse_args()
    if getattr(args, "k", 1) < 1:
        parser.error("-k precisa ser pelo menos 1")
    if args.command == "contexto":
        write_packages(args.entrada, args.saida)
    elif args.command == "entrada":
        write_views(args.entrada, args.saida)
    elif args.command == "consolidar":
        consolidate(args.candidatos, args.saida, args.contexto, args.prompt)
    elif args.command == "pendentes":
        report_pending(args.candidatos, args.entrada, args.contexto, args.base, args.maximo, args.limiar)
    elif args.command == "manual":
        write_manual(args.pdf, args.saida)
    elif args.command == "indexar-manual":
        build_manual_index(args.manual, args.saida, args.modelo)
    elif args.command == "buscar-manual":
        search_manual(args.indice, args.texto, args.k, args.modo)
    elif args.command == "avaliar-manual":
        evaluate_manual(args.indice, args.consultas, args.k)
    elif args.command == "cobertura":
        report_coverage(args.entrada)
    elif args.command == "indexar":
        build_index(args.descricoes, args.saida, args.contexto, args.gobr, args.modelo)
    elif args.command == "buscar":
        search(args.indice, args.texto, args.k)
    else:
        evaluate_index(args.indice, args.consultas, args.k)


if __name__ == "__main__":
    main()
