import math
from math import *
def convert_coords(x, y, canvas, to_canvas=False):
    width, height = canvas.winfo_width(), canvas.winfo_height()
    if to_canvas:
        return (x * scale_factor(canvas) + width / 2, y * -scale_factor(canvas) + height / 2)
    else:
        return (x - width / 2) / scale_factor(canvas), (height / 2 - y) / scale_factor(canvas)

def scale_factor(canvas):
    width, height = canvas.winfo_width(), canvas.winfo_height()
    return min(width, height) / 2
def draw_circle(canvas, x, y, r, color, fill=True, tag=None):
        """Draw a circle on the canvas."""
        x1, y1 =convert_coords(x - r, y - r, canvas,to_canvas=True)
        x2, y2 =convert_coords(x + r, y + r, canvas,to_canvas=True)
        canvas.create_oval(x1, y1, x2, y2, outline=color, fill=color if fill else "", tags=tag)
def calculate_line_equation(point1, point2):
        """
        Retourne l'équation de la droite passant par point1 et point2 sous la forme (a, b),
        où 'a' est la pente et 'b' est l'ordonnée à l'origine.
        Si la droite est verticale, retourne None.
        """
        x1, y1 = point1
        x2, y2 = point2

        # Vérifier si la droite est verticale (x1 == x2)
        if x1 == x2:
            return None  # La pente est infinie pour une droite verticale

        # Calcul de la pente (a)
        a = (y2 - y1) / (x2 - x1)

        # Calcul de l'ordonnée à l'origine (b)
        b = y1 - a * x1

        return f"{round(a,2)}x+ {round(b,2)}\n"
def calculate_half_line_equation(point1, point2):
    """
    Retourne l'équation de la droite passant par point1 et point2 sous la forme (a, b),
    où 'a' est la pente et 'b' est l'ordonnée à l'origine.
    Si la droite est verticale, retourne None.
    """
    x1, y1 = point1
    x2, y2 = point2

    # Vérifier si la droite est verticale (x1 == x2)
    if x1 == x2:
        return None  # La pente est infinie pour une droite verticale

    # Calcul de la pente (a)
    a = (y2 - y1) / (x2 - x1)

    # Calcul de l'ordonnée à l'origine (b)
    b = y1 - a * x1

    return a, b
def does_half_line_cross_x(green1_position, ball_position, x_value):
    """
    Vérifie si la demi-droite ayant pour origine le robot green1 et passant par la balle
    croise l'axe x = 0.9 entre y = 0.30 et y = -0.30. Si oui, retourne True, sinon False.
    """
    # Récupère l'équation de la demi-droite y = mx + b
    line_equation = calculate_half_line_equation(green1_position, ball_position)
    
    if line_equation is None:
        # Cas où la ligne est verticale (slope indéfinie), donc pas d'intersection possible
        return False
    
    slope, intercept = line_equation
    
    # Calcul de y pour x = 0.9 (y = mx + b)
   
    y_at_x = slope * x_value + intercept
    
    # Vérifie si y est entre -0.30 et 0.30
    if -0.30 <= y_at_x <= 0.30:
        return True
    else:
        return False

def draw_graduations(canvas):
        """Draw graduation lines and labels for better visualization."""
        scale = scale_factor(canvas)
        width, height = canvas.winfo_width(), canvas.winfo_height()

        # Draw X axis graduations and labels
        for i in range(-10, 11):
            x = i / 10.0
            canvas_x = convert_coords(x, 0, canvas,to_canvas=True)[0]
            canvas.create_line(canvas_x, 0, canvas_x, height, fill="gray", width=1, tags="static")
            if i % 1 == 0:  # Label every 0.5 units
                canvas.create_text(canvas_x, height - 15, text=str(i / 10.0), fill="white", font=("Arial", 10), tags="static")

        # Draw Y axis graduations and labels
        for j in range(-7, 8):
            y = j / 10.0
            canvas_y = convert_coords(0, y,canvas, to_canvas=True)[1]
            canvas.create_line(0, canvas_y, width, canvas_y, fill="gray", width=1, tags="static")
            if j % 1 == 0:  # Label every 0.5 units
                canvas.create_text(15, canvas_y, text=str(-j / 10.0), fill="white", font=("Arial", 10), tags="static")