#!/usr/bin/env python

import sys

from PyQt4 import QtGui, QtCore, QtDeclarative

#from disks.controllers import Controller
from disks.models import DriveModel



class DisksView(QtDeclarative.QDeclarativeView):

    def __init__(self, parent=None):
        QtDeclarative.QDeclarativeView.__init__(self, parent)

        self.driveModel = DriveModel(self)
        self.driveModel.populate()

        #self.controller = Controller(self)

        self.context = self.rootContext()

        self.context.setContextProperty('driveModel', self.driveModel)

        self.setSource(QtCore.QUrl('disks/views/Disks.qml'))
        self.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.setWindowTitle('Disks')


def start():

    app = QtGui.QApplication(sys.argv)

    #locale = QtCore.QLocale.system()
    #translator = QtCore.QTranslator()

    #i18n_file = 'SystemServices_' + locale.name() + '.qm'
    #i18n_path = '/usr/share/mandriva/mcc2/frontends/services/views/i18n/'

    #if (translator.load(i18n_file, i18n_path)):
    #    app.installTranslator(translator)

    view = DisksView()
    view.show()
    app.exec_()


if __name__ == '__main__':
    start()
