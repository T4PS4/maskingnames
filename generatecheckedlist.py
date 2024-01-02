import os
import xml.etree.ElementTree as ET
import Levenshtein
import re
import logging
import tkinter as tk

def genetiivi(etunimi):
    last_char = etunimi[-1].lower()
    if etunimi.endswith("kk") or etunimi.endswith("pp") or etunimi.endswith("tt"):
        return etunimi[:-1] + "n"
    elif etunimi.endswith("n"):
        return etunimi
    elif etunimi.endswith("i"):
        return etunimi[:-1] + "n"
    elif last_char not in 'aeiou':
        return etunimi +"in"
    else:
        return etunimi + "n"

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

def tobe_checked(word, namelist, wholetext):
    #go through all names to be checked 
  #  logging.info('checking word: '+word)
 #  
    for name in namelist:
        name = name.lower()
  #      logging.info(word+'  '+name)
        if word == name:
 #           logging.info(f"wholetext")
    #        print(f"exact match   {name} ::::         {wholetext} ")
            #return ask_to_mask()
            return True
        elif word.startswith(name) or word.endswith(name) and len(word) > 2:
    #        logging.info(f"exact match as substring at beginning or end: {name}  ::::       {wholetext}")
#            print(f"exact match as substring at beginning or end: {name}  ::::       {wholetext} ")
            return True
            #return ask_to_mask()
        elif name in word:
         #   logging.info(f"partial match {name} ::::         {wholetext} ")
 #           print(f"partial match {name} ::::         {wholetext} ")
            return True
        
        else:
            #if lenght of compared words are close
            if abs(len(name) - len(word)) < 3:

                body = namebody(name)
                if word.startswith(body):
  #                  logging.info(f"{name} alku löytyi sanan {word} alusta, ::::        {wholetext} ")
     #               print(f"{name} alku löytyi sanan {word} alusta, ::::        {wholetext} ")
                    
                 #   if ask_to_mask():
                 #       return True
                 #   else:
                    return True

    return False


    

def process_element(element, namelist, file_name, checked):
#    logging.info('Element text found in checked list: '+"\n".join(map(str, checked)))
    if element.text in checked:
 #       logging.info('Element text found in checked list: '+element.text)
        return True
 #   else:
 #       logging.info('Element text NOT found in checked list: '+element.text)

    elemtext = element.text
    
    pattern = r'.+.'  
    patternextra = r'[\(\)!/]'
 
    #split element text words into list of separate words

    origwords = elemtext.split()

    nonewlines = elemtext.replace("\n", "")
    rawtext = nonewlines.replace("", "")
    rawtext = re.sub(patternextra, '', rawtext)
    rawtext = rawtext.lower()
    rawwords = rawtext.split()

    words = [tempword.lstrip() for tempword in rawwords]

    #logging.info(','.join(map(str, origwords)))
    #logging.info(','.join(map(str, words)))
    #logging.info('----------------------------')

    
    
    for index, item in enumerate(words):
            
        if tobe_checked(item,namelist,nonewlines) == True:
            if element.text not in checked:
                logging.info('Element stored to checked list: '+element.text)
                checked.append(element.text)
            else:
                logging.info('Element already in checked list: '+element.text)
 
 
               
    return True


 


def main():
  
    checked = []
    checked_path = "C:/TIEDOSTOT/python/checked.txt"


    if os.path.exists(checked_path):
        with open(checked_path, 'r', encoding="ISO-8859-15") as checkedfile:
            checked = [line.strip() for line in checkedfile]      

     
    with open("C:/TIEDOSTOT/python/nimet.txt", 'r', encoding="Latin-1") as file:
        namelist = [line.strip() for line in file]
    
   
    directory_path = "C:/TIEDOSTOT/python/xml/vero"
    directory_path2 = "C:/TIEDOSTOT/python/xml/tilastokeskus"

    for rootdir, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(rootdir, file_name)
            tree = ET.parse(file_path)
            root = tree.getroot()

            lista = []
            elements_to_process = get_elements(root, lista)

        
         
            for selected_element in elements_to_process:
                if selected_element is not None:
                    for child in selected_element:
                        if child.tag == "RowDefinitionHeaderText" or child.tag == "ArticleName" or child.tag == "RowDefinitionDetails":
                            process_element(child, namelist, file_name,checked)

                else:
                    print("Selected element not found.")
            
    for rootdir, dirs, files in os.walk(directory_path2):
        for file_name in files:
            file_path = os.path.join(rootdir, file_name)
            tree = ET.parse(file_path)
            root = tree.getroot()

            lista = []
            elements_to_process = get_elements(root, lista)

        
         
            for selected_element in elements_to_process:
                if selected_element is not None:
                    for child in selected_element:
                        if child.tag == "RowDefinitionHeaderText" or child.tag == "ArticleName" or child.tag == "RowDefinitionDetails":
                            process_element(child, namelist, file_name,checked)

                else:
                    print("Selected element not found.")



        
    with open(checked_path, "w") as cfile:

        for item in checked:
           cfile.write(item + '\n')


    

if __name__ == "__main__":
    # Configure the logging
    log_file_path = os.path.join("C:/TIEDOSTOT/python/", 'maskaus.log')
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(message)s')

#    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

    main()
