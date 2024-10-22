// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

import QtQuick
import view.Project
import QtQuick.Controls


Window {
    id: mainWindow
    width: Constants.width
    height: Constants.height
    visible: true
    title: Constants.title

    function loadListeningScreen() {
        screenLoader.source = "ListeningScreen.ui.qml"
    }
    function loadStartScreen() {
        screenLoader.source = "StartScreen.ui.qml"
    }
    function loadResultScreen() {
        screenLoader.source = "ResultScreen.ui.qml"
    }

    // A loader to dynamically load different screens
    Loader {
        id: screenLoader
        anchors.fill: parent

        source: "StartScreen.ui.qml"  // Load the StartScreen by default
    }

    Text {
        id: title_text
        text: Constants.title
        font.bold: true
        font.pointSize: Constants.fontsize.title
        
        anchors.top: parent.top
        anchors.topMargin: Constants.titleTopMargin
        anchors.horizontalCenter: parent.horizontalCenter
        font.family: Constants.font.family
    }
}
