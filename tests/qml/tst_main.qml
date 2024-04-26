import QtQuick
import QtTest
import Hello

TestCase {
    name: "Tests main window"
    when: windowShown

    Component {
        id: component
        Main {}
    }

    function test_main() {
        let item = createTemporaryObject(component, this)

        let text = findChild(item, "text")
        compare(text.text, "Hello, world!")
    }
}
