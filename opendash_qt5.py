#!/usr/bin/env python3
"""
Argent Opendash Qt5 v3.1 — Cinnamon Edition
Monitor, Optimizador y Gestor del Sistema

Versión Qt5 diseñada para Cinnamon y cualquier entorno de escritorio.
Motor de renderizado Qt5 completamente independiente del compositor
Muffin — sin conflictos GL, sin freezes.

Tavo78ok · MIT License
https://github.com/Tavo78ok/Argent-Opendash-Gtk4-libadwaita
"""

import sys, os, math, re, stat, threading, subprocess, platform, glob, time
from collections import deque

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QTabWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QLineEdit, QListWidget, QListWidgetItem, QScrollArea,
    QSlider, QSplitter, QSizePolicy, QMessageBox, QDialog,
    QDialogButtonBox, QProgressBar, QStackedWidget, QButtonGroup,
    QAbstractItemView, QGroupBox, QCheckBox
)
from PyQt5.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, pyqtSlot, QObject, QSize, QRect, QPoint
)
from PyQt5.QtGui import (
    QPainter, QPen, QBrush, QColor, QPainterPath, QFont,
    QFontMetrics, QPalette, QLinearGradient, QIcon, QPixmap
)
import psutil

# ═══════════════════════════════════════════════════════════
#  SECCIÓN 1 — CONSTANTES
# ═══════════════════════════════════════════════════════════
APP_NAME    = 'Argent Opendash Qt5'
APP_VERSION = '3.1'
BINARY      = 'argent-opendash-qt5'
AUTOSTART_F = os.path.expanduser('~/.config/autostart/argent-opendash-qt5.desktop')
PERFIL_F    = os.path.expanduser('~/.opendash_perfil')

# Colores neon
C_GREEN  = QColor(0,   255, 163)
C_CYAN   = QColor(0,   207, 255)
C_AMBER  = QColor(251, 191,  36)
C_RED    = QColor(255,  68,  68)
C_PURPLE = QColor(168, 139, 248)
C_ORANGE = QColor(251, 146,  60)

BG_DARK  = QColor(13,  15,  20)
BG_CARD  = QColor(20,  23,  32)
BG_CARD2 = QColor(13,  16,  24)

# ═══════════════════════════════════════════════════════════
#  SECCIÓN 2 — QSS STYLESHEET
# ═══════════════════════════════════════════════════════════
QSS = """
QMainWindow, QDialog {
    background-color: #0d0f14;
}
QWidget {
    background-color: #0d0f14;
    color: rgba(255,255,255,0.85);
    font-size: 13px;
}
QTabWidget::pane {
    border: none;
    background-color: #0d0f14;
}
QTabWidget::tab-bar { alignment: left; }
QTabBar::tab {
    background-color: #141720;
    color: rgba(255,255,255,0.78);
    padding: 8px 16px;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 12px;
    font-weight: 600;
    min-width: 90px;
}
QTabBar::tab:selected {
    color: #00ffa3;
    border-bottom: 2px solid #00ffa3;
    background-color: #0d0f14;
    font-weight: 700;
}
QTabBar::tab:hover:!selected {
    color: rgba(255,255,255,0.92);
    background-color: #181b24;
}
QTabBar QToolButton {
    background-color: #141720;
    border: none;
    color: white;
}
QPushButton {
    background-color: #1c1f2a;
    color: rgba(255,255,255,0.70);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 8px;
    padding: 6px 16px;
    font-size: 12px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #222636;
    color: white;
    border-color: rgba(255,255,255,0.20);
}
QPushButton:pressed { background-color: #141720; }
QPushButton#btn_action {
    background-color: #00ffa3;
    color: #060a08;
    border: none;
    font-weight: 800;
}
QPushButton#btn_action:hover { background-color: #00e892; }
QPushButton#btn_stop {
    background-color: rgba(255,68,68,0.15);
    color: #ff7070;
    border-color: rgba(255,68,68,0.25);
}
QPushButton#btn_start {
    background-color: rgba(0,255,163,0.12);
    color: #00ffa3;
    border-color: rgba(0,255,163,0.25);
}
QPushButton#btn_install {
    background-color: rgba(0,207,255,0.14);
    color: #00cfff;
    border-color: rgba(0,207,255,0.25);
}
QLineEdit, QListWidget {
    background-color: #141720;
    color: rgba(255,255,255,0.82);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 12px;
}
QLineEdit:focus {
    border-color: rgba(0,255,163,0.45);
}
QListWidget::item {
    padding: 6px 8px;
    border-radius: 6px;
}
QListWidget::item:selected {
    background-color: rgba(0,255,163,0.12);
    color: #00ffa3;
}
QListWidget::item:hover:!selected {
    background-color: rgba(255,255,255,0.04);
}
QScrollBar:vertical {
    background-color: #141720;
    width: 7px;
    border-radius: 3px;
}
QScrollBar::handle:vertical {
    background-color: rgba(255,255,255,0.18);
    border-radius: 3px;
    min-height: 24px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    background-color: #141720;
    height: 7px;
    border-radius: 3px;
}
QScrollBar::handle:horizontal {
    background-color: rgba(255,255,255,0.18);
    border-radius: 3px;
    min-width: 24px;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QSlider::groove:horizontal {
    background-color: #1c1f2a;
    height: 5px;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background-color: #00ffa3;
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QSlider::sub-page:horizontal {
    background-color: #00ffa3;
    border-radius: 2px;
}
QProgressBar {
    background-color: #1c2030;
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #00ffa3;
    border-radius: 4px;
}
QSplitter::handle { background-color: rgba(255,255,255,0.06); }
QMessageBox {
    background-color: #141720;
}
QMessageBox QLabel { color: white; }
"""

# Estilo de switch tipo toggle (más consistente que checkbox plano)
TOGGLE_SWITCH_QSS = """
QCheckBox::indicator {
    width: 40px;
    height: 20px;
    border-radius: 10px;
    background-color: #2a2e3a;
    border: 1px solid rgba(255,255,255,0.12);
}
QCheckBox::indicator:checked {
    background-color: #00ffa3;
    border: 1px solid #00ffa3;
}
QCheckBox::indicator:unchecked:hover {
    background-color: #343948;
}
"""

# ═══════════════════════════════════════════════════════════
#  SECCIÓN 3 — HELPERS UI
# ═══════════════════════════════════════════════════════════
def card(widget, radius=12):
    """Envuelve un widget en un QFrame con estilo card."""
    f = QFrame()
    f.setStyleSheet(f"""
        QFrame {{
            background-color: #141720;
            border-radius: {radius}px;
            border: 1px solid rgba(255,255,255,0.06);
        }}
    """)
    lay = QVBoxLayout(f)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.addWidget(widget)
    return f

def section_lbl(text):
    l = QLabel(text)
    l.setStyleSheet(
        "color: rgba(255,255,255,0.22); font-size: 10px; "
        "font-weight: 800; letter-spacing: 4px;")
    return l

def unit_lbl(text, color=None):
    l = QLabel(text)
    css = "color: rgba(255,255,255,0.38); font-size: 12px;"
    if color:
        css = f"color: {color}; font-size: 12px;"
    l.setStyleSheet(css)
    return l

def mono_lbl(text="—"):
    l = QLabel(text)
    l.setStyleSheet(
        "font-family: monospace; font-size: 12px; "
        "color: rgba(255,255,255,0.72); background: transparent;")
    l.setTextInteractionFlags(Qt.TextSelectableByMouse)
    return l

def neon_btn(text, style="default"):
    b = QPushButton(text)
    ids = {"action":"btn_action","stop":"btn_stop",
           "start":"btn_start","install":"btn_install"}
    if style in ids:
        b.setObjectName(ids[style])
    return b

# ═══════════════════════════════════════════════════════════
#  SECCIÓN 4 — CAPA DE HARDWARE
# ═══════════════════════════════════════════════════════════
_temp_cache = {'value': None}
_temp_lock  = threading.Lock()

# Sensores hwmon seguros (solo CPU/ACPI, nunca GPU)
_SAFE_HW_SENSORS = {'coretemp','k10temp','zenpower','acpitz',
                    'cpu_thermal','w83795','nct6775','nct6776',
                    'it8728','it8792','f71882fg'}
_SKIP_HW_SENSORS = {'nouveau','nvidia','radeon','amdgpu','i915'}

def _temp_updater():
    while True:
        val = None
        # Método 1: thermal_zone (rápido, nunca cuelga)
        for path in sorted(glob.glob('/sys/class/thermal/thermal_zone*/temp')):
            try:
                t = int(open(path).read().strip()) / 1000.0
                if 20.0 < t < 115.0:
                    val = t; break
            except Exception:
                pass
        # Método 2: hwmon filtrado por nombre de sensor
        # Solo sensores CPU/ACPI — nunca GPU (pueden necesitar X11)
        if val is None:
            for hwmon_dir in sorted(glob.glob('/sys/class/hwmon/hwmon*')):
                try:
                    name = open(f'{hwmon_dir}/name').read().strip().lower()
                    if name in _SKIP_HW_SENSORS:
                        continue          # GPU — saltar
                    if name not in _SAFE_HW_SENSORS:
                        continue          # Desconocido — saltar por seguridad
                    # Leer primera temp de este sensor
                    for temp_f in sorted(glob.glob(f'{hwmon_dir}/temp*_input')):
                        try:
                            t = int(open(temp_f).read().strip()) / 1000.0
                            if 20.0 < t < 115.0:
                                val = t; break
                        except Exception:
                            pass
                    if val is not None:
                        break
                except Exception:
                    pass
        with _temp_lock:
            _temp_cache['value'] = val
        time.sleep(10)

def hw_temp():
    with _temp_lock:
        return _temp_cache['value']

def hw_cmd(*args, timeout=4):
    try:
        return subprocess.check_output(
            list(args), text=True,
            stderr=subprocess.DEVNULL,
            timeout=timeout).strip()
    except Exception:
        return ''

def hw_partitions():
    skip = {'tmpfs','devtmpfs','squashfs','overlay','proc',
            'sysfs','cgroup','cgroup2','pstore','efivarfs',''}
    result = []
    try:
        for p in psutil.disk_partitions(all=False):
            if p.fstype in skip: continue
            try:
                u = psutil.disk_usage(p.mountpoint)
                result.append({
                    'mount':  p.mountpoint,
                    'device': p.device.replace('/dev/',''),
                    'fstype': p.fstype,
                    'total':  u.total/(1024**3),
                    'used':   u.used/(1024**3),
                    'pct':    u.percent})
            except Exception:
                pass
    except Exception:
        pass
    return result

def hw_procs_top():
    rows = []
    try:
        for p in psutil.process_iter(['pid','name','cpu_percent','memory_percent']):
            try:
                i = p.info
                rows.append((i['pid'],(i['name'] or '')[:20],
                             i['cpu_percent'] or 0.0,
                             i['memory_percent'] or 0.0))
            except (psutil.NoSuchProcess,psutil.AccessDenied,
                    psutil.ZombieProcess):
                pass
    except Exception:
        pass
    rows.sort(key=lambda x: x[2], reverse=True)
    return rows

def hw_get_volume():
    try:
        out = hw_cmd('pactl','get-sink-volume','@DEFAULT_SINK@')
        m = re.search(r'(\d+)%', out)
        return int(m.group(1)) if m else 50
    except Exception:
        return 50

def hw_set_volume(pct):
    try:
        subprocess.run(
            ['pactl','set-sink-volume','@DEFAULT_SINK@',f'{int(pct)}%'],
            capture_output=True, timeout=2)
    except Exception:
        pass

def _backlight_dev():
    try:
        devs = os.listdir('/sys/class/backlight')
        if devs: return '/sys/class/backlight/' + devs[0]
    except Exception:
        pass
    return None

def hw_get_brightness():
    dev = _backlight_dev()
    if dev:
        try:
            cur = int(open(f'{dev}/brightness').read())
            mx  = int(open(f'{dev}/max_brightness').read())
            return cur/mx*100 if mx else 100.0
        except Exception:
            pass
    try:
        cur = hw_cmd('brightnessctl','get')
        mx  = hw_cmd('brightnessctl','max')
        if cur and mx and int(mx) > 0:
            return int(cur)/int(mx)*100
    except Exception:
        pass
    try:
        out = hw_cmd('xrandr','--verbose')
        m = re.search(r'Brightness:\s*([\d.]+)', out)
        if m: return float(m.group(1))*100
    except Exception:
        pass
    return 100.0

def hw_set_brightness(pct):
    pct = max(1, min(100, int(pct)))
    try:
        r = subprocess.run(['brightnessctl','set',f'{pct}%'],
                          capture_output=True, timeout=2)
        if r.returncode == 0: return
    except Exception:
        pass
    dev = _backlight_dev()
    if dev:
        try:
            mx = int(open(f'{dev}/max_brightness').read())
            v  = max(1, int(mx*pct/100))
            try: open(f'{dev}/brightness','w').write(str(v)); return
            except PermissionError:
                subprocess.run(['pkexec','tee',f'{dev}/brightness'],
                               input=str(v), text=True,
                               capture_output=True, timeout=5)
                return
        except Exception:
            pass
    try:
        b = pct/100
        out = hw_cmd('xrandr')
        for mon in re.findall(r'^(\S+) connected', out, re.MULTILINE):
            subprocess.run(['xrandr','--output',mon,'--brightness',f'{b:.2f}'],
                          capture_output=True, timeout=2)
    except Exception:
        pass

def _run_in_terminal(script, need_root=True):
    path = '/tmp/argent_od_qt5.sh'
    try:
        with open(path,'w') as f: f.write(script)
        os.chmod(path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    except Exception:
        return
    cmd = ['pkexec','bash',path] if need_root else ['bash',path]
    for term in ['x-terminal-emulator','xterm','mate-terminal',
                 'gnome-terminal','konsole','xfce4-terminal']:
        try:
            subprocess.Popen([term,'-e',' '.join(cmd)])
            return
        except FileNotFoundError:
            continue

def run_bg(fn, *args, **kwargs):
    t = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
    t.start(); return t

# ═══════════════════════════════════════════════════════════
#  SECCIÓN 5 — WIDGETS PERSONALIZADOS
# ═══════════════════════════════════════════════════════════
class RingMeter(QWidget):
    def __init__(self, color: QColor, size=80, parent=None):
        super().__init__(parent)
        self._color = color
        self._val   = 0.0
        self.setFixedSize(size, size)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def setValue(self, v):
        self._val = max(0.0, min(1.0, float(v)))
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        pad  = 8
        r    = min(w, h) / 2 - pad
        cx   = w / 2
        cy   = h / 2
        lw   = max(5, int(r * 0.13))
        rect = QRect(int(cx-r), int(cy-r), int(r*2), int(r*2))

        # Arco fondo
        pen_bg = QPen(QColor(33, 38, 52), lw, Qt.SolidLine, Qt.RoundCap)
        p.setPen(pen_bg)
        p.drawArc(rect, 225 * 16, -270 * 16)

        if self._val > 0.01:
            span = int(-270 * 16 * self._val)
            # Halo
            pen_halo = QPen(QColor(self._color.red(),
                                   self._color.green(),
                                   self._color.blue(), 25),
                            lw + 6, Qt.SolidLine, Qt.RoundCap)
            p.setPen(pen_halo)
            p.drawArc(rect, 225 * 16, span)
            # Arco principal
            pen_main = QPen(self._color, lw, Qt.SolidLine, Qt.RoundCap)
            p.setPen(pen_main)
            p.drawArc(rect, 225 * 16, span)
        p.end()


class HistoryGraph(QWidget):
    def __init__(self, color: QColor, label='', maxlen=60,
                 height=70, parent=None):
        super().__init__(parent)
        self._color = color
        self._label = label
        self._data  = deque([0.0]*maxlen, maxlen=maxlen)
        self.setMinimumHeight(height)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def push(self, pct):
        self._data.append(max(0.0, min(100.0, float(pct))) / 100.0)
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        # Fondo
        p.fillRect(0, 0, w, h, QColor(15, 18, 26))

        pts = list(self._data)
        n   = len(pts)
        if n < 2: return

        pad  = h * 0.08
        step = w / (n - 1)

        def py(v): return h - pad - v * (h - 2 * pad)

        # Grid
        pen_grid = QPen(QColor(255, 255, 255, 10), 1)
        p.setPen(pen_grid)
        for frac in (0.25, 0.5, 0.75):
            y = int(py(frac))
            p.drawLine(0, y, w, y)

        # Área rellena
        path_fill = QPainterPath()
        path_fill.moveTo(0, h)
        for i, v in enumerate(pts):
            path_fill.lineTo(i * step, py(v))
        path_fill.lineTo((n-1) * step, h)
        path_fill.closeSubpath()

        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0, QColor(self._color.red(),
                                  self._color.green(),
                                  self._color.blue(), 40))
        grad.setColorAt(1, QColor(self._color.red(),
                                  self._color.green(),
                                  self._color.blue(), 0))
        p.fillPath(path_fill, QBrush(grad))

        # Línea principal
        path_line = QPainterPath()
        path_line.moveTo(0, py(pts[0]))
        for i, v in enumerate(pts[1:], 1):
            path_line.lineTo(i * step, py(v))

        pen_line = QPen(self._color, 1.8, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        p.setPen(pen_line)
        p.drawPath(path_line)

        # Etiqueta
        p.setPen(QPen(QColor(self._color.red(),
                             self._color.green(),
                             self._color.blue(), 210)))
        p.setFont(QFont('monospace', 9))
        cur = pts[-1] * 100
        p.drawText(8, 16, f'{self._label}  {cur:.0f}%')
        p.end()


class MetricCard(QFrame):
    def __init__(self, title, color: QColor, ring_size=80, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #141720;
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.06);
            }
        """)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 12, 10, 12)
        lay.setSpacing(4)
        lay.setAlignment(Qt.AlignCenter)

        self._ring = RingMeter(color, ring_size)
        self._ring.setAlignment = lambda _: None  # no-op
        lay.addWidget(self._ring, 0, Qt.AlignCenter)

        self._val = QLabel('—')
        self._val.setStyleSheet(
            'font-size: 26px; font-weight: 900; color: white; '
            'background: transparent; border: none;')
        self._val.setAlignment(Qt.AlignCenter)
        lay.addWidget(self._val)

        self._sub = QLabel(title.upper())
        self._sub.setStyleSheet(
            'font-size: 9px; font-weight: 700; letter-spacing: 2px; '
            'color: rgba(255,255,255,0.32); background: transparent; border: none;')
        self._sub.setAlignment(Qt.AlignCenter)
        lay.addWidget(self._sub)

    def update_data(self, txt, pct):
        self._val.setText(txt)
        self._ring.setValue(pct / 100)

# ═══════════════════════════════════════════════════════════
#  SECCIÓN 6 — VENTANA PRINCIPAL
# ═══════════════════════════════════════════════════════════
class OpenDashQt5(QMainWindow):

    # Señales Qt — thread-safe por diseño
    sig_metrics  = pyqtSignal(dict)
    sig_procs    = pyqtSignal(list)
    sig_parts    = pyqtSignal(list)
    sig_apt      = pyqtSignal(list)
    sig_flat     = pyqtSignal(list)
    sig_svcs     = pyqtSignal(list)
    sig_sysinfo  = pyqtSignal(str)
    sig_toast    = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'{APP_NAME} v{APP_VERSION}')
        self.resize(980, 680)
        self.setMinimumSize(820, 560)
        # Ícono de la app desde sistema o desde archivo local
        app_icon = QIcon.fromTheme('argent-opendash-qt5')
        if app_icon.isNull():
            for path in ('/usr/share/pixmaps/argent-opendash-qt5.png',
                         '/usr/share/icons/hicolor/256x256/apps/argent-opendash-qt5.png',
                         os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      'argent-opendash.png')):
                if os.path.exists(path):
                    app_icon = QIcon(path)
                    break
        if not app_icon.isNull():
            self.setWindowIcon(app_icon)

        # Estado
        self._dark      = True
        self._metrics   = {}
        self._all_apt   = []
        self._all_flat  = []
        self._services  = []
        self._part_bars = {}
        self._net_last  = 0
        try:
            io = psutil.net_io_counters()
            self._net_last = io.bytes_recv + io.bytes_sent
        except Exception:
            pass

        # Debounce sliders
        self._br_timer  = QTimer(); self._br_timer.setSingleShot(True)
        self._vol_timer = QTimer(); self._vol_timer.setSingleShot(True)
        self._br_timer.timeout.connect(self._apply_br)
        self._vol_timer.timeout.connect(self._apply_vol)
        self._br_pend = self._vol_pend = None

        # Debounce APT search
        self._apt_search_timer = QTimer(); self._apt_search_timer.setSingleShot(True)
        self._apt_search_timer.timeout.connect(self._do_filter_apt)

        # Conectar señales
        self.sig_metrics.connect(self._on_metrics)
        self.sig_procs.connect(self._on_procs)
        self.sig_parts.connect(self._on_parts)
        self.sig_apt.connect(self._on_apt)
        self.sig_flat.connect(self._on_flat)
        self.sig_svcs.connect(self._on_svcs)
        self.sig_sysinfo.connect(self._on_sysinfo)
        self.sig_toast.connect(self._show_toast)

        # Construir UI
        self._build_ui()

        # Arrancar hilos daemon
        threading.Thread(target=_temp_updater,     daemon=True).start()
        threading.Thread(target=self._hw_loop,     daemon=True).start()
        threading.Thread(target=self._procs_loop,  daemon=True).start()

        # Timer principal 1s — solo actualiza widgets con datos del cache
        self._tick_timer = QTimer()
        self._tick_timer.timeout.connect(self._tick)
        self._tick_timer.start(1000)

        # Carga inicial en hilos
        QTimer.singleShot(400, self._init_heavy)

    # ── Construcción UI ────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        lay = QVBoxLayout(central)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        self._tabs = QTabWidget()
        self._tabs.setDocumentMode(True)
        self._tabs.setIconSize(QSize(18, 18))
        lay.addWidget(self._tabs)

        # Íconos simbólicos Papirus-Dark (monocromáticos, integrados al tema)
        # Para cada pestaña: probar simbólico primero, luego color completo
        _tab_defs = [
            (self._tab_dashboard, 'Dashboard',
             ['computer-symbolic',              'computer',
              'video-display-symbolic',         'video-display']),
            (self._tab_monitor,   'Monitor',
             ['utilities-system-monitor-symbolic', 'utilities-system-monitor',
              'org.gnome.SystemMonitor-symbolic',  'system-search-symbolic']),
            (self._tab_gamer,     'Gamer',
             ['applications-games-symbolic',    'applications-games',
              'input-gaming-symbolic',          'input-gaming']),
            (self._tab_software,  'Software',
             ['system-software-install-symbolic','system-software-install',
              'package-install-symbolic',        'package-install']),
            (self._tab_inicio,    'Inicio',
             ['system-run-symbolic',            'system-run',
              'media-playback-start-symbolic',   'media-playback-start']),
            (self._tab_servicios, 'Servicios',
             ['preferences-system-symbolic',    'preferences-system',
              'applications-system-symbolic',   'applications-system']),
            (self._tab_controles, 'Controles',
             ['preferences-desktop-symbolic',   'preferences-desktop',
              'configure-symbolic',             'configure']),
        ]
        for build_fn, title, icon_names in _tab_defs:
            icon = QIcon()
            for name in icon_names:
                icon = QIcon.fromTheme(name)
                if not icon.isNull(): break
            self._tabs.addTab(build_fn(), icon, title)

        # Toast label (notificación inline)
        self._toast_lbl = QLabel('')
        self._toast_lbl.setStyleSheet(
            'background-color: #141720; color: #00ffa3; '
            'padding: 6px 16px; border-radius: 8px; '
            'font-size: 12px; font-weight: 600;')
        self._toast_lbl.setAlignment(Qt.AlignCenter)
        self._toast_lbl.hide()
        lay.addWidget(self._toast_lbl)
        self._toast_timer = QTimer()
        self._toast_timer.setSingleShot(True)
        self._toast_timer.timeout.connect(self._toast_lbl.hide)

    def _show_toast(self, msg):
        self._toast_lbl.setText(msg)
        self._toast_lbl.show()
        self._toast_timer.start(3000)

    # ── TAB 1: DASHBOARD ───────────────────────────────────
    def _tab_dashboard(self):
        root = QWidget()
        lay  = QVBoxLayout(root)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(10)

        # Header
        hdr = QHBoxLayout()
        hdr.addWidget(section_lbl('ESTADO DEL SISTEMA'))
        hdr.addStretch()
        btn_ram = neon_btn('Optimizar RAM', 'action')
        btn_cln = neon_btn('Limpieza', 'action')
        btn_ram.clicked.connect(self._do_optimize_ram)
        btn_cln.clicked.connect(self._do_clean)
        hdr.addWidget(btn_ram); hdr.addWidget(btn_cln)
        lay.addLayout(hdr)

        # Metric cards
        cards = QHBoxLayout(); cards.setSpacing(10)
        self._c_cpu  = MetricCard('CPU',   C_GREEN)
        self._c_ram  = MetricCard('RAM',   C_CYAN)
        self._c_disk = MetricCard('Disco', C_AMBER)
        self._c_temp = MetricCard('Temp',  C_RED)
        for c in (self._c_cpu, self._c_ram, self._c_disk, self._c_temp):
            cards.addWidget(c)
        lay.addLayout(cards)

        # Gráficos históricos
        graphs = QHBoxLayout(); graphs.setSpacing(10)
        for color, attr, label in (
            (C_GREEN,  '_g_cpu', 'CPU'),
            (C_CYAN,   '_g_ram', 'RAM'),
            (C_PURPLE, '_g_net', 'Red KB/s'),
        ):
            g = HistoryGraph(color, label)
            setattr(self, attr, g)
            f = QFrame()
            f.setStyleSheet('QFrame { background-color: #141720; '
                           'border-radius: 12px; '
                           'border: 1px solid rgba(255,255,255,0.06); }')
            fl = QVBoxLayout(f); fl.setContentsMargins(10,8,10,8)
            fl.addWidget(g)
            graphs.addWidget(f)
        lay.addLayout(graphs)

        # Particiones
        part_frame = QFrame()
        part_frame.setStyleSheet(
            'QFrame { background-color: #141720; border-radius: 12px; '
            'border: 1px solid rgba(255,255,255,0.06); }')
        part_lay = QVBoxLayout(part_frame)
        part_lay.setContentsMargins(14, 10, 14, 10)
        part_lay.setSpacing(8)
        part_lay.addWidget(section_lbl('PARTICIONES'))
        self._parts_lay = QVBoxLayout()
        self._parts_lay.setSpacing(6)
        part_lay.addLayout(self._parts_lay)
        lay.addWidget(part_frame)

        # Especificaciones
        spec_frame = QFrame()
        spec_frame.setStyleSheet(
            'QFrame { background-color: #141720; border-radius: 12px; '
            'border: 1px solid rgba(255,255,255,0.06); }')
        spec_lay = QVBoxLayout(spec_frame)
        spec_lay.setContentsMargins(14, 10, 14, 10)
        spec_lay.addWidget(section_lbl('ESPECIFICACIONES DEL SISTEMA'))
        self._info_lbl = mono_lbl('Cargando...')
        self._info_lbl.setWordWrap(True)
        spec_lay.addWidget(self._info_lbl)
        self._ip_lbl = unit_lbl('—', '#00cfff')
        spec_lay.addWidget(self._ip_lbl)
        lay.addWidget(spec_frame)

        return root

    # ── TAB 2: MONITOR ─────────────────────────────────────
    def _tab_monitor(self):
        root = QWidget()
        lay  = QVBoxLayout(root)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(10)
        lay.addWidget(section_lbl('MONITOR DETALLADO'))

        # Temp + Net
        row = QHBoxLayout(); row.setSpacing(10)

        tc = QFrame()
        tc.setStyleSheet('QFrame { background-color: #141720; '
                        'border-radius: 12px; '
                        'border: 1px solid rgba(255,255,255,0.06); }')
        tl = QVBoxLayout(tc); tl.setContentsMargins(12,10,12,10); tl.setSpacing(6)
        tl.addWidget(unit_lbl('TEMPERATURA'))
        self._temp_lbl = mono_lbl('—')
        tl.addWidget(self._temp_lbl)
        self._g_temp = HistoryGraph(C_RED,'TEMP °C',height=65)
        tl.addWidget(self._g_temp)
        row.addWidget(tc)

        nc = QFrame()
        nc.setStyleSheet('QFrame { background-color: #141720; '
                        'border-radius: 12px; '
                        'border: 1px solid rgba(255,255,255,0.06); }')
        nl = QVBoxLayout(nc); nl.setContentsMargins(12,10,12,10); nl.setSpacing(6)
        nl.addWidget(unit_lbl('RED'))
        self._net_lbl = mono_lbl('—')
        nl.addWidget(self._net_lbl)
        self._g_net_m = HistoryGraph(C_PURPLE,'KB/s',height=65)
        nl.addWidget(self._g_net_m)
        row.addWidget(nc)
        lay.addLayout(row)

        lay.addWidget(section_lbl('PROCESOS'))
        self._proc_list = QListWidget()
        self._proc_list.setFont(QFont('monospace', 11))
        lay.addWidget(self._proc_list)

        return root

    # ── TAB 3: GAMER ───────────────────────────────────────
    def _tab_gamer(self):
        root = QWidget()
        lay  = QVBoxLayout(root)
        lay.setContentsMargins(40, 20, 40, 20)
        lay.setSpacing(12)

        title = QLabel('OPTIMIZACIÓN DE RENDIMIENTO')
        title.setStyleSheet(
            'font-size: 18px; font-weight: 900; color: #00ffa3;')
        lay.addWidget(title)
        lay.addWidget(unit_lbl('Seleccioná un perfil de energía.'))

        self._gamer_btns = {}
        for key, lbl_txt, desc in [
            ('power-saver','MODO AHORRO',
             'Reduce frecuencia del CPU. Ideal para batería y silencio.'),
            ('balanced','MODO BALANCEADO',
             'Equilibrio inteligente entre temperatura y velocidad.'),
            ('performance','MODO GAMER',
             'Desbloquea límites de energía para máxima performance.'),
        ]:
            btn = QPushButton(f'{lbl_txt}\n{desc}')
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #141720;
                    color: rgba(255,255,255,0.80);
                    border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 12px;
                    padding: 16px 20px;
                    text-align: left;
                    font-size: 13px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #1c1f2a;
                    border-color: rgba(255,255,255,0.15);
                }
                QPushButton[active="true"] {
                    background-color: rgba(0,255,163,0.12);
                    color: #00ffa3;
                    border-color: rgba(0,255,163,0.40);
                }
            """)
            btn.setMinimumHeight(70)
            btn.clicked.connect(lambda _, k=key: self._on_profile(k))
            self._gamer_btns[key] = btn
            lay.addWidget(btn)

        self._ppd_warn = QLabel('')
        self._ppd_warn.setStyleSheet('color: #fbbf24; font-size: 11px;')
        self._ppd_warn.setWordWrap(True)
        self._ppd_warn.hide()
        lay.addWidget(self._ppd_warn)

        tip = QFrame()
        tip.setStyleSheet('QFrame { background-color: #141720; '
                         'border-radius: 10px; '
                         'border: 1px solid rgba(255,255,255,0.05); }')
        tl = QVBoxLayout(tip); tl.setContentsMargins(14,10,14,10)
        tl.addWidget(unit_lbl('TIPS'))
        tl.addWidget(mono_lbl(
            '• Modo Gamer: enchufado a la corriente.\n'
            '• Balanceado: si los ventiladores hacen ruido.\n'
            '• Ahorro: para navegar sin calentar.'))
        lay.addWidget(tip)
        lay.addStretch()

        QTimer.singleShot(300, self._load_perfil)
        return root

    def _on_profile(self, key):
        for k, b in self._gamer_btns.items():
            b.setProperty('active', k == key)
            b.style().unpolish(b); b.style().polish(b)
        try:
            open(PERFIL_F,'w').write(key)
        except Exception:
            pass
        if not hw_cmd('which','powerprofilesctl'):
            self._ppd_warn.setText(
                '⚠ power-profiles-daemon no instalado.\n'
                '  sudo apt install power-profiles-daemon')
            self._ppd_warn.show()
            self.sig_toast.emit('⚠ power-profiles-daemon no instalado')
            return
        self._ppd_warn.hide()
        run_bg(lambda: hw_cmd('powerprofilesctl','set',key))
        self.sig_toast.emit(f'Perfil activado: {key}')

    def _load_perfil(self):
        key = 'balanced'
        if os.path.exists(PERFIL_F):
            key = open(PERFIL_F).read().strip()
        if key in self._gamer_btns:
            self._gamer_btns[key].setProperty('active','true')
            b = self._gamer_btns[key]
            b.style().unpolish(b); b.style().polish(b)
        if not hw_cmd('which','powerprofilesctl'):
            self._ppd_warn.setText(
                '⚠ power-profiles-daemon no instalado.\n'
                '  sudo apt install power-profiles-daemon')
            self._ppd_warn.show()

    # ── TAB 4: SOFTWARE ────────────────────────────────────
    def _tab_software(self):
        root = QWidget()
        lay  = QVBoxLayout(root)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(8)

        # Switcher APT / Flatpak
        sw = QHBoxLayout()
        self._btn_apt  = QPushButton('📦  APT')
        self._btn_flat = QPushButton('📱  Flatpak')
        for b in (self._btn_apt, self._btn_flat):
            b.setCheckable(True)
            b.setStyleSheet("""
                QPushButton { border-radius: 8px; padding: 6px 20px;
                              font-weight: 700; font-size: 12px; }
                QPushButton:checked {
                    background-color: rgba(0,255,163,0.14);
                    color: #00ffa3;
                    border: 1px solid rgba(0,255,163,0.35); }
                QPushButton:!checked {
                    background-color: #141720;
                    color: rgba(255,255,255,0.50);
                    border: 1px solid rgba(255,255,255,0.08); }
            """)
        self._btn_apt.setChecked(True)
        self._btn_apt.clicked.connect(lambda: self._sw_toggle('apt'))
        self._btn_flat.clicked.connect(lambda: self._sw_toggle('flat'))
        sw.addStretch(); sw.addWidget(self._btn_apt)
        sw.addWidget(self._btn_flat); sw.addStretch()
        lay.addLayout(sw)

        self._sw_stack = QStackedWidget()
        self._sw_stack.addWidget(self._apt_panel())
        self._sw_stack.addWidget(self._flat_panel())
        lay.addWidget(self._sw_stack)
        return root

    def _sw_toggle(self, which):
        is_apt = which == 'apt'
        self._btn_apt.setChecked(is_apt)
        self._btn_flat.setChecked(not is_apt)
        self._sw_stack.setCurrentIndex(0 if is_apt else 1)

    def _apt_panel(self):
        root = QWidget()
        lay  = QHBoxLayout(root); lay.setSpacing(10)

        left = QWidget(); ll = QVBoxLayout(left); ll.setSpacing(6)
        hdr  = QHBoxLayout()
        hdr.addWidget(section_lbl('PAQUETES APT'))
        hdr.addStretch()
        self._apt_cnt = unit_lbl('')
        hdr.addWidget(self._apt_cnt); ll.addLayout(hdr)

        self._apt_search = QLineEdit()
        self._apt_search.setPlaceholderText('Buscar por nombre o descripción...')
        self._apt_search.textChanged.connect(
            lambda: self._apt_search_timer.start(250))
        ll.addWidget(self._apt_search)

        br = QHBoxLayout(); br.setSpacing(8)
        bi = neon_btn('Instalar','install')
        bi.clicked.connect(self._apt_install_dlg)
        bu = neon_btn('Desinstalar','stop')
        bu.clicked.connect(self._apt_uninstall)
        bref = QPushButton('↺')
        bref.setToolTip('Actualizar lista')
        bref.clicked.connect(lambda: run_bg(self._load_apt))
        br.addWidget(bi); br.addWidget(bu)
        br.addStretch(); br.addWidget(bref)
        ll.addLayout(br)

        self._apt_list = QListWidget()
        ll.addWidget(self._apt_list)
        self._apt_list.itemSelectionChanged.connect(self._apt_selected)
        lay.addWidget(left, 3)

        # Detalle
        right = QFrame()
        right.setStyleSheet(
            'QFrame { background-color: #0d1018; border-radius: 12px; '
            'border: 1px solid rgba(255,255,255,0.08); }')
        right.setFixedWidth(260)
        rl = QVBoxLayout(right); rl.setContentsMargins(14,14,14,14); rl.setSpacing(8)
        rl.addWidget(section_lbl('DETALLE'))
        self._apt_name = QLabel('—'); self._apt_name.setStyleSheet('color:#00ffa3; font-weight:700;')
        self._apt_ver  = unit_lbl('Versión: —')
        self._apt_sz   = unit_lbl('Tamaño: —')
        self._apt_arch = unit_lbl('Arch: —')
        self._apt_sec  = unit_lbl('Sección: —')
        self._apt_desc = QLabel('—')
        self._apt_desc.setWordWrap(True)
        self._apt_desc.setStyleSheet('color: rgba(255,255,255,0.45); font-size:11px;')
        for w in (self._apt_name, self._apt_ver, self._apt_sz,
                  self._apt_arch, self._apt_sec,
                  QLabel('—————'), self._apt_desc):
            rl.addWidget(w)
        rl.addStretch()
        bcp = QPushButton('📋 Copiar nombre')
        bcp.clicked.connect(self._apt_copy)
        rl.addWidget(bcp)
        lay.addWidget(right, 0)
        return root

    def _flat_panel(self):
        root = QWidget()
        lay  = QHBoxLayout(root); lay.setSpacing(10)

        left = QWidget(); ll = QVBoxLayout(left); ll.setSpacing(6)
        hdr  = QHBoxLayout()
        hdr.addWidget(section_lbl('APPS FLATPAK'))
        hdr.addStretch()
        self._flat_cnt = unit_lbl('')
        hdr.addWidget(self._flat_cnt); ll.addLayout(hdr)

        self._flat_search = QLineEdit()
        self._flat_search.setPlaceholderText('Buscar app Flatpak...')
        self._flat_search.textChanged.connect(self._filter_flat)
        ll.addWidget(self._flat_search)

        br = QHBoxLayout(); br.setSpacing(8)
        bu = neon_btn('Desinstalar','stop')
        bu.clicked.connect(self._flat_uninstall)
        bref = QPushButton('↺')
        bref.clicked.connect(lambda: run_bg(self._load_flat))
        br.addWidget(bu); br.addStretch(); br.addWidget(bref)
        ll.addLayout(br)

        self._flat_warn = QLabel('')
        self._flat_warn.setStyleSheet('color: #fbbf24; font-size: 11px;')
        ll.addWidget(self._flat_warn)

        self._flat_list = QListWidget()
        ll.addWidget(self._flat_list)
        self._flat_list.itemSelectionChanged.connect(self._flat_selected)
        lay.addWidget(left, 3)

        right = QFrame()
        right.setStyleSheet(
            'QFrame { background-color: #0d1018; border-radius: 12px; '
            'border: 1px solid rgba(255,255,255,0.08); }')
        right.setFixedWidth(260)
        rl = QVBoxLayout(right); rl.setContentsMargins(14,14,14,14); rl.setSpacing(8)
        rl.addWidget(section_lbl('DETALLE'))
        self._flat_name = QLabel('—'); self._flat_name.setStyleSheet('color:#00cfff; font-weight:700;')
        self._flat_id   = unit_lbl('ID: —')
        self._flat_ver  = unit_lbl('Versión: —')
        self._flat_sz   = unit_lbl('Tamaño: —')
        self._flat_orig = unit_lbl('Origen: —')
        for w in (self._flat_name, self._flat_id, self._flat_ver,
                  self._flat_sz, self._flat_orig):
            rl.addWidget(w)
        rl.addStretch()
        bcp = QPushButton('📋 Copiar App ID')
        bcp.clicked.connect(self._flat_copy)
        rl.addWidget(bcp)
        lay.addWidget(right, 0)
        return root

    # ── TAB 5: INICIO ──────────────────────────────────────
    def _tab_inicio(self):
        root = QWidget()
        lay  = QVBoxLayout(root)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(10)

        hdr = QHBoxLayout()
        hdr.addWidget(section_lbl('GESTIÓN DE AUTOSTART'))
        hdr.addStretch()
        brel = QPushButton('↺ Recargar')
        brel.clicked.connect(self._load_autostart)
        hdr.addWidget(brel); lay.addLayout(hdr)

        self._as_area = QScrollArea()
        self._as_area.setWidgetResizable(True)
        self._as_content = QWidget()
        self._as_lay = QVBoxLayout(self._as_content)
        self._as_lay.setSpacing(6); self._as_lay.addStretch()
        self._as_area.setWidget(self._as_content)
        lay.addWidget(self._as_area)

        QTimer.singleShot(400, self._load_autostart)
        return root

    # ── TAB 6: SERVICIOS ───────────────────────────────────
    def _tab_servicios(self):
        root = QWidget()
        lay  = QVBoxLayout(root)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(8)

        hdr = QHBoxLayout()
        hdr.addWidget(section_lbl('SERVICIOS SYSTEMD'))
        hdr.addStretch()
        self._svc_search = QLineEdit()
        self._svc_search.setPlaceholderText('Filtrar servicios...')
        self._svc_search.setFixedWidth(220)
        self._svc_search.textChanged.connect(self._filter_svcs)
        hdr.addWidget(self._svc_search)
        brel = QPushButton('↺ Recargar')
        brel.clicked.connect(lambda: run_bg(self._load_svcs))
        hdr.addWidget(brel); lay.addLayout(hdr)

        leg = QHBoxLayout()
        for dot,txt in (('🟢','Activo'),('⚫','Inactivo'),('🔴','Fallido')):
            leg.addWidget(unit_lbl(f'{dot} {txt}'))
        leg.addStretch(); lay.addLayout(leg)

        self._svc_area = QScrollArea()
        self._svc_area.setWidgetResizable(True)
        self._svc_content = QWidget()
        self._svc_lay = QVBoxLayout(self._svc_content)
        self._svc_lay.setSpacing(4); self._svc_lay.addStretch()
        self._svc_area.setWidget(self._svc_content)
        lay.addWidget(self._svc_area)
        return root

    # ── TAB 7: CONTROLES ───────────────────────────────────
    def _tab_controles(self):
        root = QWidget()
        lay  = QVBoxLayout(root)
        lay.setContentsMargins(24, 14, 24, 14)
        lay.setSpacing(12)
        lay.addWidget(section_lbl('CONTROLES DEL SISTEMA'))

        # Autostart
        as_f = self._ctrl_frame()
        al   = QHBoxLayout(as_f); al.setContentsMargins(16,12,16,12)
        ac   = QVBoxLayout()
        ac.addWidget(QLabel('INICIAR CON EL SISTEMA'))
        ac.addWidget(unit_lbl('Agrega OpenDash al autostart de tu sesión.'))
        al.addLayout(ac); al.addStretch()
        from PyQt5.QtWidgets import QCheckBox
        self._as_chk = QCheckBox()
        self._as_chk.setChecked(os.path.exists(AUTOSTART_F))
        self._as_chk.toggled.connect(self._on_autostart)
        self._as_chk.setStyleSheet(TOGGLE_SWITCH_QSS)
        al.addWidget(self._as_chk)
        lay.addWidget(as_f)

        # Brillo
        br_f = self._ctrl_frame()
        bl   = QVBoxLayout(br_f); bl.setContentsMargins(16,12,16,12); bl.setSpacing(8)
        bh   = QHBoxLayout()
        bh.addWidget(QLabel('BRILLO DE PANTALLA'))
        bh.addStretch()
        self._br_val = QLabel('—'); self._br_val.setStyleSheet('color:#fbbf24;')
        bh.addWidget(self._br_val); bl.addLayout(bh)
        dev = _backlight_dev()
        meth = ('backlight físico' if dev
                else 'brightnessctl' if hw_cmd('which','brightnessctl')
                else 'xrandr')
        bl.addWidget(unit_lbl(f'Método: {meth}'))
        self._br_sl = QSlider(Qt.Horizontal)
        self._br_sl.setRange(1, 100)
        run_bg(lambda: (self._br_sl.setValue(int(hw_get_brightness())),
                        self._br_val.setText(f'{int(hw_get_brightness())}%')))
        self._br_sl.valueChanged.connect(self._on_br)
        bl.addWidget(self._br_sl)
        lay.addWidget(br_f)

        # Volumen
        vf  = self._ctrl_frame()
        vl  = QVBoxLayout(vf); vl.setContentsMargins(16,12,16,12); vl.setSpacing(8)
        vh  = QHBoxLayout()
        vh.addWidget(QLabel('VOLUMEN DEL SISTEMA'))
        vh.addStretch()
        self._vol_val = QLabel('—'); self._vol_val.setStyleSheet('color:#00cfff;')
        vh.addWidget(self._vol_val); vl.addLayout(vh)
        self._vol_sl = QSlider(Qt.Horizontal)
        self._vol_sl.setRange(0, 100)
        vol = hw_get_volume()
        self._vol_sl.setValue(vol); self._vol_val.setText(f'{vol}%')
        self._vol_sl.valueChanged.connect(self._on_vol)
        vl.addWidget(self._vol_sl)
        lay.addWidget(vf)

        # TRIM SSD
        tf  = self._ctrl_frame()
        tl  = QHBoxLayout(tf); tl.setContentsMargins(16,12,16,12)
        tc  = QVBoxLayout()
        tc.addWidget(QLabel('TRIM SSD'))
        tc.addWidget(unit_lbl('Ejecuta fstrim -av para optimizar SSDs montados.'))
        tl.addLayout(tc); tl.addStretch()
        bt = neon_btn('Ejecutar TRIM','start')
        bt.clicked.connect(self._do_trim)
        tl.addWidget(bt)
        lay.addWidget(tf)

        # Tema
        thf = self._ctrl_frame()
        thl = QHBoxLayout(thf); thl.setContentsMargins(16,12,16,12)
        thl.addWidget(QLabel('TEMA DE INTERFAZ')); thl.addStretch()
        self._theme_lbl = QLabel('Oscuro')
        self._theme_lbl.setStyleSheet('color:#00ffa3;')
        thl.addWidget(self._theme_lbl)
        self._theme_chk = QCheckBox()
        self._theme_chk.setChecked(True)
        self._theme_chk.toggled.connect(self._on_theme)
        self._theme_chk.setStyleSheet(TOGGLE_SWITCH_QSS)
        thl.addWidget(self._theme_chk)
        lay.addWidget(thf)
        lay.addStretch()
        return root

    def _ctrl_frame(self):
        f = QFrame()
        f.setStyleSheet('QFrame { background-color: #141720; '
                       'border-radius: 12px; '
                       'border: 1px solid rgba(255,255,255,0.06); }')
        return f

    # ── MANEJADORES DE EVENTOS ─────────────────────────────
    def _on_autostart(self, checked):
        if checked:
            try:
                os.makedirs(os.path.dirname(AUTOSTART_F), exist_ok=True)
                open(AUTOSTART_F,'w').write(
                    '[Desktop Entry]\nType=Application\n'
                    f'Name={APP_NAME}\nExec={BINARY}\n'
                    'Hidden=false\nNoDisplay=false\n'
                    'X-GNOME-Autostart-enabled=true\n')
                self.sig_toast.emit(f'{APP_NAME} agregado al inicio')
            except Exception as e:
                self.sig_toast.emit(f'Error: {e}')
        else:
            try:
                os.remove(AUTOSTART_F)
                self.sig_toast.emit(f'{APP_NAME} removido del inicio')
            except FileNotFoundError:
                pass

    def _on_br(self, v):
        self._br_val.setText(f'{v}%')
        self._br_pend = v
        self._br_timer.start(250)

    def _apply_br(self):
        if self._br_pend is not None:
            run_bg(hw_set_brightness, self._br_pend)

    def _on_vol(self, v):
        self._vol_val.setText(f'{v}%')
        self._vol_pend = v
        self._vol_timer.start(150)

    def _apply_vol(self):
        if self._vol_pend is not None:
            run_bg(hw_set_volume, self._vol_pend)

    def _on_theme(self, dark):
        self._dark = dark
        self._theme_lbl.setText('Oscuro' if dark else 'Claro')
        app = QApplication.instance()
        if dark:
            app.setStyleSheet(QSS)
        else:
            app.setStyleSheet('')

    # ── APT handlers ───────────────────────────────────────
    def _do_filter_apt(self):
        q = self._apt_search.text().lower()
        self._apt_list.clear()
        shown = total = 0
        for pkg in self._all_apt:
            if q and q not in pkg['name'].lower() and q not in pkg['desc'].lower():
                continue
            total += 1
            if shown >= 200: continue
            shown += 1
            item = QListWidgetItem(f"{pkg['name']}  —  {pkg['desc'][:50]}  [{pkg['size']}]")
            item.setData(Qt.UserRole, pkg['name'])
            self._apt_list.addItem(item)
        suf = f' (+{total-shown} más)' if total > shown else ''
        self._apt_cnt.setText(f'{total} paquetes{suf}')

    def _filter_flat(self):
        q = self._flat_search.text().lower()
        self._flat_list.clear()
        total = 0
        for pkg in self._all_flat:
            if q and q not in pkg['name'].lower() and q not in pkg['id'].lower():
                continue
            total += 1
            item = QListWidgetItem(f"{pkg['name']}  [{pkg['id']}]  {pkg['size']}")
            item.setData(Qt.UserRole, pkg['id'])
            self._flat_list.addItem(item)
        self._flat_cnt.setText(f'{total} apps Flatpak')

    def _apt_selected(self):
        items = self._apt_list.selectedItems()
        if not items: return
        name = items[0].data(Qt.UserRole)
        pkg  = next((p for p in self._all_apt if p['name']==name), None)
        if pkg:
            self._apt_name.setText(pkg['name'])
            self._apt_ver.setText(f"Versión:  {pkg['ver']}")
            self._apt_sz.setText(f"Tamaño:  {pkg['size']}")
            self._apt_arch.setText(f"Arch:       {pkg['arch']}")
            self._apt_sec.setText(f"Sección:  {pkg['sec']}")
            self._apt_desc.setText(pkg['desc'] or '—')

    def _apt_copy(self):
        items = self._apt_list.selectedItems()
        if not items: self.sig_toast.emit('Seleccioná un paquete'); return
        name = items[0].data(Qt.UserRole)
        QApplication.clipboard().setText(name)
        self.sig_toast.emit(f'Copiado: {name}')

    def _apt_uninstall(self):
        items = self._apt_list.selectedItems()
        if not items: self.sig_toast.emit('Seleccioná un paquete'); return
        name = items[0].data(Qt.UserRole)
        r = QMessageBox.question(self,'Desinstalar',
            f'¿Eliminar «{name}»?\nEsta acción no es fácilmente reversible.',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if r == QMessageBox.Yes:
            def _l():
                self._launch_terminal(
                    f'#!/bin/bash\napt purge -y {name} && apt autoremove -y\n'
                    f'echo\nread -p "Listo. Presione Enter..."', need_root=True)
                self.sig_toast.emit(f'Desinstalando {name}...')
                time.sleep(10)
                run_bg(self._load_apt)
            run_bg(_l)

    def _apt_install_dlg(self):
        dlg = QDialog(self)
        dlg.setWindowTitle('Instalar paquete APT')
        lay = QVBoxLayout(dlg)
        lay.addWidget(QLabel('Nombre del paquete:'))
        entry = QLineEdit(); entry.setPlaceholderText('ej: htop, vlc...')
        lay.addWidget(entry)
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        lay.addWidget(btns)
        if dlg.exec_() == QDialog.Accepted:
            name = entry.text().strip()
            if name:
                def _l():
                    self._launch_terminal(
                        f'#!/bin/bash\napt install -y {name}\n'
                        f'echo\nread -p "Listo. Presione Enter..."', need_root=True)
                    self.sig_toast.emit(f'Instalando {name}...')
                    time.sleep(12)
                    run_bg(self._load_apt)
                run_bg(_l)

    def _flat_selected(self):
        items = self._flat_list.selectedItems()
        if not items: return
        aid = items[0].data(Qt.UserRole)
        pkg = next((p for p in self._all_flat if p['id']==aid), None)
        if pkg:
            self._flat_name.setText(pkg['name'])
            self._flat_id.setText(f"App ID:   {pkg['id']}")
            self._flat_ver.setText(f"Versión:  {pkg['ver']}")
            self._flat_sz.setText(f"Tamaño:  {pkg['size']}")
            self._flat_orig.setText(f"Origen:   {pkg['origin']}")

    def _flat_copy(self):
        items = self._flat_list.selectedItems()
        if not items: self.sig_toast.emit('Seleccioná una app'); return
        QApplication.clipboard().setText(items[0].data(Qt.UserRole))
        self.sig_toast.emit(f'Copiado: {items[0].data(Qt.UserRole)}')

    def _flat_uninstall(self):
        items = self._flat_list.selectedItems()
        if not items: self.sig_toast.emit('Seleccioná una app'); return
        aid = items[0].data(Qt.UserRole)
        r = QMessageBox.question(self,'Desinstalar Flatpak',
            f'¿Eliminar «{aid}»?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if r == QMessageBox.Yes:
            def _l():
                self._launch_terminal(
                    f'#!/bin/bash\nflatpak uninstall -y {aid}\n'
                    f'echo\nread -p "Listo. Presione Enter..."', need_root=False)
                self.sig_toast.emit(f'Desinstalando {aid}...')
                time.sleep(8)
                run_bg(self._load_flat)
            run_bg(_l)

    # ── Servicios handlers ─────────────────────────────────
    def _filter_svcs(self):
        self._on_svcs(self._services)

    def _svc_action(self, name, action):
        def _run():
            try:
                subprocess.run(
                    ['pkexec','systemctl',action,f'{name}.service'],
                    capture_output=True, timeout=12)
                self.sig_toast.emit(f'{action.capitalize()}: {name}')
                run_bg(self._load_svcs)
            except Exception as e:
                self.sig_toast.emit(f'Error: {e}')
        run_bg(_run)

    # ── Autostart ──────────────────────────────────────────
    def _load_autostart(self):
        # Limpiar
        while self._as_lay.count() > 1:
            item = self._as_lay.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        path = os.path.expanduser('~/.config/autostart')
        if not os.path.exists(path):
            self._as_lay.insertWidget(0, unit_lbl('No hay apps de autostart.'))
            return

        idx = 0
        for archivo in sorted(os.listdir(path)):
            if not archivo.endswith(('.desktop','.disabled')): continue
            activo = archivo.endswith('.desktop')
            nombre = archivo.replace('.desktop','').replace('.disabled','').capitalize()

            row = QFrame()
            row.setStyleSheet('QFrame { background-color: #141720; '
                             'border-radius: 10px; '
                             'border: 1px solid rgba(255,255,255,0.05); }')
            rl = QHBoxLayout(row); rl.setContentsMargins(12,8,12,8)
            # Ícono del tema en vez de emoji (más consistente en Qt5)
            ic_lbl = QLabel()
            ic_name = 'media-playback-start' if activo else 'media-playback-pause'
            ic = QIcon.fromTheme(ic_name)
            if not ic.isNull():
                ic_lbl.setPixmap(ic.pixmap(QSize(16,16)))
            else:
                dot = QLabel('●')
                dot.setStyleSheet(f"color: {'#00ffa3' if activo else 'rgba(255,255,255,0.35)'}; font-size: 10px;")
                rl.addWidget(dot)
            if not ic.isNull():
                rl.addWidget(ic_lbl)
            rl.addWidget(QLabel(nombre)); rl.addStretch()
            btn = neon_btn('Desactivar' if activo else 'Activar',
                          'stop' if activo else 'start')
            btn.clicked.connect(lambda _, a=archivo: self._toggle_as(a))
            rl.addWidget(btn)
            self._as_lay.insertWidget(idx, row)
            idx += 1

    def _toggle_as(self, archivo):
        path = os.path.expanduser('~/.config/autostart')
        old  = os.path.join(path, archivo)
        new  = (old.replace('.desktop','.disabled')
                if archivo.endswith('.desktop')
                else old.replace('.disabled','.desktop'))
        try:
            os.rename(old, new); self._load_autostart()
        except Exception as e:
            self.sig_toast.emit(f'Error: {e}')

    # ── Acciones del sistema ───────────────────────────────
    def _launch_terminal(self, script, need_root=True):
        """Lanza terminal y baja la ventana principal para que quede al frente."""
        def _do():
            _run_in_terminal(script, need_root)
        run_bg(_do)
        # Bajar la ventana 600ms después para que la terminal aparezca al frente
        QTimer.singleShot(600, self.lower)

    def _do_clean(self):
        usuario = os.environ.get('USER','user')
        self._launch_terminal(
            '#!/bin/bash\n'
            "echo '=== Argent Opendash - Limpieza ==='\n"
            "echo '>> Cache de RAM...'\n"
            'sync\necho 3 > /proc/sys/vm/drop_caches\n'
            "echo '>> Papelera...'\n"
            f'rm -rf /home/{usuario}/.local/share/Trash/files/* 2>/dev/null || true\n'
            f'rm -rf /home/{usuario}/.local/share/Trash/info/*  2>/dev/null || true\n'
            "echo '>> Cache de APT...'\napt clean\n"
            "echo\necho '=== Limpieza completada ==='\n"
            "read -p 'Presione Enter...'", need_root=True)
        self.sig_toast.emit('Limpieza iniciada...')

    def _do_optimize_ram(self):
        def _run():
            try:
                r = subprocess.run(
                    ['pkexec','sh','-c','sync; echo 3 > /proc/sys/vm/drop_caches'],
                    capture_output=True, timeout=15)
                self.sig_toast.emit(
                    '¡RAM optimizada!' if r.returncode==0 else 'No se pudo optimizar')
            except Exception as e:
                self.sig_toast.emit(f'Error: {e}')
        run_bg(_run)

    def _do_trim(self):
        self._launch_terminal(
            '#!/bin/bash\necho "=== TRIM SSD ==="\n'
            'fstrim -av\necho\nread -p "Listo. Presione Enter..."',
            need_root=True)
        self.sig_toast.emit('TRIM iniciado...')

    # ── HILOS DE DATOS ─────────────────────────────────────
    def _hw_loop(self):
        """Solo llamadas psutil rápidas. Temperatura desde caché sysfs."""
        prev_io = None
        try: prev_io = psutil.net_io_counters()
        except Exception: pass

        while True:
            try:
                cpu  = psutil.cpu_percent(interval=None)
                mem  = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                io   = psutil.net_io_counters()
                try: addrs = psutil.net_if_addrs()
                except Exception: addrs = {}

                diff = 0.0
                if io and prev_io:
                    diff = ((io.bytes_recv+io.bytes_sent) -
                            (prev_io.bytes_recv+prev_io.bytes_sent)) / 1024
                if io: prev_io = io

                ifaces = {}
                for name, ads in (addrs or {}).items():
                    if name == 'lo': continue
                    for a in ads:
                        if a.family == 2: ifaces[name] = a.address; break

                self.sig_metrics.emit({
                    'cpu':      cpu or 0,
                    'ram_used': mem.used/(1024**3) if mem else 0,
                    'ram_pct':  mem.percent if mem else 0,
                    'disk_free':disk.free/(1024**3) if disk else 0,
                    'disk_pct': disk.percent if disk else 0,
                    'temp':     hw_temp(),
                    'net_diff': max(0, diff),
                    'net_recv': io.bytes_recv/(1024**3) if io else 0,
                    'net_sent': io.bytes_sent/(1024**3) if io else 0,
                    'ifaces':   ifaces,
                })
            except Exception:
                pass
            time.sleep(1)

    def _procs_loop(self):
        while True:
            try:
                self.sig_procs.emit(hw_procs_top())
            except Exception:
                pass
            time.sleep(3)

    def _init_heavy(self):
        run_bg(self._load_sysinfo)
        run_bg(self._load_apt)
        run_bg(self._load_flat)
        run_bg(self._load_svcs)
        run_bg(self._load_parts)
        # Recargar particiones cada 30s
        QTimer.singleShot(30000, lambda: run_bg(self._load_parts))

    def _load_sysinfo(self):
        try:
            u    = platform.uname()
            cpu  = ''
            try:
                for line in open('/proc/cpuinfo'):
                    if 'model name' in line:
                        cpu = line.split(':')[1].strip()[:44]; break
            except Exception:
                cpu = platform.processor()[:44] or 'N/A'
            pkgs = hw_cmd('sh','-c','dpkg -l | wc -l',timeout=3)
            gpu  = hw_cmd('sh','-c',
                          r"lspci | grep -E 'VGA|3D' | cut -d: -f3 | head -1",
                          timeout=3)[:42] or 'N/A'
            mem  = psutil.virtual_memory()
            ram  = f'{mem.total/(1024**3):.1f} GB'
            try:
                s  = float(open('/proc/uptime').read().split()[0])
                up = f"{int(s//3600)}h {int((s%3600)//60)}m"
            except Exception: up='N/A'
            text = (f' OS:       ArgOs Platinum Edition\n'
                    f' HOST:     {u.node}\n'
                    f' KERNEL:   {u.release}\n'
                    f' CPU:      {cpu}\n'
                    f' GPU:      {gpu}\n'
                    f' RAM:      {ram} total\n'
                    f' PAQUETES: {pkgs} (dpkg)\n'
                    f' UPTIME:   {up}')
            self.sig_sysinfo.emit(text)
        except Exception:
            pass

    def _load_parts(self):
        parts = hw_partitions()
        if parts: self.sig_parts.emit(parts)

    def _load_apt(self):
        try:
            out = hw_cmd('sh','-c',
                "dpkg-query -W -f='${Package}\\t${Version}\\t"
                "${Installed-Size}\\t${Architecture}\\t"
                "${Section}\\t${binary:Summary}\\n'", timeout=20)
            apps = []
            for line in out.split('\n'):
                if not line.strip(): continue
                parts = line.split('\t')
                if len(parts) < 6: continue
                name,ver,sk,arch,sec,desc = parts[:6]
                if not name.strip(): continue
                try:
                    k = int(sk.strip())
                    ss = f'{k//1024} MB' if k>=1024 else f'{k} KB'
                except Exception: ss='—'
                apps.append({'name':name.strip(),'ver':ver.strip(),
                             'size':ss,'arch':arch.strip(),
                             'sec':sec.strip() or '—','desc':desc.strip()})
            apps.sort(key=lambda x: x['name'])
            self.sig_apt.emit(apps)
        except Exception:
            pass

    def _load_flat(self):
        if not hw_cmd('which','flatpak'):
            self.sig_toast.emit('Flatpak no instalado en este sistema')
            return
        apps = []
        for cols in ('name,application,version,size,origin',
                     'name,app,version,branch,origin'):
            out = hw_cmd('sh','-c',f'flatpak list --app --columns={cols}',timeout=15)
            if out and '\t' in out:
                for line in out.split('\n'):
                    if not line.strip(): continue
                    p = line.split('\t')
                    if len(p) < 2: continue
                    aid = p[1].strip()
                    if '.' in aid:
                        apps.append({'name':p[0].strip() or aid,'id':aid,
                                     'ver': p[2].strip() if len(p)>2 else '—',
                                     'size':p[3].strip() if len(p)>3 else '—',
                                     'origin':p[4].strip() if len(p)>4 else '—'})
                if apps: break
        apps.sort(key=lambda x: x['name'].lower())
        self.sig_flat.emit(apps)

    def _load_svcs(self):
        try:
            out = hw_cmd('systemctl','list-units','--type=service',
                         '--all','--no-pager','--plain','--no-legend',timeout=10)
            svcs = []
            for line in out.strip().split('\n'):
                p = line.split(None,4)
                if len(p) >= 4:
                    svcs.append((p[0].replace('.service',''),p[2],p[3],
                                 p[4] if len(p)>4 else ''))
            self.sig_svcs.emit(svcs)
        except Exception as e:
            self.sig_toast.emit(f'Error servicios: {e}')

    # ── Slots de señales (hilo principal) ──────────────────
    def _tick(self):
        """QTimer en hilo principal — lee métricas del dict ya calculado."""
        m = self._metrics
        if not m: return
        try:
            cpu = m.get('cpu',0)
            self._c_cpu.update_data(f'{int(cpu)}%', cpu)
            self._g_cpu.push(cpu)

            ru = m.get('ram_used',0); rp = m.get('ram_pct',0)
            self._c_ram.update_data(f'{ru:.1f}G', rp)
            self._g_ram.push(rp)

            df = m.get('disk_free',0); dp = m.get('disk_pct',0)
            self._c_disk.update_data(f'{df:.0f}G', dp)

            temp = m.get('temp')
            if temp is not None:
                self._c_temp.update_data(f'{int(temp)}°', min(temp,100))
                self._g_temp.push(min(temp,100))
                self._temp_lbl.setText(f'CPU: {int(temp)} °C')
            else:
                self._c_temp.update_data('N/A', 0)
                self._temp_lbl.setText('Sensor no detectado')

            diff = m.get('net_diff',0)
            np   = min(diff/500*100, 100)
            self._g_net.push(np); self._g_net_m.push(np)
            self._net_lbl.setText(
                f"↓ {m.get('net_recv',0):.2f} GB  "
                f"↑ {m.get('net_sent',0):.2f} GB   "
                f"{diff:.1f} KB/s")

            ifaces = m.get('ifaces',{})
            self._ip_lbl.setText(' RED:  ' + '  |  '.join(
                f'{n}: {ip}' for n,ip in ifaces.items()) if ifaces else '—')
        except Exception:
            pass

    @pyqtSlot(dict)
    def _on_metrics(self, m):
        self._metrics = m

    @pyqtSlot(list)
    def _on_procs(self, rows):
        self._proc_list.clear()
        for pid,name,cpu,mem in rows[:20]:
            self._proc_list.addItem(
                f'{pid:<8}{name:<22}{cpu:<8.1f}{mem:.1f}%')

    @pyqtSlot(list)
    def _on_parts(self, parts):
        # Limpiar widgets anteriores
        while self._parts_lay.count():
            item = self._parts_lay.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        for p in parts:
            row = QHBoxLayout(); row.setSpacing(10)
            lbl_txt = QLabel(f"{p['mount']}  ({p['device']} {p['fstype']})")
            lbl_txt.setStyleSheet('font-family: monospace; font-size: 11px; '
                                  'background: transparent;')
            lbl_txt.setFixedWidth(210)
            bar = QProgressBar()
            bar.setRange(0, 100); bar.setValue(int(p['pct']))
            bar.setTextVisible(False)
            bar.setFixedHeight(8)
            if p['pct'] >= 90:
                bar.setStyleSheet('QProgressBar::chunk { background-color: #ff4444; }')
            elif p['pct'] >= 70:
                bar.setStyleSheet('QProgressBar::chunk { background-color: #fbbf24; }')
            sz = unit_lbl(f"{p['used']:.1f}/{p['total']:.1f} GB ({int(p['pct'])}%)")
            sz.setFixedWidth(175)
            row.addWidget(lbl_txt); row.addWidget(bar); row.addWidget(sz)
            w = QWidget(); w.setLayout(row)
            self._parts_lay.addWidget(w)

    @pyqtSlot(list)
    def _on_apt(self, apps):
        self._all_apt = apps; self._do_filter_apt()

    @pyqtSlot(list)
    def _on_flat(self, apps):
        self._all_flat = apps; self._filter_flat()

    @pyqtSlot(list)
    def _on_svcs(self, svcs):
        self._services = svcs
        q = self._svc_search.text().lower() if hasattr(self,'_svc_search') else ''

        # Limpiar
        while self._svc_lay.count() > 1:
            item = self._svc_lay.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        shown = 0
        for name,active,sub,desc in svcs:
            if q and q not in name.lower() and q not in desc.lower(): continue
            if shown >= 120: break
            shown += 1
            row = QFrame()
            row.setStyleSheet('QFrame { background-color: #141720; '
                             'border-radius: 8px; '
                             'border: 1px solid rgba(255,255,255,0.05); }')
            rl = QHBoxLayout(row); rl.setContentsMargins(10,6,10,6); rl.setSpacing(8)
            # Dot de color con CSS en vez de emoji
            dot_lbl = QLabel('●')
            if sub == 'running':
                dot_lbl.setStyleSheet('color: #00ffa3; font-size: 14px; background: transparent;')
            elif active == 'failed':
                dot_lbl.setStyleSheet('color: #ff4444; font-size: 14px; background: transparent;')
            else:
                dot_lbl.setStyleSheet('color: rgba(255,255,255,0.30); font-size: 14px; background: transparent;')
            rl.addWidget(dot_lbl)
            info = QVBoxLayout(); info.setSpacing(1)
            nl = QLabel(name); nl.setStyleSheet('font-weight:600; background:transparent;')
            info.addWidget(nl)
            if desc:
                dl = unit_lbl(desc[:64])
                info.addWidget(dl)
            rl.addLayout(info); rl.addStretch()
            running = sub == 'running'
            btn = neon_btn('■ Detener' if running else '▶ Iniciar',
                          'stop' if running else 'start')
            btn.clicked.connect(
                lambda _, n=name, r=running:
                self._svc_action(n, 'stop' if r else 'start'))
            rl.addWidget(btn)
            self._svc_lay.insertWidget(shown-1, row)

    @pyqtSlot(str)
    def _on_sysinfo(self, text):
        self._info_lbl.setText(text)

    @pyqtSlot(str)
    def _show_toast(self, msg):
        self._toast_lbl.setText(msg)
        self._toast_lbl.show()
        self._toast_timer.start(3000)

# ═══════════════════════════════════════════════════════════
#  SECCIÓN 7 — ENTRADA DE LA APP
# ═══════════════════════════════════════════════════════════
def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    # Usar Papirus-Dark para íconos en tema oscuro
    # Fallback: Papirus → tema del sistema
    for theme in ('Papirus-Dark', 'Papirus', ''):
        QIcon.setThemeName(theme)
        test = QIcon.fromTheme('computer')
        if not test.isNull():
            break
    app.setStyleSheet(QSS)

    win = OpenDashQt5()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
