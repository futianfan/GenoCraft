# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

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

from bulk_rna_workflow.differential_analysis import run_differential_analysis
from bulk_rna_workflow.gene_set_enrichment_analysis import run_gsea_analysis
from bulk_rna_workflow.network_analysis import run_network_analysis
from bulk_rna_workflow.normalization import normalize_rnaseq_data
from genocraft_secrets import constants

rest_api = Api(version="1.0", title="GenoCraft API")

ALLOWED_FILE_TYPES = ['text/plain', 'text/csv']

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

        genename_file = None
        control_file = None
        case_file = None

        if upload_own_file:
            number_of_files = int(request.form.get('number_of_files'))
            for idx in range(number_of_files):
                file = request.files.get('file-' + str(idx))
                file_stream = file.stream
                file_type = file.content_type
                if file_type not in ALLOWED_FILE_TYPES:
                    return {
                               "success": False,
                               "msg": "Only .csv or .txt files are allowed."
                           }, 500

                file_stream.seek(0)
                if file.filename == 'case.txt':
                    case_file = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', header=None, sep='\t'))
                elif file.filename == 'control.txt':
                    control_file = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', header=None, sep='\t'))
                elif file.filename == 'genename.txt':
                    genename_file = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1', header=None, sep='\t'))
                else:
                    pass # TO-DO
        else:
            file_directory = os.path.dirname('./data/')
            genename_file = pd.DataFrame(pd.read_csv(open(os.path.join(file_directory, 'genename.txt'), 'r'), header=None, sep='\t'))
            case_file = pd.DataFrame(pd.read_csv(open(os.path.join(file_directory, 'case.txt'), 'r'), header=None, sep='\t'))
            control_file = pd.DataFrame(pd.read_csv(open(os.path.join(file_directory, 'control.txt'), 'r'), header=None, sep='\t'))

        qualityControlSelected = request.form.get('quality_control') == 'true'
        normalizationSelected = request.form.get('normalization') == 'true'
        visualizationAfterNormSelected = request.form.get('visualization_after_normalization') == 'true'
        differentialSelected = request.form.get('differential_analysis') == 'true'
        networkSelected = request.form.get('network_analysis') == 'true'
        geneSelected = request.form.get('gene_set_enrichment_analysis') == 'true'
        visualizationSelected = request.form.get('visualization') == 'true'

        results = []
        if normalizationSelected:
            if case_file is None or control_file is None:
                return {
                       "success": False,
                       "msg": "Missing files for normalization."
                   }, 500
            case_file, control_file = normalize_rnaseq_data(case_file, control_file)
            results.extend([
                {
                    'filename': 'normalized_cases.txt',
                    'content_type': 'text/plain',
                    'content': case_file.to_csv(header=None, index=None, sep=' ')
                },
                {
                    'filename': 'normalized_controls.txt',
                    'content_type': 'text/plain',
                    'content': control_file.to_csv(header=None, index=None, sep=' ')
                }
            ])

        significant_genes = None
        significant_cases = None
        significant_controls = None

        if differentialSelected:
            if genename_file is None or case_file is None or control_file is None:
                return {
                           "success": False,
                           "msg": "Missing files for differential analysis."
                       }, 500
            significant_genes, significant_cases, significant_controls = run_differential_analysis(genename_file, case_file, control_file)
            results.extend([
                {
                    'filename': 'differential_analysis_significant_genes.txt',
                    'content_type': 'text/plain',
                    'content': significant_genes.to_csv(header=None, index=None, sep=' ')
                },
                {
                    'filename': 'differential_analysis_significant_cases.txt',
                    'content_type': 'text/plain',
                    'content': significant_cases.to_csv(header=None, index=None, sep=' ')
                },
                {
                    'filename': 'differential_analysis_significant_controls.txt',
                    'content_type': 'text/plain',
                    'content': significant_controls.to_csv(header=None, index=None, sep=' ')
                }
           ])

        if networkSelected:
            if significant_genes is None or significant_cases is None or significant_controls is None:
                return {
                           "success": False,
                           "msg": "Missing files or pre-requisite step for network analysis."
                       }, 500

            differential_network_img, differential_network_df = run_network_analysis(significant_cases, significant_controls, significant_genes)
            results.extend([
                {
                    'filename': 'differential_network.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(differential_network_img).decode('utf8')
                },
                {
                    'filename': 'differential_network.csv',
                    'content_type': 'text/csv',
                    'content': differential_network_df.to_csv(header=True, index=None, sep=',')
                }
            ])

        if geneSelected:
            if significant_genes is None:
                return {
                           "success": False,
                           "msg": "Missing files for gene set enrichment analysis."
                       }, 500
            pathway_with_pvalues_img, pathway_with_pvalues_csv = run_gsea_analysis(significant_genes)
            results.extend([
                {
                    'filename': 'GSEA_pathway_with_pvalues.png',
                    'content_type': 'image/png',
                    'content': base64.b64encode(pathway_with_pvalues_img).decode('utf8')
                },
                {
                    'filename': 'GSEA_pathway_with_pvalues.csv',
                    'content_type': 'text/csv',
                    'content': pathway_with_pvalues_csv.to_csv(header=True, index=None, sep=',')
                }
           ])

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
        return {
                   "success": False,
                   "msg": "Sorry! Single cell analysis is not yet supported."
               }, 500

        upload_own_file = request.form.get('upload_own_file') == 'true'

        if upload_own_file:
            file = request.files.get('file')
            file_stream = file.stream
            file_type = file.content_type
            if file_type != 'text/csv':
                return {
                        "success": False,
                        "msg": "Only CSV is allowed."
                       }, 500

            file_stream.seek(0)
            df = pd.DataFrame(pd.read_csv(file_stream, encoding='latin-1'))
        else:
            pass

        normalizationSelected = request.form.get('normalization') == 'true'
        qualitySelected = request.form.get('quality_control') == 'true'
        clusteringSelected = request.form.get('clustering') == 'true'
        visualizationSelected = request.form.get('visualization') == 'true'
        differentialSelected = request.form.get('differential_analysis') == 'true'
        networkSelected = request.form.get('network_analysis') == 'true'
        pathwaySelected = request.form.get('pathway_analysis') == 'true'

        return {
            'upload_own_file': upload_own_file,
            'normalization': normalizationSelected,
            'quality_control' : qualitySelected,
            'clustering': clusteringSelected,
            'visualization': visualizationSelected,
            'differential_analysis': differentialSelected,
            'network_analysis': networkSelected,
            'pathway_analysis': pathwaySelected,
        }
