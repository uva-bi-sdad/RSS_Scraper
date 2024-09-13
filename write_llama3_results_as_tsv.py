import sys

FIELDS = ["green_innovation","business_innovation", "green_product", "green_process", "company", "official_company_name", "product_or_process", "likely_naics_codes", "greenwashing"]

DELIMITER = "\t"

NEW_LINE_INDICATOR = "=================================="

def remove_line_breaks(field_str):
    return_text = field_str.replace("\n", " ")
    return_text = field_str.replace("\t", " ")
    return_text = field_str.replace(",", "")
    return_text = return_text.strip()
    return return_text

_, llama_results, output_tsv = sys.argv

# Open the llama_results file
fin=open(llama_results, "r")

# Open the output file
fout=open(output_tsv, "w")

headers = "title" + DELIMITER + "link" + DELIMITER + DELIMITER.join(FIELDS) 
fout.write(f"{headers}\n")

# Loop through fin a line at a time and respond accordingly
first_line = True
new_line = True

for line in fin:
    # if new_line is true, we need to write out the line to tsv (if not first_line)
    # and reinitialize all the variables.
    if new_line:
        if not first_line:
            fout.write(f"{title}{DELIMITER}{link}{DELIMITER}{green_innovation}{DELIMITER}{business_innovation}{DELIMITER}{green_product}{DELIMITER}{green_process}{DELIMITER}{company}{DELIMITER}{official_company_name}{DELIMITER}{product_or_process}{DELIMITER}{likely_naics_codes}{DELIMITER}{greenwashing}\n")
        
        # initialize variables
        title=""
        link=""
        green_innovation=""
        business_innovation=""
        green_product=""
        green_process=""
        company=""
        official_company_name=""
        product_or_process=""
        likely_naics_codes=""
        greenwashing=""
        new_line = False

    # Read this line and see how to assign it
    if line.find("Article ") == 0:
        if first_line:
            first_line = False
        else:
            new_line = True

    elif line.find("article text:") == 0:
        link = remove_line_breaks(line)[0:150]
        title = link
    elif line.find("green_innovation") == 0:
        green_innovation = line.replace("green_innovation:", "").strip()
        print(green_innovation)
    elif line.find("business_innovation") == 0:
        business_innovation = line.replace("business_innovation:", "").strip()
    elif line.find("green_product") == 0:
        green_product = line.replace("green_product:", "").strip()
    elif line.find("green_process") == 0:
        green_process = line.replace("green_process:", "").strip()
    elif line.find("company") == 0:
        company = line.replace("company:", "").strip()
    elif line.find("official_company_name") == 0:
        official_company_name = line.replace("official_company_name:", "").strip()
    elif line.find("product_or_process") == 0:
        product_or_process = line.replace("product_or_process:", "").strip()
    elif line.find("likely_naics_codes") == 0:
        likely_naics_codes = line.replace("likely_naics_codes:", "").strip()
    elif line.find("greenwashing") == 0:
        greenwashing = line.replace("greenwashing:", "").strip()
    elif line.find("summary") == 0:
        continue
    else:
        continue
        
# write last line
fout.write(f"{title}{DELIMITER}{link}{DELIMITER}{green_innovation}{DELIMITER}{business_innovation}{DELIMITER}{green_product}{DELIMITER}{green_process}{DELIMITER}{company}{DELIMITER}{official_company_name}{DELIMITER}{product_or_process}{DELIMITER}{likely_naics_codes}{DELIMITER}{greenwashing}\n")

fin.close()
fout.close()
