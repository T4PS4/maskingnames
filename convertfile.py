


input_file_path = 'C:/TIEDOSTOT/python/masking/nimet.txt'
output_file_path = 'C:/TIEDOSTOT/python/masking/output_iso8859_15.txt'

# Read the UTF-8 file
with open(input_file_path, 'r', encoding='utf-8') as utf8_file:
    utf8_content = utf8_file.read()

# Write the content to a new file with ISO-8859-1 encoding
with open(output_file_path, 'w', encoding='iso-8859-1') as iso88591_file:
    iso88591_file.write(utf8_content)

exit

# Read the file with Latin-1 encoding
with open(input_file_path, 'r', encoding='utf-8') as input_file:
    latin1_content = input_file.read()

# Convert the Latin-1 content to Unicode
unicode_content = latin1_content.encode('utf-8').decode('ISO-8859-1')

# Write the Unicode content to the file with ISO-8859-15 encoding
with open(output_file_path, 'w', encoding='ISO-8859-1') as output_file:
    output_file.write(unicode_content)

exit

