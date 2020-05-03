from falcon import HTTPInternalServerError, HTTPUnprocessableEntity, HTTPPreconditionFailed, HTTPBadRequest, HTTPConflict, HTTPNotFound, HTTPUnauthorized, HTTPForbidden

class Base:
    def send_HTTP_error(self, error_code=500, message='Something went wrong in server while processing request'):
        if error_code == 400:
            raise HTTPBadRequest(description=message)
        elif error_code == 401:
            raise HTTPUnauthorized(description=message)
        elif error_code == 403:
            raise HTTPForbidden(description=message)
        elif error_code == 404:
            raise HTTPNotFound()
        elif error_code == 409:
            raise HTTPConflict(description=message)
        elif error_code == 412:
            raise HTTPPreconditionFailed(description=message)
        elif error_code == 422:
            raise HTTPUnprocessableEntity(description=message)
        else:
            raise HTTPInternalServerError(description=message)