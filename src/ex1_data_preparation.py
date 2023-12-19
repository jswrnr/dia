from typing import List
import os

def filter_block(block: List[str]) -> bool:
    # check if the block has at least 4 lines
    #and check if the first line starts with #*, the second with #@, the third with #t, the fourth with #c and the fifth with #index
    if len(block) < 5 or not block[0].startswith("#*") or not block[1].startswith("#@") or not block[2].startswith("#t") or not block[3].startswith("#c") or not block[4].startswith("#index"):
        return False
    #first filter by date
    #take the third line and get characters 2-5 as a number
    year = int(block[2][2:6])
    # if the year is not between 1995 and 2004 return
    if year < 1995 or year > 2004:
        return False
    # check if the publication venue contains the strings “SIGMOD” or “VLDB” (case insensitive)
    venue = block[3][1:]
    if "SIGMOD" not in venue.upper() and "VLDB" not in venue.upper():
        return False
    return True
    
def map_block(block: List[str]) -> dict:
    # get the title
    title = block[0][2:]
    # get the authors
    authors = block[1][2:].split(",")
    for i in range(len(authors)):
        authors[i] = authors[i].strip()
    authors = ", ".join(authors)
    # get the year
    year = int(block[2][2:6])
    # get the publication venue
    venue = block[3][1:]
    # get the index
    index = block[4][6:]
    # create a dictionary with the mapped values
    mapped_block = {
        "title": title,
        "authors": authors,
        "year": year,
        "venue": venue,
        "index": index,
    }
    return mapped_block  

def save_block(block, file_name: str):
    # open the file in append mode
    with open(file_name, 'a', encoding='utf-8') as file:
        # create a string in csv format
        string = f"{block['title']};{block['authors']};{block['year']};{block['venue']};{block['index']}\n"
        # write the string to the file
        file.write(string)



def process_block(block: List[str]):
    # filter unwanted blocks
    if not filter_block(block):
        return None
    return map_block(block)



def process_file(inputFileName: str, outputFileName: str):
# delete the output file if it exists
    try:
        os.remove(outputFileName)
    except OSError:
        pass
# Open in read mode
    with open(inputFileName, 'r', encoding='utf-8') as file:
        #declare block as an empty string array
        block: List[str] = []

        for line in file:
            # If the line is empty, it means the end of a block
            if line.strip() == '':
                if block:
                    # if the block is not empty, process the block
                    processed_block = process_block(block)
                    if processed_block:
                        # if the processed block is not empty, save it
                        save_block(processed_block, outputFileName)
                    block = []  # Reset the block
            else:
                # If the line is not empty, add it to the block
                block.append(line.strip())

        if block:
        # Process the remaining block if it is not empty
            processed_block = process_block(block)
            if processed_block:
                # if the processed block is not empty, save it
                save_block(processed_block, outputFileName)

def main():
    process_file('data/dblp.txt', 'data/DBLP_1995_2004.csv')
   # process_file('data/citation-acm-v8.txt', 'data/ACM_1995_2004.csv')

if __name__ == '__main__':
    main()

