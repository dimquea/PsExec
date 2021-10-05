import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "psexec"

def setup(hass, config):
    def exec(call):
        import uuid

        from smbprotocol.connection import Connection
        from smbprotocol.session import Session

        from pypsexec.scmr import Service

        host = call.data.get('host')
        username = call.data.get('username')
        password = call.data.get('password')
        encrypt = call.data.get('encrypt', True)

        command = call.data.get('command')

        try:
            connection = Connection(uuid.uuid4(), host)
            connection.connect()
            session = Session(connection, username, password,
                              require_encryption=encrypt)
            session.connect()
            service = Service('HomeAssistant', session)
            service.open()

            try:
                service.create(command)
            except:
                _LOGGER.exception("Can't create service")

            try:
                service.start()
            except:
                # Random EXE-file can't be complete service,
                # so we have error even with success execute
                pass

            try:
                service.delete()
            except:
                _LOGGER.exception("Can't delete service")

            service.close()
            connection.disconnect()

        except:
            _LOGGER.exception(f"Can't connect to: {host}")

    hass.services.register(DOMAIN, 'exec', exec)

    return True
