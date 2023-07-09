def save_stream_to_file2(stream, filepath):
    with open(filepath, 'wb') as f:
        f.write(stream.read())



if __name__ == '__main__':
    ### 1. quality control 
    from GSEA import run_gsea_analysis, save_stream_to_file 

    import pandas as pd 
    import re 
    from quality_control import filter_low_counts 
    df = pd.read_csv('GSE99611_read_count.csv', sep = ',', dtype={0: str})
    df = df.dropna()

    #### ID2name ####
    id2name = pd.read_csv('id_to_name.csv', sep=',')
    first_column = id2name.iloc[:, 0]
    last_column = id2name.iloc[:, -3]
    id2name = dict()
    for ii, (gene_id, gene_line) in enumerate(zip(first_column, last_column)):

        try:
            idx1 = gene_line.index('(')
            idx2 = gene_line.index(')')
        except:
            continue 
        gene_name = gene_line[idx1+1:idx2]
        if any(char.islower() for char in gene_name) or len(gene_name) > 7 or ' ' in gene_name or ',' in gene_name\
            or '/' in gene_name or '-' in gene_name or "'" in gene_name: 
            continue 
        print(gene_id, gene_name)
        id2name[str(gene_id)] = gene_name
        if ii > 10000: 
            break 
    df['gene_name'] = df['ID_REF'].map(id2name)
    df = df.dropna(subset=['gene_name'])
    #### ID2name ####


    gene_name_list = df['gene_name'].tolist()
    print(gene_name_list, df)
    df = df.drop('ID_REF', axis=1)
    # df = df.drop('gene_name', axis=1)
    df = df.set_index('gene_name')
    df_filtered = filter_low_counts(df)

    ### 1.5 randomly generating case_samples control_samples 
    patient_names = df.columns.tolist()
    print(patient_names)
    case_samples = patient_names[:13]
    control_samples = patient_names[13:]
    print('case vs control:', case_samples, control_samples)
    ### 2. normalize 
    # with open('case_label.txt') as fin:
    #     lines = fin.readlines() 
    #     case_samples = [line.strip() for line in lines]
    # with open('control_label.txt') as fin:
    #     lines = fin.readlines() 
    #     control_samples = [line.strip() for line in lines]

    from Normalize import normalize_rnaseq_data 
    # print(case_samples, control_samples)
    df, case_df_cpm, control_df_cpm = normalize_rnaseq_data(df, case_samples, control_samples)
    print('normalize', df.shape, case_df_cpm.shape, df, case_df_cpm)

    ### 3. visualize 
    case_df_cpm = case_df_cpm[:1000]
    control_df_cpm = control_df_cpm[:1000]
    print(df, case_df_cpm, control_df_cpm)
    print(case_df_cpm.isna().sum())
    print(control_df_cpm.isna().sum()) 
    from Visualize import visualize  
    stream = visualize(case_df_cpm, control_df_cpm) 
    ### figure 
    save_stream_to_file(stream, 'figure/clustering.png')


    ### 4. differential analysis 
    from differential_analysis import run_differential_analysis
    # with open('read_counts.csv', 'r') as fin:
    #     lines = fin.readlines()[1:]
    #     gene_names = [line.split()[0] for line in lines] 
    # genename_list = gene_names[:len(case_df_cpm)]
    # print('deg', genename_list)
    genename_list_short = gene_name_list[:1000]

    significant_genes, significant_cases, significant_controls = \
        run_differential_analysis(genename_list_short, case_df_cpm, control_df_cpm) 
    ### figure 

    column = significant_genes.columns.tolist()[0]
    # print(column)
    significant_genes = significant_genes[0].tolist() 
    print('significant \n', significant_genes, len(significant_genes), type(significant_genes))
    with open('significant_gene.txt', 'w') as fout:
    	for gene in significant_genes:
	    	fout.write(gene + '\n') 

    ### 5/6. GSEA 
    from GSEA import run_gsea_analysis, save_stream_to_file 
    gene_names_file = 'significant_gene.txt'
    stream = run_gsea_analysis(gene_names_file, 'pathway_with_pvalues.csv')
    save_stream_to_file(stream, 'figure/gsea.png')
    ### figure 



