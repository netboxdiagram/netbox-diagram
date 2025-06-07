from importlib.metadata import metadata

from netbox.plugins import PluginConfig

metadata = metadata('netbox_diagram')


class NetboxDiagram(PluginConfig):
    name = metadata.get('Name').replace('-', '_')
    verbose_name = metadata.get('Summary')
    description = metadata.get('Description')
    version = metadata.get('Version')
    author = metadata.get('Author')
    author_email = metadata.get('Author-email')
    base_url = 'diagram'
    min_version = '4.1.0'
    required_settings = []
    default_settings = {}
    queues = []

    def ready(self):
        super().ready()

        from netbox_diagram import signals  # noqa: F401


config = NetboxDiagram
