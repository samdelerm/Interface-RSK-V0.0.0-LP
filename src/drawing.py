from src.geometry_utils import *
from math import *

def draw_static_elements(canvas):
    """Dessine les éléments statiques du terrain de football."""
    canvas.delete("static")
    # Lignes du terrain
    canvas.create_line(convert_coords(-1, -0.6, canvas, True), convert_coords(1, -0.6, canvas, True), fill="white", width=5, tags="static")
    # Draw the boundaries
    canvas.create_line(convert_coords(-1, -0.6,canvas, True),convert_coords(1, -0.6, canvas,True), fill="white", width=5, tags="static")
    canvas.create_line(convert_coords(-1, 0.6, canvas,True), convert_coords(1, 0.6, canvas,True), fill="white", width=5, tags="static")
    canvas.create_line(convert_coords(-1, -0.6, canvas,True),convert_coords(-1, 0.6, canvas,True), fill="white", width=5, tags="static")
    canvas.create_line(convert_coords(1, -0.6, canvas,True), convert_coords(1, 0.6, canvas,True), fill="white", width=5, tags="static")
    canvas.create_line(convert_coords(-1, -0.3, canvas,True), convert_coords(-0.9, -0.3, canvas,True), fill="white", width=5, tags="static")
    canvas.create_line(convert_coords(-1, 0.3, canvas,True), convert_coords(-0.9, 0.3, canvas,True), fill="white", width=5, tags="static")
    canvas.create_line(convert_coords(1, -0.3, canvas,True), convert_coords(0.9, -0.3, canvas,True), fill="white", width=5, tags="static")
    canvas.create_line(convert_coords(1, 0.3, canvas,True), convert_coords(0.9, 0.3, canvas,True), fill="white", width=5, tags="static")
    canvas.create_line(convert_coords(0,0,canvas,True),convert_coords(0,0.1,canvas,True),fill="#00ff01",width=5,tags="static")
    canvas.create_line(convert_coords(0,0,canvas,True),convert_coords(0.1,0,canvas,True),fill="#ff0001",width=5,tags="static")
    # Draw the goals
    canvas.create_rectangle(convert_coords(-1, -0.4, canvas,True), convert_coords(-0.6, 0.4, canvas,True), outline="black", width=3.5, tags="static")
    canvas.create_rectangle(convert_coords(1, -0.4, canvas,True), convert_coords(0.6, 0.4, canvas,True), outline="black", width=3.5, tags="static")
    canvas.create_line(convert_coords(-1, -0.4, canvas,True), convert_coords(-1, 0.4, canvas,True), fill="black", width=3.5, tags="static")
    canvas.create_line(convert_coords(1, -0.4, canvas,True), convert_coords(1, 0.4, canvas,True), fill="black", width=3.5, tags="static")
    

    # Draw the center circle
    draw_circle(canvas,x=0, y=0, r=0.3,color= "black", fill=False, tag="static")
    draw_circle(canvas,x=0.46, y=-0.3, r=0.05,color= "black", fill=False, tag="static")
    draw_circle(canvas,x=-0.46, y=0.3, r=0.05,color= "black", fill=False, tag="static")
    draw_circle(canvas,x=0.46, y=0.3, r=0.05,color= "black", fill=False, tag="static")
    draw_circle(canvas,x=-0.46, y=-0.3, r=0.05,color= "black", fill=False, tag="static")
    draw_graduations(canvas)
# Autres éléments statiques (génération du terrain)

from math import atan2, cos, sin, sqrt

def draw_half_line_from_green1_to_ball(client,canvas, green1_position, ball_position, blue_positions, tolerance=0.1):
    """
    Trace une demi-droite depuis le robot green1 passant par la balle,
    tout en s'arrêtant si elle croise la position d'un robot adverse
    avec une tolérance de 0.1 unités.
    """
    x_green1, y_green1 = green1_position
    x_ball, y_ball = ball_position

    # Calcul de l'angle entre green1 et la balle
    angle = atan2(y_ball - y_green1, x_ball - x_green1)
    
    # Fixer une longueur arbitraire pour la demi-droite
    length = 2  # longueur de la demi-droite (par exemple 2 unités sur le terrain)
    
    # Parcourir chaque petit segment de la demi-droite pour vérifier les intersections
    step_size = 0.01  # Taille des pas pour parcourir la demi-droite
    for t in range(int(length / step_size)):
        # Calculer la position actuelle sur la demi-droite
        x_current = x_green1 + t * step_size * cos(angle)
        y_current = y_green1 + t * step_size * sin(angle)

        # Vérifier si la position actuelle croise un robot adverse
        for blue_pos in blue_positions:
            x_blue, y_blue = blue_pos
            distance_to_blue = sqrt((x_current - x_blue) ** 2 + (y_current - y_blue) ** 2)
            if distance_to_blue <= tolerance:
                # Si la demi-droite passe trop près d'un robot adverse, arrêter ici
                x_end = x_current
                y_end = y_current
                
                break
        else:
            # Si aucun robot n'est croisé, continuer
            continue
        # Si un robot est croisé, sortir des boucles
        break
    else:
        # Si aucun robot n'est croisé, la demi-droite atteint sa longueur maximale
        x_end = x_green1 + length * cos(angle)
        y_end = y_green1 + length * sin(angle)

    # Convertir les coordonnées pour le canvas
    x1_canvas, y1_canvas = convert_coords(x_green1, y_green1, canvas, True)
    x2_canvas, y2_canvas = convert_coords(x_end, y_end, canvas, True)
    if does_half_line_cross_x(client.green1.position, ball_position, -0.9):
        for blue_pos in blue_positions:
            x_blue, y_blue = blue_pos
            distance_to_blue = sqrt((x_current - x_blue) ** 2 + (y_current - y_blue) ** 2)
            if distance_to_blue >= tolerance:
                #draw_circle(canvas, x=-0.3, y=0.8, r=0.02, color="red", fill=True, tag="dynamic")
                canvas.create_text(convert_coords(-0.3, 0.8, canvas, True), text="But Vert", fill="red", tags="dynamic",font=("Arial",15))
    if does_half_line_cross_x(client.blue1.position, ball_position, 0.9):
        for blue_pos in blue_positions:
            x_blue, y_blue = blue_pos
            distance_to_blue = sqrt((x_current - x_blue) ** 2 + (y_current - y_blue) ** 2)
            if distance_to_blue >= tolerance:
                #draw_circle(canvas, x=0.3, y=0.8, r=0.02, color="blue", fill=True, tag="dynamic")
                canvas.create_text(convert_coords(0.3, 0.8, canvas, True), text="But Bleu", fill="blue", tags="dynamic",font=("Arial",15))
    # Tracer la demi-droite
    canvas.create_line(x1_canvas, y1_canvas, x2_canvas, y2_canvas, fill="red", width=2, tags="dynamic")


def draw_dynamic_elements(canvas, client, ):
    """Dessine les éléments dynamiques (robots, ballon, etc.)"""
    canvas.delete("dynamic")
    
    
    ball_position = client.ball
    robots = [client.green1, client.green2, client.blue1, client.blue2]
    i=0
    
    # Dessin des éléments dynamiques
    for robot in robots:
        i+=1
        if i<3 :
            fill="#00FF10"  
            outline="black"
        else:
            fill="blue"
            outline="white"
        x, y = robot.position
        canvas.create_oval(convert_coords(x - 0.05, y - 0.05, canvas, True), 
                           convert_coords(x + 0.05, y + 0.05, canvas, True), 
                           outline=outline, fill=fill, tags="dynamic")

    # Dessin de la balle
    x, y = ball_position
    canvas.create_oval(convert_coords(x - 0.02, y - 0.02, canvas, True), 
                       convert_coords(x + 0.02, y + 0.02, canvas, True), 
                       outline="orange", fill="orange", tags="dynamic")
    
    # Dessin de la demi-droite
    draw_half_line_from_green1_to_ball(client,canvas, client.green1.position, ball_position,[client.blue1.position, client.blue2.position])
    draw_half_line_from_green1_to_ball(client,canvas, client.blue1.position, ball_position,[client.green1.position, client.green2.position])

    
    # Dessin de l'alerte si un but peut être marqué
   
