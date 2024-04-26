from qtpy.QtCore import QObject
from qtpy.QtQuick import QQuickItem


def test_text(qmlbot):
    item = qmlbot.load("Hello/main.qml")

    text = item.findChild(QQuickItem, "text")
    assert text.property("text") == "Hello, world!"
