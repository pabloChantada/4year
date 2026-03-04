import mesa
import random
from agent import BaseAgent

'''
TODO: MODULARIZAR CORRECTAMENTE, LOS CHECK SOLO DEBERIAN COMPROBAR
NO EJECUTAR NADA, SOLO DEVOLVER UNA LISTA DE AGENTES A REPRODUCIR O ELIMINAR
'''

class KowloonModel(mesa.Model):
    def __init__(self, width=200, height=200, num_agents=100):
        super().__init__()
        self.race_chance = 50  # Chance for an agent to be "White" (0-100)
        self.num_agents = num_agents
        self.agents_eliminated_count = 0  # Track total agents eliminated
        # Torus makes the grid finite
        self.grid = mesa.space.MultiGrid(width, height, torus=True)

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Total residents": lambda m: sum(
                    1 for a in m.agents if isinstance(a, BaseAgent)
                ),
                "White residents": lambda m: sum(
                    1 for a in m.agents if isinstance(a, BaseAgent) and a.agent_type == "White"
                ),
                "Black residents": lambda m: sum(
                    1 for a in m.agents if isinstance(a, BaseAgent) and a.agent_type == "Black"
                ),
                "Agents eliminated": lambda m: m.agents_eliminated_count,
            },
            agent_reporters={
                "agent_type": "agent_type",
                "pos": "pos",
            }
        )
        for _ in range(self.num_agents):
            agent_type = "White" if random.randint(0, 100) < self.race_chance else "Black"
            a = BaseAgent(self, agent_type=agent_type)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
    
    def _check_reproduction(self):
        agents_to_reproduce = [a for a in self.agents if
                               getattr(a, 'should_reproduce', False)]
        for agent in agents_to_reproduce:
            new_agent = BaseAgent(self, agent_type=agent.agent_type)
            # Place in a nearby random cell
            possible_positions = self.grid.get_neighborhood(
                agent.pos, moore=True, include_center=False
            )
            if possible_positions:
                new_pos = self.random.choice(possible_positions)
                self.grid.place_agent(new_agent, new_pos)
            else:
                # Fallback: place at agent's current position if no neighbors
                self.grid.place_agent(new_agent, agent.pos)
            agent.should_reproduce = False  # Reset reproduction flag

    def _check_racism(self):
        """Remove agents who are isolated minorities in their neighborhood"""
        agents_to_remove = []
        
        for agent in self.agents:
            # Get neighborhood (3 cells radius)
            neighborhood = []
            x, y = agent.pos
            distance = 3
            for i in range(x - distance, x + distance + 1):
                for j in range(y - distance, y + distance + 1):
                    if (i, j) != agent.pos:
                        wrapped_x = i % self.grid.width
                        wrapped_y = j % self.grid.height
                        agents_in_cell = self.grid.get_cell_list_contents((wrapped_x, wrapped_y))
                        neighborhood.extend(agents_in_cell)
            
            if neighborhood:
                same_type = sum(1 for n in neighborhood if n.agent_type == agent.agent_type)
                total = len(neighborhood)
                similarity_ratio = same_type / total if total > 0 else 0.5
                
                # If you're less than 20% of your neighborhood AND there are >5 neighbors
                # you have a chance to be eliminated
                if similarity_ratio < 0.2 and total > 5:
                    if self.random.random() < 0.3:  # 30% chance if isolated
                        agents_to_remove.append(agent)
        
        for agent in agents_to_remove:
            self.agents_eliminated_count += 1
            self.grid.remove_agent(agent)
            agent.remove()
    
    def step(self):
        self.agents.shuffle_do("step")
        self._check_reproduction()  # Check reproduction after all agents moved
        self._check_racism()  # Remove agents with neighbors of different type
        self.datacollector.collect(self)  # Collect data after all changes
        
        # Print progress
        total = len([a for a in self.agents if isinstance(a, BaseAgent)])
        white = len([a for a in self.agents if isinstance(a, BaseAgent) and a.agent_type == "White"])
        black = len([a for a in self.agents if isinstance(a, BaseAgent) and a.agent_type == "Black"])
        print(f"Step {self.time}: Total={total}, White={white}, Black={black}, Eliminated={self.agents_eliminated_count}")

