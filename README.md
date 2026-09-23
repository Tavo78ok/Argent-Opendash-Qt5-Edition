# Argent Opendash Qt5 — Cinnamon Edition

### Monitor, Optimizador y Gestor del Sistema — OpenArgentOS Platinum Edition

![Qt5](https://img.shields.io/badge/Qt-5-41cd52?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow?style=flat-square)
![Version](https://img.shields.io/badge/Versión-3.1-purple?style=flat-square)
![License](https://img.shields.io/badge/Licencia-MIT-lightgrey?style=flat-square)
![Platform](https://img.shields.io/badge/Plataforma-Cinnamon%20%2F%20Debian-orange?style=flat-square)

---
<img width="1440" height="900" alt="Captura de pantalla de 2026-09-23 20-48-01" src="https://github.com/user-attachments/assets/80759b19-7d7a-4c29-8925-1ec3b4cd8efe" />
<img width="1440" height="900" alt="Captura de pantalla de 2026-09-23 20-48-21" src="https://github.com/user-attachments/assets/a1da482e-6eed-4b67-884e-775b7cdd6282" />
<img width="1440" height="900" alt="Captura de pantalla de 2026-09-23 20-48-32" src="https://github.com/user-attachments/assets/45e2b2fb-2e34-4530-bd37-48f0ad9425e4" />
<img width="1440" height="900" alt="Captura de pantalla de 2026-09-23 20-48-44" src="https://github.com/user-attachments/assets/ea6dc401-e165-4373-8db9-8ae75eee8c81" />
<img width="1440" height="900" alt="Captura de pantalla de 2026-09-23 20-48-54" src="https://github.com/user-attachments/assets/8604bf1f-7eb8-4879-a7f1-fb447642f6ae" />
<img width="1440" height="900" alt="Captura de pantalla de 2026-09-23 20-49-04" src="https://github.com/user-attachments/assets/ef50d0ec-6473-43cd-9032-6e938f33065c" />
<img width="1440" height="900" alt="Captura de pantalla de 2026-09-23 20-49-16" src="https://github.com/user-attachments/assets/6bcb4099-4816-4bc6-9bb4-be7bba9e93f3" />


## Descripción

**Argent Opendash Qt5** es la edición para **Cinnamon** del dashboard de sistema de OpenArgentOS Platinum. Nace porque la versión GTK4/libadwaita del proyecto ([Argent-Opendash-Gtk4-libadwaita](https://github.com/Tavo78ok/Argent-Opendash-Gtk4-libadwaita)) puede congelarse en Cinnamon por un conflicto entre el renderer GL de GTK4 y el compositor Muffin en hardware gráfico antiguo (probado en GeForce 210).

Esta versión usa **PyQt5**, con un motor de renderizado completamente independiente del compositor — sin conflictos GL, sin freezes. Misma estética neon, mismas 7 pestañas, misma funcionalidad completa.

**¿Qué versión usar?**
| Entorno de escritorio | Versión recomendada |
|---|---|
| XFCE, GNOME, KDE, MATE | [GTK4/libadwaita](https://github.com/Tavo78ok/Argent-Opendash-Gtk4-libadwaita) |
| Cinnamon | **Qt5 (este repo)** |

---

## Capturas

> Dashboard con ring meters, gráficos históricos, particiones y especificaciones del sistema — corriendo fluido en Cinnamon.

---

## Funciones por pestaña

### Dashboard
- 4 ring meters animados: CPU, RAM, Disco, Temperatura
- Gráficos históricos en tiempo real: CPU, RAM, Red (últimos 60s)
- Particiones montadas con barra de progreso — refresco automático cada 30s
- Especificaciones del sistema: OS, HOST, KERNEL, CPU, GPU, RAM total, paquetes, uptime, IP de red

### Monitor
- Temperatura CPU en tiempo real (lectura directa desde sysfs, filtrada por sensores seguros)
- Estadísticas de red con gráfico histórico
- Lista de procesos ordenada por uso de CPU

### Gamer
- Perfiles de energía: Ahorro, Balanceado, Gamer (vía `power-profiles-daemon`)
- El perfil seleccionado persiste entre sesiones

### Software
- Switcher APT / Flatpak
- **APT**: búsqueda, detalle (versión, tamaño, arquitectura, sección), instalar, desinstalar
- **Flatpak**: búsqueda, detalle (App ID, versión, tamaño, origen), desinstalar

### Inicio
- Gestión de aplicaciones de autostart (`~/.config/autostart`) con activar/desactivar

### Servicios
- Lista de servicios systemd con estado (activo/inactivo/fallido)
- Búsqueda, iniciar/detener con `pkexec`

### Controles
- Toggle "Iniciar con el sistema"
- Brillo de pantalla (backlight, brightnessctl o xrandr, con debounce)
- Volumen del sistema (`pactl`, con debounce)
- TRIM SSD (`fstrim -av`)
- Toggle tema claro/oscuro

---

## Por qué Qt5 y no GTK4 en Cinnamon

Cinnamon usa **Muffin**, un compositor derivado de Mutter que gestiona su propio contexto OpenGL. GTK4 desde la versión 4.x usa GL como renderer por defecto para sus widgets, incluyendo `DrawingArea` (usados aquí para los ring meters y gráficos históricos). En hardware gráfico limitado o con drivers antiguos (probado en NVIDIA GeForce 210), la negociación de contexto GL entre GTK4 y Muffin puede colgar el hilo principal de la aplicación después de un tiempo de uso.

Qt5 no comparte ese contexto GL con el compositor de la misma manera — su motor de widgets (`QPainter`, usado aquí para los mismos ring meters y gráficos) renderiza de forma independiente. El resultado: misma app, mismo hardware, sin freezes.

---

## Instalación

### Opción 1 — Paquete .deb (recomendado)

```bash
sudo dpkg -i argent-opendash-qt5_3.1_all.deb
```

El script de post-instalación detecta e instala automáticamente `python3-pyqt5`, `psutil` y las dependencias opcionales.

### Opción 2 — Desde el código fuente

```bash
sudo apt install python3 python3-pyqt5 python3-pip \
    brightnessctl pulseaudio-utils power-profiles-daemon \
    policykit-1 flatpak

pip3 install psutil --break-system-packages

python3 opendash_qt5.py
```

---

## Dependencias

| Paquete | Uso | Tipo |
|---|---|---|
| `python3-pyqt5` | Interfaz Qt5 | Requerido |
| `psutil` | Métricas del sistema | Requerido |
| `brightnessctl` | Control de brillo | Opcional |
| `pulseaudio-utils` | Control de volumen (`pactl`) | Opcional |
| `power-profiles-daemon` | Perfiles de energía | Opcional |
| `policykit-1` | Autenticación `pkexec` | Opcional |
| `flatpak` | Gestión de apps Flatpak | Opcional |

---

## Construir desde el fuente

### .deb

```bash
git clone https://github.com/Tavo78ok/Argent-Opendash-Gtk4-libadwaita
cd Argent-Opendash-Gtk4-libadwaita  # o la carpeta con opendash_qt5.py
chmod +x build-deb.sh
./build-deb.sh
```

### AppImage

```bash
chmod +x build-appimage.sh
./build-appimage.sh
```

> **Nota:** el AppImage no bundlea PyQt5 (depende de librerías Qt nativas del sistema). El sistema destino necesita `python3-pyqt5` instalado. `psutil` sí viene bundleado.

---

## Arquitectura

```
opendash_qt5.py
├── Constantes y paleta neon
├── QSS (estilos globales, incluye TOGGLE_SWITCH_QSS)
├── Helpers UI (card, section_lbl, mono_lbl, neon_btn...)
├── Capa de hardware
│   ├── _temp_updater — hilo daemon, lee sysfs (thermal_zone + hwmon filtrado)
│   ├── hw_partitions, hw_procs_top, hw_get_volume, hw_get_brightness...
│   └── _run_in_terminal — lanza scripts con pkexec
├── RingMeter       — gauge circular con QPainter
├── HistoryGraph    — gráfico de línea histórico con QPainter
├── MetricCard      — tarjeta con ring + valor + etiqueta
└── OpenDashQt5(QMainWindow)
    ├── Señales pyqtSignal — comunicación thread-safe entre hilos y UI
    │   sig_metrics, sig_procs, sig_parts, sig_apt, sig_flat, sig_svcs...
    ├── Hilos daemon
    │   ├── _hw_loop      — CPU/RAM/disco/red cada 1s
    │   ├── _procs_loop   — procesos cada 3s
    │   └── _temp_updater — temperatura cada 10s (sysfs)
    ├── 7 pestañas: Dashboard, Monitor, Gamer, Software, Inicio, Servicios, Controles
    └── QTimer principal — actualiza widgets desde el caché de métricas
```

**Diseño clave:** ninguna llamada de hardware bloqueante corre en el hilo de Qt. Los hilos daemon emiten señales (`pyqtSignal`) que Qt entrega de forma segura al hilo principal — nunca hay una llamada directa desde un hilo secundario a un widget.

---

## Comando en terminal

```bash
argent-opendash-qt5
```

---

## Changelog

### v3.1 — Cinnamon Edition (Septiembre 2026)
- Primera versión Qt5, migrada 1:1 desde la edición GTK4/libadwaita
- Arquitectura de señales Qt (`pyqtSignal`) en vez de `GLib.idle_add`
- Temperatura desde sysfs con filtrado de sensores (evita sensores GPU que pueden requerir X11)
- Íconos de pestañas vía `QIcon.fromTheme()` (compatible con Papirus-Dark)
- Switches de estilo toggle para Autostart y Tema
- Terminal se muestra al frente al ejecutar acciones (limpieza, instalar, TRIM)
- Sin freezes confirmado en Cinnamon con GeForce 210 + Pentium E5400

---

## Proyecto hermano

**[Argent Opendash GTK4 libadwaita](https://github.com/Tavo78ok/Argent-Opendash-Gtk4-libadwaita)** — la versión original para XFCE, GNOME y KDE.

---

## Autor

**Tavo** ([@Tavo78ok](https://github.com/Tavo78ok))
Proyecto: **OpenArgentOS (Platinum Edition)**
Licencia: MIT
