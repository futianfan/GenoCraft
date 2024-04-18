# Single-cell RNA-seq Preprocessing Workflow Using STAR

Welcome to the detailed preprocessing steps for single-cell RNA-seq analysis using the STAR aligner. This guide will walk you through the complete process from installation to the final analysis in R, ensuring you have a solid foundation to build your single-cell analysis on.

## Contents

1. [Installation](#1-installation)
2. [Preparing the Reference Genome](#2-preparing-the-reference-genome)
3. [Aligning the Reads](#3-aligning-the-reads)
4. [Post-Alignment Processing](#4-post-alignment-processing)
5. [Analyzing in R](#5-analyzing-in-r)

## 1. Installation

**Get started by installing STAR:**

Clone the STAR repository and compile the source to ensure you have the latest version:

```bash
git clone https://github.com/alexdobin/STAR.git
cd STAR/source
make STAR
```

## 2. Preparing the Reference Genome

**Before alignment, set up your reference genome:**

Creating a genome index is crucial for efficient alignment. You'll need the genome sequence in FASTA format and gene annotations in GTF format:

```bash
STAR --runThreadN NumberOfThreads \
     --runMode genomeGenerate \
     --genomeDir /path/to/genomeDir \
     --genomeFastaFiles /path/to/genome.fasta \
     --sjdbGTFfile /path/to/annotations.gtf \
     --sjdbOverhang ReadLength-1
```

- **NumberOfThreads**: Adjust this to match your CPU capabilities for faster processing.
- **ReadLength**: Typically the length of your RNA-seq reads minus one. This parameter optimizes the genome index for your specific read length.

## 3. Aligning the Reads

**Proceed to align your reads to the reference genome:**

Utilize the STAR aligner to map your RNA-seq reads efficiently:

```bash
STAR --genomeDir /path/to/genomeDir \
     --readFilesIn /path/to/read1.fastq /path/to/read2.fastq \
     --runThreadN NumberOfThreads \
     --outFileNamePrefix /path/to/outputPrefix \
     --outSAMtype BAM SortedByCoordinate
```

- **ReadFilesIn**: Specify single-end or paired-end reads appropriately.

## 4. Post-Alignment Processing

**Convert the STAR alignment outputs to count matrices:**

This step is pivotal for subsequent single-cell RNA-seq analysis:

```bash
featureCounts -T NumberOfThreads \
              -a /path/to/annotations.gtf \
              -o counts.txt \
              -g gene_id \
              /path/to/alignedReads.bam
```

- **featureCounts** is used here to summarize gene expression levels from the aligned reads.

## 5. Analyzing in R

**Load your data into R and start your analysis using Seurat or other tools:**

```r
library(Seurat)
counts <- Read10X(data.dir = "/path/to/countMatrixDirectory")
seurat_object <- CreateSeuratObject(counts = counts)
```

- **Seurat**: A comprehensive package for single-cell genomics data analysis, allowing you to perform normalization, variable gene identification, clustering, and more.

---
