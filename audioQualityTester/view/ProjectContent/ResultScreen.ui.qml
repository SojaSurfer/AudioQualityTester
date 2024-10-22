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
                "color": formattedResult[i].correct ? Qt.rgba(0, 1, 0, 0.3): Qt.rgba(1, 0, 0, 0.3)
            });
        };
        resultScreenController.setup()
    }


    Column {
        id: content_column
        anchors.top: parent.top
        anchors.topMargin: Constants.resultScreen.contentColTopMargin // different col size for this window
        anchors.bottom: parent.bottom
        anchors.bottomMargin: Constants.contentColBottomMargin
        anchors.left: parent.left
        anchors.leftMargin: Constants.contentColSideMargin
        anchors.right: parent.right
        anchors.rightMargin: Constants.contentColSideMargin

        spacing: Constants.contentColSpacing


        Row {
            id: headerRow
            width: Constants.resultScreen.rowWidth
            height: Constants.resultScreen.headerRowHeight

            Text {
                id: header1_text
                width: Constants.resultScreen.textBoxWidth
                height: Constants.resultScreen.headerRowHeight
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter

                text: qsTr("Result")
                font.pixelSize: Constants.fontsize.subheader
                font.bold: true
                z: 1
            }
            Text {
                id: header2_text
                width: Constants.resultScreen.imageBoxWidth
                height: Constants.resultScreen.headerRowHeight
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter

                text: qsTr("Spectrogram")
                font.pixelSize: Constants.fontsize.subheader
                font.bold: true
                z: 1
            }
            Text {
                id: header3_text
                width: Constants.resultScreen.imageBoxWidth
                height: Constants.resultScreen.headerRowHeight
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter

                text: qsTr("MEL Spectrogram")
                font.pixelSize: Constants.fontsize.subheader
                font.bold: true
                z: 1
            }
        }

        Row {
            id: listView_row
            width: parent.width
            height: Constants.resultScreen.listViewHeight

            spacing: Constants.contentRowSpacing


            ListView {
                id: rowListView
                // width: Constants.resultScreen.rowWidth
                // height: parent.height - Constants.resultScreen.headerRowHeight
                width: parent.width
                height: parent.height


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
                        spacing: Constants.contentRowSpacing

                        Rectangle {
                            width: Constants.resultScreen.textBoxWidth
                            height: Constants.resultScreen.itemHeight
                            color: model.color
                            anchors.verticalCenter: parent.verticalCenter
                            // radius: 5  // Rounded corners if needed

                            z: 4

                            Text {
                                anchors.top: parent.top
                                anchors.topMargin: Constants.resultScreen.textInfoMargin
                                anchors.left: parent.left
                                anchors.leftMargin: Constants.resultScreen.textInfoMargin
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
                width: Constants.popupSize[0]
                height: Constants.popupSize[1]
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
        }

        Row {
            id: busyIndicatorRow
            height: Constants.listeningScreen.rowHeight
            width: 200

            anchors.horizontalCenter: parent.horizontalCenter  // Center the entire row
            spacing: Constants.contentRowSpacing  // Define spacing between the elements

            BusyIndicator {
                id: submitButtonPressed_BusyIndicator
                anchors.horizontalCenter: parent.horizontalCenter

                visible: false
                running: visible
            }
        }

        Row {
            id: buttonsRow
            width: Constants.resultScreen.buttonRowSize[0]
            height: Constants.resultScreen.buttonRowSize[1]

            anchors.horizontalCenter: parent.horizontalCenter
            spacing: Constants.resultScreen.narrowRowSpacing  


            Button {
                id: back_button
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
                width: Constants.buttonDim[0]
                height: Constants.buttonDim[1]

                text: qsTr("Save Data")
                font.pointSize: Constants.fontsize.button

                onClicked: resultScreenController.saveDataButtonPressed()
            }

            Button {
                id: restart_button
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
    }
}