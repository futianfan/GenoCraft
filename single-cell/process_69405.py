input_file = "GSE69405_PROCESSED_GENE_TPM_ALL.txt"
output_file = "GSE69405_PROCESSED_GENE_TPM_ALL_ready.txt"

with open(input_file, 'r') as fin:
	lines = fin.readlines() 
	with open(output_file, 'w') as fout:
		for line in lines:
			line = line.strip().split() 
			line = [line[1]] + line[3:]
			line = '\t'.join(line) + '\n'
			fout.write(line)




