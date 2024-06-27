import csv
import re
import argparse


'''
This script extract the second element of fasta header and allows for further parsing of a strain name specifically. This script assumes the following: 

1. The strain name is the second element of the fasta header 
2. The primary delimter is "|".
3. The strain name contains the following format: 
    type/host/location/strain/year 
    e.g. A/human/Victoria/1234/2024

This script then splits the ID based on a specified delimiter, and writes the results to a TSV (Tab-Separated Values) file. It also includes the original header as the first column in the TSV file.

Extract Headers: The script reads a multi-FASTA file and extracts the headers.
Parse Headers: It extracts the sequence ID from the headers, which is located between the first pair of | delimiters.
Split Headers: The sequence ID is split into multiple parts based on the / delimiter.
Write to TSV: The original headers and the split parts are written to an output TSV file. The script ensures the output file includes column names specified by the user.

The script can be run from the command line and accepts the following arguments:

-i or --input: Path to the input multi-FASTA file (required).
-o or --output: Path to the output TSV file (required).
--column-names: List of column names for the output TSV file (required).

'''

def extract_and_split_headers(fasta_file):
    original_headers = []
    split_headers = []

    with open(fasta_file, 'r') as file:
        for line in file:
            if line.startswith('>'):
                # Extract the original header line
                original_header = line[1:].strip()  # Remove the '>' and strip newline
                original_headers.append(original_header)
                
                # Use regex to extract the sequence ID within the first pair of | delimiters
                match = re.search(r'\|([^|]+)\|', original_header)
                if match:
                    sequence_id = match.group(1)
                    split_headers.append(sequence_id.split('/'))
    
    return original_headers, split_headers

def write_to_tsv(original_headers, split_headers, output_file, column_names):
    max_columns = max(len(header) for header in split_headers)

    # Extend column_names if they are fewer than the maximum number of columns
    if len(column_names) < max_columns:
        column_names += [f'Part{i}' for i in range(len(column_names) + 1, max_columns + 1)]

    # Add the column name for the original header
    column_names = ['OriginalHeader'] + column_names[:max_columns]
    
    with open(output_file, 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        writer.writerow(column_names)  # Write the column names
        for original_header, split_header in zip(original_headers, split_headers):
            writer.writerow([original_header] + split_header + [''] * (max_columns - len(split_header)))  # Pad with empty strings if necessary

def main():
    parser = argparse.ArgumentParser(description='Extract and split headers from a multi-FASTA file and write to a TSV file.')
    parser.add_argument('-i', '--input', required=True, help='Path to the input multi-FASTA file')
    parser.add_argument('-o', '--output', required=True, help='Path to the output TSV file')
    parser.add_argument('--column-names', required=True, nargs='+', help='Column names for the output TSV file')

    args = parser.parse_args()

    original_headers, split_headers = extract_and_split_headers(args.input)
    write_to_tsv(original_headers, split_headers, args.output, args.column_names)

    print(f"Data has been written to {args.output}")

if __name__ == "__main__":
    main()
