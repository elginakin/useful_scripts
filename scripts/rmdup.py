import os
import argparse
import subprocess

def remove_duplicates(input_path, output_dir):
    """
    Remove duplicate sequences from FASTA files based on the strain name portion of the sequence headers.

    Args:
        input_path (str): Path to the input FASTA file or directory containing FASTA files.
        output_dir (str): Path to the output directory where the non-redundant FASTA files will be saved.
    """
    if os.path.isfile(input_path):
        # If input_path is a file, process the single FASTA file
        base_filename = os.path.splitext(os.path.basename(input_path))[0]
        output_file = os.path.join(output_dir, f"{base_filename}.rmdup.fasta")
        run_seqkit_rmdup(input_path, output_file)
    elif os.path.isdir(input_path):
        # If input_path is a directory, process all FASTA files in the directory
        for root, dirs, files in os.walk(input_path):
            for file in files:
                if file.endswith(".fasta"):
                    input_file = os.path.join(root, file)
                    base_filename = os.path.splitext(file)[0]
                    output_file = os.path.join(output_dir, f"{base_filename}.rmdup.fasta")
                    run_seqkit_rmdup(input_file, output_file)
    else:
        print(f"Error: {input_path} is not a valid file or directory.")

def run_seqkit_rmdup(input_file, output_file):
    """
    Run the seqkit rmdup command with the provided regular expression.

    Args:
        input_file (str): Path to the input FASTA file.
        output_file (str): Path to the output non-redundant FASTA file.
    """
    seqkit_cmd = [
        "seqkit", "rmdup",
        "-n", "--id-regexp", r"\|([^|]+)\|",
        input_file,
    ]
    with open(output_file, "w") as out_file:
        subprocess.run(seqkit_cmd, stdout=out_file, check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove duplicate sequences from FASTA files.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input FASTA file or directory containing FASTA files.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output directory for non-redundant FASTA files.")
    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    remove_duplicates(args.input, args.output)
