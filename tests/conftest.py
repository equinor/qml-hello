from pathlib import Path
from typing import Union
from PySide6.QtCore import QObject, QUrl
from PySide6.QtQml import QQmlComponent, QQmlEngine
from PySide6.QtQuick import QQuickItem
import pytest

from qml_hello.main import init_qapp, QML_PATH


@pytest.fixture(scope="session")
def qapp_cls():
    return init_qapp


@pytest.fixture
def qml_engine(qapp):
    return QQmlEngine(qapp)


class QmlBot:
    def __init__(self, parent: QObject | None = None) -> None:
        self.engine = QQmlEngine(parent)

    def load(self, path: Union[Path, str]) -> QQuickItem:
        self.component = QQmlComponent(self.engine)
        self.component.loadUrl(QUrl.fromLocalFile(QML_PATH / path))
        assert (
            self.component.status() == QQmlComponent.Status.Ready
        ), self.component.errorString()

        self.item = self.component.createObject()
        return self.item


@pytest.fixture
def qmlbot(qapp) -> QmlBot:
    return QmlBot(qapp)
