import mesa

class BaseAgent(mesa.Agent):
    def __init__(self, model, agent_type="White"):
        super().__init__(model)
        self.agent_type = agent_type
        self.eliminated = False
        
    def _get_neighbors(self):
        return self.model.grid.get_neighbors(
            self.pos,
            moore=True,  # Allow diagonal movement
            include_center=False  # Don't include the current position as a possible step
        )

    def step(self):
        # Check if should reproduce - only with same-type neighbors and with probability
        neighbors = self._get_neighbors()
        same_type_neighbors = [n for n in neighbors if n.agent_type == self.agent_type]
        
        # Only reproduce if has 2+ same-type neighbors and passes probability check (20%)
        if len(same_type_neighbors) >= 2 and self.random.random() < 0.7:
            self.should_reproduce = True
        
        # Move
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)