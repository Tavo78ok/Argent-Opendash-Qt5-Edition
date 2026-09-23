#!/bin/bash
# ═══════════════════════════════════════════════════════════
#  Argent Opendash Qt5 v3.1 — Cinnamon Edition — build-appimage.sh
#  Uso: chmod +x build-appimage.sh && ./build-appimage.sh
#
#  Requiere en el sistema host: python3-pyqt5
# ═══════════════════════════════════════════════════════════
set -e

NAME="ArgentOpendashQt5"
VERSION="3.1"
ARCH="x86_64"
OUT="${NAME}-${VERSION}-${ARCH}.AppImage"
APPDIR="${NAME}.AppDir"
ID="io.github.Tavo78ok.ArgentOpendashQt5"
SRC="opendash_qt5.py"
ICO="argent-opendash.png"

G='\033[0;32m'; C='\033[0;36m'; Y='\033[1;33m'; R='\033[0;31m'; N='\033[0m'

echo -e "\n${C}╔══════════════════════════════════════════════╗"
echo -e "║  Argent Opendash Qt5 v${VERSION} — AppImage      ║"
echo -e "╚══════════════════════════════════════════════╝${N}\n"

[ ! -f "$SRC" ] && echo -e "${R}✗ $SRC no encontrado en el directorio actual${N}" && exit 1

echo -e "${Y}▶ Verificando PyQt5...${N}"
python3 -c "import PyQt5.QtWidgets" 2>/dev/null || {
    echo -e "${R}✗ PyQt5 no disponible${N}"
    echo "  sudo apt install python3-pyqt5"
    exit 1
}
echo -e "${G}  ✓ PyQt5 OK${N}"

echo -e "${Y}▶ appimagetool...${N}"
if command -v appimagetool &>/dev/null; then
    TOOL=appimagetool
    echo -e "${G}  ✓ encontrado${N}"
else
    wget -q "https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage" \
        -O /tmp/appimagetool
    chmod +x /tmp/appimagetool
    TOOL=/tmp/appimagetool
    echo -e "${G}  ✓ descargado${N}"
fi

echo -e "${Y}▶ Creando AppDir...${N}"
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/lib/argent-opendash-qt5"
mkdir -p "$APPDIR/usr/lib/python-packages"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$APPDIR/usr/share/icons/hicolor/128x128/apps"
mkdir -p "$APPDIR/usr/share/icons/hicolor/48x48/apps"
echo -e "${G}  ✓${N}"

echo -e "${Y}▶ Bundleando dependencias Python...${N}"
# PyQt5 NO se bundlea (depende de libs Qt del sistema) — se usa el del host
# Solo bundleamos psutil, que es puro Python + C ext liviana
pip3 install psutil \
    --target="$APPDIR/usr/lib/python-packages" \
    --quiet --no-deps 2>/dev/null || \
pip3 install psutil \
    --target="$APPDIR/usr/lib/python-packages" \
    --quiet 2>/dev/null
echo -e "${G}  ✓ psutil bundleado (PyQt5 se usa del sistema)${N}"

echo -e "${Y}▶ Copiando app...${N}"
cp "$SRC" "$APPDIR/usr/lib/argent-opendash-qt5/opendash.py"
chmod 644 "$APPDIR/usr/lib/argent-opendash-qt5/opendash.py"

if [ -f "$ICO" ]; then
    cp "$ICO" "$APPDIR/argent-opendash-qt5.png"
    cp "$ICO" "$APPDIR/usr/share/icons/hicolor/256x256/apps/argent-opendash-qt5.png"
    cp "$ICO" "$APPDIR/usr/lib/argent-opendash-qt5/argent-opendash.png"
    command -v convert &>/dev/null && {
        convert "$ICO" -resize 128x128 \
            "$APPDIR/usr/share/icons/hicolor/128x128/apps/argent-opendash-qt5.png"
        convert "$ICO" -resize 48x48 \
            "$APPDIR/usr/share/icons/hicolor/48x48/apps/argent-opendash-qt5.png"
    }
    echo -e "${G}  ✓ Íconos${N}"
else
    echo -e "${Y}  ⚠ $ICO no encontrado${N}"
    python3 -c "
from PIL import Image, ImageDraw
img = Image.new('RGBA',(64,64),(0,0,0,0))
d = ImageDraw.Draw(img)
d.ellipse([4,4,60,60],fill=(0,255,163,255))
d.ellipse([18,18,46,46],fill=(14,15,20,255))
img.save('$APPDIR/argent-opendash-qt5.png','PNG')
" 2>/dev/null || true
fi

cat > "$APPDIR/AppRun" << 'APPRUN'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
# psutil bundleado; PyQt5 se toma del sistema (requiere python3-pyqt5 instalado)
export PYTHONPATH="$APPDIR/usr/lib/python-packages:${PYTHONPATH:-}"
exec python3 "$APPDIR/usr/lib/argent-opendash-qt5/opendash.py" "$@"
APPRUN
chmod 755 "$APPDIR/AppRun"

cat > "$APPDIR/usr/share/applications/${ID}.desktop" << DESKTOP
[Desktop Entry]
Version=1.0
Type=Application
Name=Argent Opendash Qt5
GenericName=Monitor del Sistema
Comment=Monitor y Gestor del Sistema ArgOs Platinum - Cinnamon Edition
Exec=argent-opendash-qt5
Icon=argent-opendash-qt5
Terminal=false
Categories=System;Monitor;
Keywords=system;monitor;cpu;ram;temperatura;servicios;cinnamon;
StartupNotify=true
X-AppImage-Version=${VERSION}
DESKTOP
cp "$APPDIR/usr/share/applications/${ID}.desktop" "$APPDIR/${ID}.desktop"

echo -e "${Y}▶ Construyendo ${OUT}...${N}"
ARCH=x86_64 "$TOOL" --no-appstream "$APPDIR" "$OUT" 2>/dev/null \
    || ARCH=x86_64 "$TOOL" "$APPDIR" "$OUT"

SZ=$(du -h "$OUT" | cut -f1)
echo -e "\n${G}╔══════════════════════════════════════════════════╗"
echo -e "║  ✅ ${OUT} (${SZ}) listo"
echo -e "╚══════════════════════════════════════════════════╝${N}\n"
echo "  NOTA: requiere python3-pyqt5 instalado en el sistema destino"
echo "        (PyQt5 no se puede bundlear fácilmente por sus libs Qt nativas)"
echo ""
echo "  Ejecutar:   chmod +x ${OUT} && ./${OUT}"
echo "  Limpiar:    rm -rf ${APPDIR}"
