

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import view.Project


Rectangle {
    width: Constants.width
    height: Constants.height
    color: Constants.backgroundColor
    
    property string selectedItemsString: "" 


    function getCompressionLevels() {
        compressionSelection_ListModel.clear()

        var compressionOptions = startScreenController.getCompressionOptions();
        console.log("Compression Options:", JSON.stringify(compressionOptions)); 

        for (var i = 0; i < compressionOptions.length; i++) {
            compressionSelection_ListModel.append({
                "identifier": compressionOptions[i].identifier,
                "text": compressionOptions[i].text,
                "selected": compressionOptions[i].selected
            })
        }
    }
    function getSelectedItems() {
        var result = "";

        for (var i = 0; i < compressionSelection_ListModel.count; i++) {
            var item = compressionSelection_ListModel.get(i);
            if (item.selected) {
                result += item.text + ", ";  // Concatenate the text of selected items
            }
        }
        result = result.replace(/,\s*$/, "") // Removes the trailing comma and any spaces

        return result;  
    }
    function handleDebugMode(debug) {
        if (debug) {
            console.log("Debug mode is ON");
            debug_checkBox.checked = true;
            fileLoad_textField.text = "/Users/julian/Documents/5 - Dev/51 Programming Languages/511 Python/511.1 Unfinished Projects/AudioQualityTester/test/temp/audio/07 Huck And Jim.mp3"
        } else {
            console.log("Debug mode is OFF");
            debug_checkBox.checked = false;
        }
    }

    Component.onCompleted: {
        handleDebugMode(startScreenController.getDebugState())
        selectedItemsString = getSelectedItems();
        getCompressionLevels()
    }
    Connections {
        target: startScreenController

        // Use the new function-based syntax for handling the signal
        function onFilePathSelected(filePath) {
            fileLoad_textField.text = filePath  // Update the text field with the selected file path
        }
        function onCorrectSettings(result) {
            if (result === true) {
                mainWindow.loadListeningScreen()
            }
        }
        function onErrorMsg(message) {
            errorText_Text.text = message
        }
    }


    Text {
        id: explanation_Text
        width: Constants.startScreen.explanationTextSize[0]
        height: Constants.startScreen.explanationTextSize[1]
        anchors.top: parent.top
        anchors.topMargin: Constants.explanationTextTopMargin
        anchors.horizontalCenter: parent.horizontalCenter

        text: Constants.startScreen.explanationText
        font.pixelSize: Constants.fontsize.body
        wrapMode: Text.WordWrap
    }

    Column {
        id: content_column
        anchors.top: parent.top
        anchors.topMargin: Constants.contentColTopMargin
        anchors.bottom: parent.bottom
        anchors.bottomMargin: Constants.contentColBottomMargin
        anchors.left: parent.left
        anchors.leftMargin: Constants.contentColSideMargin
        anchors.right: parent.right
        anchors.rightMargin: Constants.contentColSideMargin

        spacing: Constants.contentColSpacing

        Text {
            id: settingsHeading_text
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter

            text: qsTr("Settings")
            font.pixelSize: Constants.fontsize.header
            font.bold: true
        }

        Row {
            id: audioFileInput_row
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: Constants.contentRowSpacing

                Label {
                    id: fileLoad_label
                    horizontalAlignment: Text.AlignRight
                    verticalAlignment: Text.AlignVCenter  // Vertically center-align the text
                    anchors.verticalCenter: parent.verticalCenter 
                    text: qsTr("Select Audio File:")
                }

                TextField {
                    id: fileLoad_textField
                    width: Constants.startScreen.fileLoadTextFieldWidth
                    placeholderText: qsTr("path/to/audio.mp3")
                    text: ""
                    anchors.verticalCenter: parent.verticalCenter 
                }

                Button {
                    id: fileLoad_Button
                    text: qsTr("Search File")
                    height: Constants.smallButtonDim[1]
                    anchors.verticalCenter: parent.verticalCenter 

                    onClicked:  {
                        startScreenController.fileLoadButtonPressed()
                        getCompressionLevels()
                    }
                }
        }


        CheckBox {
            id: audioOnce_checkBox
            anchors.horizontalCenter: parent.horizontalCenter

            text: qsTr("Play audio only once")
            checkState: Qt.Unchecked
            tristate: false
        }

        CheckBox {
            id: debug_checkBox
            anchors.horizontalCenter: parent.horizontalCenter

            text: qsTr("Debug")
            tristate: false
            checked: true
        }

        ListModel {
            id: compressionSelection_ListModel
        }

        Item {
            id: compressionSelection
            width: Constants.startScreen.fileLoadTextFieldWidth
            height: Constants.startScreen.compressionScrollViewHeight

            anchors.horizontalCenter: parent.horizontalCenter
            

            Column {
                anchors.fill: parent
                anchors.rightMargin: 0
                spacing: Constants.startScreen.compressionSpacing

                Text {
                    width: compressionSelection.width
                    wrapMode: Text.WordWrap
                    
                    text: "Select Compression Levels:"
                }

                // Wrapping ListView with a ScrollBar
                ScrollView {
                    width: parent ? parent.width : 0 
                    height: Constants.startScreen.compressionScrollViewHeight
                    clip: true

                    ListView {
                        id: listView
                        width: parent ? parent.width : 0 
                        height: Constants.startScreen.compressionListViewHeight
                        model: compressionSelection_ListModel

                        // Each item in the ListView has a CheckBox and Text
                        delegate: Rectangle {
                            width: parent ? parent.width : 0 
                            height: Constants.startScreen.compressionViewElemHeight
                            color: selected ? Constants.startScreen.compressionSelected : Constants.startScreen.compressionUnselected

                            Row {
                                anchors.fill: parent

                                CheckBox {
                                    checked: model.selected // Display the 'selected' state
                                    anchors.verticalCenter: parent.verticalCenter

                                    // When checked/unchecked, update the 'selected' state in the model
                                    onCheckedChanged:  {
                                        compressionSelection_ListModel.set(index, {"selected": checked})
                                        selectedItemsString = getSelectedItems()
                                    }
                                }

                                Text {
                                    text: model.text // Display the text from the model
                                    anchors.verticalCenter: parent.verticalCenter // Align text vertically
                                }
                            }
                        }
                    }

                    // ScrollBar attached to the ListView
                    ScrollBar.vertical: ScrollBar {
                        policy: ScrollBar.AlwaysOn
                        anchors.right: parent.right // Place scroll bar on the right side
                        height: parent.height // Extend scrollbar height to match the parent
                    }
                }

                Text {
                    id: selectedItemsText
                    width: compressionSelection.width
                    wrapMode: Text.WordWrap

                    text: "Selected Compression Levels: " + selectedItemsString
                }
            }
        }

        Rectangle {
            width: 1  // Minimal width to avoid visual artifacts
            height: Constants.startScreen.spacingAfterScrollView  // Custom margin between the Button and the ListView
            color: "transparent"  // Invisible spacer
        }


        Button {
            id: start_button
            width: Constants.buttonDim[0]
            height: Constants.buttonDim[1]
            anchors.horizontalCenter: parent.horizontalCenter

            text: qsTr("Start")
            font.pixelSize: Constants.fontsize.button


            onClicked: {
                // Show the busy indicator immediately
                startButtonPressed_BusyIndicator.visible = true
                errorText_Text.text = ""

                delayedTaskTimer.start()
            }
        }

        Timer {
            id: delayedTaskTimer
            interval: 100  // 100 ms delay to allow the UI to update
            repeat: false

            onTriggered: {
                let data = {
                    "fileLoad": fileLoad_textField.text,
                    "audioOnce": audioOnce_checkBox.checked,
                    "debug": debug_checkBox.checked,
                }

                let compressionData = []
                for (let i = 0; i < compressionSelection_ListModel.count; i++) {
                    let item = compressionSelection_ListModel.get(i)
                    compressionData.push({
                        "id": item.identifier,
                        "name": item.text,
                        "selected": item.selected
                    })
                }

                // Call the function after the UI has updated
                startScreenController.startButtonPressed(data, compressionData)

                // Hide the busy indicator after the task is complete
                startButtonPressed_BusyIndicator.visible = false
            }
        }


        BusyIndicator {
            id: startButtonPressed_BusyIndicator
            anchors.horizontalCenter: parent.horizontalCenter
            y: 900
            visible: false
            running: visible
        }

        Text {
            id: errorText_Text
            x: Constants.errorTextCoord[0]
            y: Constants.errorTextCoord[1]
            width: Constants.errorTextWidth
            anchors.horizontalCenter: parent.horizontalCenter

            text: ""
            color: Constants.errorTextColor
            font.pixelSize: Constants.fontsize.body
            wrapMode: Text.Wrap
        }
    }
}

