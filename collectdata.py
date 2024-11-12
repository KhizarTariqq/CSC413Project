import requests
import re

# GitHub repository details
owner = "thechangelog"
repo = "transcripts"
folder_path = "practicalai"

# Output file path
output_file = "all_transcripts.txt"
cleaned_file = "all_transcripts_cleaned.txt"

# GitHub API URL for repository content
api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{folder_path}"

def get_file_content(file_url):
    """Fetch the content of a file from its raw URL."""
    response = requests.get(file_url)
    response.raise_for_status()
    return response.text

def accumulate_transcripts():
    """Accumulate text from all .md files into a single .txt file."""
    response = requests.get(api_url)
    response.raise_for_status()
    files = response.json()
    
    with open(output_file, "w", encoding="utf-8") as outfile:
        for file_info in files:
            if file_info["name"].endswith(".md"):
                print(f"Processing file: {file_info['name']}")
                
                file_content = get_file_content(file_info["download_url"])
                outfile.write(file_content + "\n\n")

    print(f"All transcripts have been saved to {output_file}")

def clean_text_file():
    """Remove line breaks, lines with '**Break**', timestamps, and citations from the text file."""
    with open(output_file, "r", encoding="utf-8") as infile, \
         open(cleaned_file, "w", encoding="utf-8") as outfile:
        
        for line in infile:
            # Remove lines that contain '**Break**'
            if "**Break**" in line:
                continue
            
            # Remove timestamps and anything inside '\[...\]'
            line = re.sub(r"\\\[[^\]]*\]", "", line)  # Remove anything inside '\[...\]' (e.g., '\[laughs\]', '\[11:57\]')

            # Remove citations, i.e., '[Something said](citation)' by keeping 'Something said' and removing the citation
            line = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", line)

            # Remove line breaks by stripping whitespace and skipping empty lines
            line = line.strip()
            if line:  # Only write non-empty lines
                outfile.write(line + "\n")  # Write each valid line on a new line
    
    print(f"Cleaned transcripts have been saved to {cleaned_file}")

def main():
    # Step 1: Accumulate all transcripts into a single .txt file
    accumulate_transcripts()
    
    # Step 2: Clean up the accumulated text file
    clean_text_file()

if __name__ == "__main__":
    main()
