import json
import html

# Step 1: Load your original glossary
with open('full_glossary_qa.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# Your data seems to be under "glossary" key
raw_entries = raw_data["glossary"]

# Step 2: Clean and convert
fixed_glossary = []

for entry in raw_entries:
    title = entry.get("title", "").strip()
    content_html = entry.get("content", "").strip()

    # Decode HTML tags like <p> and entities
    content_text = html.unescape(content_html)
    content_text = content_text.replace("<p>", "").replace("</p>", "").replace("<br>", "").strip()

    if title and content_text:
        fixed_glossary.append({
            "question": f"What is {title}?",
            "answer": content_text
        })

# Step 3: Save cleaned glossary
with open('glossary_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(fixed_glossary, f, indent=2)

print(f"✅ Successfully created 'glossary_cleaned.json' with {len(fixed_glossary)} entries!")
