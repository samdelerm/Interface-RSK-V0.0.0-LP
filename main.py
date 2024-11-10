from src.soccer_sim import SoccerFieldSimulator
from src.client import initialize_client



if __name__ == "__main__":
    
    
    client = initialize_client()  # Initialise le client rsk
    
    app = SoccerFieldSimulator(client)  # Crée l'interface utilisateur avec le client
    app.mainloop()  # Démarre la boucle principale de l'application




