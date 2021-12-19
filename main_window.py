from PySide6 import QtCore, QtWidgets, QtGui, QtOpenGLWidgets
from math import cos, sin, pi
from pixels import Pixels
from effects import rainbowLine, redGreen, snake, rainbowBursts
import PySide6
import time

class MainWindow(QtWidgets.QWidget):
    PIXEL_SIZE = 18
    DEFAUL_COUNT = 100
    DEFAUL_FRAME_DELAY = 30

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Neopixel Effect Simulator")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect( self.next_frame )

        self.setup_effects()

        self.rootVBox = QtWidgets.QVBoxLayout(self)
        self.setup_toolbar()
        self.setup_scene()
        self.reset_scene()

    def setup_effects(self):
        self.pixels: Pixels = Pixels(MainWindow.DEFAUL_COUNT, 2.8)
        self.effects = [            
            snake.Snake(self.pixels, 30, 8, 255, 0, 0, 0),
            rainbowLine.RainbowLine(self.pixels, 255),
            rainbowBursts.RainbowBursts(self.pixels, 255, 20),
        ]
        self.effect = self.effects[2]

    def setup_scene(self):
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setInteractive(False)
        self.rootVBox.addWidget(self.view)
        self.last_time = time.time()
        self.frame_count = 0

    def setup_toolbar(self):
        self.buttons_bar = QtWidgets.QHBoxLayout()

        pixelCountLabel = QtWidgets.QLabel("Pixel Count")
        self.buttons_bar.addWidget(pixelCountLabel)

        self.pixelCountBox = QtWidgets.QSpinBox()
        self.pixelCountBox.setMaximum(5000)
        self.pixelCountBox.setValue(MainWindow.DEFAUL_COUNT)
        self.buttons_bar.addWidget(self.pixelCountBox)
        
        frameDelayLabel = QtWidgets.QLabel("Frame Delay (ms)")
        self.buttons_bar.addWidget(frameDelayLabel)

        self.frameDelayBox = QtWidgets.QSpinBox()
        self.frameDelayBox.setMaximum(5000)
        self.frameDelayBox.setValue(MainWindow.DEFAUL_FRAME_DELAY)
        self.buttons_bar.addWidget(self.frameDelayBox)
        
        self.button_reset = QtWidgets.QPushButton("Reset")
        self.button_reset.clicked.connect(self.reset_scene)
        self.buttons_bar.addWidget(self.button_reset)

        self.button_run = QtWidgets.QPushButton("Run")
        self.button_run.clicked.connect(self.run)
        self.buttons_bar.addWidget(self.button_run)
        
        self.button_pause = QtWidgets.QPushButton("Pause")
        self.button_pause.clicked.connect(self.pause)
        self.buttons_bar.addWidget(self.button_pause)
        
        self.button_next_frame = QtWidgets.QPushButton('Next Frame')
        self.button_next_frame.clicked.connect(self.next_frame)
        self.buttons_bar.addWidget(self.button_next_frame)
        
        self.button_zoomin = QtWidgets.QPushButton("Zoom In")
        self.button_zoomin.clicked.connect(self.zoomin_pressed)
        self.buttons_bar.addWidget(self.button_zoomin)
        
        self.button_zoomout = QtWidgets.QPushButton('Zoom Out')
        self.button_zoomout.clicked.connect(self.zoomout_pressed)
        self.buttons_bar.addWidget(self.button_zoomout)

        self.label_fps = QtWidgets.QLabel(f'fps:0')
        self.buttons_bar.addWidget(self.label_fps)
        
        self.rootVBox.addLayout(self.buttons_bar)

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        rect = self.scene.sceneRect()
        self.view.fitInView(rect, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.view.repaint()
        return super().resizeEvent(event)

    def render_scene(self):
        self.calculate_fps()

        for i, shape in enumerate(self.scene.items(QtCore.Qt.SortOrder.AscendingOrder)):
            pixel = self.pixels[i]
            color = QtGui.QColor(pixel['red'], pixel['green'], pixel['blue'])
            shape.setPen(color)
            shape.setBrush(color)

    def calculate_fps(self):
        self.frame_count = self.frame_count + 1
        currentTime = time.time()
        if int(currentTime) > int(self.last_time):
            diff = currentTime - self.last_time
            fps = int(self.frame_count/diff)
            self.label_fps.setText(f'fps:{fps:3d}')
            self.frame_count = 0
            self.last_time = currentTime
 
    @QtCore.Slot()
    def reset_scene(self):
        self.scene.clear()
        self.scene.setBackgroundBrush(QtGui.QColor(0, 0, 0))

        self.timer.setInterval(self.frameDelayBox.value())
        pixelCount = self.pixelCountBox.value()

        if (self.pixels.numPixels() != pixelCount):
            self.pixels: Pixels = Pixels(pixelCount, 1)

        self.effect.reset()
        self.effect.next_frame()

        amplitude = 500
        waweLength = 500

        for i in range(self.pixels.count):
            self.scene.addEllipse(
                waweLength * cos(i * ((pi*2)/pixelCount)),
                amplitude * sin(i * ((pi*2)/pixelCount)),
                MainWindow.PIXEL_SIZE,
                MainWindow.PIXEL_SIZE
            )
        
        self.render_scene()
        
    @QtCore.Slot()
    def run(self):
        self.timer.start()
    
    @QtCore.Slot()
    def pause(self):
        self.timer.stop()

    @QtCore.Slot()
    def zoomin_pressed(self):
        self.view.scale(1.1, 1.1)

    @QtCore.Slot()
    def zoomout_pressed(self):
        self.view.scale(1/1.1, 1/1.1)

    @QtCore.Slot()
    def next_frame(self):
        self.effect.next_frame()
        self.render_scene()