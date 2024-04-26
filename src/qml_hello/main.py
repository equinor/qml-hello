from __future__ import annotations

import sys
import signal
from pathlib import Path
from types import FrameType, TracebackType
from typing import Any, Sequence
from qtpy import PYSIDE6
from qtpy.QtCore import QTimer, QUrl, QThread
from qtpy.QtWidgets import QApplication
from qtpy.QtQml import QQmlApplicationEngine, QQmlComponent, qmlRegisterType, QQmlEngine


QML_PATH = Path(__file__).parent / "qml"


def init_qapp(args: Sequence[str]) -> QApplication:
    if PYSIDE6:
        from PySide6.QtQml import QQmlDebuggingEnabler

        QQmlDebuggingEnabler.enableDebugging(True)

    qapp = QApplication(args)

    # Qt should yield program execution to Python every 500ms
    timer = QTimer(qapp)
    timer.timeout.connect(lambda: None)
    timer.start(500)

    next_handler = signal.getsignal(signal.SIGINT)
    next_excepthook = sys.excepthook

    def reset() -> None:
        signal.signal(signal.SIGINT, next_handler)
        sys.excepthook = next_excepthook

    def sighandler(signum: int, frame: FrameType | None) -> Any:
        qapp.exit(-signum)
        reset()
        if callable(next_handler):
            return next_handler(signum, frame)

    def excepthook(
        exctype: type[BaseException], exc: BaseException, exc_tb: TracebackType | None
    ) -> Any:
        print(exctype, exc, exc_tb)
        qapp.exit(2)
        reset()
        raise exc
        return next_excepthook(exctype, exc, exc_tb)

    sys.excepthook = excepthook
    signal.signal(signal.SIGINT, sighandler)

    return qapp


def load_component(engine: QQmlEngine, path: Path) -> QQmlComponent:
    component = QQmlComponent(engine)
    component.loadUrl(QUrl.fromLocalFile(str(path)))
    if component.status() != QQmlComponent.Status.Ready:
        sys.exit(f"Failure when loading {path}:\n{component.errorString()}")
    return component


def main() -> None:
    app = init_qapp(sys.argv)

    engine = QQmlEngine(app)
    engine.addImportPath(str(QML_PATH.resolve()))
    component = load_component(engine, QML_PATH / "Hello/main.qml")

    object = component.createObject()
    object.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
