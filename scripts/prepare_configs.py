"""Create local YOLO configurations without modifying extracted datasets."""
import argparse
import json
from pathlib import Path


NAMES = [f"load_{value}" for value in (50, 60, 70, 80, 90, 100, 110)]
EXPECTED = {"Indoor_condition_dataset": {"train": 2016, "val": 112, "test": 924},
            "Multiscene_synthetic_dataset": {"train": 210, "val": 70, "test": 70}}


def write_yaml(path, payload):
    # JSON is valid YAML and avoids requiring a separate YAML parser.
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=Path("datasets"))
    parser.add_argument("--output-dir", type=Path, default=Path("configs"))
    args = parser.parse_args()
    data_root = args.data_root.resolve()
    output = args.output_dir.resolve()
    roots = {name: data_root / name for name in EXPECTED}
    payloads = []
    for name, root in roots.items():
        for split, expected in EXPECTED[name].items():
            folder = root / "images" / split
            if not folder.is_dir():
                raise FileNotFoundError(f"Missing image directory: {folder}")
            images = [p for p in folder.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg"}]
            if len(images) != expected:
                raise ValueError(f"{folder}: expected {expected} images, found {len(images)}")
            for image in images:
                label = root / "labels" / split / (image.stem + ".txt")
                if not label.is_file():
                    raise FileNotFoundError(f"Missing label: {label}")
        config = {"path": root.as_posix(), "train": "images/train", "val": "images/val",
                  "test": "images/test", "names": NAMES}
        stem = "indoor" if name == "Indoor_condition_dataset" else "synthetic"
        payloads.append((output / (stem + ".yaml"), config))

    indoor = roots["Indoor_condition_dataset"]
    lists = sorted((indoor / "test_slices").glob("*.txt"))
    if len(lists) != 8:
        raise ValueError(f"Expected 8 indoor test membership lists, found {len(lists)}")
    local_lists = []
    for source in lists:
        images = []
        for row in source.read_text(encoding="utf-8-sig").splitlines():
            if not row.strip():
                continue
            filename = row.strip().replace("\\", "/").rsplit("/", 1)[-1]
            image = indoor / "images" / "test" / filename
            if not image.is_file():
                raise FileNotFoundError(f"Subset image not found: {image}")
            images.append(image.as_posix())
        if len(images) != len(set(images)):
            raise ValueError(f"Duplicate membership in {source.name}")
        local_txt = output / "test_slices" / source.name
        local_lists.append((local_txt, "\n".join(images) + "\n"))
        payloads.append((local_txt.with_suffix(".yaml"), {
            "path": indoor.as_posix(), "train": "images/train", "val": "images/val",
            "test": local_txt.as_posix(), "names": NAMES}))

    # All source paths are checked before writing generated configuration files.
    for destination, body in local_lists:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(body, encoding="utf-8")
    for destination, payload in payloads:
        write_yaml(destination, payload)
    print(f"Created {len(payloads)} configurations and {len(local_lists)} test lists in {output}")
    print("Extracted images, labels, metadata and original configurations were not changed.")


if __name__ == "__main__":
    main()
