






input_file_path = 'C:/TIEDOSTOT/python/nimet.txt'
output_file_path = 'C:/TIEDOSTOT/python/output_iso8859_15.txt'

# Read the file with Latin-1 encoding
with open(input_file_path, 'r', encoding='latin-1') as input_file:
    latin1_content = input_file.read()

# Convert the Latin-1 content to Unicode
unicode_content = latin1_content.encode('latin-1').decode('ISO-8859-15')

# Write the Unicode content to the file with ISO-8859-15 encoding
with open(output_file_path, 'w', encoding='ISO-8859-15') as output_file:
    output_file.write(unicode_content)

