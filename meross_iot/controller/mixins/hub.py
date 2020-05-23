import logging

from meross_iot.model.enums import Namespace

_LOGGER = logging.getLogger(__name__)


class HubMixn(object):
    __PUSH_MAP = {
        Namespace.HUB_ONLINE: 'online',
        Namespace.HUB_TOGGLEX: 'togglex',
    }

    def __init__(self, device_uuid: str,
                 manager,
                 **kwargs):
        super().__init__(device_uuid=device_uuid, manager=manager, **kwargs)

    def handle_push_notification(self, namespace: Namespace, data: dict) -> bool:
        locally_handled = False
        target_data_key = self.__PUSH_MAP.get(namespace)

        if target_data_key is not None:
            _LOGGER.debug(f"{self.__class__.__name__} handling push notification for namespace {namespace}")
            payload = data.get(target_data_key)
            if payload is None:
                _LOGGER.error(f"{self.__class__.__name__} could not find {target_data_key} attribute in push notification data: "
                              f"{data}")
                locally_handled = False
            else:
                notification_data = data.get(target_data_key, [])
                for subdev_state in notification_data:
                    subdev_id = subdev_state.get('id')

                    # Check the specific subdevice has been registered with this hub...
                    subdev = self.get_subdevice(subdevice_id=subdev_id)
                    if subdev is None:
                        _LOGGER.warning(
                            f"Received an update for a subdevice (id {subdev_id}) that has not yet been "
                            f"registered with this hub. The update will be skipped.")
                        return False
                    else:
                        subdev.handle_push_notification(namespace=namespace, data=data)
                locally_handled = True

        # Always call the parent handler when done with local specific logic. This gives the opportunity to all
        # ancestors to catch all events.
        parent_handled = super().handle_push_notification(namespace=namespace, data=data)
        return locally_handled or parent_handled


class HubMs100Mixin(object):
    _execute_command: callable
    _abilities_spec: dict
    get_subdevice: callable
    uuid: str

    def __init__(self, device_uuid: str,
                 manager,
                 **kwargs):
        super().__init__(device_uuid=device_uuid, manager=manager, **kwargs)

    def handle_push_notification(self, namespace: Namespace, data: dict) -> bool:
        raise NotImplementedError("TODO")
        pass


class HubMts100Mixin(object):
    __PUSH_MAP = {
        Namespace.HUB_MTS100_MODE: 'mode',
        Namespace.HUB_MTS100_TEMPERATURE: 'temperature'
    }
    _execute_command: callable
    _abilities_spec: dict
    get_subdevice: callable
    uuid: str

    def __init__(self, device_uuid: str,
                 manager,
                 **kwargs):
        super().__init__(device_uuid=device_uuid, manager=manager, **kwargs)

    def handle_push_notification(self, namespace: Namespace, data: dict) -> bool:
        locally_handled = False
        target_data_key = self.__PUSH_MAP.get(namespace)

        if target_data_key is not None:
            _LOGGER.debug(f"{self.__class__.__name__} handling push notification for namespace {namespace}")
            payload = data.get(target_data_key)
            if payload is None:
                _LOGGER.error(f"{self.__class__.__name__} could not find {target_data_key} attribute in push notification data: "
                              f"{data}")
                locally_handled = False
            else:
                notification_data = data.get(target_data_key, [])
                for subdev_state in notification_data:
                    subdev_id = subdev_state.get('id')

                    # Check the specific subdevice has been registered with this hub...
                    subdev = self.get_subdevice(subdevice_id=subdev_id)
                    if subdev is None:
                        _LOGGER.warning(
                            f"Received an update for a subdevice (id {subdev_id}) that has not yet been "
                            f"registered with this hub. The update will be skipped.")
                        return False
                    else:
                        subdev.handle_push_notification(namespace=namespace, data=data)
                locally_handled = True

        # Always call the parent handler when done with local specific logic. This gives the opportunity to all
        # ancestors to catch all events.
        parent_handled = super().handle_push_notification(namespace=namespace, data=data)
        return locally_handled or parent_handled