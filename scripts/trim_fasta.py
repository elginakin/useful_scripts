"""
A simple script for trimming single or multi-fasta files according to nt or aa position. The parameters include:
    - input_file (str): Path to the input FASTA file.
    - output_file (str): Path to the output trimmed FASTA file.
    - start_position (int): Start position for trimming.
    - stop_position (int): Stop position for trimming.
"""

import argparse
import os
from Bio import SeqIO

def trim_fasta(input_file, output_file, start_position, stop_position):

    try:
        with open(input_file, 'r') as handle:
            records = SeqIO.parse(handle, 'fasta')
            trimmed_records = []

            for record in records:
                trimmed_record = record[start_position:stop_position] # absolute starting position
                trimmed_records.append(trimmed_record)

            with open(output_file, 'w') as out_handle:
                SeqIO.write(trimmed_records, out_handle, 'fasta')

        num_records_trimmed = len(trimmed_records)
        print(f"Trimming completed successfully!")
        print(f"Input file: {input_file}")
        print(f"Output file: {output_file}")
        print(f"Start position: {start_position}")
        print(f"Stop position: {stop_position}")
        print(f"Total records trimmed: {num_records_trimmed}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trim sequences in a FASTA file based on start and stop positions.")
    parser.add_argument("-i", "--input", dest="input_file", required=True, help="Path to the input FASTA file.")
    parser.add_argument("-o", "--output", dest="output_file", required=True, help="Path to the output trimmed FASTA file.")
    parser.add_argument("-s", "--start", dest="start_position", type=int, required=True, help="Start position for trimming.")
    parser.add_argument("-e", "--end", dest="stop_position", type=int, required=True, help="Stop position for trimming.")

    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
    else:
        trim_fasta(args.input_file, args.output_file, args.start_position, args.stop_position)