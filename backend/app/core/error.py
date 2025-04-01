from app import constants



def print_error_in_code(error, error_in_code):
    response = {'error': str(error)}
    if constants.SHOW_ERROR_IN_CODE:
        response['code_error'] = str(error_in_code)
    
    return response
        