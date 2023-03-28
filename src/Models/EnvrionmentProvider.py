class EnvironmentProvider:
    # PORT: str = os.environ['PORT']
    # URL: str = os.environ['URL']

    @staticmethod
    def VideoStreamerParameters():
        return {
            # 'port': EnvironmentProvider.PORT,
            # 'url': EnvironmentProvider.URL,
            "port": 123,
            "address": "asdf",
        }
