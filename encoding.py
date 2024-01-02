
import os
import chardet
import xml.etree.ElementTree as ET


def muuta(file_path):
    for rootdir, dirs, files in os.walk(file_path):
        for file_name in files:
            file_path = os.path.join(rootdir, file_name)
            tree = ET.parse(file_path)
            root = tree.getroot()



            new_file_path = os.path.join("C:/TIEDOSTOT/python/ISO/tilastokeskus", file_name)
                #logging.info('Writing file out: '+new_file_path)
            xml_version="1.0"
            encoding="ISO-8859-15"
            xml_declaration = f'<?xml version="{xml_version}" encoding="{encoding}"?>\n'
        

            with open(new_file_path, "wb") as file:
             #   file.write(xml_declaration.encode(encoding))
                tree.write(file, encoding=encoding)





input_file_pathchecked = 'C:/TIEDOSTOT/python/checked.txt'
input_file_pathutf = 'C:/TIEDOSTOT/python/nimet.txt'
output_file_path = 'C:/TIEDOSTOT/python/output_iso8859_15.txt'
directory_path = "C:/TIEDOSTOT/python/xml/vero/yd_te_0000010296"
directory_path = "C:/TIEDOSTOT/python/ISO/tilastokeskus/yd_te_0000010297"
#"C:\TIEDOSTOT\python\ISO\tilastokeskus\yd_te_0000010299"
#directory_path = "C:/TIEDOSTOT/python/YD/xx/1stWeek/tilastokeskus/yd_te_0000010297"

def detect_file_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

# Example usage
xxdirectory_path = "C:/TIEDOSTOT/python/xml/tilastokeskus"
#muuta(xxdirectory_path)    
#exit
file_path = directory_path
detected_encoding = detect_file_encoding(file_path)

print(f"The detected encoding of the file {file_path} is: {detected_encoding}")

exit

input_file_path = input_file_pathutf 
#output_file_path = 'output_iso885915_file.txt'

# Read the UTF-8 file
with open(input_file_path, 'r', encoding='utf-8') as utf8_file:
    utf8_content = utf8_file.read()

# Decode the UTF-8 content into ISO-8859-15
iso885915_content = utf8_content.encode('iso-8859-15', errors='replace').decode('iso-8859-15')

# Write the ISO-8859-15 content to a new file
with open(output_file_path, 'w', encoding='iso-8859-15') as iso885915_file:
    iso885915_file.write(iso885915_content)

output_file_path = 'output_iso885915_file.txt'

# Read the UTF-8 file
with open(input_file_path, 'r', encoding='utf-8') as utf8_file:
    utf8_content = utf8_file.read()

# Decode the UTF-8 content into ISO-8859-15
iso885915_content = utf8_content.encode('iso-8859-15', errors='replace').decode('iso-8859-15')

# Write the ISO-8859-15 content to a new file
with open(output_file_path, 'w', encoding='iso-8859-15') as iso885915_file:
    iso885915_file.write(iso885915_content)
