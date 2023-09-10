# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import sys
import base64
import os
from collections import defaultdict

from flask import request
from flask_restx import Api, Resource
import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    RunRealtimeReportRequest,
)

from bulk_rna_workflow import quality_control as bulk_qc
from bulk_rna_workflow import differential_analysis as bulk_diff
from bulk_rna_workflow import gene_set_enrichment_analysis as bulk_gsea
from bulk_rna_workflow import network_analysis as bulk_network
from bulk_rna_workflow import normalize as bulk_norm
from bulk_rna_workflow import normalization_visualize as bulk_visual

from genocraft_secrets import constants

from single_cell_rna_workflow import normalize as sc_norm
from single_cell_rna_workflow import reduce_dimension as sc_dimension
from single_cell_rna_workflow import clustering as sc_clus
from single_cell_rna_workflow import visualization as sc_visual
from single_cell_rna_workflow import differential_expression as sc_diff
from single_cell_rna_workflow import gene_set_enrichment_analysis as sc_gsea

from protein_workflow import quality_control as protein_qc
from protein_workflow import imputation as protein_imp
from protein_workflow import normalization as protein_norm
from protein_workflow import visualization as protein_visual
from protein_workflow import differential_analysis as protein_diff
from protein_workflow import gene_set_enrichment_analysis as protein_gsea

rest_api = Api(version="1.0", title="GenoCraft API")

BULK_ALLOWED_FILE_TYPES = ['text/plain', 'text/csv']
SINGLE_ALLOWED_FILE_TYPES = ['text/csv']
PROTEIN_ALLOWED_FILE_TYPES = ['text/csv']


@rest_api.route('/api/time')
class Time(Resource):
    def get(self):
        import time
        return {'time': time.strftime("%I:%M:%S %p", time.localtime())}


@rest_api.route('/api/google-analytics-report')
class GoogleAnalyticsReport(Resource):
    def get(self):
        os.environ[
            'GOOGLE_APPLICATION_CREDENTIALS'] = f"genocraft_secrets/{constants.GOOGLE_ANALYTICS_CREDENTIAL_FILE_NAME}"
        client = BetaAnalyticsDataClient()

        requestAccumulate = RunReportRequest(
            property=f"properties/{constants.PROPERTY_ID}",
            dimensions=[Dimension(name="eventName")],
            metrics=[Metric(name="eventCount")],
            date_ranges=[DateRange(start_date="2023-06-01", end_date="today")],
        )

        requestRealTime = RunRealtimeReportRequest(
            property=f"properties/{constants.PROPERTY_ID}",
            dimensions=[Dimension(name="eventName")],
            metrics=[Metric(name="eventCount")],
        )
        responseAccumulate = client.run_report(requestAccumulate)

        responseRealTime = client.run_realtime_report(requestRealTime)

        report = defaultdict(lambda: 0)
        for row in responseAccumulate.rows:
            report[row.dimension_values[0].value] = int(row.metric_values[0].value)

        for row in responseRealTime.rows:
            report[row.dimension_values[0].value] += int(row.metric_values[0].value)

        return {
                   "success": True,
                   "page_view": report["page_view"],
                   "bulk_api_triggered": report["Click-Bulk-Start"],
                   "single_api_triggered": report["Click-Single-Cell-Start"],
               }, 200


@rest_api.route('/api/analyze/bulk')
class AnalyzeBulk(Resource):
    def post(self):
        upload_own_file = request.form.get('upload_own_file') == 'true'
        number_of_files = 0

        read_counts_df = None
        control_label_file = None
        case_label_file = None

        if upload_own_file:
            number_of_files = int(request.form.get('number_of_files'))
            for idx in range(number_of_files):
                file = request.files.get('file-' + str(idx))
                file_stream = file.stream
                file_type = file.content_type
                if file_type not in BULK_ALLOWED_FILE_TYPES:
                    return {
                               "success": False,
                               "msg": "Only .csv or .txt files are allowed."
                           }, 500

                file_stream.seek(0)
                if file.filename == 'case_label.txt':
                    case_label_file = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', header=None))
                elif file.filename == 'control_label.txt':
                    control_label_file = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', header=None))
                elif file.filename == 'read_counts.csv':
                    read_counts_df = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    print("=== read_counts_df ===\n", read_counts_df.shape, read_counts_df.head())
                else:
                    pass  # TO-DO
        else:
            file_directory = os.path.dirname('./demo_data/bulk_data/')
            read_counts_df = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'read_counts.csv'), 'r'), index_col=0, header=0))
            case_label_file = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'case_label.txt'), 'r'), header=None))
            control_label_file = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'control_label.txt'), 'r'), header=None))
            print("=== DEMO read_counts_df ===\n", read_counts_df.head())

        case_label_list = None
        control_label_list = None
        if case_label_file is not None:
            case_label_list = [x[0].strip() for x in case_label_file.values.tolist()]
            print("=== case_label_list ===\n", len(case_label_list), case_label_list[:10])
        if control_label_file is not None:
            control_label_list = [x[0].strip() for x in control_label_file.values.tolist()]
            print("=== control_label_list ===\n", len(control_label_list), control_label_list[:10])

        qualityControlSelected = request.form.get('quality_control') == 'true'
        normalizationSelected = request.form.get('normalization') == 'true'
        visualizationAfterNormSelected = request.form.get('visualization_after_normalization') == 'true'
        differentialSelected = request.form.get('differential_analysis') == 'true'
        networkSelected = request.form.get('network_analysis') == 'true'
        geneSelected = request.form.get('gene_set_enrichment_analysis') == 'true'
        visualizationSelected = request.form.get('visualization') == 'true'

        results = []
        quality_controlled_df = None
        if qualityControlSelected:
            if read_counts_df is None:
                return {
                           "success": False,
                           "msg": "Missing files for quality control."
                       }, 500
            quality_controlled_df = bulk_qc.filter_low_counts(read_counts_df)
            results.append(
                {
                    'filename': 'quality_control_results.csv',
                    'content_type': 'text/csv',
                    'content': quality_controlled_df.to_csv(header=True, index=True, sep=',')
                }
            )

        normalized_cases = None
        normalized_controls = None

        if normalizationSelected:
            if quality_controlled_df is None or case_label_file is None or control_label_file is None:
                return {
                           "success": False,
                           "msg": "Missing files for normalization."
                       }, 500

            normalized_cases, normalized_controls = bulk_norm.normalize_rnaseq_data(quality_controlled_df, case_label_list,
                                                                          control_label_list)
            results.extend([
                {
                    'filename': 'normalized_cases.csv',
                    'content_type': 'text/csv',
                    'content': normalized_cases.to_csv(header=True, index=True, sep=',')
                },
                {
                    'filename': 'normalized_controls.csv',
                    'content_type': 'text/csv',
                    'content': normalized_controls.to_csv(header=True, index=True, sep=',')
                }
            ])

        if visualizationAfterNormSelected:
            if normalized_cases is None or normalized_controls is None:
                return {
                           "success": False,
                           "msg": "Missing files for normalization visualization."
                       }, 500
            normalized_data_visualization_img = bulk_visual.visualize(normalized_cases, normalized_controls)
            results.append(
                {
                    'filename': 'normalization_visualization.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(normalized_data_visualization_img).decode('utf8')
                },
            )

        significant_genes = None
        significant_cases = None
        significant_controls = None

        if differentialSelected:
            if quality_controlled_df is None or normalized_cases is None or normalized_controls is None:
                return {
                           "success": False,
                           "msg": "Missing files for differential analysis."
                       }, 500

            gene_name_list = [str(x).strip() for x in quality_controlled_df.index]
            significant_genes, significant_cases, significant_controls = bulk_diff.run_differential_analysis(gene_name_list,
                                                                                                   normalized_cases,
                                                                                                   normalized_controls)
            results.extend([
                {
                    'filename': 'differential_analysis_significant_genes.txt',
                    'content_type': 'text/plain',
                    'content': significant_genes.to_csv(header=None, index=None, sep=' ')
                },
                {
                    'filename': 'differential_analysis_significant_cases.csv',
                    'content_type': 'text/csv',
                    'content': significant_cases.to_csv(header=True, index=True, sep=',')
                },
                {
                    'filename': 'differential_analysis_significant_controls.csv',
                    'content_type': 'text/csv',
                    'content': significant_controls.to_csv(header=True, index=True, sep=',')
                }
            ])

        if networkSelected:
            if significant_genes is None or significant_cases is None or significant_controls is None:
                return {
                           "success": False,
                           "msg": "Missing files or pre-requisite step for network analysis."
                       }, 500

            differential_network_img, differential_network_df = bulk_network.run_network_analysis(significant_cases,
                                                                                     significant_controls,
                                                                                     significant_genes)

            if differential_network_df is not None:
                results.append(
                    {
                        'filename': 'network_analysis.csv',
                        'content_type': 'text/csv',
                        'content': differential_network_df.to_csv(header=True, index=None, sep=',')
                    }
                )

            if differential_network_img is not None:
                results.append(
                    {
                        'filename': 'network_analysis.png',
                        'content_type': 'image/png',
                        'content': base64.b64encode(differential_network_img).decode('utf8')
                    },
                )

        if geneSelected:
            if significant_genes is None:
                return {
                           "success": False,
                           "msg": "Missing files for gene set enrichment analysis."
                       }, 500
            pathway_with_pvalues_img, pathway_with_pvalues_csv = bulk_gsea.run_gsea_analysis(significant_genes)

            if pathway_with_pvalues_csv is not None:
                results.append(
                    {
                        'filename': 'GSEA_pathway_with_pvalues.csv',
                        'content_type': 'text/csv',
                        'content': pathway_with_pvalues_csv.to_csv(header=True, index=None, sep=',')
                    }
                )

            if pathway_with_pvalues_img is not None:
                results.append(
                    {
                        'filename': 'GSEA_pathway_with_pvalues.png',
                        'content_type': 'image/png',
                        'content': base64.b64encode(pathway_with_pvalues_img).decode('utf8')
                    }
                )

        return {
                   "success": True,
                   'upload_own_file': upload_own_file,
                   'quality_control': qualityControlSelected,
                   'normalization': normalizationSelected,
                   'visualization_after_normalization': visualizationAfterNormSelected,
                   'differential_analysis': differentialSelected,
                   'network_analysis': networkSelected,
                   'gene_set_enrichment_analysis': geneSelected,
                   'visualization': visualizationSelected,
                   'number_of_files': number_of_files,
                   'results': results
               }, 200


@rest_api.route('/api/analyze/single-cell')
class AnalyzeSingleCell(Resource):
    def post(self):
        upload_own_file = request.form.get('upload_own_file') == 'true'
        number_of_files = 0

        read_counts_df = None
        normalized_read_counts_df = None
        reduced_dimension_read_counts_df = None
        significant_gene_df = None
        clustered_result = None

        if upload_own_file:
            number_of_files = int(request.form.get('number_of_files'))
            for idx in range(number_of_files):
                file = request.files.get('file-' + str(idx))
                file_stream = file.stream
                file_type = file.content_type
                if file_type not in SINGLE_ALLOWED_FILE_TYPES:
                    return {
                               "success": False,
                               "msg": "Only .csv files are allowed."
                           }, 500

                file_stream.seek(0)
                if file.filename == 'read_counts.csv':
                    read_counts_df = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    print("=== read_counts_df ===\n", read_counts_df.head())
                elif file.filename == 'normalized_read_counts.csv':
                    normalized_read_counts_df = pd.DataFrame(
                        pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    print("=== normalized_read_counts_df ===\n", normalized_read_counts_df.head())
                else:
                    pass  # TO-DO
        else:
            file_directory = os.path.dirname('./demo_data/single_cell_data/')
            normalized_read_counts_df = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'normalized_read_counts.csv'), 'r'), index_col=0,
                            header=0))
            print("=== DEMO normalized_read_counts_df ===\n", normalized_read_counts_df.head())

        normalizationSelected = request.form.get('normalization') == 'true'
        clusteringSelected = request.form.get('clustering') == 'true'
        visualizationSelected = request.form.get('visualization') == 'true'
        differentialSelected = request.form.get('differential_analysis') == 'true'
        networkSelected = request.form.get('network_analysis') == 'true'
        pathwaySelected = request.form.get('pathway_analysis') == 'true'

        index = None
        header = None
        if read_counts_df is not None:
            header = read_counts_df.columns.values.tolist()
            index = read_counts_df.index

        results = []
        if normalizationSelected:
            if not upload_own_file:  # FOR CASE STUDY
                pass
            else:
                if read_counts_df is None:
                    return {
                               "success": False,
                               "msg": "Missing files for normalization."
                           }, 500
                normalized_read_counts_df = sc_norm.normalize_data(read_counts_df)
                normalized_read_counts_df.set_index(keys=index)
                normalized_read_counts_df.columns = header
                results.append(
                    {
                        'filename': 'normalized_read_counts.csv',
                        'content_type': 'text/csv',
                        'content': normalized_read_counts_df.to_csv(header=True, index=True, sep=',')
                    }
                )

        if clusteringSelected:
            if normalized_read_counts_df is None:
                return {
                           "success": False,
                           "msg": "Missing files for clustering."
                       }, 500

            reduced_dimension_read_counts_df = sc_dimension.reduce_dimension(normalized_read_counts_df)
            clustered_result = sc_clus.perform_clustering(reduced_dimension_read_counts_df)

        if visualizationSelected:
            if reduced_dimension_read_counts_df is None or clustered_result is None:
                return {
                           "success": False,
                           "msg": "Missing files for clustering visualization."
                       }, 500

            clustered_img = sc_visual.plot_clusters(reduced_dimension_read_counts_df, clustered_result)
            results.append(
                {
                    'filename': 'clustering_visualization.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(clustered_img).decode('utf8')
                },
            )

        if differentialSelected:
            if normalized_read_counts_df is None or clustered_result is None:
                return {
                           "success": False,
                           "msg": "Missing files for differential analysis."
                       }, 500
            significant_gene_df, significant_gene_and_expression = sc_diff.differential_expression(normalized_read_counts_df,
                                                                                           clustered_result)
            results.append(
                {
                    'filename': 'differential_analysis_significant_gene.csv',
                    'content_type': 'text/csv',
                    'content': significant_gene_df.to_csv(header=False, index=False, sep=',')
                }
            )

            differential_analysis_heatmap = sc_diff.plot_differential_analysis_heatmap(significant_gene_and_expression)
            results.append(
                {
                    'filename': 'differential_analysis_heatmap.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(differential_analysis_heatmap).decode('utf8')
                },
            )

        if pathwaySelected:
            if significant_gene_df is None:
                return {
                           "success": False,
                           "msg": "Missing files for pathway analysis."
                       }, 500

            pathway_with_pvalues_img, pathway_with_pvalues_csv = sc_gsea.run_gsea_analysis(significant_gene_df)

            if pathway_with_pvalues_csv is not None:
                results.append(
                    {
                        'filename': 'pathway_with_pvalues.csv',
                        'content_type': 'text/csv',
                        'content': pathway_with_pvalues_csv.to_csv(header=True, index=None, sep=',')
                    }
                )

            if pathway_with_pvalues_img is not None:
                results.append(
                    {
                        'filename': 'pathway_analysis_visualization.png',
                        'content_type': 'image/png',
                        'content': base64.b64encode(pathway_with_pvalues_img).decode('utf8')
                    }
                )

        response = {
            "success": True,
            'upload_own_file': upload_own_file,
            'normalization': normalizationSelected,
            'clustering': clusteringSelected,
            'visualization': visualizationSelected,
            'differential_analysis': differentialSelected,
            'network_analysis': networkSelected,
            'pathway_analysis': pathwaySelected,
            'number_of_files': number_of_files,
            'results': results
        }

        print("=== response size ===\n", sys.getsizeof(response))
        return response


@rest_api.route('/api/analyze/protein')
class AnalyzeProtein(Resource):
    def post(self):
        upload_own_file = request.form.get('upload_own_file') == 'true'
        number_of_files = 0

        read_counts_df = None
        normalized_read_counts_df = None
        significant_gene_df = None
        case_label_file = None
        control_label_file = None

        if upload_own_file:
            number_of_files = int(request.form.get('number_of_files'))
            for idx in range(number_of_files):
                file = request.files.get('file-' + str(idx))
                file_stream = file.stream
                file_type = file.content_type
                if file_type not in SINGLE_ALLOWED_FILE_TYPES:
                    return {
                               "success": False,
                               "msg": "Only .csv files are allowed."
                           }, 500

                file_stream.seek(0)
                if file.filename == 'read_counts.csv':
                    read_counts_df = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    print("=== read_counts_df ===\n", read_counts_df.head())
                elif file.filename == 'normalized_read_counts.csv':
                    normalized_read_counts_df = pd.DataFrame(
                        pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    print("=== normalized_read_counts_df ===\n", normalized_read_counts_df.head())
                else:
                    pass  # TO-DO
        else:
            file_directory = os.path.dirname('./demo_data/protein_data/')
            read_counts_df = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'read_counts.csv'), 'r'), index_col=0, header=0))
            case_label_file = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'case_label.txt'), 'r'), header=None))
            control_label_file = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'control_label.txt'), 'r'), header=None))
            print("=== DEMO read_counts_df ===\n", read_counts_df.head())

        case_label_list = None
        control_label_list = None
        if case_label_file is not None:
            case_label_list = [x[0].strip() for x in case_label_file.values.tolist()]
            print("=== case_label_list ===\n", len(case_label_list), case_label_list[:10])
        if control_label_file is not None:
            control_label_list = [x[0].strip() for x in control_label_file.values.tolist()]
            print("=== control_label_list ===\n", len(control_label_list), control_label_list[:10])

        qualityControlSelected = request.form.get('quality_control') == 'true'
        imputationSelected = request.form.get('imputation') == 'true'
        normalizationSelected = request.form.get('normalization') == 'true'
        visualizationSelected = request.form.get('visualization') == 'true'
        differentialSelected = request.form.get('differential_analysis') == 'true'
        networkSelected = request.form.get('network_analysis') == 'true'
        pathwaySelected = request.form.get('pathway_analysis') == 'true'

        results = []

        quality_controlled_df = None
        if qualityControlSelected:
            if read_counts_df is None:
                return {
                           "success": False,
                           "msg": "Missing files for quality control."
                       }, 500
            quality_controlled_df = protein_qc.filter_low_counts(read_counts_df)
            results.append(
                {
                    'filename': 'quality_control_results.csv',
                    'content_type': 'text/csv',
                    'content': quality_controlled_df.to_csv(header=True, index=True, sep=',')
                }
            )

        imputed_df = None
        if imputationSelected:
            if quality_controlled_df is None:
                return {
                           "success": False,
                           "msg": "Missing files for imputation."
                       }, 500
            imputed_df = protein_imp.impute_missing_values(quality_controlled_df)
            results.append(
                {
                    'filename': 'imputation_results.csv',
                    'content_type': 'text/csv',
                    'content': imputed_df.to_csv(header=True, index=True, sep=',')
                }
            )

        normalized_cases = None
        normalized_controls = None

        if normalizationSelected:
            if quality_controlled_df is None or case_label_file is None or control_label_file is None:
                return {
                           "success": False,
                           "msg": "Missing files for normalization."
                       }, 500

            normalized_cases, normalized_controls = protein_norm.normalize_protein_data(quality_controlled_df, case_label_list,
                                                                           control_label_list)
            results.extend([
                {
                    'filename': 'normalized_cases.csv',
                    'content_type': 'text/csv',
                    'content': normalized_cases.to_csv(header=True, index=True, sep=',')
                },
                {
                    'filename': 'normalized_controls.csv',
                    'content_type': 'text/csv',
                    'content': normalized_controls.to_csv(header=True, index=True, sep=',')
                }
            ])

        if visualizationSelected:
            if normalized_cases is None or normalized_controls is None:
                return {
                           "success": False,
                           "msg": "Missing files for normalization visualization."
                       }, 500
            normalized_data_visualization_img = protein_visual.visualize(normalized_cases, normalized_controls)
            results.append(
                {
                    'filename': 'normalization_visualization.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(normalized_data_visualization_img).decode('utf8')
                },
            )

        significant_genes = None
        significant_cases = None
        significant_controls = None

        if differentialSelected:
            if quality_controlled_df is None or normalized_cases is None or normalized_controls is None:
                return {
                           "success": False,
                           "msg": "Missing files for differential analysis."
                       }, 500

            gene_name_list = [str(x).strip() for x in quality_controlled_df.index]
            significant_genes, significant_cases, significant_controls = protein_diff.run_differential_analysis(
                gene_name_list,
                normalized_cases,
                normalized_controls)
            results.extend([
                {
                    'filename': 'differential_analysis_significant_genes.txt',
                    'content_type': 'text/plain',
                    'content': significant_genes.to_csv(header=None, index=None, sep=' ')
                },
                {
                    'filename': 'differential_analysis_significant_cases.csv',
                    'content_type': 'text/csv',
                    'content': significant_cases.to_csv(header=True, index=True, sep=',')
                },
                {
                    'filename': 'differential_analysis_significant_controls.csv',
                    'content_type': 'text/csv',
                    'content': significant_controls.to_csv(header=True, index=True, sep=',')
                }
            ])

        if pathwaySelected:
            if significant_genes is None:
                return {
                           "success": False,
                           "msg": "Missing files for gene set enrichment analysis."
                       }, 500
            pathway_with_pvalues_img, pathway_with_pvalues_csv = protein_gsea.run_gsea_analysis(significant_genes)

            if pathway_with_pvalues_csv is not None:
                results.append(
                    {
                        'filename': 'GSEA_pathway_with_pvalues.csv',
                        'content_type': 'text/csv',
                        'content': pathway_with_pvalues_csv.to_csv(header=True, index=None, sep=',')
                    }
                )

            if pathway_with_pvalues_img is not None:
                results.append(
                    {
                        'filename': 'GSEA_pathway_with_pvalues.png',
                        'content_type': 'image/png',
                        'content': base64.b64encode(pathway_with_pvalues_img).decode('utf8')
                    }
                )

        '''
        if networkSelected:
            if significant_genes is None or significant_cases is None or significant_controls is None:
                return {
                           "success": False,
                           "msg": "Missing files or pre-requisite step for network analysis."
                       }, 500

            differential_network_img, differential_network_df = run_network_analysis(significant_cases,
                                                                                     significant_controls,
                                                                                     significant_genes)

            if differential_network_df is not None:
                results.append(
                    {
                        'filename': 'network_analysis.csv',
                        'content_type': 'text/csv',
                        'content': differential_network_df.to_csv(header=True, index=None, sep=',')
                    }
                )

            if differential_network_img is not None:
                results.append(
                    {
                        'filename': 'network_analysis.png',
                        'content_type': 'image/png',
                        'content': base64.b64encode(differential_network_img).decode('utf8')
                    },
                )
        '''

        response = {
            "success": True,
            'upload_own_file': upload_own_file,
            'quality_control': qualityControlSelected,
            'imputation': imputationSelected,
            'normalization': normalizationSelected,
            'visualization': visualizationSelected,
            'differential_analysis': differentialSelected,
            'network_analysis': networkSelected,
            'pathway_analysis': pathwaySelected,
            'number_of_files': number_of_files,
            'results': results
        }

        print("=== response size ===\n", sys.getsizeof(response))
        return response
