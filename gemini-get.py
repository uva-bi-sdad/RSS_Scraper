import pathlib
import textwrap
import os
import sys

import google.generativeai as genai

import argparse
import glob
import pandas as pd
import json
import time
from time import gmtime, strftime
from threading import Lock

DELIMITER = "\t"
SLEEPTIME =10 

def clean_json_text(json_text):
    return_text = json_text.replace("json", "")
    return_text = return_text.replace("JSON", "")
    return_text = return_text.replace("```", "")
    return_text = return_text.strip()
    return return_text

def remove_line_breaks(field_str):
    return_text = field_str.replace("\n", " ")
    return_text = return_text.strip()
    return return_text

def call_gemini(input_json, output_file, test_mode, template, model, json_lines):
 
    print(f"Processing input file {input_json}") 
    fin = pd.read_json(input_json, lines=True)

    # print(template)
    # extract labels from the template pdf
    label_list_df = template.loc[template["mode"] == "query"]
    label_list = label_list_df["label"].to_list()

    # Create definition and query messages
    definition = ""
    query_dict = {}
    
    for index, templine in template.iterrows():
        if templine["mode"] == "definition":
            definition += " " + templine["content"]
        else: 
            query_dict[templine["label"]] = templine["content"]

    message_start = "Return a JSON object with elements "
    key_count = 0
    for key in label_list:
        if key_count == 0:
            message_start += " '" + key + "'"
        else:
            message_start += ", '" + key + "'"
        key_count += 1

    message_start += " where: "

    key_count = 0
    for key in query_dict:
        if key_count == 0:
            message_start += query_dict[key]  
        else:
            message_start += "; "+ query_dict[key]
        key_count += 1
    message_start += "."

    fout = open(output_file, "w")
    label_str = DELIMITER.join(label_list)
    if not json_lines:
        fout.write(f"title{DELIMITER}link{DELIMITER}{label_str}\n")
    
    # Send the definitions as one block
    time.sleep(SLEEPTIME)
    row_count = 0

    for key, row in fin.iterrows():
            
        if row["text"] is None:
            print(f"Article '{row['title']}' from file {input_json} could not be scraped.")
            continue
        else:
            row_count += 1
            if json_lines:
                dict = {"title": row["title"], "link": row["link"]}
            else:
                output_line = row["title"] + DELIMITER + row["link"]
            
            article = "Article: " + row["text"]

            try:
                messages = []
                messages.append({"role": "model", "parts": [definition]})
                messages.append({'role':'model', 'parts':[article]})
                messages.append({'role':'user', 'parts':[message_start]})
                # print(messages)
                response = model.generate_content(messages)
                time.sleep(SLEEPTIME)
                response_answers = clean_json_text(response.text)
            except ValueError as err:
                print(f"ERROR: {err}")
                continue
            except Exception as err:
                print("ERROR: Unknown error occurred: ", err)
                continue

            try:
                response_json = json.loads(response_answers)
            except:
                print(f"ERROR: Could not interpret gemini output for {row['title']} in {input_json}")
                continue 
            if json_lines:
                dict = {"title": row["title"], "link": row["link"]}
            else:
                output_line = row["title"] + DELIMITER + row["link"]
            for label in label_list:
                # get next item for output
                try:
                    if json_lines:
                        dict.update({label: response_json[label]})
                    else:
                        temp_label_output = response_json[label]
                except:
                    if json_lines:
                        dict.update({label: None})
                    else:
                        temp_label_output = "not found"
                if not json_lines:
                    output_line += DELIMITER + remove_line_breaks(str(temp_label_output))
                    
            # write the output for this run
            if json_lines:
                fout.write(f'{json.dumps(dict)}\n')
            else:
                fout.write(f'{output_line}\n')

    del fin
    if not test_mode:
        fout.close()    

    # chat.end_chat()
    print(f"Finished processing output file {output_file}; attempted {row_count} rows")

    return 


def main(args):
    # Read the gemini token from your environment variables
    GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
    print(f"Start time: {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")

    genai.configure(api_key=GOOGLE_API_KEY)

    # gemini-pro is an alias for gemini-1.0-pro
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    news_files = glob.glob(args.dir_to_news + "/*.json")
    if len(news_files) == 0:
        raise Exception("No .json files were found in directory: " + args.dir_to_news)
    
    template = pd.read_json(args.template, lines=True)

    for file in news_files:
        if (args.json_lines):
            outfile = args.output_dir + "/" + "gemini_" + file.split("/")[-1]
        else:    
            outfile = args.output_dir + "/" + "gemini_" + file.split("/")[-1].replace("json", "tsv")
        call_gemini(file, outfile, args.test_mode, template, model, args.json_lines)

    # clean up
    del template
    print(f"End time: {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")
    
    return


def check_args(args):
    if args.dir_to_news is not None:
        if not os.path.isdir(args.dir_to_news):
            raise ValueError("dir_to_news {} is not a valid directory".format(args.dir_to_news))

    if not args.output_dir is None and not os.path.isdir(args.output_dir):
        raise ValueError('Output directory (%s) is not a valid directory' % (
            os.path.abspath(args.outdir)))

    if args.test_mode is None:
        args.test_mode is False

    if args.json_lines is None:
        args.json_lines is False
    
    if not args.template is None and not os.path.isfile(args.template):
        raise ValueError('Template file path (%s) is not a valid file path' % (
            os.path.abspath(args.template)))
    
    return args


if __name__ == '__main__':
    from threading import Thread
    parser = argparse.ArgumentParser(description="Evaluating news articles using OpenAPI")
    parser.add_argument("-dir", "--dir_to_news", help="directory to the news json files generated by news_get.py",
                        required=True)
    parser.add_argument('-o', '--output_dir', type=str, required=True)
    parser.add_argument('-test', '--test_mode', help='allows script to be run without calling openai for testing', action=argparse.BooleanOptionalAction)
    parser.add_argument('-t', '--template', type=str,
                        help='json file with template of questions for openai', required=True)
    parser.add_argument('-j', '--json_lines', help='whether to write the output to json-lines instead of csv', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    args = check_args(args)
    main(args)

