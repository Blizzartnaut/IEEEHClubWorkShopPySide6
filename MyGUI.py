import sys
import io
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QVBoxLayout

#Imported UI
from GUIWorkshopUI import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self = Ui_MainWindow()
        self.setupUi(self)

        # Connect the navigation buttons to their respective slots
        self.button_next.clicked.connect(self.go_next_tab)
        self.button_prev.clicked.connect(self.go_previous_tab)

        # Call the function to plot the graph on label_1
        self.plot_graph()

        # Setup a timer to update the clock on tab 2 (label_2)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)  # update every 1000 ms (1 second)
        self.update_clock()  # initial update

        if hasattr(self, 'label_3'):
            # Create the QWebEngineView
            self.web_view = QWebEngineView(self)
            # Set the URL to the desired webpage
            self.web_view.setUrl(QUrl("https://github.com/Blizzartnaut/WorkingPipBoy"))
            
            # Replace label_3 in its parent layout with the web view
            parent_layout = QVBoxLayout(self.label_3)
            self.label_3.setLayout(parent_layout)
            parent_layout.addWidget(self.web_view)

    def go_next_tab(self):
        current_index = self.tabWidget.currentIndex()
        count = self.tabWidget.count()
        next_index = (current_index + 1) % count
        self.tabWidget.setCurrentIndex(next_index)

    def go_previous_tab(self):
        current_index = self.tabWidget.currentIndex()
        count = self.tabWidget.count()
        previous_index = (current_index - 1) % count
        self.tabWidget.setCurrentIndex(previous_index)

    def plot_graph(self):
        # Create a matplotlib figure with a persistent canvas
        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        # Generate data points
        x = np.linspace(0, 10, 500)
        # Choose three functions that all fall within y=0 to y=10:
        y1 = x
        y2 = 5 * np.sin(x) + 5
        y3 = 5 * np.cos(x) + 5

        # Plot each function with a label
        ax.plot(x, y1, label="f(x) = x")
        ax.plot(x, y2, label="f(x) = 5*sin(x)+5")
        ax.plot(x, y3, label="f(x) = 5*cos(x)+5")

        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Mathematical Functions")
        ax.legend()
        fig.tight_layout()

        # Convert the matplotlib figure to a QPixmap
        canvas = FigureCanvasAgg(fig)
        buf = io.BytesIO()
        canvas.print_png(buf)
        buf.seek(0)
        image = QImage.fromData(buf.getvalue())
        pixmap = QPixmap.fromImage(image)

        # Set the pixmap to label_1
        self.label_1.setPixmap(pixmap)
        # Allow the label to scale the pixmap appropriately
        self.label_1.setScaledContents(True)

        # Clean up the figure to free up memory
        plt.close(fig)

    def update_clock(self):
        # Get the current system time
        now = datetime.datetime.now()
        # Format it as HH:MM:SS
        time_string = now.strftime("%H:%M:%S")
        # Update label_2 with the current time
        self.label_2.setText(time_string)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())