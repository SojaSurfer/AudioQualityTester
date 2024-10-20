pragma Singleton
import QtQuick 2.15

QtObject {
    readonly property int width: 1200
    readonly property int height: 1000
    readonly property string title: "Audio Quality Tester"
    readonly property color backgroundColor: "#EAEAEA"

    readonly property int titleTopMargin: 20

    readonly property int explanationTextTopMargin: 100
    readonly property int contentColTopMargin: 200
    readonly property int contentColBottomMargin: 50
    readonly property int contentColSideMargin: 100
    readonly property int contentColSpacing: 20
    readonly property int contentRowSpacing: 20

    property var popupSize: [width * 0.7, height * 0.7]


    property var fontsize: QtObject {
        readonly property int body: 12
        readonly property int button: 18
        readonly property int title: 32
        readonly property int header: 22
        readonly property int subheader: 16
        readonly property int colHeader: 14
        readonly property int emphasis: 14
    }

    property var buttonDim: [120, 50] // width, height
    property var smallButtonDim: [80, 35]

    property var errorTextCoord: [350, 750]
    readonly property int errorTextWidth: 400
    readonly property color errorTextColor: "red"



    property string relativeFontDirectory: "fonts"
    /* Edit this comment to add your custom font */
    readonly property font font: Qt.font({
                                             family: "Arial",  // Replace with your desired font
                                             pixelSize: 16     // Adjust pixel size
                                         })
    readonly property font largeFont: Qt.font({
                                                  family: "Arial",  // Replace with your desired font
                                                  pixelSize: 24     // Adjust pixel size for large font
                                              })


    property var startScreen: QtObject {
        property var explanationTextSize: [700, 80]
        readonly property int fileLoadTextFieldWidth: 350
        readonly property int compressionScrollViewHeight: 200
        readonly property int compressionListViewHeight: 150
        readonly property int compressionSpacing: 10
        readonly property int compressionViewElemHeight: 40
        readonly property color compressionSelected: "lightblue"
        readonly property color compressionUnselected: "white"
        readonly property int spacingAfterScrollView: 100
        readonly property string explanationText: "This is a template text which will explain the tool. This is a template text which will explain the tool. This is a template text which will explain the tool. This is a template text which will explain the tool."
    }

    property var listeningScreen: QtObject {
        readonly property int maxAudioDurationDefault: 100
        readonly property int rowHeight: 50
        readonly property int rowSpacing: 20

        property var rowLabelSize: [60, 25]
        property var rowComboBoxSize: [220, 40]
        property var rowPlayButtonSize: [60, 30]
        property var rowSize: [rowLabelSize[0] + rowComboBoxSize[0] + rowPlayButtonSize[0] + (2 * rowSpacing), rowHeight]
        
        readonly property int sliderLabelWidth: 140
        property var sliderTextFileSize: [40, 30]
        property var sliderSize: [250, 40]
        property var sliderRowSize: [sliderTextFileSize[0] + sliderSize[0] + sliderLabelWidth + rowPlayButtonSize[0]+ (2 * rowSpacing), rowHeight]
    
        property var buttonRowSize: [(2*Constants.buttonDim[0]) + (2*rowSpacing), rowHeight]
    }


    property var resultScreen: QtObject {
        readonly property int contentColTopMargin: 100
        
        readonly property int textBoxWidth: 180
        readonly property int imageBoxWidth: 420

        readonly property string rowColor: "white" // "transparent"
        readonly property string rowBorderColor: "black"
        readonly property int rowBorderWidth: 1
        readonly property int rowHeight: 300
        readonly property int rowWidth: 1050
        readonly property int rowInnerMargin: 5
        readonly property int headerRowHeight: 30

        readonly property int buttonWidth: 120
        readonly property int buttonHeight: 60
        readonly property int fontsizeButton: 18


        readonly property int listViewHeight: 650
        readonly property int narrowRowSpacing: 10
        property var buttonRowSize: [(4*Constants.buttonDim[0]) + (4*narrowRowSpacing), 50]

        property var itemHeight: rowHeight - (2 * rowInnerMargin)

        readonly property int textInfoMargin: 10

        readonly property string resultInfoText: "Example 01\nYour Selection:\nFormat:\nSample Rate:\nBitrate:\nListening Duration:\n"

    }
}