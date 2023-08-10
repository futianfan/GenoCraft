def save_stream_to_file2(stream, filepath):
    with open(filepath, 'wb') as f:
        f.write(stream.read())



if __name__ == '__main__':
    ### 1. quality control 
    from GSEA import run_gsea_analysis, save_stream_to_file 

    import pandas as pd 
    import re 
    from quality_control import filter_low_counts 
    df = pd.read_csv('protein_expression.csv', sep = ',', dtype={0: str})
    df = df.set_index(df.columns[0], drop=True)
    df_filtered = filter_low_counts(df)
    
    with open('sample_label.csv', 'r') as fin:
        lines = fin.readlines()
    labels = [int(line.strip().split(',')[1]) for line in lines]

    ### 1.5 randomly generating case_samples control_samples 
    patient_names = df.columns.tolist()
    print(patient_names, len(patient_names))
    case_samples = [patient for label,patient in zip(labels, patient_names) if label==1]
    control_samples = [patient for label,patient in zip(labels, patient_names) if label==0]
    print('case vs control:', case_samples, control_samples)
    
    ### 2.missing data imputation
        # Filter out low counts
    # Perform missing data imputation
    from impute import impute_missing_values
    df_imputed = impute_missing_values(df_filtered)
    df_imputed.to_csv('df_impute.csv')
    # exit()

    ### 3. normalize 
    from Normalize import normalize_rnaseq_data 
    # print(case_samples, control_samples)
    df, case_df_cpm, control_df_cpm = normalize_rnaseq_data(df_imputed, case_samples, control_samples)
    print('normalize', df.shape, case_df_cpm.shape, df, case_df_cpm)

    ### 4. visualize 
    case_df_cpm = case_df_cpm[:1000]
    control_df_cpm = control_df_cpm[:1000]
    print(df, case_df_cpm, control_df_cpm)
    print(case_df_cpm.isna().sum())
    print(control_df_cpm.isna().sum()) 
    from Visualize import visualize  
    stream = visualize(case_df_cpm, control_df_cpm) 
    # save_stream_to_file(stream, 'figure/clustering.png')


    ### 5. differential analysis 
    from differential_analysis import run_differential_analysis
    # with open('read_counts.csv', 'r') as fin:
    #     lines = fin.readlines()[1:]
    #     gene_names = [line.split()[0] for line in lines] 
    # genename_list = gene_names[:len(case_df_cpm)]
    # print('deg', genename_list)
    genename_list_short = df.index.tolist() ## ['ALB','AGT','APOA1','APOB','B2M' ... ] 
    # genename_list_short = ['PROT_'+str(i+1) for i in range(100)]
    # print('df', df)
    # print('genename_list_short', genename_list_short)
    # print('case_df_cpm', case_df_cpm)
    # exit() 
    significant_genes, significant_cases, significant_controls = \
        run_differential_analysis(genename_list_short, case_df_cpm, control_df_cpm) 
    ### figure 

    # print('significant_genes', significant_genes)
    # print('significant_cases', significant_cases)
    # exit() 

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
    # save_stream_to_file(stream, 'figure/gsea.png')
    ### figure 


