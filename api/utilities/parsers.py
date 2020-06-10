from flask_restx import reqparse, inputs
from werkzeug.datastructures import FileStorage
import werkzeug

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_arguments.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                                  default=10, help='Results per page')
pagination_arguments.add_argument('category_id', type=int, required=False, default=None,
                                  help="Used to filter items by category. All other arguments will be ignored except for pagination arguments")
pagination_arguments.add_argument('user_email', type=str, required=False, default=None,
                                  help='Used to select the items for a certain user')
pagination_arguments.add_argument('freelancer_flag', type=inputs.boolean, required=False, default=False,
                                  help='Used to differentiate which items to select for user (items for employers or freelancers)')

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', type=FileStorage, location='files',  required=True)


attachment_input = reqparse.RequestParser()
attachment_input.add_argument('file_name', type=str, required=True)
attachment_input.add_argument('file_type', type=str, choices=['.txt', '.zip', '.rar', '.png', '.jpg', '.jpeg'], required=True)
attachment_input.add_argument('user_email', type=inputs.email(), required=True)
attachment_input.add_argument('job_id', type=int, required=True)

delivered_project_asset_input = reqparse.RequestParser()
delivered_project_asset_input.add_argument('file_name', type=str, required=True)
delivered_project_asset_input.add_argument('file_type', type=str, choices=['.txt', '.rar', '.tar', '.zip', '.png', '.jpg', '.jpeg'], required=True)
delivered_project_asset_input.add_argument('employer_email', type=inputs.email(), required=True)
delivered_project_asset_input.add_argument('project_id', type=int, required=True)
delivered_project_asset_input.add_argument('job_id', type=int, required=True)
delivered_project_asset_input.add_argument('message', type=str, required=True)


asset_input = reqparse.RequestParser()
asset_input.add_argument('file_name', type=str, required=True)
asset_input.add_argument('file_type', type=str, choices=['.zip', '.rar', '.tar', '.png', '.jpg', '.jpeg'], required=True)
asset_input.add_argument('asset_type', type=str, choices=['image', 'archive'], required=True)
asset_input.add_argument('project_for_sale_id', type=int, required=True)