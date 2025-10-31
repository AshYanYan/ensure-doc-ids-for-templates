import csv
import json
from pathlib import Path, PosixPath
from sys import stdout

from flatten_dict import flatten

all_pdf_templates_in_dev = "pdf-templates-dev.json"
all_pdf_templates_in_prod = "pdf-templates-prod.json"

dev_pdf_templates = []
for line in Path(all_pdf_templates_in_dev).read_text().splitlines():
    dev_pdf_templates.append(json.loads(line))

prod_pdf_templates = []
for line in Path(all_pdf_templates_in_prod).read_text().splitlines():
    prod_pdf_templates.append(json.loads(line))

dev_templates_with_docID = {}
dev_templates_without_docID = {}
prod_templates_with_docID = {}
prod_templates_without_docID = {}

 # Scaffolding for csv file
fieldnames = [
    "PDF Template ID",
    "PDF Template Name",
    "HAS DOC ID?"
]

dev_rows: list[dict] = []
prod_rows: list[dict] = []

def find_doc_ids_in_dev_templates():
    """
        Iterate through all the templates in dev and find any/all with '{doc_id}'
        Loads the PDF templates and writes them to templates_with_docID folder
    """
    output_path = Path("./output/dev_templates_with_docID")
    output_path.mkdir(parents=True, exist_ok=True)

    for pdf_template in dev_pdf_templates:
        pdf_id = pdf_template["id"]
        pdf_name = pdf_template["name"]
        flattened_pdf_template = flatten(pdf_template, enumerate_types=(list,))

        for path, value in flattened_pdf_template.items():
            if isinstance(value, str) and 'doc_id' in value:
                # print(path, value)
                dev_templates_with_docID[pdf_id] = pdf_name
                dev_rows.append(
                    {
                        "PDF Template ID": pdf_id,
                        "PDF Template Name": pdf_name,
                        "HAS DOC ID?": 'YES'
                    }
                )
                with open(f"./output/dev_templates_with_docID/{pdf_id}.json", "w", encoding="utf-8") as f:
                    json.dump(pdf_template, f, indent=4, default=str)

def find_missing_doc_ids_in_dev_templates():
    """
        Iterate through dev_pdf_templates, search for templates not in dev_templates_with_docID
        If the template is not in present in templates_with_docID, and 'test' is not in the name,
        loads the PDF templates and writes them to templates_without_docID folder
    """
    output_path = Path("./output/dev_templates_without_docID")
    output_path.mkdir(parents=True, exist_ok=True)

    for pdf_template in dev_pdf_templates:
        pdf_id = pdf_template["id"]
        pdf_name = pdf_template["name"]

        if "TEST" not in pdf_name.upper():
            if pdf_id not in dev_templates_with_docID:
                dev_templates_without_docID[pdf_id] = pdf_template
                dev_rows.append(
                    {
                        "PDF Template ID": pdf_id,
                        "PDF Template Name": pdf_name,
                        "HAS DOC ID?": 'NO'
                    }
                )
                with open(f"./output/dev_templates_without_docID/{pdf_id}.json", "w", encoding="utf-8") as f:
                    json.dump(pdf_template, f, indent=4, default=str)

    # print(f"There are {len(dev_pdf_templates)} total templates in dev")
    # print(f"There are {len(dev_templates_with_docID)} templates in dev that have doc IDs")
    # print(f"There are {len(dev_templates_without_docID)} templates in dev that DONT have doc IDs")

def find_doc_ids_in_prod_templates():
    """
        Iterate through all the templates in prod and find any/all with '{doc_id}'
        Loads the PDF templates and writes them to templates_with_docID folder
    """

    output_path = Path("./output/prod_templates_with_docID")
    output_path.mkdir(parents=True, exist_ok=True)

    for pdf_template in prod_pdf_templates:
        pdf_id = pdf_template["id"]
        pdf_name = pdf_template["name"]
        flattened_pdf_template = flatten(pdf_template, enumerate_types=(list,))

        for path, value in flattened_pdf_template.items():
            # if 'PA_batch+followup_Molina' in pdf_name:
                # print(path, value)
                # if isinstance(value, str) and '{doc_id}' in value:
                #     print("found doc id!! ")

            if isinstance(value, str) and '{doc_id}' in value:
                # print(path, value)
                # print(f" PDF ID:{pdf_id}, PDF Name:{pdf_name}")
                prod_templates_with_docID[pdf_id] = pdf_name
                prod_rows.append(
                    {
                        "PDF Template ID": pdf_id,
                        "PDF Template Name": pdf_name,
                        "HAS DOC ID?": 'YES'
                    }
                )
                with open(f"./output/prod_templates_with_docID/{pdf_id}.json", "w", encoding="utf-8") as f:
                    json.dump(pdf_template, f, indent=4, default=str)

def find_missing_doc_ids_in_prod_templates():
    """
        Iterate through prod_pdf_templates, search for templates not in prod_templates_with_docID
        If the template is not in present in templates_with_docID,
        loads the PDF templates and writes them to templates_without_docID folder
    """
    output_path = Path("./output/prod_templates_without_docID")
    output_path.mkdir(parents=True, exist_ok=True)

    for pdf_template in prod_pdf_templates:
        pdf_id = pdf_template["id"]
        pdf_name = pdf_template["name"]

        if pdf_id not in prod_templates_with_docID:
            prod_templates_without_docID[pdf_id] = pdf_template
            prod_rows.append(
                {
                    "PDF Template ID": pdf_id,
                    "PDF Template Name": pdf_name,
                    "HAS DOC ID?": 'NO'
                }
            )
            with open(f"./output/prod_templates_without_docID/{pdf_id}.json", "w", encoding="utf-8") as f:
                json.dump(pdf_template, f, indent=4, default=str)


    # print(f"There are {len(prod_pdf_templates)} total templates in prod")
    # print(f"There are {len(prod_templates_with_docID)} templates in prod that have doc IDs")
    # print(f"There are {len(prod_templates_without_docID)} templates in prod that DONT have doc IDs")

def main():


    output_path = Path("./output/templates_without_docID")
    output_path.mkdir(parents=True, exist_ok=True)

    find_doc_ids_in_dev_templates()
    find_doc_ids_in_prod_templates()
    find_missing_doc_ids_in_dev_templates()
    find_missing_doc_ids_in_prod_templates()

    with open(f"./output/dev-results.tsv", "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, dialect="excel-tab")
        writer.writeheader()
        writer.writerows(dev_rows)

    with open(f"./output/prod-results.tsv", "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, dialect="excel-tab")
        writer.writeheader()
        writer.writerows(prod_rows)

if __name__ == "__main__":
    main()
