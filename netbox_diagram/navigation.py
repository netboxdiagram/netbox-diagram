from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

items = (
    PluginMenuItem(
        link="plugins:netbox_diagram:diagram_list",
        link_text="Diagrams",
        permissions=["netbox_diagram.view_diagrams"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_diagram:diagram_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),
)
menu = PluginMenu(label="Diagrams", groups=(("Diagrams", items),), icon_class="mdi mdi-pencil")
