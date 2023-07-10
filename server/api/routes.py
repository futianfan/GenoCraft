# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import sys, base64, os
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

from bulk_rna_workflow.quality_control import filter_low_counts
from bulk_rna_workflow.differential_analysis import run_differential_analysis
from bulk_rna_workflow.gene_set_enrichment_analysis import run_gsea_analysis as bulk_run_gsea_analysis
from bulk_rna_workflow.network_analysis import run_network_analysis
from bulk_rna_workflow.normalize import normalize_rnaseq_data
from bulk_rna_workflow.normalization_visualize import visualize
from genocraft_secrets import constants

from single_cell_rna_workflow.normalize import normalize_data
from single_cell_rna_workflow.reduce_dimension import reduce_dimension
from single_cell_rna_workflow.clustering import perform_clustering
from single_cell_rna_workflow.visualization import plot_clusters
from single_cell_rna_workflow.differential_expression import differential_expression, plot_differential_analysis_heatmap
from single_cell_rna_workflow.gene_set_enrichment_analysis import run_gsea_analysis as single_cell_run_gsea_analysis

rest_api = Api(version="1.0", title="GenoCraft API")

BULK_ALLOWED_FILE_TYPES = ['text/plain', 'text/csv']
SINGLE_ALLOWED_FILE_TYPES = ['text/csv']
PROTEIN_ALLOWED_FILE_TYPES = ['text/csv']

"""
    Flask-Restx models for api request and response data
"""

'''
signup_model = rest_api.model('SignUpModel', {"username": fields.String(required=True, min_length=2, max_length=32),
                                              "email": fields.String(required=True, min_length=4, max_length=64),
                                              "password": fields.String(required=True, min_length=4, max_length=16)
                                              })

login_model = rest_api.model('LoginModel', {"email": fields.String(required=True, min_length=4, max_length=64),
                                            "password": fields.String(required=True, min_length=4, max_length=16)
                                            })

user_edit_model = rest_api.model('UserEditModel', {"userID": fields.String(required=True, min_length=1, max_length=32),
                                                   "username": fields.String(required=True, min_length=2, max_length=32),
                                                   "email": fields.String(required=True, min_length=4, max_length=64)
                                                   })
'''

'''
"""
   Helper function for JWT token required
"""

def token_required(f):

    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if "authorization" in request.headers:
            token = request.headers["authorization"]

        if not token:
            return {"success": False, "msg": "Valid JWT token is missing"}, 400

        try:
            data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=["HS256"])
            current_user = Users.get_by_email(data["email"])

            if not current_user:
                return {"success": False,
                        "msg": "Sorry. Wrong auth token. This user does not exist."}, 400

            token_expired = db.session.query(JWTTokenBlocklist.id).filter_by(jwt_token=token).scalar()

            if token_expired is not None:
                return {"success": False, "msg": "Token revoked."}, 400

            if not current_user.check_jwt_auth_active():
                return {"success": False, "msg": "Token expired."}, 400

        except:
            return {"success": False, "msg": "Token is invalid"}, 400

        return f(current_user, *args, **kwargs)

    return decorator


"""
    Flask-Restx routes
"""


@rest_api.route('/api/users/register')
class Register(Resource):
    """
       Creates a new user by taking 'signup_model' input
    """

    @rest_api.expect(signup_model, validate=True)
    def post(self):

        req_data = request.get_json()

        _username = req_data.get("username")
        _email = req_data.get("email")
        _password = req_data.get("password")

        user_exists = Users.get_by_email(_email)
        if user_exists:
            return {"success": False,
                    "msg": "Email already taken"}, 400

        new_user = Users(username=_username, email=_email)

        new_user.set_password(_password)
        new_user.save()

        return {"success": True,
                "userID": new_user.id,
                "msg": "The user was successfully registered"}, 200


@rest_api.route('/api/users/login')
class Login(Resource):
    """
       Login user by taking 'login_model' input and return JWT token
    """

    @rest_api.expect(login_model, validate=True)
    def post(self):

        req_data = request.get_json()

        _email = req_data.get("email")
        _password = req_data.get("password")

        user_exists = Users.get_by_email(_email)

        if not user_exists:
            return {"success": False,
                    "msg": "This email does not exist."}, 400

        if not user_exists.check_password(_password):
            return {"success": False,
                    "msg": "Wrong credentials."}, 400

        # create access token uwing JWT
        token = jwt.encode({'email': _email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, BaseConfig.SECRET_KEY)

        user_exists.set_jwt_auth_active(True)
        user_exists.save()

        return {"success": True,
                "token": token,
                "user": user_exists.toJSON()}, 200


@rest_api.route('/api/users/edit')
class EditUser(Resource):
    """
       Edits User's username or password or both using 'user_edit_model' input
    """

    @rest_api.expect(user_edit_model)
    @token_required
    def post(self, current_user):

        req_data = request.get_json()

        _new_username = req_data.get("username")
        _new_email = req_data.get("email")

        if _new_username:
            self.update_username(_new_username)

        if _new_email:
            self.update_email(_new_email)

        self.save()

        return {"success": True}, 200


@rest_api.route('/api/users/logout')
class LogoutUser(Resource):
    """
       Logs out User using 'logout_model' input
    """

    @token_required
    def post(self, current_user):

        _jwt_token = request.headers["authorization"]

        jwt_block = JWTTokenBlocklist(jwt_token=_jwt_token, created_at=datetime.now(timezone.utc))
        jwt_block.save()

        self.set_jwt_auth_active(False)
        self.save()

        return {"success": True}, 200


@rest_api.route('/api/sessions/oauth/github/')
class GitHubLogin(Resource):
    def get(self):
        code = request.args.get('code')
        client_id = BaseConfig.GITHUB_CLIENT_ID
        client_secret = BaseConfig.GITHUB_CLIENT_SECRET
        root_url = 'https://github.com/login/oauth/access_token'

        params = { 'client_id': client_id, 'client_secret': client_secret, 'code': code }

        data = requests.post(root_url, params=params, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        })

        response = data._content.decode('utf-8')
        access_token = response.split('&')[0].split('=')[1]

        user_data = requests.get('https://api.github.com/user', headers={
            "Authorization": "Bearer " + access_token
        }).json()
        
        user_exists = Users.get_by_username(user_data['login'])
        if user_exists:
            user = user_exists
        else:
            try:
                user = Users(username=user_data['login'], email=user_data['email'])
                user.save()
            except:
                user = Users(username=user_data['login'])
                user.save()
        
        user_json = user.toJSON()

        token = jwt.encode({"username": user_json['username'], 'exp': datetime.utcnow() + timedelta(minutes=30)}, BaseConfig.SECRET_KEY)
        user.set_jwt_auth_active(True)
        user.save()

        return {"success": True,
                "user": {
                    "_id": user_json['_id'],
                    "email": user_json['email'],
                    "username": user_json['username'],
                    "token": token,
                }}, 200
'''


@rest_api.route('/api/time')
class Time(Resource):
    def get(self):
        import time
        return {'time': time.strftime("%I:%M:%S %p", time.localtime())}


@rest_api.route('/api/google-analytics-report')
class GoogleAnalyticsReport(Resource):
    def get(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"genocraft_secrets/{constants.GOOGLE_ANALYTICS_CREDENTIAL_FILE_NAME}"
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
                    pass # TO-DO
        else:
            file_directory = os.path.dirname('./demo_data/bulk_data/')
            read_counts_df = pd.DataFrame(pd.read_csv(open(os.path.join(file_directory, 'read_counts.csv'), 'r'), index_col=0, header=0))
            case_label_file = pd.DataFrame(pd.read_csv(open(os.path.join(file_directory, 'case_label.txt'), 'r'), header=None))
            control_label_file = pd.DataFrame(pd.read_csv(open(os.path.join(file_directory, 'control_label.txt'), 'r'), header=None))
            print("=== read_counts_df ===\n", read_counts_df.head())

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
            quality_controlled_df = filter_low_counts(read_counts_df)
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

            normalized_cases, normalized_controls = normalize_rnaseq_data(quality_controlled_df, case_label_list, control_label_list)
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
            normalized_data_visualization_img = visualize(normalized_cases, normalized_controls)
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
            significant_genes, significant_cases, significant_controls = run_differential_analysis(gene_name_list, normalized_cases, normalized_controls)
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

            differential_network_img, differential_network_df = run_network_analysis(significant_cases, significant_controls, significant_genes)

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
            pathway_with_pvalues_img, pathway_with_pvalues_csv = bulk_run_gsea_analysis(significant_genes)

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
                    normalized_read_counts_df = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', index_col=0, header=0))
                    print("=== normalized_read_counts_df ===\n", normalized_read_counts_df.head())
                else:
                    pass # TO-DO
        else:
            file_directory = os.path.dirname('./demo_data/single_cell_data/')
            normalized_read_counts_df = pd.DataFrame(pd.read_csv(open(os.path.join(file_directory, 'normalized_read_counts.csv'), 'r'), index_col=0, header=0))
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
                normalized_read_counts_df = normalize_data(read_counts_df)
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

            reduced_dimension_read_counts_df = reduce_dimension(normalized_read_counts_df)
            clustered_result = perform_clustering(reduced_dimension_read_counts_df)
            print(clustered_result)

        if visualizationSelected:
            if reduced_dimension_read_counts_df is None or clustered_result is None:
                return {
                           "success": False,
                           "msg": "Missing files for clustering visualization."
                       }, 500

            clustered_img = plot_clusters(reduced_dimension_read_counts_df, clustered_result)
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
            significant_gene_df, significant_gene_and_expression = differential_expression(normalized_read_counts_df, clustered_result)
            results.append(
                {
                    'filename': 'differential_analysis_significant_gene.csv',
                    'content_type': 'text/csv',
                    'content': significant_gene_df.to_csv(header=False, index=False, sep=',')
                }
            )

            differential_analysis_heatmap = plot_differential_analysis_heatmap(significant_gene_and_expression)
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

            pathway_with_pvalues_img, pathway_with_pvalues_csv = single_cell_run_gsea_analysis(significant_gene_df)

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
