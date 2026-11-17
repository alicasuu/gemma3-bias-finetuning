"""Paired TextVQA v0.5.1 validation: Gemma-3-12B-IT base vs. saved V5 LoRA.

Intended for Google Colab A100. This script never trains or changes the adapter.
The official TextVQA data/metric are downloaded at runtime; results go to Drive.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import time
import zipfile

import numpy as np


BASE_ID = "google/gemma-3-12b-it"
VAL_URL = "https://dl.fbaipublicfiles.com/textvqa/data/TextVQA_0.5.1_val.json"
IMAGE_URL = "https://dl.fbaipublicfiles.com/textvqa/images/train_val_images.zip"
# Meta's official evaluator, not a separately invented exact-match metric.
EVALUATOR_URL = (
    "https://raw.githubusercontent.com/facebookresearch/mmf/"
    "main/mmf/utils/m4c_evaluators.py"
)
SEED = 45
MAX_NEW_TOKENS = 48
PROMPT_PREFIX = (
    "Answer the question about the image. "
    "Respond with only the short answer, without an explanation.\nQuestion: "
)
RAW_COLUMNS = (
    "question_id", "image_id", "question", "prediction", "status", "error", "seconds"
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download_once(url: str, destination: Path, minimum_bytes: int) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.stat().st_size >= minimum_bytes:
        print(f"Using existing {destination} ({destination.stat().st_size:,} bytes)")
        return
    # -c resumes a partially downloaded 7-GB ZIP after a Colab disconnect.
    print(f"Downloading {url} -> {destination}", flush=True)
    subprocess.run(["wget", "--continue", "--progress=dot:giga", "--output-document", str(destination), url], check=True)
    if destination.stat().st_size < minimum_bytes:
        raise RuntimeError(f"Incomplete download: {destination}")


def choose_questions(annotations: dict, n_questions: int) -> list[dict]:
    data = annotations["data"]
    if len(data) != 5000:
        raise ValueError(f"Expected 5,000 TextVQA v0.5.1 validation questions, got {len(data)}")
    if len({str(x["question_id"]) for x in data}) != len(data):
        raise ValueError("Duplicate question IDs in validation annotations")
    ordered = sorted(data, key=lambda row: int(row["question_id"]))
    if not (1 <= n_questions <= len(ordered)):
        raise ValueError("n_questions must be in [1, 5000]")
    if n_questions < len(ordered):
        chosen_ids = set(random.Random(SEED).sample(range(len(ordered)), n_questions))
        ordered = [item for i, item in enumerate(ordered) if i in chosen_ids]
    for item in ordered:
        if len(item.get("answers", [])) != 10:
            raise ValueError("Validation annotations must have 10 ground-truth answers per question")
    return ordered


def read_successes(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if rows and set(rows[0]) != set(RAW_COLUMNS):
        raise ValueError(f"Unexpected CSV header in {path}; do not mix experiment formats")
    done = {}
    for row in rows:
        if row["status"] == "completed":
            done[row["question_id"]] = row
    return done


def append_result(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fresh = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=RAW_COLUMNS)
        if fresh:
            writer.writeheader()
        writer.writerow(row)
        stream.flush()
        os.fsync(stream.fileno())


def load_evaluator(local_path: Path):
    download_once(EVALUATOR_URL, local_path, minimum_bytes=9000)
    spec = importlib.util.spec_from_file_location("official_mmf_textvqa_evaluator", local_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not import official TextVQA evaluator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.TextVQAAccuracyEvaluator(), sha256_file(local_path)


def per_question_accuracy(evaluator, prediction: str, references: list[str]) -> float:
    # The official scorer performs EvalAI answer normalization and 10-annotator
    # leave-one-out soft matching (different from naive exact match).
    return float(evaluator.eval_pred_list([{"pred_answer": prediction, "gt_answers": references}]))


def paired_cluster_test(
    base: np.ndarray, tuned: np.ndarray, image_ids: list[str],
    *, bootstrap_iterations: int = 5000, permutations: int = 10000, seed: int = SEED,
) -> dict:
    """Image-clustered 95% bootstrap CI and paired sign-flip permutation p-value.

    Questions can share an image, so the image is the independent resampling unit.
    """
    if len(base) != len(tuned) or len(base) != len(image_ids) or len(base) == 0:
        raise ValueError("Paired score arrays and image IDs must have equal nonzero length")
    differences = np.asarray(tuned, dtype=float) - np.asarray(base, dtype=float)
    unique_images, inverse = np.unique(np.asarray(image_ids), return_inverse=True)
    group_sums = np.bincount(inverse, weights=differences)
    group_counts = np.bincount(inverse)
    rng = np.random.default_rng(seed)
    n_groups = len(unique_images)
    bootstrap = np.empty(bootstrap_iterations)
    for iteration in range(bootstrap_iterations):
        chosen = rng.integers(0, n_groups, size=n_groups)
        bootstrap[iteration] = group_sums[chosen].sum() / group_counts[chosen].sum()
    observed = float(differences.mean())
    extreme = 0
    for _ in range(permutations):
        signs = rng.choice(np.array([-1.0, 1.0]), size=n_groups)
        null_diff = float((signs * group_sums).sum() / group_counts.sum())
        extreme += abs(null_diff) >= abs(observed) - 1e-12
    low, high = np.quantile(bootstrap, [0.025, 0.975])
    return {
        "delta_percentage_points": 100 * observed,
        "delta_95pct_cluster_bootstrap_ci_pp": [100 * float(low), 100 * float(high)],
        "paired_image_cluster_signflip_two_sided_p": (extreme + 1) / (permutations + 1),
        "distinct_image_clusters": int(n_groups),
        "bootstrap_iterations": bootstrap_iterations,
        "signflip_permutations": permutations,
        "improved_questions": int(np.count_nonzero(differences > 1e-9)),
        "worse_questions": int(np.count_nonzero(differences < -1e-9)),
        "tied_questions": int(np.count_nonzero(abs(differences) <= 1e-9)),
    }


def score_saved_results(samples: list[dict], output_dir: Path, metric_path: Path) -> dict:
    base = read_successes(output_dir / "base_raw.csv")
    tuned = read_successes(output_dir / "v5_raw.csv")
    keys = [str(item["question_id"]) for item in samples]
    missing_base = [key for key in keys if key not in base]
    missing_v5 = [key for key in keys if key not in tuned]
    if missing_base or missing_v5:
        raise RuntimeError(
            f"Incomplete pair: {len(missing_base)} base and {len(missing_v5)} V5 predictions "
            "missing. Resume inference before reporting the result."
        )
    evaluator, source_hash = load_evaluator(metric_path)
    base_scores = np.array([
        per_question_accuracy(evaluator, base[key]["prediction"], sample["answers"])
        for key, sample in zip(keys, samples)
    ])
    v5_scores = np.array([
        per_question_accuracy(evaluator, tuned[key]["prediction"], sample["answers"])
        for key, sample in zip(keys, samples)
    ])
    image_ids = [str(row["image_id"]) for row in samples]
    statistical_test = paired_cluster_test(base_scores, v5_scores, image_ids)
    summary = {
        "benchmark": "TextVQA v0.5.1 validation",
        "sample_definition": "all 5,000 questions" if len(samples) == 5000 else "fixed-seed pilot subset",
        "n_questions": len(samples),
        "base_vqa_accuracy_percent": 100 * float(base_scores.mean()),
        "v5_vqa_accuracy_percent": 100 * float(v5_scores.mean()),
        **statistical_test,
        "statistically_significant_at_0_05": statistical_test["paired_image_cluster_signflip_two_sided_p"] < 0.05,
        "reference_evaluator": EVALUATOR_URL,
        "reference_evaluator_sha256": source_hash,
        "important_note": "Pilot results are not full-validation benchmark results; no test-set score is claimed.",
    }
    outfile = output_dir / f"summary_n{len(samples)}.json"
    outfile.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return summary


def generate_answer(model, processor, image, question: str, torch) -> str:
    messages = [{
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": PROMPT_PREFIX + question},
        ],
    }]
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = processor(text=text, images=[image], return_tensors="pt")
    inputs = {name: value.to("cuda:0") if torch.is_tensor(value) else value for name, value in inputs.items()}
    with torch.inference_mode():
        result = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            pad_token_id=processor.tokenizer.eos_token_id,
        )
    continuation = result[0][inputs["input_ids"].shape[-1]:]
    return processor.decode(continuation, skip_special_tokens=True).strip()


def infer_one_model(model, processor, samples, zf, image_index, output_csv, torch):
    done = read_successes(output_csv)
    pending = [sample for sample in samples if str(sample["question_id"]) not in done]
    print(f"{output_csv.name}: already {len(samples) - len(pending)}/{len(samples)}; remaining {len(pending)}")
    for index, item in enumerate(pending, 1):
        qid = str(item["question_id"])
        image_id = str(item["image_id"])
        member = image_index.get(image_id)
        if member is None:
            raise FileNotFoundError(f"Image {image_id}.jpg absent from official ZIP")
        start = time.perf_counter()
        with zf.open(member) as stream:
            from PIL import Image
            with Image.open(io.BytesIO(stream.read())) as source:
                image = source.convert("RGB")
        try:
            answer = generate_answer(model, processor, image, item["question"], torch)
            torch.cuda.synchronize()
        except Exception as exc:
            append_result(output_csv, {
                "question_id": qid, "image_id": image_id, "question": item["question"],
                "prediction": "", "status": "error", "error": repr(exc),
                "seconds": f"{time.perf_counter() - start:.3f}",
            })
            raise RuntimeError(f"Inference stopped on {qid}; prior successes retained") from exc
        append_result(output_csv, {
            "question_id": qid, "image_id": image_id, "question": item["question"],
            "prediction": answer, "status": "completed", "error": "",
            "seconds": f"{time.perf_counter() - start:.3f}",
        })
        if index % 25 == 0 or index == len(pending):
            print(f"{output_csv.name}: {index}/{len(pending)} new answers saved", flush=True)


def run(args) -> None:
    import torch
    from transformers import AutoProcessor, BitsAndBytesConfig, Gemma3ForConditionalGeneration
    from peft import PeftModel

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU is required; select Colab A100 before running")
    print("GPU:", torch.cuda.get_device_name(0))
    adapter_dir = Path(args.adapter)
    assert (adapter_dir / "adapter_config.json").is_file(), f"V5 config missing: {adapter_dir}"
    assert (adapter_dir / "adapter_model.safetensors").is_file(), f"V5 adapter weights missing: {adapter_dir}"
    output_dir = Path(args.outdir)
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = Path(args.cachedir)
    val_file = cache_dir / "TextVQA_0.5.1_val.json"
    zip_path = cache_dir / "train_val_images.zip"
    download_once(VAL_URL, val_file, minimum_bytes=2_000_000)
    # A 7-GB ZIP is kept in temporary Colab storage, not duplicated into Drive.
    if not zip_path.exists() and shutil.disk_usage(cache_dir).free < 9_000_000_000:
        raise RuntimeError("Need at least 9 GB free temporary disk for official TextVQA images")
    download_once(IMAGE_URL, zip_path, minimum_bytes=7_000_000_000)
    with val_file.open(encoding="utf-8") as stream:
        samples = choose_questions(json.load(stream), args.n)

    config = {
        "base_id": BASE_ID,
        "adapter_path": str(adapter_dir),
        "adapter_sha256": sha256_file(adapter_dir / "adapter_model.safetensors"),
        "annotation_sha256": sha256_file(val_file),
        "dataset_version": "TextVQA v0.5.1 validation",
        "annotation_url": VAL_URL,
        "image_url": IMAGE_URL,
        "seed": SEED,
        "prompt_prefix": PROMPT_PREFIX,
        "max_new_tokens": MAX_NEW_TOKENS,
        "do_sample": False,
        "quantization": "bitsandbytes 4-bit NF4, double quant, bfloat16 compute",
        "transformers_version": __import__("transformers").__version__,
        "torch_version": torch.__version__,
        "peft_version": __import__("peft").__version__,
    }
    metadata_file = output_dir / "run_config.json"
    if metadata_file.exists():
        prior = json.loads(metadata_file.read_text(encoding="utf-8"))
        # n is deliberately omitted so a fixed-seed pilot can be extended to all 5k.
        if prior != config:
            raise RuntimeError("Experiment configuration changed. Use a NEW --outdir; do not mix previous rows.")
    else:
        metadata_file.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    base_done = read_successes(output_dir / "base_raw.csv")
    v5_done = read_successes(output_dir / "v5_raw.csv")
    requested = {str(item["question_id"]) for item in samples}
    need_base = bool(requested - base_done.keys())
    need_v5 = bool(requested - v5_done.keys())
    if need_base or need_v5:
        bnb = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        processor = AutoProcessor.from_pretrained(BASE_ID)
        print("Loading Gemma 3 12B base model, no training")
        base_model = Gemma3ForConditionalGeneration.from_pretrained(
            BASE_ID, quantization_config=bnb, device_map={"": 0},
            dtype=torch.bfloat16, attn_implementation="eager",
        )
        base_model.eval()
        base_model.config.use_cache = True
        with zipfile.ZipFile(zip_path) as zf:
            image_index = {Path(name).stem: name for name in zf.namelist() if name.lower().endswith(".jpg")}
            if need_base:
                infer_one_model(base_model, processor, samples, zf, image_index,
                                output_dir / "base_raw.csv", torch)
            if need_v5:
                print("Attaching saved V5 LoRA to the SAME base weights; no training")
                tuned_model = PeftModel.from_pretrained(base_model, str(adapter_dir), is_trainable=False)
                tuned_model.eval()
                tuned_model.config.use_cache = True
                infer_one_model(tuned_model, processor, samples, zf, image_index,
                                output_dir / "v5_raw.csv", torch)
    score_saved_results(samples, output_dir, cache_dir / "m4c_evaluators.py")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=5000, help="5,000 for full validation; 100/200 for pilot")
    parser.add_argument("--adapter", default="/content/drive/MyDrive/IAT/models/gemma3-12b-v5-v4-optimized-freshbase")
    parser.add_argument("--outdir", default="/content/drive/MyDrive/IAT/results/gemma/textvqa_base_vs_v5")
    parser.add_argument("--cachedir", default="/content/textvqa_cache")
    parser.add_argument("--score-only", action="store_true", help="CPU scoring of existing complete CSVs")
    return parser.parse_args(argv)


if __name__ == "__main__":
    arguments = parse_args()
    if arguments.score_only:
        folder = Path(arguments.cachedir)
        val_path = folder / "TextVQA_0.5.1_val.json"
        download_once(VAL_URL, val_path, minimum_bytes=2_000_000)
        with val_path.open(encoding="utf-8") as stream:
            questions = choose_questions(json.load(stream), arguments.n)
        score_saved_results(questions, Path(arguments.outdir), folder / "m4c_evaluators.py")
    else:
        run(arguments)
