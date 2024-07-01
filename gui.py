import streamlit as st
import os
from PIL import Image, ImageDraw, ImageOps

# Funktion, um die Positionen in Koordinaten umzuwandeln
def position_to_coords(position):
    col = ord(position[0].upper()) - ord('A')
    row = 8 - int(position[1])
    return row, col

# Funktion, um einen kontrastierenden Rand um die Figurenbilder hinzuzufügen
def add_contrasting_border(image, border_size=5):
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    # Hintergrundfarbe bestimmen
    bg_color = image.getpixel((0, 0))[:3]
    # Kontrastierende Randfarbe auswählen
    border_color = (0, 0, 0) if bg_color == (255, 255, 255) else (255, 255, 255)
    # Rand hinzufügen
    new_image = ImageOps.expand(image, border=border_size, fill=border_color)
    return new_image

# Funktion, um die Figurenpositionen aus dem Texteingabefeld zu parsen
def parse_positions(input_text):
    positions = {}
    for line in input_text.splitlines():
        parts = line.strip().split()
        if len(parts) != 2:
            continue
        figure, position = parts
        if figure in positions:
            if isinstance(positions[figure], list):
                positions[figure].append(position)
            else:
                positions[figure] = [positions[figure], position]
        else:
            positions[figure] = position
    return positions

# Funktion, um das Schachbrett zu zeichnen
def draw_chessboard(draw, square_size, light_color, dark_color):
    for row in range(8):
        for col in range(8):
            color = light_color if (row + col) % 2 == 0 else dark_color
            draw.rectangle([col * square_size, row * square_size, (col + 1) * square_size, (row + 1) * square_size], fill=color)

# Standard-Positionen der Figuren
default_placement = {
    "white_king": "E1", "white_queen": "D1", "white_rook": ["A1", "H1"],
    "white_bishop": ["C1", "F1"], "white_knight": ["B1", "G1"], "white_pawn": ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"],
    "black_king": "E8", "black_queen": "D8", "black_rook": ["A8", "H8"],
    "black_bishop": ["C8", "F8"], "black_knight": ["B8", "G8"], "black_pawn": ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7"]
}

# Setze den Titel der App
st.title("Schachbrett mit allen Schachfiguren")

# Sidebar für die Positionseingabe
st.sidebar.title("Figurenpositionierung")
positions_input = st.sidebar.text_area("Geben Sie die neuen Positionen der Figuren ein (z.B. 'white_king E1'):")
placement = parse_positions(positions_input) if positions_input else default_placement

# Definiere die Größe des Schachbretts und der Felder
board_size = 8
square_size = 80

# Definiere die Farben für das Schachbrett
light_color = (240, 217, 181)  # Weiß
dark_color = (181, 136, 99)    # Grün

# Erstelle ein leeres Schachbrett-Bild
chessboard_img = Image.new("RGBA", (board_size * square_size, board_size * square_size), (255, 255, 255, 0))
draw = ImageDraw.Draw(chessboard_img)

# Zeichne das Schachbrett
draw_chessboard(draw, square_size, light_color, dark_color)

# Lade die Bilder und füge sie dem Schachbrett hinzu
image_dir = "images"  # Passe diesen Pfad an, falls nötig
for figure, positions in placement.items():
    if isinstance(positions, list):
        for pos in positions:
            row, col = position_to_coords(pos)
            image_path = os.path.join(image_dir, f"{figure}.png")
            if os.path.exists(image_path):
                piece_img = Image.open(image_path).resize((square_size, square_size), Image.Resampling.LANCZOS)
                chessboard_img.paste(piece_img, (col * square_size, row * square_size), piece_img)
    else:
        row, col = position_to_coords(positions)
        image_path = os.path.join(image_dir, f"{figure}.png")
        if os.path.exists(image_path):
            piece_img = Image.open(image_path).resize((square_size, square_size), Image.Resampling.LANCZOS)
            chessboard_img.paste(piece_img, (col * square_size, row * square_size), piece_img)

# Zeige das Schachbrett-Bild in Streamlit an
st.image(chessboard_img)
