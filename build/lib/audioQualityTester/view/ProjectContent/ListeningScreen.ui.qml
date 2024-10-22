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

    property int maxDuration: Constants.listeningScreen.maxAudioDurationDefault
    property int startTime: audioStart_slider.value
    property real currentProgress: 0.0


    QtObject {
        id: utils

        function handlePlayButtonClick(clickedButton) {
            
            listeningScreenController.play(clickedButton.objectName, audioStart_slider.value)
            utils.startProgressBar()

            utils.resetButtonFont()
            clickedButton.font.bold = true
        }

        function handleStopButtonClick() {
            
            listeningScreenController.stop()
            progressTimer.stop()
            
            utils.resetButtonFont()
        }

        function resetButtonFont() {
            // Reset button bold font for all buttons
            let buttonList = [roundButton1, roundButton2, roundButton3, roundButton4, roundButton5]
            for (let i = 0; i < buttonList.length; i++) {
                buttonList[i].font.bold = false
            }
        }

        function handleAudioFileDuration(duration) {
            maxDuration = duration
            audioStart_slider.to = duration
            console.log("Audio duration adjusted to:", duration)
        }

        function startProgressBar() {
            startTime = 0
            currentProgress = audioStart_slider.value
            audioProgress_progressBar.from = startTime
            audioProgress_progressBar.to = maxDuration
            progressTimer.start()
        }

        function handleSubmitButtonClick() {
            submitButtonPressed_BusyIndicator.visible = true

            let comboBoxList = [comboBox1, comboBox2, comboBox3, comboBox4, comboBox5]
            let comboBoxChoices = []
            
            for (let i = 0; i < comboBoxList.length; i++) {
                let item = comboBoxList[i]
                comboBoxChoices.push(item.currentText)
            }

            listeningScreenController.submitButtonPressed(comboBoxChoices)
            mainWindow.loadResultScreen()
        }
    }

    Connections {
        target: listeningScreenController
        function onAudioFileDuration(duration) { 
            utils.handleAudioFileDuration(duration)
        }
        function onErrorMsg(message) {
            errorText_Text.text = message
        }
    }

    Component.onCompleted: {
        listeningScreenController.setup()
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
            id: examples_header
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
            text: qsTr("Examples")
            font.pixelSize: Constants.fontsize.header
            font.bold: true
        }

        Row {
            id: slider_row
            width: Constants.listeningScreen.sliderRowSize[0]
            height: Constants.listeningScreen.sliderRowSize[1]

            anchors.horizontalCenter: parent.horizontalCenter  // Center the entire row
            spacing: Constants.contentRowSpacing  // Define spacing between the elements

            Label {
                id: label6
                width: Constants.listeningScreen.sliderLabelWidth
                anchors.verticalCenter: parent.verticalCenter 

                text: qsTr("Start Audio from second:")

            }

            TextField {
                id: textField
                width: Constants.listeningScreen.sliderTextFileSize[0]
                height: Constants.listeningScreen.sliderTextFileSize[1]
                horizontalAlignment: Text.AlignRight
                verticalAlignment: Text.AlignVCenter
                anchors.verticalCenter: parent.verticalCenter 

                placeholderText: qsTr("Text Field")
                text: audioStart_slider.value
                readOnly: true
            }

            Slider {
                id: audioStart_slider
                width: Constants.listeningScreen.sliderSize[0]
                height: Constants.listeningScreen.sliderSize[1]
                anchors.verticalCenter: parent.verticalCenter 

                value: 0
                stepSize: 1
                to: maxDuration
                wheelEnabled: false
            }

            Button {
                id: stop_button
                width: Constants.smallButtonDim[0]
                height: Constants.smallButtonDim[1]
                anchors.verticalCenter: parent.verticalCenter 

                text: qsTr("Stop")

                onClicked:  utils.handleStopButtonClick()
            }
        }


        Row {
            id: row1
            width: Constants.listeningScreen.rowSize[0]
            height: Constants.listeningScreen.rowSize[1]

            anchors.horizontalCenter: parent.horizontalCenter  // Center the entire row
            spacing: Constants.contentRowSpacing  // Define spacing between the elements

            Label {
                id: label1
                width: Constants.listeningScreen.rowLabelSize[0]
                height: Constants.listeningScreen.rowLabelSize[1]
                horizontalAlignment: Text.AlignRight 
                verticalAlignment: Text.AlignVCenter
                anchors.verticalCenter: parent.verticalCenter  // Align the label vertically

                text: qsTr("Example 01")
                font.pointSize: Constants.fontsize.emphasis
            }

            ComboBox {
                id: comboBox1
                width: Constants.listeningScreen.rowComboBoxSize[0]
                height: Constants.listeningScreen.rowComboBoxSize[1]
                anchors.verticalCenter: parent.verticalCenter  // Align the ComboBox vertically

                model: listeningScreenController.comboBoxElems
            }

            RoundButton {
                id: roundButton1
                width: Constants.listeningScreen.rowPlayButtonSize[0]
                height: Constants.listeningScreen.rowPlayButtonSize[1]
                anchors.verticalCenter: parent.verticalCenter  // Align the button vertically

                text: "Play"
                objectName: "roundButton_01"
                onClicked: utils.handlePlayButtonClick(this)
            }
        }

        Row {
            id: row2
            width: Constants.listeningScreen.rowSize[0]
            height: Constants.listeningScreen.rowSize[1]

            anchors.horizontalCenter: parent.horizontalCenter  // Center the entire row
            spacing: Constants.contentRowSpacing  // Define spacing between the elements

            Label {
                id: label2
                width: Constants.listeningScreen.rowLabelSize[0]
                height: Constants.listeningScreen.rowLabelSize[1]
                horizontalAlignment: Text.AlignRight 
                verticalAlignment: Text.AlignVCenter
                anchors.verticalCenter: parent.verticalCenter  // Align the label vertically

                text: qsTr("Example 02")
                font.pointSize: Constants.fontsize.emphasis
            }

            ComboBox {
                id: comboBox2
                width: Constants.listeningScreen.rowComboBoxSize[0]
                height: Constants.listeningScreen.rowComboBoxSize[1]
                anchors.verticalCenter: parent.verticalCenter  // Align the ComboBox vertically

                model: listeningScreenController.comboBoxElems
            }

            RoundButton {
                id: roundButton2
                width: Constants.listeningScreen.rowPlayButtonSize[0]
                height: Constants.listeningScreen.rowPlayButtonSize[1]
                anchors.verticalCenter: parent.verticalCenter  // Align the button vertically

                text: "Play"
                objectName: "roundButton_02"
                onClicked: utils.handlePlayButtonClick(this)
            }
        }

        Row {
            id: row3
            width: Constants.listeningScreen.rowSize[0]
            height: Constants.listeningScreen.rowSize[1]

            anchors.horizontalCenter: parent.horizontalCenter  // Center the entire row
            spacing: Constants.contentRowSpacing  // Define spacing between the elements

            Label {
                id: label3
                width: Constants.listeningScreen.rowLabelSize[0]
                height: Constants.listeningScreen.rowLabelSize[1]
                horizontalAlignment: Text.AlignRight 
                verticalAlignment: Text.AlignVCenter
                anchors.verticalCenter: parent.verticalCenter  // Align the label vertically

                text: qsTr("Example 03")
                font.pointSize: Constants.fontsize.emphasis
            }

            ComboBox {
                id: comboBox3
                width: Constants.listeningScreen.rowComboBoxSize[0]
                height: Constants.listeningScreen.rowComboBoxSize[1]
                anchors.verticalCenter: parent.verticalCenter  // Align the ComboBox vertically

                model: listeningScreenController.comboBoxElems
            }

            RoundButton {
                id: roundButton3
                width: Constants.listeningScreen.rowPlayButtonSize[0]
                height: Constants.listeningScreen.rowPlayButtonSize[1]
                anchors.verticalCenter: parent.verticalCenter  // Align the button vertically

                text: "Play"
                objectName: "roundButton_03"
                onClicked: utils.handlePlayButtonClick(this)
            }
        }

        Row {
            id: row4
            width: Constants.listeningScreen.rowSize[0]
            height: Constants.listeningScreen.rowSize[1]

            anchors.horizontalCenter: parent.horizontalCenter  // Center the entire row
            spacing: Constants.contentRowSpacing  // Define spacing between the elements

            Label {
                id: label4
                width: Constants.listeningScreen.rowLabelSize[0]
                height: Constants.listeningScreen.rowLabelSize[1]
                horizontalAlignment: Text.AlignRight 
                verticalAlignment: Text.AlignVCenter
                anchors.verticalCenter: parent.verticalCenter  // Align the label vertically

                text: qsTr("Example 04")
                font.pointSize: Constants.fontsize.emphasis
            }

            ComboBox {
                id: comboBox4
                width: Constants.listeningScreen.rowComboBoxSize[0]
                height: Constants.listeningScreen.rowComboBoxSize[1]
                anchors.verticalCenter: parent.verticalCenter  // Align the ComboBox vertically

                model: listeningScreenController.comboBoxElems
            }

            RoundButton {
                id: roundButton4
                width: Constants.listeningScreen.rowPlayButtonSize[0]
                height: Constants.listeningScreen.rowPlayButtonSize[1]
                anchors.verticalCenter: parent.verticalCenter  // Align the button vertically

                text: "Play"
                objectName: "roundButton_04"
                onClicked: utils.handlePlayButtonClick(this)
            }
        }

        Row {
            id: row5
            width: Constants.listeningScreen.rowSize[0]
            height: Constants.listeningScreen.rowSize[1]

            anchors.horizontalCenter: parent.horizontalCenter  // Center the entire row
            spacing: Constants.contentRowSpacing  // Define spacing between the elements

            Label {
                id: label5
                width: Constants.listeningScreen.rowLabelSize[0]
                height: Constants.listeningScreen.rowLabelSize[1]
                horizontalAlignment: Text.AlignRight 
                verticalAlignment: Text.AlignVCenter
                anchors.verticalCenter: parent.verticalCenter  // Align the label vertically

                text: qsTr("Example 05")
                font.pointSize: Constants.fontsize.emphasis
            }

            ComboBox {
                id: comboBox5
                width: Constants.listeningScreen.rowComboBoxSize[0]
                height: Constants.listeningScreen.rowComboBoxSize[1]
                anchors.verticalCenter: parent.verticalCenter  // Align the ComboBox vertically

                model: listeningScreenController.comboBoxElems
            }

            RoundButton {
                id: roundButton5
                width: Constants.listeningScreen.rowPlayButtonSize[0]
                height: Constants.listeningScreen.rowPlayButtonSize[1]
                anchors.verticalCenter: parent.verticalCenter  // Align the button vertically

                text: "Play"
                objectName: "roundButton_05"
                onClicked: utils.handlePlayButtonClick(this)
            }
        }


        Row {
            id: progressRow
            width: Constants.listeningScreen.rowSize[0]
            height: Constants.listeningScreen.rowSize[1]

            anchors.horizontalCenter: parent.horizontalCenter  // Center the entire row
            spacing: Constants.contentRowSpacing  // Define spacing between the elements

            Text {
                id: progressText_text
                anchors.verticalCenter: parent.verticalCenter 

                text: listeningScreenController.progressText
                font.pixelSize: Constants.fontsize.emphasis
            }

            ProgressBar {
                id: audioProgress_progressBar
                width: Constants.listeningScreen.sliderSize[0]
                anchors.verticalCenter: parent.verticalCenter 

                from: startTime
                to: maxDuration
                value: currentProgress
            }

            Timer {
                id: progressTimer
                interval: 1000  // Update every second
                repeat: true
                running: false  // Start manually with a function call
                onTriggered: {
                    currentProgress += 1
                    listeningScreenController.setCurrentProgress(currentProgress)
                    if (currentProgress >= maxDuration) {
                        progressTimer.stop()
                    }
                }
            }
        }

        Row {
            id: errorRow
            width: Constants.errorTextWidth
            height: Constants.listeningScreen.rowHeight

            anchors.horizontalCenter: parent.horizontalCenter  // Center the entire row
            spacing: Constants.contentRowSpacing  // Define spacing between the elements

            Text {
                id: errorText_Text
                width: Constants.errorTextWidth

                anchors.verticalCenter: parent.verticalCenter 
                text: ""
                color: Constants.errorTextColor
                font.pixelSize: Constants.fontsize.body
                wrapMode: Text.Wrap
            }
        }

        Row {
            id: buttonsRow
            width: Constants.listeningScreen.buttonRowSize[0]
            height: Constants.listeningScreen.buttonRowSize[1]

            anchors.horizontalCenter: parent.horizontalCenter
            spacing: Constants.contentRowSpacing

            Button {
                id: back_button
                width: Constants.buttonDim[0]
                height: Constants.buttonDim[1]
                anchors.verticalCenter: parent.verticalCenter 

                text: qsTr("Back")
                font.pointSize: Constants.fontsize.button

                onClicked: {
                    utils.handleStopButtonClick()
                    mainWindow.loadStartScreen()
                }
            }

            Button {
                id: submit_button
                width: Constants.buttonDim[0]
                height: Constants.buttonDim[1]
                anchors.verticalCenter: parent.verticalCenter 

                text: qsTr("Submit")
                font.pointSize: Constants.fontsize.button

                onClicked: {
                    utils.handleSubmitButtonClick()
                }
            }
        }

        Row {
            id: busyIndicatorRow
            height: Constants.listeningScreen.rowHeight

            anchors.horizontalCenter: parent.horizontalCenter  // Center the entire row
            spacing: Constants.contentRowSpacing  // Define spacing between the elements

            BusyIndicator {
                id: submitButtonPressed_BusyIndicator
                anchors.horizontalCenter: parent.horizontalCenter

                visible: false
                running: visible
            }
        }
    }
}
