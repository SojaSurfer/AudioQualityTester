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
    id: root
    width: mainWindow.width
    height: mainWindow.height
    color: Constants.backgroundColor

    // property string resultText: "Example 01\nYour Selection:\nFormat:\nSample Rate:\nBitrate:\nListening Duration:\n"

    function showImagePopup(imageSource) {
        enlargedImage.source = imageSource;
        imagePopup.open();
    }

    Component.onCompleted: {
        var formattedResult = [];

        // Clear the existing model in case there is data
        resultModel.clear();

        formattedResult = listeningScreenController.getFormatResult();
        console.log("formattedResult", formattedResult)

        // Populate the ListModel with the formatted result
        for (var i = 0; i < formattedResult.length; i++) {
            resultModel.append({
                "resultText": formattedResult[i].resultText,
                "spectrogramSource": formattedResult[i].spectrogramSource,
                "melSource": formattedResult[i].melSource,
                "color": formattedResult[i].backgroundColor
            });
        };
        resultScreenController.setup()
    }



    Row {
        id: headerRow
        x: Constants.resultScreen.rowStartX
        y: 100
        width: Constants.resultScreen.rowWidth
        height: Constants.resultScreen.headerRowHeight

        Text {
            id: header1_text
            x: 0
            y: 0
            width: Constants.resultScreen.textBoxWidth
            height: Constants.resultScreen.headerRowHeight
            text: qsTr("Result")
            font.pixelSize: Constants.fontsize.colHeader
            font.bold: true
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            z: 1
        }
        Text {
            id: header2_text
            x: 150
            y: 0
            width: Constants.resultScreen.imageBoxWidth
            height: Constants.resultScreen.headerRowHeight
            text: qsTr("Spectrogram")
            font.pixelSize: Constants.fontsize.colHeader
            font.bold: true
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            z: 1
        }
        Text {
            id: header3_text
            x: 550
            y: 0
            width: Constants.resultScreen.imageBoxWidth
            height: Constants.resultScreen.headerRowHeight
            text: qsTr("MEL Spectrogram")
            font.pixelSize: Constants.fontsize.colHeader
            font.bold: true
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            z: 1
        }
    }

    ListView {
        id: rowListView
        anchors.top: headerRow.bottom
        anchors.topMargin: 10
        anchors.left: parent.left
        anchors.leftMargin: Constants.resultScreen.rowStartX
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 150
        width: Constants.resultScreen.rowWidth
        height: parent.height - Constants.resultScreen.headerRowHeight

        clip: true
        model: ListModel { id: resultModel }

        delegate: Rectangle {
            width: Constants.resultScreen.rowWidth
            height: Constants.resultScreen.rowHeight
            color: Constants.resultScreen.rowColor
            border.color: Constants.resultScreen.rowBorderColor
            border.width: Constants.resultScreen.rowBorderWidth

            Row {
                anchors.fill: parent
                spacing: 15 // Constants.resultScreen.rowInnerMargin  // Control the space between elements

                Rectangle {
                    width: Constants.resultScreen.textBoxWidth
                    height: Constants.resultScreen.itemHeight
                    color: model.color
                    anchors.verticalCenter: parent.verticalCenter
                    // radius: 5  // Rounded corners if needed

                    z: 4

                    Text {
                        // anchors.margins: 20
                        anchors.top: parent.top
                        anchors.topMargin: 10
                        anchors.left: parent.left
                        anchors.leftMargin: 10

                        text: model.resultText
                        font.pixelSize: Constants.fontsize.colHeader
                        wrapMode: Text.WordWrap
                        z: 5
                    }
                }

                Image {
                    width: Constants.resultScreen.imageBoxWidth
                    height: Constants.resultScreen.itemHeight
                    source: model.spectrogramSource
                    fillMode: Image.PreserveAspectFit

                    MouseArea {
                        anchors.fill: parent
                        onClicked: root.showImagePopup(model.spectrogramSource)
                    }
                }

                Image {
                    width: Constants.resultScreen.imageBoxWidth
                    height: Constants.resultScreen.itemHeight
                    source: model.melSource
                    fillMode: Image.PreserveAspectFit

                    MouseArea {
                        anchors.fill: parent
                        onClicked: root.showImagePopup(model.melSource)
                    }
                }
            }
        }

        ScrollBar.vertical: ScrollBar {
            policy: ScrollBar.AlwaysOn
        }
    }
    // Single Popup for enlarged image display
    Popup {
        id: imagePopup
        modal: true
        focus: true
        width: root.width * 0.7
        height: root.height * 0.7
        closePolicy: Popup.CloseOnEscape
        onClosed: imagePopup.visible = false
        anchors.centerIn: parent

        Rectangle {
            anchors.fill: parent
            anchors.centerIn: parent
            color: "black"

            // Close the popup when clicking on the background outside the image
            MouseArea {
                anchors.fill: parent
                onClicked: imagePopup.close()
            }

            Image {
                id: enlargedImage
                anchors.centerIn: parent
                visible: true
                fillMode: Image.PreserveAspectFit
            }
        }
    }


    Button {
        id: back_button
        x: 386
        y: Constants.resultScreen.buttonsStartY
        width: Constants.buttonDim[0]
        height: Constants.buttonDim[1]
        text: qsTr("Back")
        font.pointSize: Constants.fontsize.button

        onClicked: {
            resultScreenController.backButtonPressed()
            mainWindow.loadListeningScreen()
        }
    }

    Button {
        id: saveData_button
        x: 537
        y: Constants.resultScreen.buttonsStartY
        width: Constants.buttonDim[0]
        height: Constants.buttonDim[1]
        text: qsTr("Save Data")
        font.pointSize: Constants.fontsize.button

        onClicked: resultScreenController.saveDataButtonPressed()
    }

    Button {
        id: restart_button
        x: 684
        y: Constants.resultScreen.buttonsStartY
        width: Constants.buttonDim[0]
        height: Constants.buttonDim[1]
        text: qsTr("Restart")
        font.pointSize: Constants.fontsize.button

        onClicked: {
            resultScreenController.restartButtonPressed()
            mainWindow.loadStartScreen()
        }
    }

    Button {
        id: exit_button
        x: 830
        y: Constants.resultScreen.buttonsStartY
        width: Constants.buttonDim[0]
        height: Constants.buttonDim[1]
        text: qsTr("Exit")
        font.pointSize: Constants.fontsize.button

        onClicked: {
            resultScreenController.exitButtonPressed()
            Qt.quit()
        }
    }
}
