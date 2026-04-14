# Flu Pipeline - Nextclade + Snipit Analysis Tool

A flexible, command-line Python script for running Nextclade followed by Snipit analysis on influenza sequences.

## Features

- **Modular execution**: Run individual steps (nextclade, filter, snipit) or the complete pipeline
- **Highly configurable**: Customize all input/output paths, segments, CDS, and visualization parameters
- **Error handling**: Continue on errors or fail fast
- **Logging**: Detailed progress reporting with optional verbose mode
- **Dry-run mode**: Preview commands before execution

## Requirements

### External Tools
- [Nextclade](https://docs.nextstrain.org/projects/nextclade/en/stable/)
- [seqkit](https://bioinf.shenwei.me/seqkit/)
- [Snipit](https://github.com/aineniamh/snipit)

### Python
- Python 3.6+
- Standard library only (no additional packages required)

## Installation

1. Make the script executable:
```bash
chmod +x flu_pipeline.py
```

2. Optionally, move to a location in your PATH:
```bash
sudo mv flu_pipeline.py /usr/local/bin/flu-pipeline
```

## Usage

### Basic Usage

Run the complete pipeline with default settings:

```bash
./flu_pipeline.py \
    --input-sequences-dir data/01_phylogenetics/data/vic \
    --nextclade-dataset-dir nextclade/flu/vic
```

### Step-by-Step Execution

Run only specific steps:

```bash
# Only Nextclade
./flu_pipeline.py --steps nextclade \
    --input-sequences-dir data/sequences \
    --nextclade-dataset-dir nextclade/flu/vic

# Only filtering (assumes Nextclade already ran)
./flu_pipeline.py --steps filter \
    --input-sequences-dir data/sequences \
    --nextclade-dataset-dir nextclade/flu/vic \
    --filter-list config/include.tsv

# Only Snipit (assumes filtering already ran)
./flu_pipeline.py --steps snipit \
    --input-sequences-dir data/sequences \
    --nextclade-dataset-dir nextclade/flu/vic
```

### Custom Segments and CDS

Specify your own segments and coding sequences:

```bash
./flu_pipeline.py \
    --segments pb2,pb1,pa,ha \
    --cds PB1,PB2,PA,HA1,HA2 \
    --input-sequences-dir data/sequences \
    --nextclade-dataset-dir nextclade/flu/vic
```

### Full Customization

```bash
./flu_pipeline.py \
    --input-sequences-dir data/01_phylogenetics/data/vic \
    --input-fasta-name sequences.fasta \
    --nextclade-dataset-dir nextclade/flu/vic \
    --nextclade-output-dir results/01_phylogenetics/snipit \
    --translation-pattern 'nextclade.cds_translation.{cds}.fasta' \
    --filter-list config/include.tsv \
    --filtered-output-dir results/01_phylogenetics/snipit \
    --snipit-output-dir figures \
    --snipit-output-prefix '01_' \
    --reference "B/Austria/1359417/2021-E3(Am2/Al1)" \
    --show-indels \
    --height 3 \
    --width 4 \
    --snipit-format png \
    --verbose
```

## Command-Line Arguments

### Pipeline Control

| Argument | Default | Description |
|----------|---------|-------------|
| `--steps` | `all` | Steps to run: `nextclade`, `filter`, `snipit`, or `all` (comma-separated) |
| `--continue-on-error` | False | Continue pipeline even if individual segments/CDS fail |
| `--verbose` | False | Enable verbose output |
| `--dry-run` | False | Print commands without executing them |

### Segment and CDS Configuration

| Argument | Default | Description |
|----------|---------|-------------|
| `--segments` | `pb2,pb1,pa,ha,np,na,mp,ns` | Segments to process (comma-separated) |
| `--cds` | `PB1,PB2,PA,HA1,HA2,NP,NA,NB,M1,BM2,NS1,NS2` | CDS to extract (comma-separated) |

### Nextclade Options

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--nextclade-dataset-dir` | ✓ | - | Directory containing Nextclade datasets |
| `--input-sequences-dir` | ✓ | - | Directory containing input sequence files organized by segment |
| `--input-fasta-name` | | `sequences.fasta` | Name of input FASTA files in each segment directory |
| `--nextclade-output-dir` | | `results/nextclade` | Directory for Nextclade output translations |
| `--translation-pattern` | | `nextclade.cds_translation.{cds}.fasta` | Pattern for translation output files |

### Filtering Options

| Argument | Default | Description |
|----------|---------|-------------|
| `--filter-list` | - | File containing sequence IDs to extract (TSV format) |
| `--filtered-output-dir` | `results/filtered` | Directory for filtered sequences |

### Snipit Options

| Argument | Default | Description |
|----------|---------|-------------|
| `--snipit-output-dir` | `figures` | Directory for Snipit output figures |
| `--snipit-output-prefix` | `01_` | Prefix for Snipit output files |
| `--sequence-type` | `aa` | Sequence type (`aa` or `nt`) |
| `--colour-palette` | `ugene` | Colour palette for Snipit |
| `--reference` | `B/Austria/1359417/2021-E3(Am2/Al1)` | Reference sequence name |
| `--show-indels` | False | Show indels in Snipit plot |
| `--height` | `3.0` | Figure height in inches |
| `--width` | `4.0` | Figure width in inches |
| `--snipit-format` | `png` | Output format (`png`, `pdf`, or `svg`) |

## Directory Structure

Expected input structure:

```
data/01_phylogenetics/data/vic/
├── pb2/
│   └── sequences.fasta
├── pb1/
│   └── sequences.fasta
├── pa/
│   └── sequences.fasta
└── ...

nextclade/flu/vic/
├── pb2/
├── pb1/
├── pa/
└── ...

config/
└── include.tsv
```

Output structure (with defaults):
```
results/
├── nextclade/
│   ├── nextclade.cds_translation.PB1.fasta
│   ├── nextclade.cds_translation.PB2.fasta
│   └── ...
└── filtered/
    ├── PB1_filtered.fasta
    ├── PB2_filtered.fasta
    └── ...

figures/
├── 01_PB1_snipit_aln.png
├── 01_PB2_snipit_aln.png
└── ...
```

## Examples

### Example 1: Recreate Your Original Bash Workflow

```bash
./flu_pipeline.py \
    --input-sequences-dir data/01_phylogenetics/data/vic \
    --nextclade-dataset-dir nextclade/flu/vic \
    --nextclade-output-dir results/01_phylogenetics/snipit \
    --translation-pattern 'nextclade.cds_translation.{cds}.fasta' \
    --filter-list config/include.tsv \
    --filtered-output-dir results/01_phylogenetics/snipit \
    --snipit-output-dir figures \
    --snipit-output-prefix '01_' \
    --reference "B/Austria/1359417/2021-E3(Am2/Al1)" \
    --show-indels \
    --height 3 \
    --width 4
```

### Example 2: Different Virus Lineage

```bash
./flu_pipeline.py \
    --input-sequences-dir data/h3n2 \
    --nextclade-dataset-dir nextclade/flu/h3n2 \
    --reference "A/Wisconsin/67/2005" \
    --snipit-output-prefix 'h3n2_'
```

### Example 3: Quick Analysis (Subset of Segments)

```bash
./flu_pipeline.py \
    --segments ha,na \
    --cds HA1,HA2,NA \
    --input-sequences-dir data/quick_test \
    --nextclade-dataset-dir nextclade/flu/vic \
    --verbose
```

### Example 4: Re-run Just Snipit with Different Settings

```bash
./flu_pipeline.py \
    --steps snipit \
    --input-sequences-dir data/sequences \
    --nextclade-dataset-dir nextclade/flu/vic \
    --height 5 \
    --width 8 \
    --snipit-format pdf \
    --colour-palette viridis
```

## Troubleshooting

### Command Not Found Errors

If you get errors about `nextclade`, `seqkit`, or `snipit` not being found:

1. Ensure the tools are installed
2. Verify they're in your PATH: `which nextclade seqkit snipit`
3. Use absolute paths if needed

### Missing Input Files

The script will report which files are missing. Check:
- Input directory structure matches expectations
- Segment names match directory names
- FASTA filename matches `--input-fasta-name`

### Empty Filtered Files

If filtering produces no sequences:
- Verify the filter list file exists and contains valid sequence IDs
- Check that sequence IDs in the filter list match those in the FASTA headers

## Development

### Adding Custom Processing Steps

To add a new processing step:

1. Add a method to the `FluentPipeline` class:
```python
def run_custom_step(self) -> bool:
    """Your custom processing step."""
    logger.info("Starting custom step...")
    # Your code here
    return True
```

2. Add it to the `run()` method:
```python
if 'custom' in steps or 'all' in steps:
    if not self.run_custom_step():
        return False
```

3. Update the `--steps` help text

### Logging

The script uses Python's logging module. Adjust logging level:
- `--verbose` for DEBUG level
- Default is INFO level
- Modify `logging.basicConfig()` for custom logging

## License

This script is provided as-is for research and analysis purposes.

## Support

For issues with:
- **This script**: Check the troubleshooting section above
- **Nextclade**: https://docs.nextstrain.org/projects/nextclade/
- **seqkit**: https://bioinf.shenwei.me/seqkit/
- **Snipit**: https://github.com/aineniamh/snipit
