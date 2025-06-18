import csv
import json
from pathlib import Path
from sys import stdout

from flatten_dict import flatten

all_pdf_templates_in_dev = "../pdf-templates-dev.json"
all_pdf_templates_in_prod = "../pdf-templates-prod.json"

dev_pdf_templates = []
for line in Path(all_pdf_templates_in_dev).read_text().splitlines():
    dev_pdf_templates.append(json.loads(line))

prod_pdf_templates = []
for line in Path(all_pdf_templates_in_dev).read_text().splitlines():
    prod_pdf_templates.append(json.loads(line))

dev_templates_with_docID = {}
dev_templates_without_docID = {}
prod_templates_with_docID = {}
prod_templates_without_docID = {}

# Scaffolding for csv file
fieldnames = [
    "PDF Template ID",
    "PDF Template Name",
    "DOC ID VARIABLE"
]

writer = csv.DictWriter(stdout, fieldnames=fieldnames, dialect="excel-tab")
writer.writeheader()

rows: list[dict] = []


#---------------DEV SECTION---------------------------------------------------------------------
# go through all the templates in dev and find ones with doc ids
# for pdf_template in dev_pdf_templates:
#     pdf_id = pdf_template["id"]
#     pdf_name = pdf_template["name"]
#     flattened_pdf_template = flatten(pdf_template, enumerate_types=(list,))

#     for path, value in flattened_pdf_template.items():
#         if len(path) == 5 and isinstance(value,str):
#             if 'doc_id' in value:
#                 # templates_with_docID[pdf_id] = pdf_template
#                 dev_templates_with_docID[pdf_id] = pdf_name
#                 rows.append(
#                     {
#                         "PDF Template ID": pdf_id,
#                         "PDF Template Name": pdf_name,
#                         "DOC ID VARIABLE": 'YES'
#                     }
#                 )
#                 with open(f"./templates_with_docID/{pdf_id}.json", "w", encoding="utf-8") as f:
#                   json.dump(pdf_template, f, indent=4, default=str)

# iterate through all_pdf_templates_in_prod.
# If they are not in templates_with_docID then add it to templates_without_docID
# for pdf_template in dev_pdf_templates:
#     pdf_id = pdf_template["id"]
#     pdf_name = pdf_template["name"]

#     if pdf_id not in dev_templates_with_docID:
#         dev_templates_without_docID[pdf_id] = pdf_template
#         rows.append(
#             {
#                 "PDF Template ID": pdf_id,
#                 "PDF Template Name": pdf_name,
#                 "DOC ID VARIABLE": 'NO'
#             }
#         )
#         with open(f"./templates_without_docID/{pdf_id}.json", "w", encoding="utf-8") as f:
#             json.dump(pdf_template, f, indent=4, default=str)






#---------------PROD SECTION---------------------------------------------------------------------
# go through all the templates in prod and find ones with doc ids
for pdf_template in prod_pdf_templates:
    pdf_id = pdf_template["id"]
    pdf_name = pdf_template["name"]
    flattened_pdf_template = flatten(pdf_template, enumerate_types=(list,))

    for path, value in flattened_pdf_template.items():
        if len(path) == 5 and isinstance(value,str):

            if 'doc_id' in value:
                # templates_with_docID[pdf_id] = pdf_template
                prod_templates_with_docID[pdf_id] = pdf_name
                rows.append(
                    {
                        "PDF Template ID": pdf_id,
                        "PDF Template Name": pdf_name,
                        "DOC ID VARIABLE": 'YES'
                    }
                )
                with open(f"./templates_with_docID/{pdf_id}.json", "w", encoding="utf-8") as f:
                  json.dump(pdf_template, f, indent=4, default=str)

# iterate through all_pdf_templates_in_prod.
# If they are not in templates_with_docID then add it to templates_without_docID
for pdf_template in prod_pdf_templates:
    pdf_id = pdf_template["id"]
    pdf_name = pdf_template["name"]

    if pdf_id not in prod_templates_with_docID:
        prod_templates_without_docID[pdf_id] = pdf_template
        rows.append(
            {
                "PDF Template ID": pdf_id,
                "PDF Template Name": pdf_name,
                "DOC ID VARIABLE": 'NO'
            }
        )
        with open(f"./templates_without_docID/{pdf_id}.json", "w", encoding="utf-8") as f:
            json.dump(pdf_template, f, indent=4, default=str)

# print(f"There are {len(dev_pdf_templates)} total templates in dev")
# print(f"There are {len(dev_templates_with_docID)} templates in dev that have doc IDs")
# print(f"There are {len(dev_templates_without_docID)} templates in dev that DONT have doc IDs")

# print('------------------------------------------------')


print(f"There are {len(prod_pdf_templates)} total templates in prod")
print(f"There are {len(prod_templates_with_docID)} templates in dev that have doc IDs")
print(f"There are {len(prod_templates_without_docID)} templates in dev that DONT have doc IDs")

writer.writerows(rows)
