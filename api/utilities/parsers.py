from flask_restplus import reqparse, inputs

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_arguments.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                                  default=10, help='Results per page')
pagination_arguments.add_argument('category_id', type=int, required=False, default=None,
                                  help="Used to filter jobs by category. All other arguments will be ignored except for pagination arguments")
pagination_arguments.add_argument('user_email', type=str, required=False, default=None,
                                  help='Used to select the jobs for a certain user')
pagination_arguments.add_argument('freelancer_flag', type=inputs.boolean, required=False, default=False,
                                  help='Used to differentiate which jobs to select for user (jobs that are posted or jobs that are being worked on)')
