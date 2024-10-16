# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import sys
import base64
import os
from collections import defaultdict

from flask import request
from flask_restx import Api, Resource, cors
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

from cross_workflow import visualize as cross_visual

rest_api = Api(version="1.0", title="GenoCraft API")

BULK_ALLOWED_FILE_TYPES = ['text/plain', 'text/csv']
SINGLE_ALLOWED_FILE_TYPES = ['text/plain', 'text/csv']
PROTEIN_ALLOWED_FILE_TYPES = ['text/plain', 'text/csv']
CROSS_ALLOWED_FILE_TYPES = ['text/plain', 'text/csv']

@rest_api.route('/api/time')
class Time(Resource):
    @cors.crossdomain(origin='*')
    def get(self):
        import time
        return {'time': time.strftime("%I:%M:%S %p", time.localtime())}


@rest_api.route('/api/google-analytics-report')
class GoogleAnalyticsReport(Resource):
    @cors.crossdomain(origin='*')
    def get(self):
        report = {}
        try:
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
        except Exception as e:
            print(f"==== Google Analytics Exception ==== {e}")

        return {
                   "success": True,
                   "page_view": report.get("page_view", None),
                   "bulk_api_triggered": report.get("Click-Bulk-Start", None),
                   "single_api_triggered": report.get("Click-Single-Cell-Start", None),
               }, 200


@rest_api.route('/api/analyze/cross')
class AnalyzeCross(Resource):
    @cors.crossdomain(origin='*')
    def post(self):
        upload_own_file = request.form.get('upload_own_file') == 'true'
        genes_df_list = []

        number_of_files = int(request.form.get('number_of_files'))

        if upload_own_file:
            for idx in range(number_of_files):
                file = request.files.get('file-' + str(idx))
                file_stream = file.stream
                file_type = file.content_type
                if file_type not in CROSS_ALLOWED_FILE_TYPES:
                    return {
                                "success": False,
                                "msg": "Only .csv or .txt files are allowed."
                            }, 500

                file_stream.seek(0)
                
                genes_df_list.append(
                    pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', header=None))
                    # significant_genes_df[0].tolist()
                )
        else:
            file_directory = os.path.dirname('./demo_data/cross_data/')

            genes_df_list.extend([
                pd.DataFrame(pd.read_csv(open(os.path.join(file_directory, 'bulk_differential_analysis_significant_genes.txt'), 'r'), header=None)),
                pd.DataFrame(pd.read_csv(open(os.path.join(file_directory, 'protein_differential_analysis_significant_genes.txt'), 'r'), header=None))
            ])

        results = []
        if len(genes_df_list) < 2:
            return {
                        "success": False,
                        "msg": "Missing files for cross visualization: differential_analysis_significant_genes.txt"
                    }, 500

        cross_gene_venn_img = cross_visual.plot_venn(genes_df_list[0][0].tolist(), genes_df_list[1][0].tolist())

        results.append(
            {
                'filename': 'cross_genes_venn.png',
                'content_type': 'image/png',
                'content': base64.b64encode(cross_gene_venn_img).decode('utf8')
            }
        )

        return {
            "success": True,
            'upload_own_file': upload_own_file,
            'number_of_files': number_of_files,
            'results': results
        }, 200


@rest_api.route('/api/analyze/bulk')
class AnalyzeBulk(Resource):
    @cors.crossdomain(origin='*')
    def post(self):
        upload_own_file = request.form.get('upload_own_file') == 'true'
        number_of_files = 0

        read_counts_df = None
        control_label_file = None
        case_label_file = None
        quality_controlled_df = None
        normalized_cases = None
        normalized_controls = None
        significant_genes = None
        significant_cases = None
        significant_controls = None

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
                if file.filename == 'read_counts.csv' or file.filename == 'read_counts.txt':
                    read_counts_df = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    #print("=== read_counts_df ===\n", read_counts_df.shape, read_counts_df.head())
                elif file.filename == 'case_label.txt':
                    case_label_file = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', header=None))
                    #print("=== case_label_file ===\n", case_label_file.head())
                elif file.filename == 'control_label.txt':
                    control_label_file = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', header=None))
                    #print("=== control_label_file ===\n", control_label_file.head())
                elif file.filename == 'quality_control_results.csv' or file.filename == 'quality_control_results.txt':
                    quality_controlled_df = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    #print("=== quality_controlled_df ===\n", quality_controlled_df.head())
                elif file.filename == 'normalized_cases.csv' or file.filename == 'normalized_cases.txt':
                    normalized_cases = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    #print("=== normalized_cases ===\n", normalized_cases.head())
                elif file.filename == 'normalized_controls.csv' or file.filename == 'normalized_controls.txt':
                    normalized_controls = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    #print("=== normalized_controls ===\n", normalized_controls.head())
                elif file.filename == 'differential_analysis_significant_genes.txt':
                    significant_genes_df = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', header=None))
                    significant_genes = significant_genes_df[0].tolist()
                    #print("=== significant_genes ===\n", significant_genes)
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
            quality_controlled_df = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'quality_control_results.csv'), 'r'), index_col=0, header=0))
            normalized_cases = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'normalized_cases.csv'), 'r'), index_col=0, header=0))
            normalized_controls = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'normalized_controls.csv'), 'r'), index_col=0, header=0))
            significant_genes_df = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'differential_analysis_significant_genes.txt'), 'r'), header=None))
            significant_genes = significant_genes_df[0].tolist()
            #print("=== DEMO read_counts_df ===\n", read_counts_df.head())

        case_label_list = None
        control_label_list = None
        if case_label_file is not None:
            case_label_list = [x[0].strip() for x in case_label_file.values.tolist()]
            #print("=== case_label_list ===\n", len(case_label_list), case_label_list[:10])
        if control_label_file is not None:
            control_label_list = [x[0].strip() for x in control_label_file.values.tolist()]
            #print("=== control_label_list ===\n", len(control_label_list), control_label_list[:10])

        qualityControlSelected = request.form.get('quality_control') == 'true'
        normalizationSelected = request.form.get('normalization') == 'true'
        visualizationAfterNormSelected = request.form.get('visualization_after_normalization') == 'true'
        differentialSelected = request.form.get('differential_analysis') == 'true'
        networkSelected = request.form.get('network_analysis') == 'true'
        geneSelected = request.form.get('gene_set_enrichment_analysis') == 'true'
        visualizationSelected = request.form.get('visualization') == 'true'

        results = []
        if qualityControlSelected:
            if read_counts_df is None:
                return {
                           "success": False,
                           "msg": "Missing files for quality control: read_counts.csv"
                       }, 500
            quality_controlled_df = bulk_qc.filter_low_counts(read_counts_df)
            results.append(
                {
                    'filename': 'quality_control_results.csv',
                    'content_type': 'text/csv',
                    'content': quality_controlled_df.to_csv(header=True, index=True, sep=',')
                }
            )

        if normalizationSelected:
            if not (quality_controlled_df is not None or read_counts_df is not None) or case_label_file is None or control_label_file is None:
                return {
                           "success": False,
                           "msg": "Missing files for normalization: case_label.txt, control_label.txt, quality_control_results.csv"
                       }, 500

            if quality_controlled_df is None:
                quality_controlled_df = read_counts_df

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
                           "msg": "Missing files for normalization visualization: normalized_cases.csv, normalized_controls.csv"
                       }, 500
            normalized_data_visualization_img = bulk_visual.visualize(normalized_cases, normalized_controls)
            results.append(
                {
                    'filename': 'normalization_visualization.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(normalized_data_visualization_img).decode('utf8')
                },
            )

        if differentialSelected:
            if normalized_cases is None or normalized_controls is None:
                return {
                           "success": False,
                           "msg": "Missing files for differential analysis: normalized_cases.csv, normalized_controls.csv"
                       }, 500

            gene_name_list = [str(x).strip() for x in normalized_cases.index]
            significant_genes, significant_cases, significant_controls = bulk_diff.run_differential_analysis(gene_name_list,
                                                                                                   normalized_cases,
                                                                                                   normalized_controls)

            significant_heatmap_img = bulk_diff.plot_heatmap(significant_cases, significant_controls)
            significant_circlize_img = bulk_diff.plot_circlize(significant_cases, significant_controls)

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
                },
                {
                    'filename': 'differential_analysis_heatmap.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(significant_heatmap_img).decode('utf8')
                },
                {
                    'filename': 'differential_analysis_circlize.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(significant_circlize_img).decode('utf8')
                }
            ])

            significant_genes = [genename[0] for genename in significant_genes.values.tolist()]

        if networkSelected:
            if significant_genes is None or significant_cases is None or significant_controls is None:
                return {
                           "success": False,
                           "msg": "Missing files or pre-requisite step for network analysis: differential_analysis_significant_genes.txt"
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
                           "msg": "Missing files for gene set enrichment analysis: differential_analysis_significant_genes.txt"
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
    @cors.crossdomain(origin='*')
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
                if file.filename == 'read_counts.csv' or file.filename == 'read_counts.txt':
                    read_counts_df = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    #print("=== read_counts_df ===\n", read_counts_df.head())
                elif file.filename == 'normalized_read_counts.csv' or file.filename == 'normalized_read_counts.txt':
                    normalized_read_counts_df = pd.DataFrame(
                        pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    #print("=== normalized_read_counts_df ===\n", normalized_read_counts_df.head())
                elif file.filename == 'differential_analysis_significant_gene.csv' or file.filename == 'differential_analysis_significant_gene.txt':
                    significant_gene_df = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', index_col=None, header=None))
                    significant_gene_df = [genename[0] for genename in significant_gene_df.values.tolist()]
                    #print("=== significant_gene_df ===\n", significant_gene_df[:10])
                else:
                    pass  # TO-DO
        else:
            file_directory = os.path.dirname('./demo_data/single_cell_data/')
            read_counts_df = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'read_counts.csv'), 'r'), index_col=0, header=0))
            normalized_read_counts_df = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'normalized_read_counts.csv'), 'r'), index_col=0, header=0))
            significant_gene_df = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'differential_analysis_significant_gene.csv'), 'r'), index_col=None, header=None))
            significant_gene_df = [genename[0] for genename in significant_gene_df.values.tolist()]
            #print("=== DEMO normalized_read_counts_df ===\n", normalized_read_counts_df.head())

        normalizationSelected = request.form.get('normalization') == 'true'
        clusteringSelected = request.form.get('clustering') == 'true'
        visualizationSelected = request.form.get('visualization') == 'true'
        differentialSelected = request.form.get('differential_analysis') == 'true'
        networkSelected = request.form.get('network_analysis') == 'true'
        pathwaySelected = request.form.get('pathway_analysis') == 'true'


        results = []
        if normalizationSelected:
            if not upload_own_file:  # FOR CASE STUDY
                #print("=== Normalization is skipped for demo data ===")
                csv_object = normalized_read_counts_df.to_csv(header=True, index=True, sep=',')
                if sys.getsizeof(csv_object) < 32_000_000:
                    results.append(
                        {
                            'filename': 'normalization_skipped_for_demo_data.csv',
                            'content_type': 'text/csv',
                            'content': csv_object
                        }
                    )
                else:
                    results.append(
                        {
                            'filename': 'normalized_file_too_large_omitted.csv',
                            'content_type': 'text/csv',
                            'content': normalized_read_counts_df.head().to_csv(header=True, index=True, sep=',')
                        }
                    )
            else:
                if read_counts_df is None:
                    return {
                               "success": False,
                               "msg": "Missing files for normalization: read_counts.csv"
                           }, 500
                normalized_read_counts_df = sc_norm.normalize_data(read_counts_df)
                csv_object = normalized_read_counts_df.to_csv(header=True, index=True, sep=',')
                if sys.getsizeof(csv_object) < 32_000_000:
                    results.append(
                        {
                            'filename': 'normalized_read_counts.csv',
                            'content_type': 'text/csv',
                            'content': csv_object
                        }
                    )
                else:
                    results.append(
                        {
                            'filename': 'normalized_file_too_large_omitted.csv',
                            'content_type': 'text/csv',
                            'content': normalized_read_counts_df.head().to_csv(header=True, index=True, sep=',')
                        }
                    )

        if clusteringSelected:
            if not (read_counts_df is not None or normalized_read_counts_df is not None):
                return {
                           "success": False,
                           "msg": "Missing files for clustering: normalized_read_counts.csv"
                       }, 500
            if normalized_read_counts_df is None:
                normalized_read_counts_df = read_counts_df

            reduced_dimension_read_counts_df = sc_dimension.reduce_dimension(normalized_read_counts_df)
            clustered_result = sc_clus.perform_clustering(reduced_dimension_read_counts_df)

        if visualizationSelected:
            if reduced_dimension_read_counts_df is None or clustered_result is None:
                return {
                           "success": False,
                           "msg": "Need to run clustering first. Clustering requires normalized_read_counts.csv"
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
                           "msg": "Need to run clustering first. Clustering requires normalized_read_counts.csv"
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

            results.append(
                {
                    'filename': 'differential_analysis_significant_gene_and_expression.csv',
                    'content_type': 'text/csv',
                    'content': significant_gene_and_expression.to_csv(header=True, index=True, sep=',')
                },
            )

            differential_analysis_heatmap = sc_diff.plot_differential_analysis_heatmap(significant_gene_and_expression)
            results.append(
                {
                    'filename': 'differential_analysis_heatmap.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(differential_analysis_heatmap).decode('utf8')
                },
            )

            significant_gene_df = [genename[0] for genename in significant_gene_df.values.tolist()]

        if pathwaySelected:
            if significant_gene_df is None:
                return {
                           "success": False,
                           "msg": "Missing files for pathway analysis: differential_analysis_significant_gene.csv"
                       }, 500

            #print("=== num of significant genes === ", len(significant_gene_df))
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

        # #print("=== response size ===\n", sys.getsizeof(response))
        return response


@rest_api.route('/api/analyze/protein')
class AnalyzeProtein(Resource):
    @cors.crossdomain(origin='*')
    def post(self):
        upload_own_file = request.form.get('upload_own_file') == 'true'
        number_of_files = 0

        read_counts_df = None
        quality_controlled_df = None
        imputed_df = None
        normalized_cases = None
        normalized_controls = None
        significant_genes = None
        case_label_file = None
        control_label_file = None

        if upload_own_file:
            number_of_files = int(request.form.get('number_of_files'))
            for idx in range(number_of_files):
                file = request.files.get('file-' + str(idx))
                file_stream = file.stream
                file_type = file.content_type
                if file_type not in PROTEIN_ALLOWED_FILE_TYPES:
                    return {
                               "success": False,
                               "msg": "Only .csv files are allowed."
                           }, 500

                file_stream.seek(0)
                if file.filename == 'read_counts.csv' or file.filename == 'read_counts.txt':
                    read_counts_df = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    #print("=== read_counts_df ===\n", read_counts_df.head())
                elif file.filename == 'case_label.txt':
                    case_label_file = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', header=None))
                    #print("=== case_label_file ===\n", case_label_file.head())
                elif file.filename == 'control_label.txt':
                    control_label_file = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', header=None))
                    #print("=== control_label_file ===\n", control_label_file.head())
                elif file.filename == 'quality_control_results.csv' or file.filename == 'quality_control_results.txt':
                    quality_controlled_df = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    #print("=== quality_controlled_df ===\n", quality_controlled_df.head())
                elif file.filename == 'imputation_results.csv' or file.filename == 'imputation_results.txt':
                    imputed_df = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    #print("=== imputed_df ===\n", imputed_df.head())
                elif file.filename == 'normalized_cases.csv' or file.filename == 'normalized_cases.txt':
                    normalized_cases = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    #print("=== normalized_cases ===\n", normalized_cases.head())
                elif file.filename == 'normalized_controls.csv' or file.filename == 'normalized_controls.txt':
                    normalized_controls = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    #print("=== normalized_controls ===\n", normalized_controls.head())
                elif file.filename == 'differential_analysis_significant_genes.txt':
                    significant_genes_df = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', header=None))
                    significant_genes = significant_genes_df[0].tolist()
                    #print("=== significant_genes ===\n", significant_genes)
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
            quality_controlled_df = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'quality_control_results.csv'), 'r'), index_col=0, header=0))
            imputed_df = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'imputation_results.csv'), 'r'), index_col=0, header=0))
            normalized_cases = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'normalized_cases.csv'), 'r'), index_col=0, header=0))
            normalized_controls = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'normalized_controls.csv'), 'r'), index_col=0, header=0))
            significant_genes_df = pd.DataFrame(
                pd.read_csv(open(os.path.join(file_directory, 'differential_analysis_significant_genes.txt'), 'r'), header=None))
            significant_genes = significant_genes_df[0].tolist()
            #print("=== DEMO read_counts_df ===\n", read_counts_df.head())

        case_label_list = None
        control_label_list = None
        if case_label_file is not None:
            case_label_list = [x[0].strip() for x in case_label_file.values.tolist()]
            #print("=== case_label_list ===\n", len(case_label_list), case_label_list[:10])
        if control_label_file is not None:
            control_label_list = [x[0].strip() for x in control_label_file.values.tolist()]
            #print("=== control_label_list ===\n", len(control_label_list), control_label_list[:10])

        qualityControlSelected = request.form.get('quality_control') == 'true'
        imputationSelected = request.form.get('imputation') == 'true'
        normalizationSelected = request.form.get('normalization') == 'true'
        visualizationSelected = request.form.get('visualization') == 'true'
        differentialSelected = request.form.get('differential_analysis') == 'true'
        networkSelected = request.form.get('network_analysis') == 'true'
        pathwaySelected = request.form.get('pathway_analysis') == 'true'


        results = []

        if qualityControlSelected:
            if read_counts_df is None:
                return {
                           "success": False,
                           "msg": "Missing files for quality control: read_counts.csv"
                       }, 500
            quality_controlled_df = protein_qc.filter_low_counts(read_counts_df)
            results.append(
                {
                    'filename': 'quality_control_results.csv',
                    'content_type': 'text/csv',
                    'content': quality_controlled_df.to_csv(header=True, index=True, sep=',')
                }
            )

        if imputationSelected:
            if not (read_counts_df is not None or quality_controlled_df is not None):
                return {
                           "success": False,
                           "msg": "Missing files for imputation: quality_control_results.csv"
                       }, 500
            if quality_controlled_df is None:
                quality_controlled_df = read_counts_df

            imputed_df = protein_imp.impute_missing_values(quality_controlled_df)
            results.append(
                {
                    'filename': 'imputation_results.csv',
                    'content_type': 'text/csv',
                    'content': imputed_df.to_csv(header=True, index=True, sep=',')
                }
            )

        if normalizationSelected:
            if not(read_counts_df is not None or imputed_df is not None or quality_controlled_df is not None) or case_label_file is None or control_label_file is None:
                return {
                           "success": False,
                           "msg": "Missing files for normalization: imputation_results.csv, case_label.txt, control_label.txt"
                       }, 500

            if imputed_df is None:
                if quality_controlled_df:
                    imputed_df = quality_controlled_df
                elif read_counts_df:
                    imputed_df = read_counts_df

            normalized_cases, normalized_controls = protein_norm.normalize_protein_data(imputed_df, case_label_list, control_label_list)
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
                           "msg": "Missing files for normalization visualization: normalized_cases.csv, normalized_controls.csv"
                       }, 500
            normalized_data_visualization_img = protein_visual.visualize(normalized_cases, normalized_controls)
            results.append(
                {
                    'filename': 'normalization_visualization.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(normalized_data_visualization_img).decode('utf8')
                },
            )

        if differentialSelected:
            if normalized_cases is None or normalized_controls is None:
                return {
                           "success": False,
                           "msg": "Missing files for differential analysis: normalized_cases.csv, normalized_controls.csv"
                       }, 500

            gene_name_list = [str(x).strip() for x in normalized_cases.index]
            #print("=== gene_name_list ===", gene_name_list)
            significant_genes, significant_cases, significant_controls, df_p_values = protein_diff.run_differential_analysis(
                gene_name_list,
                normalized_cases,
                normalized_controls)
            
            significant_heatmap_img = protein_diff.plot_heatmap(significant_cases, significant_controls)
            significant_circlize_img = protein_diff.plot_circlize(significant_cases, significant_controls)
            
            ### v2 ### 
            # Define case_df_cpm and control_df_cpm
            case_df_cpm = normalized_cases
            control_df_cpm = normalized_controls

            # Define case_samples and control_samples
            case_samples = case_label_list
            control_samples = control_label_list



            protein_volcano_img = protein_diff.plot_volcano(df_p_values)
            protein_pca_img = protein_diff.plot_pca(pd.concat([case_df_cpm, control_df_cpm], axis=0), labels=case_samples + control_samples)
            protein_umap_img = protein_diff.plot_umap(pd.concat([case_df_cpm, control_df_cpm], axis=0), labels=case_samples + control_samples)
            # protein_diff.plot_heatmap(significant_cases)
            protein_venn_img = protein_diff.plot_venn(significant_genes, gene_name_list, labels=("Significant Genes", "All Genes"))
            protein_boxplot_img = protein_diff.plot_boxplot(significant_cases, significant_controls)
            protein_qqplot_img = protein_diff.plot_qqplot(df_p_values['p-value'])
            protein_meanvariance_img = protein_diff.plot_mean_variance(significant_cases, significant_controls)

            results.extend([
                {
                    'filename': 'differential_analysis_significant_genes.txt',
                    'content_type': 'text/plain',
                    'content': '\n'.join(significant_genes)
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
                },
                {
                    'filename': 'differential_analysis_heatmap.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(significant_heatmap_img).decode('utf8')
                },
                {
                    'filename': 'differential_analysis_circlize.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(significant_circlize_img).decode('utf8')
                },
                {
                    'filename': 'differential_analysis_volcano.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(protein_volcano_img).decode('utf8')
                },
                {
                    'filename': 'differential_analysis_pca.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(protein_pca_img).decode('utf8')
                },
                {
                    'filename': 'differential_analysis_umap.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(protein_umap_img).decode('utf8')
                },
                {
                    'filename': 'differential_analysis_venn.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(protein_venn_img).decode('utf8')
                },
                {
                    'filename': 'differential_analysis_boxplot.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(protein_boxplot_img).decode('utf8')
                },  
                {
                    'filename': 'differential_analysis_qqplot.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(protein_qqplot_img).decode('utf8')
                },
                {
                    'filename': 'differential_analysis_meanvariance.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(protein_meanvariance_img).decode('utf8')
                },
            ])
            significant_genes = [genename[0] for genename in significant_genes]

        if pathwaySelected:
            if significant_genes is None:
                return {
                           "success": False,
                           "msg": "Missing files for Gene Set Enrichment Analysis: differential_analysis_significant_genes.txt"
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

        # #print("=== response size ===\n", sys.getsizeof(response))
        return response
