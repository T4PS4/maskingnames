import chardet

def detectfile(file):
    with open(file, 'rb') as f:
        return chardet.detect(f.read())


def utf8_to_iso8859(string_utf8):
    try:
        # Decode the UTF-8 string
        decoded_string = string_utf8.encode('latin-1', 'replace').decode('utf-8')

        # Encode the string to ISO-8859-1
        iso8859_string = decoded_string.encode('iso8859-15', 'replace').decode('latin-1')
        
        return iso8859_string
    except Exception as e:
        print(f"Error: {e}")
        return string_utf8



def get_elements(element, lista):
    if element.tag == 'InvoiceRow' or  element.tag == 'InvoiceDetails':
        lista.append(element)

    for child in element:
        get_elements(child, lista)

    return lista


def namebody(name):
    length = len(name)
    if length < 4:
        return name
    
    if "kk" in name or "pp" in name or "tt" in name:
        if length == 4:
            return name[:-2]
        return name[:-3]   

    return name[:-2] 

def ask_to_mask():

    while True:
        user_input = input("mask y/n/enter for no : ")
        if user_input.lower() == "":
            return False
        elif user_input.lower() == "y":
            return True
        elif user_input.lower() == "n":
            return False
        else:
            print("Invalid input. Please enter either 'yes' or 'no'.")



def detect_encoding(input_bytes):
    result = chardet.detect(input_bytes)
    return result['encoding']