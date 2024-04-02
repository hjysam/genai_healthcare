import glob, re, csv, config 
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document

mulitple_splits = []  # Initialize a list to hold individual Document objects

# To delete the database if exists previously   
try: 
    vectordb.delete_collection()
except:
    pass

# Function to process text files for PDF articles
def langchain_pdf_article(file_paths):
    # Iterate through each text file path in the list
    for txt_file in file_paths: 
        # Open and read the file
        with open(txt_file, 'r', encoding='utf-8-sig') as file:
            lines = file.readlines()
        splits = []
        metadata = {}  # Initialize a dictionary to store metadata
        # Process each line in the file
        for line in lines:
            # If line starts with 'source:', extract and store source info
            if line.startswith('source:'):
                source =  line.split(":", 1)[1].strip()

            # If line starts with 'page:', update the page number in metadata
            elif line.startswith('page'):
                page = int(re.findall(r'\d+', line)[0])
    
            # If line is not empty, create a Document with content and metadata
            elif line != '\n':
                page_content = line.strip()
                metadata = {
                        "source": source,
                        "page": page  # Default page number
                    }
                splits.append(Document(page_content=page_content, metadata=metadata))
        mulitple_splits.extend(splits)


# Function to process text files for website content
def langchain_website(file_paths):
    # Similar structure to langchain_pdf_article but with different metadata extraction
    for txt_file in file_paths: 
        with open(txt_file, 'r', encoding='utf-8-sig') as file:
            lines = file.readlines()
        splits = []
        metadata = {}  # Initialize a dictionary to store metadata        
        for line in lines:
            if line.startswith('source:'):
                source = line.split(":", 1)[1].strip()

            elif line.startswith('title'):
                title = line.split(":", 1)[1].strip()
            
            elif line != '\n':
                page_content = line.strip()
                metadata = {"source": source, "title": title}

                splits.append(Document(page_content=page_content, metadata=metadata))
        mulitple_splits.extend(splits)

# Function to process CSV files for PDF presentations
def langchain_pdf_ppt(file_paths):
    # Iterates through each CSV file, reading and processing its content
    for csv_file in file_paths:
        with open(csv_file, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                metadata = {
                    "source": str(row[1]),
                    "page": int(row[2])
                }
                mulitple_splits.append(Document(page_content=str(row[0]), metadata=metadata))



txt_files = glob.glob('data/*.txt') 
csv_files = glob.glob('data/*.csv')

# Splitting text files into two groups for processing
first_group_txt_files, second_group_txt_files = txt_files[:4], txt_files[4:]

# Process each group of files into LangChain format and update to search vector engine
langchain_pdf_article(first_group_txt_files)
langchain_website(second_group_txt_files)
langchain_pdf_ppt(csv_files)


# To keep a record of mulitple splits 
with open('result/mulitple_splits.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    # Write all rows to the CSV file
    writer.writerows(mulitple_splits)

# Update mulitple splits to search vector engine
vectordb = Chroma.from_documents(documents=mulitple_splits,embedding=config.embedding,)
