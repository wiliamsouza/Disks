import dbus

from PyQt4 import QtCore


bus = dbus.SystemBus()
proxy = bus.get_object('org.freedesktop.UDisks', '/org/freedesktop/UDisks')
interface = dbus.Interface(proxy, 'org.freedesktop.UDisks')


class Partition(QtCore.QObject):

    def __init__(self, properties, parent=None):
        QtCore.QObject.__init__(self, parent)
        self._properties = properties

    def __str__(self):
        return str(self._properties['DeviceFile'])

    def _getName(self):
        return str(self._properties['DeviceFile'])

    changed = QtCore.pyqtSignal()

    name = QtCore.pyqtProperty(unicode, _getName, notify=changed)


class Drive(QtCore.QObject):

    def __init__(self, properties, parent=None):
        QtCore.QObject.__init__(self, parent)
        self._properties = properties
        self._partition = []

    def __str__(self):
        return str(self._properties['DeviceFile'])

    def addPartition(self, partition):
         self._partition.append(partition)

    def _getName(self):
         return str(self._properties['DeviceFile'])

    changed = QtCore.pyqtSignal()

    name = QtCore.pyqtProperty(unicode, _getName, notify=changed)


class DriveModel(QtCore.QAbstractListModel):

    COLUMNS = ('drive',)

    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self._drivers = []
        self.setRoleNames(dict(enumerate(DriveModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._drivers)

    def data(self, index, role):
        if index.isValid() and role == DriveModel.COLUMNS.index('drive'):
            return self._drivers[index.row()]
        return None

    def populate(self):
        drivers = {}
        partitions = {}

        for device in interface.EnumerateDevices():
            deviceProxy = bus.get_object('org.freedesktop.UDisks', device)
            deviceInterface = dbus.Interface(deviceProxy, 'org.freedesktop.DBus.Properties')
            deviceProperties = deviceInterface.GetAll('org.freedesktop.UDisks.Device')

            if deviceProperties['DeviceIsDrive'] == 1:
                drivers[str(device)] = Drive(deviceProperties)
                continue

            if deviceProperties['DeviceIsPartition'] == 1:
                try:
                    # Check if partition key alrealy exist
                    partitions[str(deviceProperties['PartitionSlave'])]
                except KeyError:
                    # if not create a empty list to the given key partition
                    partitions[str(deviceProperties['PartitionSlave'])] = []
                partitions[str(deviceProperties['PartitionSlave'])].append(Partition(deviceProperties))
                continue

        for (driver_name, driver_klass) in drivers.items():
            try:
                for partition in partitions[driver_name]:
                    driver_klass.addPartition(partition)
            except KeyError:
                # A keyError is raised if the given drive don't have partitions
                pass
            self._drivers.append(driver_klass)
