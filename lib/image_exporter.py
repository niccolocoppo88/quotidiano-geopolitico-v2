"""
lib/image_exporter.py — Export PDF → PNG
"""
import os
import subprocess
from config import OUTPUT_DIR

def pdf_to_png(pdf_path: str, png_path: str, dpi: int = 72) -> bool:
    """Converte un PDF in PNG usando pdftoppm (poppler-utils) o PyMuPDF."""
    try:
        # Prova pdftoppm (poppler)
        cmd = [
            "pdftoppm",
            "-r", str(dpi),
            "-png",
            "-singlefile",
            "-f", "1",
            "-l", "1",
            pdf_path,
            png_path.rsplit(".", 1)[0],  # pdftoppm aggiunge .png
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and os.path.exists(png_path):
            print(f"[image_exporter] Convertito: {pdf_path} → {png_path}")
            return True
    except FileNotFoundError:
        pass  # pdftoppm not available

    try:
        # Fallback: PyMuPDF (fitz)
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        page = doc[0]
        # Scale to 1200x1650 at 72dpi
        mat = fitz.Matrix(dpi/72, dpi/72)
        pix = page.get_pixmap(matrix=mat)
        pix.save(png_path)
        doc.close()
        print(f"[image_exporter] Convertito (PyMuPDF): {pdf_path} → {png_path}")
        return True
    except ImportError:
        pass

    try:
        # Fallback: Pillow
        from PIL import Image as PILImage
        # Usa pdf2image se disponibile
        from pdf2image import convert_from_path
        images = convert_from_path(pdf_path, dpi=dpi)
        if images:
            images[0].save(png_path, "PNG")
            print(f"[image_exporter] Convertito (Pillow): {pdf_path} → {png_path}")
            return True
    except ImportError:
        pass

    print(f"[image_exporter] ERRORE: nessun convertitore PDF→PNG disponibile")
    return False


def export_all(pdf_paths: list[str]) -> list[str]:
    """Converte tutti i PDF in PNG, restituisce lista percorsi PNG."""
    png_paths = []
    for pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            print(f"[image_exporter] ERRORE: PDF non trovato: {pdf_path}")
            continue
        base = os.path.splitext(pdf_path)[0]
        png_path = base + ".png"
        if pdf_to_png(pdf_path, png_path):
            png_paths.append(png_path)
        else:
            # Prova con PyMuPDF direttamente
            try:
                import fitz
                doc = fitz.open(pdf_path)
                page = doc[0]
                mat = fitz.Matrix(1, 1)  # 72dpi = 1x scale
                pix = page.get_pixmap(matrix=mat)
                pix.save(png_path)
                doc.close()
                png_paths.append(png_path)
                print(f"[image_exporter] Convertito (fitz fallback): {png_path}")
            except Exception as e:
                print(f"[image_exporter] ERRORE conversione {pdf_path}: {e}")
    return png_paths
