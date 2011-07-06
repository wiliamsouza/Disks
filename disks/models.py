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
	return self._properties['DeviceFile']

    def _getName(self):
            return self._properties['DeviceFile']

    changed = QtCore.pyqtSignal()

    name = QtCore.pyqtProperty(unicode, _getName, notify=changed)


class Drive(QtCore.QObject):

    def __init__(self, properties, parent=None):
	QtCore.QObject.__init__(self, parent)
	self._properties = properties
	self._partition = []

    def __str__(self):
        return self._properties['DeviceFile']

    def addPartition(self, partition):
	self._partition.append(partition)

    def _getName(self):
	return self._properties['DeviceFile']

    changed = QtCore.pyqtSignal()

    name = QtCore.pyqtProperty(unicode, _getName, notify=changed)


class DriveModel(QtCore.QAbstractListModel):

    COLUMNS = ('drive',)

    def __init__(self, parent=None):
	QtCore.QAbstractListModel.__init__(self, parent)
	self._drivers = []

    def populate(self):
	drivers = {}
	partitions = {}

	for device in interface.EnumerateDevices():
	    deviceProxy = bus.get_object('org.freedesktop.UDisks', device)
	    deviceInterface = dbus.Interface(deviceProxy, 'org.freedesktop.DBus.Properties')
	    deviceProperties = deviceInterface.GetAll('org.freedesktop.UDisks.Device')

	    if deviceProperties['DeviceIsDrive'] == 1:
		drivers[device] = Drive(deviceProperties)
		continue

	    if deviceProperties['DeviceIsPartition'] == 1:
		try:
		    partitions[deviceProperties['PartitionSlave']]
		except KeyError:
		    partitions[deviceProperties['PartitionSlave']] = []
		partitions[deviceProperties['PartitionSlave']].append(Partition(deviceProperties))
		continue

	for partitionDrive in partitions.keys():
	     for partition in partitions[partitionDrive]:
		drivers[partitionDrive].addPartition(partition)

	self._drivers = drivers.items()


#if __name__ == '__main__':
#    dm = DriveModel()
#    dm.populate()
