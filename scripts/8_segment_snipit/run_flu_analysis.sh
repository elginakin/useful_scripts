#!/bin/bash
# Example wrapper script showing how to use flu_pipeline.py with your exact original setup
# Save this as run_flu_analysis.sh and make it executable: chmod +x run_flu_analysis.sh

# This recreates your original bash workflow but with the Python script

segment_snipit.py \
    --input-sequences-dir data/vic \
    --nextclade-dataset-dir nextclade/flu/vic \
    --nextclade-output-dir results/nextclade \
    --translation-pattern 'nextclade.cds_translation.{cds}.fasta' \
    --filter-list include.tsv \
    --filtered-output-dir results/snipit \
    --snipit-output-dir figures \
    --reference "JH23898" \
    --height 3 \
    --width 4 \
    --snipit-format png \
    --verbose

# Optional: Run with --dry-run first to preview commands
# ./flu_pipeline.py --dry-run [... same arguments ...]
