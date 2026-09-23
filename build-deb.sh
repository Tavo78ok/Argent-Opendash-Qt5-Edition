#!/bin/bash
# ═══════════════════════════════════════════════════════════
#  Argent Opendash Qt5 v3.1 — Cinnamon Edition — build-deb.sh
#  Uso: chmod +x build-deb.sh && ./build-deb.sh
# ═══════════════════════════════════════════════════════════
set -e

PKG="argent-opendash-qt5"
VERSION="3.1"
ARCH="all"
DEB="${PKG}_${VERSION}_${ARCH}.deb"
DIR="deb_build/${PKG}_${VERSION}_${ARCH}"
BIN="argent-opendash-qt5"
LIB="usr/lib/argent-opendash-qt5"
SRC="opendash_qt5.py"
ICO="argent-opendash.png"

G='\033[0;32m'; C='\033[0;36m'; Y='\033[1;33m'; R='\033[0;31m'; N='\033[0m'

echo -e "\n${C}╔══════════════════════════════════════════════╗"
echo -e "║  Argent Opendash Qt5 v${VERSION} — Cinnamon .deb ║"
echo -e "╚══════════════════════════════════════════════╝${N}\n"

[ ! -f "$SRC" ] && echo -e "${R}✗ $SRC no encontrado en el directorio actual${N}" && exit 1

echo -e "${Y}▶ Herramientas...${N}"
MISS=()
command -v dpkg-deb &>/dev/null || MISS+=("dpkg-dev")
command -v convert  &>/dev/null || MISS+=("imagemagick")
[ ${#MISS[@]} -gt 0 ] && sudo apt-get install -y "${MISS[@]}" -q
echo -e "${G}  ✓${N}"

echo -e "${Y}▶ Estructura...${N}"
rm -rf deb_build
mkdir -p "${DIR}/DEBIAN" "${DIR}/usr/bin" "${DIR}/${LIB}"
mkdir -p "${DIR}/usr/share/applications"
mkdir -p "${DIR}/usr/share/icons/hicolor/256x256/apps"
mkdir -p "${DIR}/usr/share/icons/hicolor/128x128/apps"
mkdir -p "${DIR}/usr/share/icons/hicolor/48x48/apps"
mkdir -p "${DIR}/usr/share/pixmaps"
echo -e "${G}  ✓${N}"

echo -e "${Y}▶ Copiando archivos...${N}"
cp "$SRC" "${DIR}/${LIB}/opendash.py"
chmod 644 "${DIR}/${LIB}/opendash.py"

if [ -f "$ICO" ]; then
    convert "$ICO" -resize 256x256 "${DIR}/usr/share/icons/hicolor/256x256/apps/argent-opendash-qt5.png"
    convert "$ICO" -resize 128x128 "${DIR}/usr/share/icons/hicolor/128x128/apps/argent-opendash-qt5.png"
    convert "$ICO" -resize 48x48   "${DIR}/usr/share/icons/hicolor/48x48/apps/argent-opendash-qt5.png"
    cp "$ICO" "${DIR}/usr/share/pixmaps/argent-opendash-qt5.png"
    # Copia junto al .py también, por si se ejecuta sin instalar
    cp "$ICO" "${DIR}/${LIB}/argent-opendash.png"
    echo -e "${G}  ✓ Íconos${N}"
else
    echo -e "${Y}  ⚠ $ICO no encontrado — sin ícono${N}"
fi

cat > "${DIR}/usr/bin/${BIN}" << 'EOF'
#!/bin/bash
exec python3 /usr/lib/argent-opendash-qt5/opendash.py "$@"
EOF
chmod 755 "${DIR}/usr/bin/${BIN}"

cat > "${DIR}/usr/share/applications/argent-opendash-qt5.desktop" << DESKTOP
[Desktop Entry]
Version=1.0
Type=Application
Name=Argent Opendash Qt5
GenericName=Monitor del Sistema
Comment=Monitor y Gestor del Sistema ArgOs Platinum - Cinnamon Edition
Exec=${BIN}
Icon=argent-opendash-qt5
Terminal=false
Categories=System;Monitor;
Keywords=system;monitor;cpu;ram;temperatura;servicios;cinnamon;
StartupNotify=true
StartupWMClass=argent-opendash-qt5
DESKTOP
echo -e "${G}  ✓${N}"

cat > "${DIR}/DEBIAN/control" << CONTROL
Package: ${PKG}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Depends: python3 (>= 3.8), python3-pyqt5, python3-pip
Maintainer: Tavo (Tavo78ok) <tavo78ok@github.com>
Homepage: https://github.com/Tavo78ok/Argent-Opendash-Gtk4-libadwaita
Description: Argent Opendash Qt5 v${VERSION} - Cinnamon Edition
 Version Qt5 de Argent Opendash, disenada para Cinnamon y cualquier
 entorno de escritorio. Motor Qt5 independiente del compositor Muffin,
 sin conflictos GL, sin freezes. Mismas 7 pestanas que la version GTK4:
 Dashboard, Monitor, Gamer, Software APT+Flatpak, Inicio,
 Servicios systemd y Controles con TRIM SSD.
CONTROL

cat > "${DIR}/DEBIAN/postinst" << 'POSTINST'
#!/bin/bash
set -e
G='\033[0;32m'; C='\033[0;36m'; Y='\033[1;33m'; N='\033[0m'
echo -e "\n${C}╔══════════════════════════════════════════╗"
echo -e "║   Argent Opendash Qt5 v3.1               ║"
echo -e "║   Cinnamon Edition                        ║"
echo -e "╚══════════════════════════════════════════╝${N}\n"
apt_q() { DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "$@" 2>/dev/null; }
py_ok() { python3 -c "import $1" 2>/dev/null; }
pip_q() { pip3 install "$1" --break-system-packages -q 2>/dev/null || pip3 install "$1" -q 2>/dev/null || true; }

echo -e "${Y}▶ python3-pyqt5...${N}"
py_ok PyQt5 && echo -e "${G}  ✓${N}" \
    || { apt_q python3-pyqt5 2>/dev/null && echo -e "${G}  ✓ instalado${N}" \
        || echo -e "${Y}  ⚠ sudo apt install python3-pyqt5${N}"; }

echo -e "${Y}▶ psutil...${N}"
py_ok psutil && echo -e "${G}  ✓${N}" \
    || { apt_q python3-psutil 2>/dev/null || pip_q psutil; }

echo -e "${Y}▶ power-profiles-daemon...${N}"
command -v powerprofilesctl &>/dev/null && echo -e "${G}  ✓${N}" \
    || { apt_q power-profiles-daemon 2>/dev/null && echo -e "${G}  ✓${N}" \
        || echo -e "${Y}  ⚠ sudo apt install power-profiles-daemon${N}"; }

for pkg in policykit-1 brightnessctl pulseaudio-utils flatpak; do
    echo -e "${Y}▶ $pkg (opcional)...${N}"
    dpkg -l "$pkg" 2>/dev/null | grep -q '^ii' && echo -e "${G}  ✓${N}" \
        || { apt_q "$pkg" 2>/dev/null && echo -e "${G}  ✓${N}" \
            || echo -e "${Y}  ⚠ opcional${N}"; }
done

chmod +x /usr/bin/argent-opendash-qt5 \
         /usr/lib/argent-opendash-qt5/opendash.py
gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
update-desktop-database /usr/share/applications/ 2>/dev/null || true

echo -e "\n${G}╔══════════════════════════════════════════╗"
echo -e "║  ✅ Argent Opendash Qt5 v3.1 instalado   ║"
echo -e "║  Terminal:  argent-opendash-qt5           ║"
echo -e "║  Menú:      buscar Argent Opendash Qt5   ║"
echo -e "╚══════════════════════════════════════════╝${N}\n"
exit 0
POSTINST
chmod 755 "${DIR}/DEBIAN/postinst"

printf '#!/bin/bash\nupdate-desktop-database /usr/share/applications/ 2>/dev/null || true\nexit 0\n' \
    > "${DIR}/DEBIAN/prerm"
chmod 755 "${DIR}/DEBIAN/prerm"

echo -e "${Y}▶ Construyendo ${DEB}...${N}"
dpkg-deb --build --root-owner-group "${DIR}" "${DEB}"

SZ=$(du -h "${DEB}" | cut -f1)
echo -e "\n${G}╔══════════════════════════════════════════════════╗"
echo -e "║  ✅ ${DEB} (${SZ}) listo"
echo -e "╚══════════════════════════════════════════════════╝${N}\n"
echo "  Instalar:     sudo dpkg -i ${DEB}"
echo "  Ejecutar:     argent-opendash-qt5"
echo "  Limpiar:      rm -rf deb_build"
