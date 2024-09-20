import json
import transformers
import torch
import time
import os
from accelerate import Accelerator
import argparse

# Initialize the accelerator
accelerator = Accelerator()

# Hardcoded base directory path
base_dir = "/scratch/alw4ey/articles/batches/"

# Set up argument parser
parser = argparse.ArgumentParser(description="Process a JSON file.")
parser.add_argument("-i","--input_file", type=str, help="The JSON file to process (without the base directory)")
parser.add_argument("-o","--output_file", type=str, help="The file to save the output (without the base directory)")
args = parser.parse_args()

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

# Initialize the text generation pipeline
pipeline = transformers.pipeline(
    "text-generation", 
    model=model_id, 
    model_kwargs={"torch_dtype": torch.bfloat16}, 
    device_map="auto"
)

# Adjust the memory management environment variable
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# Print the devices being used
print("Devices being used:")
for param_name, device in pipeline.model.hf_device_map.items():
    print(f"{param_name}: {device}")

# Define the dialogs
dialogs = [
    [
        {"role": "system", "content": "Your role is that of an economist specializing in the evaluation of green product and process innovations."},
        {"role": "user", "content": "A 'green innovation' is an innovation that contributes to environmental sustainability goals."},
        {"role": "user", "content": "'Business innovation' is defined as a new or improved product or business process (or combination thereof) that differs significantly from the firm's previous products or business processes and that has been introduced on the market or brought into use by the firm."},
        {"role": "user", "content": "A 'green product' can be defined comprehensively as any good or service that is designed, manufactured, and used in a way that significantly reduces its environmental impact throughout its life cycle. This encompasses the use of environmentally benign materials, sustainable production processes that minimize energy consumption and waste, and product functionalities that support recycling and low environmental impact during usage and disposal. Green products also strive to conserve natural resources and reduce the use of toxic substances, thereby enhancing or protecting the environment while promoting both ecological and human health benefits."},
        {"role": "user", "content": "A 'green process' refers to a method or technique in manufacturing, production, or any other operational activity that minimizes environmental impacts and promotes sustainability. These processes aim to reduce waste, conserve natural resources, decrease energy consumption, and limit the release of harmful substances into the environment. Green processes often involve using renewable resources, recycling materials, employing energy-efficient technologies, and ensuring that products are biodegradable or easily recyclable at the end of their life cycle."},
        {"role": "user", "content": "'Greenwashing' is the act of making false or misleading statements about the environmental benefits of a product or practice. This deceptive marketing tactic involves the dissemination of misleading or false information to give the impression that a company's products, aims, or policies are environmentally responsible when this may not be the case. Greenwashing can manifest in various forms, such as through advertising, public statements, eco-labeling, or packaging that suggests environmental benefits which are unsubstantiated or exaggerated."}, 
        {"role": "user", "content": "If the article satisfies the definitions of green innovation, respond with the phrase: 'TRUE' and the reason why this is green innovation. If not, respond with the phrase 'FALSE' and the reason why this is not green innovation. Label this text 'green_innovation'."},
        # {"role": "user", "content": "If the article talks about a good or service that meets the definition of business product innovation, respond with the phrase 'TRUE' and the reason why it is a business product innovation. If not, respond with the phrase 'FALSE' and the reason why this is not a business product innovation. Label this text 'business_product_innovation'."},
        # {"role": "user", "content": "If the article talks about a production or delivery method that meets the definition of business process innovation, respond with the phrase 'TRUE' and the reason why this is a business process innovation. If not, respond with the phrase 'FALSE' and the reason why this is not a business process innovation. Label this text 'business_process_innovation'."},
        {"role": "user", "content": "If the article talks about a product or process  that meets the definition of business innovation, respond with the phrase 'TRUE' and the reason why this is a business innovation. If not, respond with the phrase 'FALSE' and the reason why this is not a business innovation. Label this text 'business_innovation'."},
        {"role": "user", "content": "If the article talks about a good or service that meets the definition of a green product, respond with the phrase 'TRUE' and the reason why it is a green product. If not, respond with the phrase 'FALSE' and the reason why this is not a green product. Label this text 'green_product'."},
        {"role": "user", "content": "If the article talks about a good or service that meets the definition of a green process, respond with the phrase 'TRUE' and the reason why it is a green process. If not, respond with the phrase 'FALSE' and the reason why this is not a green process. Label this text 'green_process'."},
        {"role": "user", "content": "If the company is identified, respond with the company name, otherwise respond with 'company not identified'  Label this text 'company'."},
        {"role": "user", "content": "If the company is identified, search the internet for all references to the company and respond with the most likely official name of the company. Label this text 'official_company_name'."},
        {"role": "user", "content": "If the product or process is named, respond with the product or process name, otherwise respond 'product or process not identified'. Label this text 'product_or_process'."},
        {"role": "user", "content": "How would you categorize this innovation using the North American Industry Classification System (NAICS)? Respond with 'Likely NAICS Codes: ' and the two most likely categories and codes. Label this text 'likely_naics_codes'."},
        {"role": "user", "content": "Respond whether or not you think the article text describing the product or process innovation is an example of greenwashing and why you answered this way. Label this text 'greenwashing'."},
        {"role": "user", "content": "Summarize the article text in 4 sentences or less. Label this text 'summary'."}
    ]
]

# Construct full paths for input and output files
input_file = os.path.join(base_dir, args.input_file)
output_file = os.path.join(base_dir, args.output_file)

# Load the JSON file
with open(input_file, 'r') as f:
    data = json.load(f)

article_texts = [entry["text"] for entry in data if "text" in entry and "title" in entry]
article_titles = [entry["title"] for entry in data if "text" in entry and "title" in entry]
total_articles = len(article_texts)
print(total_articles)

# Initialize the timer
start_time = time.time()

with open(output_file, 'w') as file:
    for idx, (article_text, article_title) in enumerate(zip(article_texts, article_titles)):
        article_content = f"article text: \"{article_text}\""
        dialogs[0].insert(9, {"role": "user", "content": article_content})

        for dialog in dialogs:
            conversation = ""
            for turn in dialog:
                role = turn["role"]
                content = turn["content"]
                if role == "system":
                    conversation += f"[{content}]\n"
                else:
                    conversation += f"{role.capitalize()}: {content}\n"
            
            # Generate a response for the user prompt
            response = pipeline(conversation, max_new_tokens=1000, do_sample=True, temperature=0.7, top_p=0.9)
            
            # Extract and print the generated response
            generated_text = response[0]['generated_text'].strip()
            print(f"Conversation:\n{conversation}")
            print(f"Generated Response:\n{generated_text}")
            print("\n==================================\n")
            file.write(f"Title:\n{article_title}\n")
            file.write(f"Conversation:\n{conversation}\n")
            file.write(f"Generated Response:\n{generated_text}\n")
            file.write("\n==================================\n")

        dialogs[0].pop(9)

        elapsed_time = time.time() - start_time
        completion_percentage = (idx + 1) / total_articles * 100
        print(f"Processed {idx + 1}/{total_articles} articles. Time elapsed: {elapsed_time:.2f} seconds. Completion: {completion_percentage:.2f}%.")
        # Clear GPU memory
        torch.cuda.empty_cache()

# Total processing time
total_time = time.time() - start_time
print(f"Total processing time: {total_time:.2f} seconds.")
