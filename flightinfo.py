class FlightInfo:
    
    def __init__(self, flight_id, departure_time, arrival_time, full_price, taxes, departure_port, arrival_port):
        self.flight_id = flight_id
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.full_price = full_price
        self.departure_port = departure_port
        self.arrival_port = arrival_port
        self.taxes = taxes
    
    def __str__(self):
        return self.flight_id + " {" + self.departure_time + " " + self.arrival_time + " " + self.full_price + " " + self.taxes + " " + self.departure_port + " " + self.arrival_port + "}"