from pypdf import PdfReader
import re # This is a Standard Regex Module

reader = PdfReader("USconstitution.pdf")

print("Number of pages:", len(reader.pages))

# Extract text from all pages and join into a single big string
full_text = ""
for page in reader.pages:
    full_text += page.extract_text() + "\n"

print("\nTotal characters before cleaning: ", len(full_text))

# Clean the repeating Footer
# This line occurs as a spaced-out footer on every page's bottom

repeating_footer = "C O N S T I T U T I O N O F T H E U N I T E D S T A T E S"
full_text = full_text.replace(repeating_footer, "")

# Also strip the resulting empty lines (multiple blank lines collapsed to one)
full_text = re.sub(r'\n{3,}', '\n\n', full_text)

print("\nTotal characters after cleaning: ", len(full_text))
print("\nFirst 1000 characters:\n")
print(full_text[:1000])

# Save it into a plain text file so it can be inspected fully if needed
with open("UScons_cleaned.txt", "w", encoding="utf-8") as f:
    f.write(full_text)

print("\nSaved full extracted and cleaned text to UScons_cleaned.txt")