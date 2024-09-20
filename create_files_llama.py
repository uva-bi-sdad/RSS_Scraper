import json
import glob
import os

# Directory containing the JSON files
directory_path = '/scratch/gjf3sa/llama3/articles/news_2'
output_directory = '/scratch/gjf3sa/llama3/articles/batches'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# List all JSON files in the directory
json_files = glob.glob(os.path.join(directory_path, '*.json'))

# Initialize a list to store parsed JSON objects
data = []

for file_path in json_files:
    with open(file_path, 'r') as f:
        print(f"Opening file path {file_path}")
        for line in f:
            try:
                # Parse each line as JSON and append to data list
                json_obj = json.loads(line)
                data.append(json_obj)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON: {line}")

# Filter out articles with both text and title
articles = [{"text": entry["text"], "title": entry["title"]} for entry in data if "text" in entry and "title" in entry]
total_articles = len(articles)
print(f"Total articles: {total_articles}")

# Split articles into groups of 30
chunk_size = 30
article_chunks = [articles[i:i + chunk_size] for i in range(0, total_articles, chunk_size)]

# Save each chunk to a separate file in the output directory
for chunk_idx, article_chunk in enumerate(article_chunks):
    output_file = os.path.join(output_directory, f'articles_chunk_{chunk_idx + 1}.json')
    with open(output_file, 'w') as file:
        json.dump(article_chunk, file, indent=4)
    print(f"Saved chunk {chunk_idx + 1}/{len(article_chunks)} to {output_file}")
