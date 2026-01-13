#!/usr/bin/env python3
"""Fill NZ Companies Register Form 9 (director consent) PDF fields.

This script downloads the PDF, lists its form fields, and fills them
with provided data. It is intended as a practical OpenManus example for
PDF form autofill workflows.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

import requests
from pypdf import PdfReader, PdfWriter
from pypdf.generic import BooleanObject, DictionaryObject, NameObject

DEFAULT_URL = (
    "https://companies-register.companiesoffice.govt.nz/assets/companies-register/"
    "forms/nzcr-form-09-director-consent.pdf"
)

DEFAULT_DATA: Dict[str, str] = {
    "CompanyName": "Example Holdings Limited",
    "CompanyNumber": "1234567",
    "DirectorFullName": "Li Wei",
    "DirectorResidentialAddress": "88 Queen Street, Auckland 1010, New Zealand",
    "DirectorEmail": "li.wei@example.com",
    "DirectorPhone": "+64 21 123 4567",
    "DirectorConsentDate": "2025-03-18",
}


def download_pdf(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    destination.write_bytes(response.content)


def list_fields(pdf_path: Path) -> Dict[str, Any]:
    reader = PdfReader(str(pdf_path))
    fields = reader.get_fields() or {}
    return {name: field.get("/V") for name, field in fields.items()}


def _ensure_need_appearances(writer: PdfWriter) -> None:
    if "/AcroForm" not in writer._root_object:
        writer._root_object.update(
            {
                NameObject("/AcroForm"): DictionaryObject(
                    {NameObject("/NeedAppearances"): BooleanObject(True)}
                )
            }
        )
        return

    writer._root_object["/AcroForm"].update(
        {NameObject("/NeedAppearances"): BooleanObject(True)}
    )


def fill_pdf(input_path: Path, output_path: Path, data: Dict[str, str]) -> None:
    reader = PdfReader(str(input_path))
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)

    for page in writer.pages:
        writer.update_page_form_field_values(page, data)

    _ensure_need_appearances(writer)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as output_file:
        writer.write(output_file)


def load_data(path: Path) -> Dict[str, str]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Auto-fill the NZ Companies Register Form 9 PDF."
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help="PDF URL to download (defaults to Form 9).",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("examples/use_case/pdf_form_autofill/form-09.pdf"),
        help="Path to save the downloaded PDF.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("examples/use_case/pdf_form_autofill/form-09-filled.pdf"),
        help="Path to write the filled PDF.",
    )
    parser.add_argument(
        "--data",
        type=Path,
        help="JSON file containing field/value mappings.",
    )
    parser.add_argument(
        "--list-fields",
        action="store_true",
        help="List available form fields and exit.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    download_pdf(args.url, args.input)

    if args.list_fields:
        fields = list_fields(args.input)
        for name in sorted(fields):
            print(name)
        return

    data = load_data(args.data) if args.data else DEFAULT_DATA
    fill_pdf(args.input, args.output, data)
    print(f"Filled PDF saved to {args.output}")


if __name__ == "__main__":
    main()
