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
    
    def _get_neighborhood(self, distance=3):
        """Get larger neighborhood for segregation analysis"""
        return self._get_neighborhood_at(self.pos, distance)
    
    def _get_neighborhood_at(self, pos, distance=3):
        """Get agents in neighborhood around a given position"""
        neighborhood = []
        x, y = pos
        for i in range(x - distance, x + distance + 1):
            for j in range(y - distance, y + distance + 1):
                if (i, j) != pos:
                    wrapped_x = i % self.model.grid.width
                    wrapped_y = j % self.model.grid.height
                    agents = self.model.grid.get_cell_list_contents((wrapped_x, wrapped_y))
                    neighborhood.extend(agents)
        return neighborhood
    
    def _get_similar_ratio(self, neighborhood):
        """Calculate ratio of same-type agents in neighborhood"""
        if not neighborhood:
            return 0.5
        same_type = sum(1 for n in neighborhood if n.agent_type == self.agent_type)
        return same_type / len(neighborhood)

    def step(self):
        # Check if should reproduce - with same-type neighbors and probability
        neighbors = self._get_neighbors()
        same_type_neighbors = [n for n in neighbors if n.agent_type == self.agent_type]
        
        if len(same_type_neighbors) >= 1 and self.random.random() < 0.15:
            self.should_reproduce = True
        
        # Move towards neighborhoods with more similar agents (segregation)
        neighborhood = self._get_neighborhood(distance=3)
        similar_ratio = self._get_similar_ratio(neighborhood)
        
        # If less than 40% similar in neighborhood, try to move to better place
        if similar_ratio < 0.4:
            # Try candidate positions and move to best one
            possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False
            )
            if possible_steps:
                best_pos = self.pos
                best_ratio = similar_ratio
                
                for candidate in possible_steps:
                    candidate_neighborhood = self._get_neighborhood_at(candidate, distance=3)
                    candidate_ratio = self._get_similar_ratio(candidate_neighborhood)
                    
                    if candidate_ratio > best_ratio:
                        best_pos = candidate
                        best_ratio = candidate_ratio
                
                self.model.grid.move_agent(self, best_pos)
            else:
                # Random move as fallback
                new_position = self.random.choice(possible_steps) if possible_steps else self.pos
                self.model.grid.move_agent(self, new_position)
        else:
            # Random move if happy with neighborhood
            possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False
            )
            if possible_steps:
                new_position = self.random.choice(possible_steps)
                self.model.grid.move_agent(self, new_position)