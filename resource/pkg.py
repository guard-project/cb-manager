import falcon
import os

class PkgResource(object):
    routes = '/pkg/{name}',
    tag = 'package'

    def on_get(self, req, resp, name):
        """
        Download the package.
        ---
        summary: Download the package
        description: Download the package
        tags: "package"
        responses:
            200:
                description: Download of the file completed.
                schema:
                    type: string
                    format: byte
            400:
                description: Bad request.
                schema: BadRequestSchema
            401:
                description: Unauthorized.
                schema: UnauthorizedSchema
            404:
                description: Not found.
                schema: NotFoundSchema
        """
        resp.downloadable_as = name
        pkg = f'pkg/{name}'
        if os.path.exists(pkg):
            try:
                resp.stream = open(pkg, 'rb')
            except:
                raise falcon.HTTPBadRequest(
                    title="Package error",
                    description="Not possible to download the package."
                )
        else:
            raise falcon.HTTPNotFound(
                title="Package error",
                description="Package not found."
            )
