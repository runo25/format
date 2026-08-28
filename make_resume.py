import jinja2
from weasyprint import HTML
import json
import os
import sys
import re

def split_skills(text):
    if not text:
        return []
    # Split on commas that are not inside parentheses
    items = re.split(r',\s*(?![^()]*\))', text)
    return [item.strip() for item in items if item.strip()]

template_loader = jinja2.FileSystemLoader(searchpath="./templates")
template_env = jinja2.Environment(loader=template_loader)
template_env.filters['split_skills'] = split_skills
template = template_env.get_template("universal_resume_template.html")
base_url = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists('output'):
    os.makedirs('output')

def generate_pdf(json_file, pdf_filename):
    if not os.path.exists(json_file):
        print(f"Error: Data file {json_file} not found.")
        return
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    output_html = template.render(data)
    pdf_path = os.path.join('output', pdf_filename)
    HTML(string=output_html, base_url=base_url).write_pdf(pdf_path)
    print(f"Awesome Resume Generated: {pdf_path}")

if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "all"

    if mode in ["oruno", "oruno-1page", "oruno-single"]:
        generate_pdf('data/resume_oruno_1page.json', 'Oruno_Awhie_Resume.pdf')
    elif mode in ["oruno-2page", "oruno-full"]:
        generate_pdf('data/resume_actual.json', 'Oruno_Awhie_Resume_2Page.pdf')
    elif mode in ["jennifer", "jennifer-links"]:
        generate_pdf('data/resume_jennifer.json', 'Jennifer_Patricia_Grill_Resume.pdf')
    elif mode in ["jennifer-no-links"]:
        generate_pdf('data/resume_jennifer_no_links.json', 'Jennifer_Patricia_Grill_Resume_No_Links.pdf')
    elif mode in ["letter", "official-letter"]:
        from make_letter import generate_letter
        generate_letter('data/letter_sample.json', 'Official_Letter_Sample.pdf')
    else:
        # Build all resumes
        generate_pdf('data/resume_oruno_1page.json', 'Oruno_Awhie_Resume.pdf')
        generate_pdf('data/resume_actual.json', 'Oruno_Awhie_Resume_2Page.pdf')
        generate_pdf('data/resume_jennifer.json', 'Jennifer_Patricia_Grill_Resume.pdf')
        generate_pdf('data/resume_jennifer_no_links.json', 'Jennifer_Patricia_Grill_Resume_No_Links.pdf')