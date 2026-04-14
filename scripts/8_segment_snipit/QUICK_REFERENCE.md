# Quick Reference Guide

## Most Common Commands

### 1. Run Everything (Default Pipeline)
```bash
./flu_pipeline.py \
    --input-sequences-dir data/01_phylogenetics/data/vic \
    --nextclade-dataset-dir nextclade/flu/vic \
    --filter-list config/include.tsv
```

### 2. Preview Commands (Dry Run)
```bash
./flu_pipeline.py \
    --input-sequences-dir data/sequences \
    --nextclade-dataset-dir nextclade/flu/vic \
    --dry-run
```

### 3. Run Only Nextclade
```bash
./flu_pipeline.py \
    --steps nextclade \
    --input-sequences-dir data/sequences \
    --nextclade-dataset-dir nextclade/flu/vic
```

### 4. Run Only Filtering
```bash
./flu_pipeline.py \
    --steps filter \
    --input-sequences-dir data/sequences \
    --nextclade-dataset-dir nextclade/flu/vic \
    --filter-list config/include.tsv
```

### 5. Run Only Snipit
```bash
./flu_pipeline.py \
    --steps snipit \
    --input-sequences-dir data/sequences \
    --nextclade-dataset-dir nextclade/flu/vic
```

### 6. Custom Segments Only
```bash
./flu_pipeline.py \
    --segments ha,na \
    --cds HA1,HA2,NA \
    --input-sequences-dir data/sequences \
    --nextclade-dataset-dir nextclade/flu/vic
```

### 7. Different Reference Sequence
```bash
./flu_pipeline.py \
    --input-sequences-dir data/sequences \
    --nextclade-dataset-dir nextclade/flu/vic \
    --reference "A/California/07/2009"
```

### 8. High-Resolution Figures (PDF)
```bash
./flu_pipeline.py \
    --input-sequences-dir data/sequences \
    --nextclade-dataset-dir nextclade/flu/vic \
    --height 6 \
    --width 10 \
    --snipit-format pdf
```

### 9. Continue Despite Errors
```bash
./flu_pipeline.py \
    --input-sequences-dir data/sequences \
    --nextclade-dataset-dir nextclade/flu/vic \
    --continue-on-error \
    --verbose
```

### 10. Full Custom Paths (Your Original Setup)
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

## Common Option Combinations

### Minimal (Required Only)
- `--input-sequences-dir` (required)
- `--nextclade-dataset-dir` (required)

### Standard Analysis
- Add: `--filter-list config/include.tsv`
- Add: `--verbose`

### Publication Figures
- Add: `--snipit-format pdf`
- Add: `--height 6 --width 10`

### Quick Test Run
- Add: `--segments ha,na`
- Add: `--cds HA1,HA2,NA`
- Add: `--dry-run` (to preview first)

## Defaults You Can Override

| What | Default | Override with |
|------|---------|---------------|
| Segments | pb2,pb1,pa,ha,np,na,mp,ns | `--segments` |
| CDS | PB1,PB2,PA,HA1,HA2,NP,NA,NB,M1,BM2,NS1,NS2 | `--cds` |
| Input file name | sequences.fasta | `--input-fasta-name` |
| Output dir (nextclade) | results/nextclade | `--nextclade-output-dir` |
| Output dir (filtered) | results/filtered | `--filtered-output-dir` |
| Output dir (snipit) | figures | `--snipit-output-dir` |
| Figure prefix | 01_ | `--snipit-output-prefix` |
| Figure format | png | `--snipit-format` |
| Figure height | 3 | `--height` |
| Figure width | 4 | `--width` |
| Sequence type | aa | `--sequence-type` |
| Color palette | ugene | `--colour-palette` |

## Troubleshooting Quick Fixes

### "Command not found: nextclade"
- Install: `conda install -c bioconda nextclade`

### "Command not found: seqkit"
- Install: `conda install -c bioconda seqkit`

### "Command not found: snipit"
- Install: `pip install snipit`

### "Input file not found"
- Check path: `ls data/01_phylogenetics/data/vic/ha/sequences.fasta`
- Verify directory structure matches expectations

### "Empty filtered output"
- Check filter file exists: `cat config/include.tsv`
- Verify sequence IDs match FASTA headers

### Want to see what's happening?
- Add: `--verbose`

### Want to preview before running?
- Add: `--dry-run`
