import requests


def get_data(request):
    rsp = None

    try:
        if request.args:
            api_url = request.args.get('api_url')
            action = request.args.get('action')

            if action == 'get':
                rsp = requests.get(api_url, verify=False).text
            elif action == 'post':
                rsp = requests.post(api_url, verify=False).text
            elif action == 'delete':
                rsp = requests.delete(api_url, verify=False).text
        else:
            rsp = 'Args not provided!'
    except Exception as e:
        rsp = 'Error: [{}]'.format(str(e))

    return 'Response: [{}]'.format(rsp)
