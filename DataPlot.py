import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QWidget,
    QVBoxLayout, QPushButton, QComboBox, QLabel, QHBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据绘图工具")
        self.setGeometry(200, 200, 800, 600)

        self.dataframes = []  # 存储多文件数据
        self.canvas = PlotCanvas(self, width=6, height=4)

        # UI 控件
        open_btn = QPushButton("打开文件")
        open_btn.clicked.connect(self.open_file)

        self.x_combo = QComboBox()
        self.y_combo = QComboBox()
        plot_btn = QPushButton("绘制")
        plot_btn.clicked.connect(self.plot_data)

        # 布局
        top_layout = QHBoxLayout()
        top_layout.addWidget(open_btn)
        top_layout.addWidget(QLabel("X轴:"))
        top_layout.addWidget(self.x_combo)
        top_layout.addWidget(QLabel("Y轴:"))
        top_layout.addWidget(self.y_combo)
        top_layout.addWidget(plot_btn)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择数据文件", "", "Data Files (*.csv *.txt *.dat)")
        if file_path:
            try:
                df = pd.read_csv(file_path, sep=None, engine="python")  # 自动识别分隔符
                self.dataframes.append(df)
                self.x_combo.clear()
                self.y_combo.clear()
                self.x_combo.addItems(df.columns)
                self.y_combo.addItems(df.columns)
            except Exception as e:
                print("文件读取失败:", e)

    def plot_data(self):
        if not self.dataframes:
            return
        x_col = self.x_combo.currentText()
        y_col = self.y_combo.currentText()
        if not x_col or not y_col:
            return

        self.canvas.ax.clear()
        for df in self.dataframes:
            if x_col in df.columns and y_col in df.columns:
                self.canvas.ax.plot(df[x_col], df[y_col], label=f"{x_col}-{y_col}")
        self.canvas.ax.legend()
        self.canvas.draw()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super().__init__(fig)


#主函数，使用QT
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotApp()
    window.show()
    sys.exit(app.exec_())
