class FlightInfo:
    
    def __init__(self, departure_time, arrival_time, best_price, departure_port, arrival_port):
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.best_price = best_price
        self.departure_port = departure_port
        self.arrival_port = arrival_port
    
    def __str__(self):
        return self.departure_time + " " + self.arrival_time + " " + self.best_price + " " + self.departure_port + " " + self.arrival_port