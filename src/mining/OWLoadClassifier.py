import Orange
from Orange.classification import svm
from Orange.evaluation import testing, scoring
from OWWidget import *
import OWGUI
import orange
import sys, os


class OWLoadClassifier(OWWidget):
    settingsList = ["filenameHistory", "selectedFileIndex", "lastFile"]
    
    def __init__(self, parent=None, signalManager=None, name="Load Classifier"):
        OWWidget.__init__(self, parent, signalManager, name, wantMainArea=False)
        
        self.outputs = [("Classifier", orange.Classifier, Dynamic)]
        
        self.filenameHistory = []
        self.selectedFileIndex = 0
        self.lastFile = os.path.expanduser("~/orange_classifier.pck")
        
        self.loadSettings()
        
        self.filenameHistory = filter(os.path.exists, self.filenameHistory)
        
        #####
        # GUI
        #####
        
        box = OWGUI.widgetBox(self.controlArea, "File", orientation="horizontal", addSpace=True)
        self.filesCombo = OWGUI.comboBox(box, self, "selectedFileIndex",
                                         items=[os.path.basename(p) for p in self.filenameHistory],
                                         tooltip="Select a recent file",
                                         callback=self.onRecentSelection)
        
        self.browseButton = OWGUI.button(box, self, "...", callback=self.browse,
                                         tooltip="Browse file system")

        self.browseButton.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.browseButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        
        OWGUI.rubber(self.controlArea)
        
        self.resize(200, 50)
        
        if self.filenameHistory:
            self.loadAndSend()
        
        
    def onRecentSelection(self):
        filename = self.filenameHistory[self.selectedFileIndex]
        self.filenameHistory.pop(self.selectedFileIndex)
        self.filenameHistory.insert(0, filename)
        self.filesCombo.removeItem(self.selectedFileIndex)
        self.filesCombo.insertItem(0, os.path.basename(filename))
        self.selectedFileIndex = 0
        
        self.loadAndSend()
        
    def browse(self):
        filename = QFileDialog.getOpenFileName(self, "Load Classifier From File",
                        self.lastFile, "Pickle files (*.pickle *.pck)\nAll files (*.*)")
        filename = unicode(filename)
        if filename:
            if filename in self.filenameHistory:
                self.selectedFileIndex = self.filenameHistory.index(filename)
                self.onRecentSelection()
                return
            self.lastFile = filename
            self.filenameHistory.insert(0, filename)
            self.filesCombo.insertItem(0, os.path.basename(filename))
            self.filesCombo.setCurrentIndex(0)
            self.selectedFileIndex = 0
            self.loadAndSend()
            
    def loadAndSend(self):
        filename = self.filenameHistory[self.selectedFileIndex]
        import cPickle
        self.error([0, 1])
        try:
            classifier = cPickle.load(open(filename, "rb"))
            self.classifier = classifier
        except Exception, ex:
            self.error(0, "Could not load classifier! %s" % str(ex))
            return
        
        if not isinstance(classifier, orange.Classifier):
            self.error(1, "'%s' is not an orange classifier" % os.path.basename(filename))
            return 
        
        self.send("Classifier", classifier)

def test_accuracy():
    correct = 0.0
    for ex in data:
        if classifier(ex) == ex.getclass():
            correct += 1
    print "Classification accuracy:", correct / len(data)
    
if __name__ == "__main__":
    app = QApplication([])
    w = OWLoadClassifier()
    w.show()
    app.exec_()
    w.saveSettings() 

    data = orange.ExampleTable("features.csv")
    classifier = w.classifier
#    for i in range(5):
#        c = classifier(data[i])
#        print "original", data[i].getclass(), "classified as", c
        
    test_accuracy()
