#!/usr/bin/env python3
"""Setuptools shim that mirrors the declarative ``pyproject.toml`` metadata."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from setuptools import find_packages, setup

ROOT = Path(__file__).resolve().parent
PROJ_METADATA = ROOT / "you-get.json"
VERSION_MODULE = ROOT / "src" / "you_get" / "version.py"


def _load_version() -> str:
    spec = importlib.util.spec_from_file_location("you_get.version", VERSION_MODULE)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive guard
        raise RuntimeError("Unable to load you_get.version module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _load_metadata() -> dict[str, object]:
    with PROJ_METADATA.open(encoding="utf-8") as handle:
        return json.load(handle)


proj_info = _load_metadata()
readme = _read_text(ROOT / "README.rst")
changelog = _read_text(ROOT / "CHANGELOG.rst")
long_description_parts = [text for text in (readme, changelog) if text]
long_description = "\n\n".join(long_description_parts)

setup(
    name=proj_info["name"],
    version=_load_version(),
    author=proj_info["author"],
    author_email=proj_info["author_email"],
    url=proj_info["url"],
    license=proj_info["license"],
    description=proj_info["description"],
    keywords=proj_info["keywords"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=find_packages("src"),
    package_dir={"": "src"},
    test_suite="tests",
    platforms="any",
    zip_safe=True,
    include_package_data=True,
    classifiers=proj_info["classifiers"],
    entry_points={"console_scripts": proj_info["console_scripts"]},
    python_requires=">=3.10",
    install_requires=["dukpy>=0.5.0"],
    extras_require={"socks": ["PySocks>=1.7.1"]},
)
