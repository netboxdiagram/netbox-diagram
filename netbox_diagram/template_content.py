from netbox.plugins import PluginTemplateExtension


class DiagramButtonsExtension(PluginTemplateExtension):
    models = ['netbox_diagram.diagram']

    def buttons(self):
        return self.render('netbox_diagram/sync_button.html')


template_extensions = [DiagramButtonsExtension]
