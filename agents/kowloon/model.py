import mesa
import random
from agent import BaseAgent

'''
TODO: MODULARIZAR CORRECTAMENTE, LOS CHECK SOLO DEBERIAN COMPROBAR
NO EJECUTAR NADA, SOLO DEVOLVER UNA LISTA DE AGENTES A REPRODUCIR O ELIMINAR

'''
class KowloonModel(mesa.Model):
    def __init__(self, width=20, height=20, num_agents=10):
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
            # Place near parent or random empty cell
            self.grid.place_agent(new_agent, agent.pos)
            agent.should_reproduce = False  # Reset reproduction flag

    def _check_racism(self):
        agents_to_remove = []
        for agent in self.agents:
            if hasattr(agent, '_get_neighbors'):
                neighbors = agent._get_neighbors()
                if neighbors:
                    if any(neighbor.agent_type != agent.agent_type for neighbor in neighbors):
                        if self.random.random() < 0.1:  # 30% chance to be eliminated if has different-type neighbors
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

