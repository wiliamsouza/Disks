import QtQuick 1.0

Rectangle {

    SystemPalette {
        id: palette
        colorGroup: SystemPalette.Active
    }

    id: window
    width: 640
    height: 480
    color: palette.window

    Rectangle {
        id: popup
        z: 10
        y: -window.height
        width: window.width
        height: window.height
        color: palette.dark
        anchors.horizontalCenter: parent.horizontalCenter

        Text {
            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.top: parent.top
            anchors.topMargin: 12
            text: "X"
            font.bold: true
            font.pointSize: 16

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    popup.state = ""
                }
            }
        }

        states : State {
            name: "show"
            PropertyChanges { target: popup; y: 0}
        }

        transitions: Transition {
            PropertyAnimation { properties: "y"; duration: 500 }
        }
    }

    /**
    ListModel {
        id: deviceModel

        ListElement {
            device: "sda"
            type: "images/drive-harddisk.png"
        }

        ListElement {
            device: "sr0"
            type: "images/drive-optical.png"
        }

        ListElement {
            device: "sdb"
            type: "images/drive-removable-media-usb-pendrive.png"
        }

        ListElement {
            device: "sdc"
            type: "images/drive-removable-media-usb.png"
        }

        ListElement {
            device: "sdd"
            type: "images/drive-removable-media.png"
        }

        ListElement {
            device: "sde"
            type: "images/drive-removable-media-usb.png"
        }
    }

    Component {
        id: deviceDelegate

        Column {
            id: wrapper

            Image {
                anchors.horizontalCenter: deviceName.horizontalCenter
                width: 64
                height: 64
                source: type

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        popup.state = "show"
                    }
                }
            }

            Text {
                id: deviceName
                text: device
                font.pointSize: 16
            }
        }
    }
    **/

    Component {
        id: driveDelegate

            Text {
                //id: deviceName
                text: model.drive.name
                font.pointSize: 16
            }

    }

    ListView {
        anchors.fill: parent
        model: driveModel
        delegate: driveDelegate
    }

    /**
    PathView {
        anchors.fill: parent
        model: deviceModel
        delegate: deviceDelegate
        path: Path {
            startX: 64
            startY: 64
            PathLine { x: 704; y: 64 }
        }
    }
    **/
}
