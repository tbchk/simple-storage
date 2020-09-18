

class StorageClient(object):
    def __init__(self, **args):

        # Services preconfigured
        self.gcs_service = None
        self.local_service = LocalStorage()

    def get_service(self, path: str):
        assert '/' in path, 'Malformed path'

        protocol = path.split('/')[0]

        if protocol == 'gs:':
            if not self.gcs_service:
                self.gcs_service = GCloudStorage()

            return self.gcs_service
        elif protocol == '':
            return self.local_service
        else:
            return None

    def ls(self, path: str) -> List[str]:
        service = self.get_service(path)

        if not service:
            raise Exception('Unknown service in path: %s' % path)

        listing = service.ls(path)
        return listing
