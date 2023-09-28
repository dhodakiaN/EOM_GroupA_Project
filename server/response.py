from controllers import check_account, create_account, get_files, download_file, upload_file


def handle_requests(event, connection, data=None):
    if event == 'login': return check_account(connection, data)
    elif event == 'signup': return create_account(connection, data)
    elif event == 'get-files' : return get_files(connection)
    elif event == 'upload-file': return upload_file(connection, data)
    elif event == 'download-file': return download_file(connection, data)
    else: connection.send('invalid-request'.encode('utf-8'))
