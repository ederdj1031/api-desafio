def transform_info(resp, columns):
    resp_json = []
    for row in resp:
        row_resp = dict(zip(columns, row))
        resp_json.append(row_resp)
        
    return resp_json