import sys
import os
import winsound
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QWidget, QHBoxLayout, QPushButton, QLabel, QVBoxLayout, QMenu, QListWidget
from PySide6.QtCore import QTimer, Qt, QPoint, QEvent
from PySide6.QtGui import QIcon, QAction
from win11toast import notify

# Adicione esta função no início do arquivo
def get_asset_path(filename):
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como executável
        return os.path.join(sys._MEIPASS, 'assets', filename)
    else:
        # Se estiver rodando como script
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', filename))

class TimeSelector(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("""
            QListWidget {
                background-color: rgba(0, 120, 212, 180);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 50);
            }
            QListWidget::item {
                padding: 5px;
                border-radius: 5px;
                color: white;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background-color: rgba(255, 255, 255, 50);
            }
            QListWidget::item:selected {
                background-color: rgba(255, 255, 255, 100);
            }
        """)
        self.addItems(["3 min", "5 min", "10 min", "15 min", "20 min", "25 min", "30 min"])
        self.itemClicked.connect(self.hide)
        self.setFixedWidth(parent.width())

    def hideEvent(self, event):
        self.parent().setFocus()
        super().hideEvent(event)

class FloatingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setWindowFlag(Qt.WindowDoesNotAcceptFocus, True)
        
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 120, 212, 180);
                border-radius: 15px;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 50);
                border-radius: 10px;
                color: white;
                font-weight: bold;
                min-width: 20px;
                max-width: 20px;
                min-height: 20px;
                max-height: 20px;
            }
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(8, 3, 8, 3)
        self.layout.setSpacing(4)

        self.time_label = QLabel("03:00")
        self.layout.addWidget(self.time_label, 1, Qt.AlignCenter)

        self.start_pause_button = QPushButton("▶")
        self.stop_button = QPushButton("■")
        self.decrease_button = QPushButton("-")
        self.increase_button = QPushButton("+")
        self.toggle_mode_button = QPushButton("M")
        self.close_button = QPushButton("❌")  # Trocado para ❌
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-radius: 10px;
                color: white;
                font-weight: bold;
                font-size: 14px;
                min-width: 20px;
                max-width: 20px;
                min-height: 20px;
                max-height: 20px;
                padding: 0;
                margin: 0;
                line-height: 20px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 100);
            }
        """)

        for button in [self.decrease_button, self.start_pause_button, self.stop_button, self.increase_button, self.toggle_mode_button, self.close_button]:
            self.layout.addWidget(button)

        self.time_selector = TimeSelector(self)
        self.time_selector.hide()

        self.time_label.mousePressEvent = self.toggle_time_selector

        self.setFixedSize(240, 35)  # Aumentado a largura para acomodar o novo botão
        self.move_to_top_center()

        self.close_button.clicked.connect(self.close)  # Conectar o sinal de clique ao método close

    def move_to_top_center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        new_x = (screen.width() - self.width()) // 2
        new_y = 0
        self.move(new_x, new_y)  # Use move() em vez de setGeometry()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def toggle_time_selector(self, event):
        if event.button() == Qt.LeftButton:
            if self.time_selector.isVisible():
                self.time_selector.hide()
            else:
                self.time_selector.setFixedWidth(self.width())
                pos = self.mapToGlobal(QPoint(0, self.height()))
                self.time_selector.move(pos)
                self.time_selector.show()
                self.time_selector.raise_()

    def event(self, event):
        if event.type() == QEvent.WindowDeactivate:
            self.time_selector.hide()
        elif event.type() == QEvent.Show:
            self.move_to_top_center()  # Chame move_to_top_center() em vez de move_to_bottom_right()
        return super().event(event)

class PomodoroTimer(QSystemTrayIcon):
    def __init__(self):
        super().__init__()

        icon_path = get_asset_path('icon.ico')
        self.setIcon(QIcon(icon_path))
        self.setVisible(True)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.default_time = 180  # 3 minutos em segundos
        self.remaining_time = self.default_time
        self.is_running = False
        self.is_focus_mode = True

        self.floating_widget = FloatingWidget()
        self.floating_widget.show()

        self.create_ui()
        self.connect_signals()

    def create_ui(self):
        self.floating_widget.time_label.setText(self.format_time(self.remaining_time))

    def connect_signals(self):
        self.floating_widget.start_pause_button.clicked.connect(self.toggle_timer)
        self.floating_widget.stop_button.clicked.connect(self.stop_timer)
        self.floating_widget.decrease_button.clicked.connect(lambda: self.adjust_time(-60))
        self.floating_widget.increase_button.clicked.connect(lambda: self.adjust_time(60))
        self.floating_widget.toggle_mode_button.clicked.connect(self.toggle_mode)
        self.floating_widget.time_selector.itemClicked.connect(self.set_time_from_selector)

        quit_action = QAction("Sair", self)
        quit_action.triggered.connect(QApplication.quit)
        self.setContextMenu(QMenu())
        self.contextMenu().addAction(quit_action)

    def toggle_timer(self):
        if self.is_running:
            self.timer.stop()
            self.floating_widget.start_pause_button.setText("▶")
        else:
            self.timer.start(1000)
            self.floating_widget.start_pause_button.setText("⏸")
        self.is_running = not self.is_running

    def stop_timer(self):
        self.timer.stop()
        self.is_running = False
        self.remaining_time = self.default_time
        self.floating_widget.start_pause_button.setText("▶")
        self.floating_widget.time_label.setText(self.format_time(self.remaining_time))

    def update_time(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.floating_widget.time_label.setText(self.format_time(self.remaining_time))
        else:
            self.timer.stop()
            self.is_running = False
            self.floating_widget.start_pause_button.setText("▶")
            self.show_notification()
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)

    def adjust_time(self, seconds):
        self.remaining_time = max(0, self.remaining_time + seconds)
        self.default_time = self.remaining_time
        self.floating_widget.time_label.setText(self.format_time(self.remaining_time))

    def format_time(self, seconds):
        minutes, secs = divmod(seconds, 60)
        return f"{minutes:02d}:{secs:02d}"

    def show_notification(self):
        notify("Pomodoro Timer", "Tempo esgotado!")
        sound_path = get_asset_path('notification.wav')
        winsound.PlaySound(sound_path, winsound.SND_FILENAME)

    def toggle_mode(self):
        self.is_focus_mode = not self.is_focus_mode
        color = "rgba(0, 120, 212, 180)" if self.is_focus_mode else "rgba(76, 175, 80, 180)"
        self.floating_widget.setStyleSheet(self.floating_widget.styleSheet().replace(
            "background-color: rgba(0, 120, 212, 180);",
            f"background-color: {color};"
        ).replace(
            "background-color: rgba(76, 175, 80, 180);",
            f"background-color: {color};"
        ))
        self.floating_widget.time_selector.setStyleSheet(
            self.floating_widget.time_selector.styleSheet().replace(
                "background-color: rgba(0, 120, 212, 180);",
                f"background-color: {color};"
            )
        )

    def set_time_from_selector(self, item):
        minutes = int(item.text().split()[0])
        self.remaining_time = minutes * 60
        self.default_time = self.remaining_time
        self.floating_widget.time_label.setText(self.format_time(self.remaining_time))

if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        # Se estiver rodando como executável, ajuste o diretório de trabalho
        os.chdir(sys._MEIPASS)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    timer = PomodoroTimer()
    sys.exit(app.exec())
