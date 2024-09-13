import argparse
import os
from openai import OpenAI
import glob
import pandas as pd
import json
from threading import Thread
from threading import Lock

DELIMITER = "\t"

def call_openai(input_json, output_file, client, test_mode, template, json_lines):
 
    print(f"Processing input file {input_json}") 
    fin = pd.read_json(input_json, lines=True)

    # print(template)
    # extract labels from the template pdf
    label_list_df = template.loc[template["mode"] == "query"]
    label_list = label_list_df["label"].to_list()

    if not test_mode:
        fout = open(output_file, "w")
        label_str = DELIMITER.join(label_list)
        if not json_lines:
           fout.write(f"title{DELIMITER}link{DELIMITER}{label_str}{DELIMITER}total_tokens\n")
    system_dict = {"role": "system", "content": "Your role is that of an economist specializing in the evaluation of green product and process innovations. You are designed to output JSON."}
    # system_dict = {"role": "system", "content": "You are a helpful assistant designed to output JSON."}
    for key, row in fin.iterrows():
        if row["text"] is None:
            print(f"Article '{row['title']}' from file {input_json} could not be scraped.")
            continue
        else:
            article_messages=[]
 
            # Add message for system role
            article_messages.append(system_dict)

            for index, templine in template.iterrows():
                if templine["mode"] == "definition":
                    # Message gets added without decoration
                    tempdict = {"role": "user", "content": templine["content"]}
                elif templine["mode"] == "query":
                    # Add label definition to the end
                    tempstr = templine["content"] + " Label this text '" + templine["label"] + "'."
                    tempdict = {"role": "user", "content": tempstr}
                else:
                    # Add the article text as content
                    temp_str = "article text: " + row["text"]
                    tempdict = {"role": "user", "content": temp_str}
                article_messages.append(tempdict)

            if not test_mode:
                # query openai
                try:
                    response = client.chat.completions.create(
                      model="gpt-4o",
                      response_format={ "type": "json_object" },
                      messages=article_messages
                   )
                except: 
                    print(f"Article '{row['title']}' from file {input_json} could not be sent to openai (text too long).")
                    continue
                    
                response_out = response.choices[0].message.content
                print(response_out)
                try:
                    response_json = json.loads(response_out)
                except:
                    print(f"ERROR: Could not interpret openai output for {row['title']} in {input_json}")
                    continue 
                if json_lines:
                    dict = {"title": row["title"], "link": row["link"]}

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
                        output_line += DELIMITER + str(temp_label_output)
                    
                total_tokens = response.usage.total_tokens

                # write the output for this run
                if json_lines:
                    dict.update({"total_tokens": total_tokens})
                    fout.write(f'{json.dumps(dict)}\n')
                else:
                    fout.write(f'{output_line}{DELIMITER}{total_tokens}\n')

    del fin
    if not test_mode:
        fout.close()    

    print(f"Finished processing output file {output_file}")

    return 


def main(args):
    # Read the openapi token from your environment variables
    client = OpenAI()
    
    news_files = glob.glob(args.dir_to_news + "/*.json")
    if len(news_files) == 0:
        raise Exception("No .json files were found in directory: " + args.dir_to_news)
    
    template = pd.read_json(args.template, lines=True)
    
    for file in news_files:
        if (args.json_lines):
            outfile = args.output_dir + "/" + "openai_" + file.split("/")[-1]
        else:    
            outfile = args.output_dir + "/" + "openai_" + file.split("/")[-1].replace("json", "tsv")
        call_openai(file, outfile, client, args.test_mode, template, args.json_lines)

    # clean up
    del template
    
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

