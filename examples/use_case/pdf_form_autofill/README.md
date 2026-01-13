# PDF Form Autofill Example (NZ Form 9)

This example shows how to use OpenManus in a practical PDF form autofill flow.
It downloads the NZ Companies Register Form 9 (director consent) PDF and fills
its fields with your data using `pypdf`.

## Setup

Install the extra dependency:

```bash
pip install pypdf
```

## Usage

Download the PDF and list field names:

```bash
python examples/use_case/pdf_form_autofill/fill_form_09.py --list-fields
```

Fill the PDF with default sample data:

```bash
python examples/use_case/pdf_form_autofill/fill_form_09.py
```

Fill the PDF with your own JSON file:

```bash
python examples/use_case/pdf_form_autofill/fill_form_09.py \
  --data examples/use_case/pdf_form_autofill/data.json
```

## Example JSON

```json
{
  "CompanyName": "Example Holdings Limited",
  "CompanyNumber": "1234567",
  "DirectorFullName": "Li Wei",
  "DirectorResidentialAddress": "88 Queen Street, Auckland 1010, New Zealand",
  "DirectorEmail": "li.wei@example.com",
  "DirectorPhone": "+64 21 123 4567",
  "DirectorConsentDate": "2025-03-18"
}
```

> Note: Use `--list-fields` first to inspect the exact field names present in the
> PDF. Update the JSON keys accordingly.
