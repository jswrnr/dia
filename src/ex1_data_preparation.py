def filter_block(block) -> bool:
    #first filter by date
    #take the third line and get characters 3-6 as a number
    year = int(block[2][3:7])
    # if the year is not between 1995 and 2004 return
    if year < 1995 or year > 2004:
        return False
    # check if the publication venue contains the strings “SIGMOD” or “VLDB” (case insensitive)
    venue = block[3][1:]
    if "SIGMOD" not in venue.upper() and "VLDB" not in venue.upper():
        return False
    
def map_block(block) -> dict:
    # get the title
    title = block[0][2:]
    # get the authors
    authors = block[1][2:].split(",").strip().join()
    # get the year
    year = int(block[2][3:7])
    # get the publication venue
    venue = block[3][1:]
    # get the index
    index = int(block[4][6:])
    # create a dictionary with the mapped values
    mapped_block = {
        "title": title,
        "authors": authors,
        "year": year,
        "venue": venue,
        "index": index,
    }
    return mapped_block  

def save_block(block, file_name):
    with open(file_name, 'a') as file:
        file.write(block)
        file.write("\n")


def process_block(block):
    # filter unwanted blocks
    if not filter_block(block):
        return 
    mapped_block = map_block(block)



def process_file(name: str):
# Open in read mode
    with open(name, 'r') as file:
        block = []

        for line in file:
            # If the line is empty, it means the end of a block
            if line.strip() == '':
                if block:
                    # if the block is not empty, process the block
                    process_block(block)
                    block = []  # Reset the block
            else:
                # If the line is not empty, add it to the block
                block.append(line.strip())

        if block:
        # Process the remaining block if it is not empty
            process_block(block)

def main():
    process_file('data/dblp.txt')

if __name__ == '__main__':
    main()

