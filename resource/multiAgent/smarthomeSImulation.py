from mesa import Agent, Model
from mesa.time import RandomActivation
import random

class ApplianceAgent(Agent):
    def __init__(self, unique_id, model, type):
        super().__init__(unique_id, model)
        self.type = type
        self.status = "off"
    
    def step(self):
        # Basic decision-making based on the environment and agent type
        if self.type == "air_conditioner":
            if self.model.temperature > 25:
                self.status = "on"
                print(f"{self.unique_id} turned on to reduce temperature")
            else:
                self.status = "off"

class SmartHomeModel(Model):
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.temperature = 22  # Starting temperature
        self.humidity = 50     # Starting humidity
        # Instantiate agents
        for i in range(5):  # Example: 5 agents of different types
            a = ApplianceAgent(i, self, type=random.choice(['air_conditioner', 'air_purifier']))
            self.schedule.add(a)

    def step(self):
        # Simulate a time step
        self.schedule.step()

# Create and run the model
model = SmartHomeModel()
for i in range(10):  # Run for 10 steps
    model.step()
