from utils.response import error_response

def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found(e):
        return error_response("Resource not found", status_code=404)

    @app.errorhandler(500)
    def server_error(e):
        return error_response("Something went wrong on our end", status_code=500)

    @app.errorhandler(Exception)
    def handle_exception(e):
        return error_response("An unexpected error occurred", status_code=500)