#!/usr/bin/env python3
"""
Flexible pipeline for running Nextclade followed by Snipit on Influenza B segments.

This script provides a command-line interface to:
1. Run Nextclade on multiple segments to generate CDS translations
2. Filter sequences using seqkit
3. Run Snipit to generate alignment visualizations
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class influenzapipeline:
    """Flexible pipeline for Nextclade and Snipit analysis."""
    
    # Default values
    DEFAULT_SEGMENTS = ['pb2', 'pb1', 'pa', 'ha', 'np', 'na', 'mp', 'ns']
    DEFAULT_CDS = ['PB1', 'PB2', 'PA', 'HA1', 'HA2', 'NP', 'NA', 'NB', 'M1', 'BM2', 'NS1', 'NS2']
    
    def __init__(self, args):
        self.args = args
        self.segments = args.segments or self.DEFAULT_SEGMENTS
        self.cds = args.cds or self.DEFAULT_CDS
        
    def run_nextclade(self) -> bool:
        """
        Run Nextclade on all specified segments.
        
        Returns:
            bool: True if all runs successful, False otherwise
        """
        logger.info("Starting Nextclade analysis...")
        
        for segment in self.segments:
            # Construct paths
            dataset_path = Path(self.args.nextclade_dataset_dir) / segment
            input_fasta = Path(self.args.input_sequences_dir) / segment / self.args.input_fasta_name
            output_translation = Path(self.args.nextclade_output_dir) / self.args.translation_pattern
            
            # Check if input exists
            if not input_fasta.exists():
                logger.error(f"Input file not found: {input_fasta}")
                return False
            
            # Create output directory if it doesn't exist
            output_translation.parent.mkdir(parents=True, exist_ok=True)
            
            # Build nextclade command
            cmd = [
                'nextclade', 'run',
                '-D', str(dataset_path),
                '--output-translations', str(output_translation),
                str(input_fasta)
            ]
            
            logger.info(f"Processing segment: {segment}")
            logger.debug(f"Command: {' '.join(cmd)}")
            
            try:
                result = subprocess.run(
                    cmd,
                    check=True,
                    capture_output=True,
                    text=True
                )
                logger.info(f"✓ Nextclade completed for {segment}")
                if self.args.verbose and result.stdout:
                    logger.debug(result.stdout)
            except subprocess.CalledProcessError as e:
                logger.error(f"✗ Nextclade failed for {segment}: {e.stderr}")
                if not self.args.continue_on_error:
                    return False
            except FileNotFoundError:
                logger.error("Nextclade not found. Please ensure it's installed and in PATH.")
                return False
        
        logger.info("Nextclade analysis completed")
        return True
    
    def filter_sequences(self) -> bool:
        """
        Filter sequences using seqkit grep.
        
        Returns:
            bool: True if all filtering successful, False otherwise
        """
        logger.info("Starting sequence filtering...")
        
        if not self.args.filter_list:
            logger.warning("No filter list specified. Skipping filtering step.")
            return True
        
        filter_file = Path(self.args.filter_list)
        if not filter_file.exists():
            logger.error(f"Filter file not found: {filter_file}")
            return False
        
        for cds in self.cds:
            # Construct paths
            input_fasta = Path(self.args.nextclade_output_dir) / self.args.translation_pattern.format(cds=cds)
            output_fasta = Path(self.args.filtered_output_dir) / f"{cds}_filtered.fasta"
            
            # Check if input exists
            if not input_fasta.exists():
                logger.warning(f"Translation file not found: {input_fasta} - skipping")
                continue
            
            # Create output directory
            output_fasta.parent.mkdir(parents=True, exist_ok=True)
            
            # Build seqkit command
            cmd = [
                'seqkit', 'grep',
                '-n',
                '-f', str(filter_file),
                str(input_fasta),
                '-o', str(output_fasta)
            ]
            
            logger.info(f"Filtering CDS: {cds}")
            logger.debug(f"Command: {' '.join(cmd)}")
            
            try:
                result = subprocess.run(
                    cmd,
                    check=True,
                    capture_output=True,
                    text=True
                )
                logger.info(f"✓ Filtering completed for {cds}")
                if self.args.verbose and result.stderr:
                    logger.debug(result.stderr)
            except subprocess.CalledProcessError as e:
                logger.error(f"✗ Filtering failed for {cds}: {e.stderr}")
                if not self.args.continue_on_error:
                    return False
            except FileNotFoundError:
                logger.error("seqkit not found. Please ensure it's installed and in PATH.")
                return False
        
        logger.info("Sequence filtering completed")
        return True
    
    def run_snipit(self) -> bool:
        """
        Run Snipit on filtered sequences.
        
        Returns:
            bool: True if all runs successful, False otherwise
        """
        logger.info("Starting Snipit visualization...")
        
        for cds in self.cds:
            # Construct paths
            input_fasta = Path(self.args.filtered_output_dir) / f"{cds}_filtered.fasta"
            output_file = Path(self.args.snipit_output_dir) / f"{self.args.snipit_output_prefix}{cds}_snipit_aln.{self.args.snipit_format}"
            
            # Check if input exists
            if not input_fasta.exists():
                logger.warning(f"Filtered file not found: {input_fasta} - skipping")
                continue
            
            # Create output directory
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Build snipit command
            cmd = [
                'snipit', str(input_fasta),
                '--sequence-type', self.args.sequence_type,
                '--colour-palette', self.args.colour_palette,
                '--output-file', str(output_file),
                '--height', str(self.args.height),
                '--width', str(self.args.width),
                '--format', self.args.snipit_format
            ]
            
            # Add reference only if provided (it's optional)
            if self.args.reference:
                cmd.extend(['--reference', self.args.reference])
            
            # Add optional flags
            if self.args.show_indels:
                cmd.append('--show-indels')
            
            logger.info(f"Generating Snipit plot for: {cds}")
            logger.debug(f"Command: {' '.join(cmd)}")
            
            try:
                result = subprocess.run(
                    cmd,
                    check=True,
                    capture_output=True,
                    text=True
                )
                logger.info(f"✓ Snipit completed for {cds}")
                if self.args.verbose and result.stderr:
                    logger.debug(result.stderr)
            except subprocess.CalledProcessError as e:
                logger.error(f"✗ Snipit failed for {cds}: {e.stderr}")
                if not self.args.continue_on_error:
                    return False
            except FileNotFoundError:
                logger.error("Snipit not found. Please ensure it's installed and in PATH.")
                return False
        
        logger.info("Snipit visualization completed")
        return True
    
    def run(self) -> bool:
        """
        Run the complete pipeline based on specified steps.
        
        Returns:
            bool: True if pipeline completed successfully
        """
        steps = self.args.steps
        
        if 'nextclade' in steps or 'all' in steps:
            if not self.run_nextclade():
                logger.error("Pipeline failed at Nextclade step")
                return False
        
        if 'filter' in steps or 'all' in steps:
            if not self.filter_sequences():
                logger.error("Pipeline failed at filtering step")
                return False
        
        if 'snipit' in steps or 'all' in steps:
            if not self.run_snipit():
                logger.error("Pipeline failed at Snipit step")
                return False
        
        logger.info("Pipeline completed successfully!")
        return True


def parse_list_arg(value: str) -> List[str]:
    """Parse comma-separated list argument."""
    return [item.strip() for item in value.split(',')]


def main():
    parser = argparse.ArgumentParser(
        description='Flexible pipeline for Nextclade and Snipit analysis of influenza sequences',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run complete pipeline with default settings
  %(prog)s --input-sequences-dir data/sequences --nextclade-dataset-dir datasets/flu/vic
  
  # Run only Nextclade step
  %(prog)s --steps nextclade --input-sequences-dir data/sequences --nextclade-dataset-dir datasets/flu/vic
  
  # Custom segments and CDS
  %(prog)s --segments pb2,pb1,pa --cds PB1,PB2,PA --input-sequences-dir data/sequences --nextclade-dataset-dir datasets/flu/vic
  
  # Full customization
  %(prog)s --input-sequences-dir data/seqs \\
           --nextclade-dataset-dir nextclade/flu/vic \\
           --nextclade-output-dir results/nextclade \\
           --filtered-output-dir results/filtered \\
           --snipit-output-dir figures \\
           --filter-list config/include.tsv \\
           --reference "B/Austria/1359417/2021-E3(Am2/Al1)"
        """
    )
    
    # Pipeline control
    parser.add_argument(
        '--steps',
        type=parse_list_arg,
        default=['all'],
        help='Steps to run: nextclade, filter, snipit, or all (default: all). Comma-separated.'
    )
    
    # Segment and CDS configuration
    parser.add_argument(
        '--segments',
        type=parse_list_arg,
        default=None,
        help=f'Segments to process (default: {",".join(influenzapipeline.DEFAULT_SEGMENTS)}). Comma-separated.'
    )
    
    parser.add_argument(
        '--cds',
        type=parse_list_arg,
        default=None,
        help=f'CDS to extract (default: {",".join(influenzapipeline.DEFAULT_CDS)}). Comma-separated.'
    )
    
    # Nextclade arguments
    nextclade_group = parser.add_argument_group('Nextclade options')
    nextclade_group.add_argument(
        '--nextclade-dataset-dir',
        required=True,
        help='Directory containing Nextclade datasets (e.g., nextclade/flu/vic/)'
    )
    
    nextclade_group.add_argument(
        '--input-sequences-dir',
        required=True,
        help='Directory containing input sequence files organized by segment'
    )
    
    nextclade_group.add_argument(
        '--input-fasta-name',
        default='sequences.fasta',
        help='Name of input FASTA files in each segment directory (default: sequences.fasta)'
    )
    
    nextclade_group.add_argument(
        '--nextclade-output-dir',
        default='results/nextclade',
        help='Directory for Nextclade output translations (default: results/nextclade)'
    )
    
    nextclade_group.add_argument(
        '--translation-pattern',
        default='nextclade.cds_translation.{cds}.fasta',
        help='Pattern for translation output files (default: nextclade.cds_translation.{cds}.fasta)'
    )
    
    # Filtering arguments
    filter_group = parser.add_argument_group('Filtering options')
    filter_group.add_argument(
        '--filter-list',
        help='File containing sequence IDs to extract (for seqkit grep -f)'
    )
    
    filter_group.add_argument(
        '--filtered-output-dir',
        default='results/filtered',
        help='Directory for filtered sequences (default: results/filtered)'
    )
    
    # Snipit arguments
    snipit_group = parser.add_argument_group('Snipit options')
    snipit_group.add_argument(
        '--snipit-output-dir',
        default='figures',
        help='Directory for Snipit output figures (default: figures)'
    )
    
    snipit_group.add_argument(
        '--snipit-output-prefix',
        default='figure_',
        help='Prefix for Snipit output files (default: figure_)'
    )
    
    snipit_group.add_argument(
        '--sequence-type',
        default='aa',
        choices=['aa', 'nt'],
        help='Sequence type for Snipit (default: aa)'
    )
    
    snipit_group.add_argument(
        '--colour-palette',
        default='ugene',
        help='Colour palette for Snipit (default: ugene)'
    )
    
    snipit_group.add_argument(
        '--reference',
        default=None,
        help='Reference sequence name (example: B/Austria/1359417/2021-E3(Am2/Al1)). Optional.'
    )
    
    snipit_group.add_argument(
        '--show-indels',
        action='store_true',
        help='Show indels in Snipit plot'
    )
    
    snipit_group.add_argument(
        '--height',
        type=float,
        default=3.0,
        help='Figure height in inches (default: 3)'
    )
    
    snipit_group.add_argument(
        '--width',
        type=float,
        default=4.0,
        help='Figure width in inches (default: 4)'
    )
    
    snipit_group.add_argument(
        '--snipit-format',
        default='png',
        choices=['png', 'pdf', 'svg'],
        help='Output format for Snipit (default: png)'
    )
    
    # General options
    parser.add_argument(
        '--continue-on-error',
        action='store_true',
        help='Continue pipeline even if individual segments/CDS fail'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print commands without executing them'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Run pipeline
    if args.dry_run:
        logger.info("DRY RUN MODE - Commands will be logged but not executed")
        logger.info(f"Segments: {args.segments or influenzapipeline.DEFAULT_SEGMENTS}")
        logger.info(f"CDS: {args.cds or influenzapipeline.DEFAULT_CDS}")
        logger.info(f"Steps: {args.steps}")
        return 0
    
    pipeline = influenzapipeline(args)
    success = pipeline.run()
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())