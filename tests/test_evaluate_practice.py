"""Unit tests for evaluate_practice functions without network or GPU."""

import json
from pathlib import Path
import pytest

from evaluate_practice import _load_eval_config, stage, PRACTICE_VIDEO


def test_load_eval_config_success(tmp_path: Path) -> None:
    """Đọc thành công file eval_config.json khi file tồn tại."""
    video_dir = tmp_path / PRACTICE_VIDEO
    video_dir.mkdir(parents=True, exist_ok=True)
    config_file = video_dir / "eval_config.json"
    config_file.write_text(json.dumps({"benchmark": "TEST_BENCH", "split": "train"}), encoding="utf-8")

    cfg = _load_eval_config(tmp_path)
    assert cfg["benchmark"] == "TEST_BENCH"
    assert cfg.get("split") == "train"


def test_load_eval_config_missing_raises(tmp_path: Path) -> None:
    """Ném FileNotFoundError khi thiếu file eval_config.json."""
    with pytest.raises(FileNotFoundError):
        _load_eval_config(tmp_path)


def test_stage_success(tmp_path: Path) -> None:
    """Stage sao chép đúng file gt, seqinfo và submission vào thư mục TrackEval."""
    lab_root = tmp_path / "lab_data"
    p_dir = lab_root / PRACTICE_VIDEO
    (p_dir / "gt").mkdir(parents=True, exist_ok=True)
    (p_dir / "gt" / "gt.txt").write_text("1,1,0,0,10,10,1,1,1\n", encoding="utf-8")
    (p_dir / "seqinfo.ini").write_text("[Sequence]\nname=video_1\n", encoding="utf-8")

    sub_file = tmp_path / "runs" / f"{PRACTICE_VIDEO}.txt"
    sub_file.parent.mkdir(parents=True, exist_ok=True)
    sub_file.write_text("1,1,0,0,10,10,1,-1,-1,-1\n", encoding="utf-8")

    trackeval_root = tmp_path / "TrackEval"

    stage(trackeval_root, lab_root, sub_file, "test_run", "BENCHMARK")

    gt_target = trackeval_root / "data" / "gt" / "mot_challenge" / "BENCHMARK-train" / PRACTICE_VIDEO / "gt" / "gt.txt"
    assert gt_target.exists()
    sub_target = trackeval_root / "data" / "trackers" / "mot_challenge" / "BENCHMARK-train" / "test_run" / "data" / f"{PRACTICE_VIDEO}.txt"
    assert sub_target.exists()

