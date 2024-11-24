from simple_plugin_manager.utils import import_all_modules_in_namespace


def discover_plugins(namespace):
    import simple_plugin_manager.synchronization_provider
    import_all_modules_in_namespace(namespace)