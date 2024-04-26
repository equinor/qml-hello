import QtQuick
import QtQuick.Controls

ApplicationWindow {
    title: "The best QML application?"
    minimumWidth: 300
    minimumHeight: 200

    Text {
        objectName: "text"
        anchors.centerIn: parent

        font.pointSize: 24
        font.bold: true

        text: "Hello, world!"
    }
}
