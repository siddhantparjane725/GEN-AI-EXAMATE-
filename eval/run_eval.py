
"""Evaluate MatdarMitra retrieval configurations."""

import json
from pathlib import Path

from app.embed import embed_texts
from app.vectorstore import search_documents
from app.rag import answer_question

BASE_DIR = Path(__file__).resolve().parents[1]

EVAL_PATH = BASE_DIR / "eval" / "eval_set.json"
OUTPUT_PATH = BASE_DIR / "eval" / "eval_results.md"

CONFIGS = {
    "Config A": {"chunk_size": 800, "top_k": 3},
    "Config B": {"chunk_size": 800, "top_k": 5}
}


def load_questions():
    with EVAL_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def evaluate(questions):
    reports = {}

    for config_name, config in CONFIGS.items():
        top_k = config["top_k"]
        hits = 0
        answerable_total = 0
        details = []

        print(f"\nRunning {config_name}: top_k={top_k}")

        for item in questions:
            question = item["question"]
            expected = set(item["expected_sources"])

            # Q6: verify the required abstention.
            if not item["answerable"]:
                response = answer_question(question)

                passed = response["answer"].strip().casefold().startswith(
                    "i don't know"
                )

                details.append({
                    "id": item["id"],
                    "question": question,
                    "expected": "I don't know",
                    "retrieved": "No source required",
                    "passed": passed
                })

                continue

            answerable_total += 1

            # Generate query embedding once per question.
            query_vector = embed_texts(
                [question],
                task_type="RETRIEVAL_QUERY"
            )[0]

            results = search_documents(
                query_vector,
                top_k=top_k
            )

            retrieved = {
                metadata.get("source", "")
                for metadata in results["metadatas"][0]
            }

            passed = bool(expected.intersection(retrieved))

            if passed:
                hits += 1

            details.append({
                "id": item["id"],
                "question": question,
                "expected": ", ".join(sorted(expected)),
                "retrieved": ", ".join(sorted(retrieved)),
                "passed": passed
            })

            print(
                f"Q{item['id']}: "
                f"{'PASS' if passed else 'CHECK'}"
            )

        hit_rate = (
            hits / answerable_total * 100
            if answerable_total else 0
        )

        q6_result = next(
            item for item in details if item["id"] == 6
        )

        reports[config_name] = {
            "chunk_size": config["chunk_size"],
            "top_k": top_k,
            "hits": hits,
            "total": answerable_total,
            "hit_rate": hit_rate,
            "q6_passed": q6_result["passed"],
            "details": details
        }

    return reports


def save_report(reports):
    lines = [
        "# MatdarMitra Evaluation Results",
        "",
        "Metric: percentage of answerable questions where at least "
        "one expected source PDF appears in the retrieved results.",
        "",
        "| Configuration | Chunk size (words) | Top K | Source hits | Hit rate | Q6 abstention |",
        "|---|---:|---:|---:|---:|---|"
    ]

    for name, report in reports.items():
        q6_status = "PASS" if report["q6_passed"] else "FAIL"

        lines.append(
            f"| {name} | {report['chunk_size']} | "
            f"{report['top_k']} | "
            f"{report['hits']}/{report['total']} | "
            f"{report['hit_rate']:.2f}% | {q6_status} |"
        )

    # Prefer higher hit rate; on a tie, prefer smaller top_k.
    winner = max(
        reports,
        key=lambda name: (
            reports[name]["hit_rate"],
            -reports[name]["top_k"]
        )
    )

    lines.extend([
        "",
        f"## Winner: {winner}",
        "",
        "The winner has the highest source hit rate. "
        "Ties are resolved in favour of the smaller top_k.",
        "",
        "## Question-level Results"
    ])

    for name, report in reports.items():
        lines.extend(["", f"### {name}", ""])

        for item in report["details"]:
            status = "PASS" if item["passed"] else "CHECK"

            lines.append(
                f"- **Q{item['id']} – {status}:** "
                f"{item['question']}"
            )
            lines.append(f"  - Expected: {item['expected']}")
            lines.append(f"  - Retrieved: {item['retrieved']}")

    OUTPUT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    print("\nWinner:", winner)
    print("Results saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    questions = load_questions()
    reports = evaluate(questions)
    save_report(reports)
