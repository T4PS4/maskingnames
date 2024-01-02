import chardet
import os
import xml.etree.ElementTree as ET
import Levenshtein
import re
import logging
import tkinter as tk



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

def tobe_masked(word, namelist, wholetext):
    #go through all names to be checked 
 #   logging.info('checking word: '+word)
         
    for name in namelist:
        name = name.lower()
 #       logging.info(word+'  '+name)
        if name == word:
   #         logging.info(f"exact match   {name} ::::         {wholetext} ")
            print(f"exact match   {name} ::::         {wholetext} ")
            return ask_to_mask()

    for name in namelist:
        name = name.lower()

        if word.startswith(name) or word.endswith(name) and len(word) > 2:
   #         logging.info(f"exact match as substring at beginning or end: {name} word {word} ::::       {wholetext}")
            print(f"exact match as substring at beginning or end: {name} word {word} ::::       {wholetext} ")
            return ask_to_mask()
        
        elif name in word:
    #        logging.info(f"partial match {name} word {word}::::         {wholetext} ")
            print(f"partial match {name} word {word}::::         {wholetext} ")
            return ask_to_mask()
        
        else:
            #if lenght of compared words are close
            if abs(len(name) - len(word)) < 3:

                body = namebody(name)
                if word.startswith(body):
   #                 logging.info(f"{name} alku löytyi sanan {word} alusta, ::::        {wholetext} ")
                    print(f"{name} alku löytyi sanan {word} alusta, ::::        {wholetext} ")
                    
                    if ask_to_mask():
                        return True
                    else:
                        return False

    return False



    

def process_element(element, namelist, file_name, checked):
#    logging.info('Element text found in checked list: '+"\n".join(map(str, checked)))
    if element.text in checked:
#        logging.info('Element text found in checked list: '+element.text)
        return True
 #   else:
 #       logging.info('Element text NOT found in checked list: '+element.text)

    elemtext = element.text
    
    pattern1 = re.compile(r'^.{1}.')
   

    patternextra = r'[\(\),-.!/]'
 
    #split element text words into list of separate words

    origwords = elemtext.split()

    nonewlines = elemtext.replace("\n", " ")
    rawtext = nonewlines.replace("", "")
    rawtext = re.sub(patternextra, ' ', rawtext)
    origcase = rawtext.split()
    rawtext = rawtext.lower()
    rawwords = rawtext.split()

    words = [tempword.lstrip() for tempword in rawwords]
    
  #  logging.info(element.text)
  #  logging.info(','.join(map(str, origwords)))
 #   logging.info(','.join(map(str, words)))
    logging.info('----------------------------')
          
  #  return True

    occurrences = []

    
    for index, item in enumerate(words):
            
        if len(item) > 1:
            if tobe_masked(item,namelist,nonewlines) == True:

         #       logging.info(','.join(map(str, origwords)))
         #       logging.info(','.join(map(str, words)))
                logging.info('----------------------------')
                logging.info('masked : '+words[index])
                occurrences.append(index)
                #check if previous or following words are "X.", X is any char
      #          if index > 0 and index < len(words):
      #              if re.match(pattern1, words[index-1]):
      #                  occurrences.append(index-1)
      #                  logging.info("match -1 : ")

      #              elif re.match(pattern1, words[index+1]):
      #                  occurrences.append(index+1)
      #                  logging.info("match +1 : ")
            
   

    if len(occurrences) == 0:
        if element.text not in checked and len(element.text) > 2:
            logging.info('Element stored to checked list: '+element.text)
            checked.append(element.text)
    else:
        logging.info('-----> '+element.text+ " masked in file "+file_name)
      
        for indexes in occurrences:
            masking = 'X'*len(words[indexes])
            origcase[indexes] = masking 
            words[indexes] = masking 
        text = ' '.join(origcase)
        logging.info('Element old value: '+element.text)
        logging.info('Element new value: '+text)
        element.text = text
            #put element text back together

              
 
    return True


 
def detect_encoding(input_bytes):
    result = chardet.detect(input_bytes)
    return result['encoding']


def main():
    logging.info('-------------------------------------------------------------------------------------')
   
    #strings that we know the answer already
    checked = []
    checked_path = "C:/TIEDOSTOT/python/checked.txt"


    if os.path.exists(checked_path):
        with open(checked_path, 'r', encoding="ISO-8859-15") as checkedfile:
            checked = [line.strip() for line in checkedfile]      

    namelist =[]
    
#    with open("C:/TIEDOSTOT/python/nimet.txt", 'r', encoding="Latin-1") as file:
#    with open("C:/TIEDOSTOT/python/output_iso8859_15.txt", 'r', encoding="ISO-8859-15") as file:
    
    with open("C:/TIEDOSTOT/python/output_iso8859_15.txt", 'r') as file:
     
        namelist = [line.strip() for line in file]

  


    
#    list_length = len(namelist)
#    logging.info(f"names: {list_length}" )
    
#    directory_path = "C:/TIEDOSTOT/python/xml/vero"
    directory_path = "C:/TIEDOSTOT/python/ISO/tilastokeskus"

    for rootdir, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(rootdir, file_name)
#            tree = ET.parse(file_path)
#            root = tree.getroot()

            with open(file_path, 'r',  encoding="Latin-1") as xml_file:
                xml_content = xml_file.read()
            root = ET.fromstring(xml_content)





            lista = []
            elements_to_process = get_elements(root, lista)

        
         
            for selected_element in elements_to_process:
                if selected_element is not None:
                  #  logging.info('Element: '+selected_element.tag)
                    for child in selected_element:
                        if child.tag == "RowDefinitionHeaderText" or child.tag == "ArticleName" or child.tag == "RowDefinitionDetails":
                         #   logging.info('Child: '+child.tag)
                            encoding = detect_encoding(b'child.text')
                            print(encoding)

                            process_element(child, namelist, file_name,checked)

                else:
                    print("Selected element not found.")
            
            new_file_path = os.path.join("C:/TIEDOSTOT/python/mod/tilastokeskus", file_name)
            #logging.info('Writing file out: '+new_file_path)
            xml_version="1.0"
            encoding="ISO-8859-15"
            xml_declaration = f'<?xml version="{xml_version}" encoding="{encoding}"?>\n'
            
     #       with open(new_file_path, "wb") as file:
     #           #file.write(xml_declaration.encode(encoding))
     #           tree.write(file, encoding=encoding)

    with open(checked_path, "w") as cfile:

        for item in checked:
           item = item.replace("\n", " ")
           if len(item) > 1:
               cfile.write(item + '\n')


    

if __name__ == "__main__":
    # Configure the logging
    log_file_path = os.path.join("C:/TIEDOSTOT/python/", 'maskaus.log')
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(message)s')

#    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

    main()
