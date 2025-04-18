input_file = "sessionlogs_v2.json"
output_file = "sessionlogs_cleaned.json"

with open(input_file, "rb") as f:
    content = f.read()

# Remove all null bytes (b'\x00')
cleaned = content.replace(b'\x00', b'')

with open(output_file, "wb") as f:
    f.write(cleaned)

print(" Cleaned and saved to", output_file)
