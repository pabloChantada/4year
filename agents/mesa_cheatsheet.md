# Python Mesa - Cheatsheet

## Instalación
```bash
pip install mesa
```

## Estructura Básica

### 1. Modelo (Model)
```python
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class MiModelo(Model):
    def __init__(self, N, width, height):
        super().__init__()
        self.num_agents = N
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        
        # DataCollector para métricas
        self.datacollector = DataCollector(
            model_reporters={"Total": lambda m: m.schedule.get_agent_count()},
            agent_reporters={"Wealth": "wealth"}
        )
        
        # Crear agentes
        for i in range(self.num_agents):
            a = MiAgente(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
    
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
```

### 2. Agente (Agent)
```python
from mesa import Agent

class MiAgente(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1
    
    def step(self):
        self.move()
        self.do_something()
    
    def move(self):
        # Movimiento aleatorio
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
```

## Schedulers (Orden de Activación)

### RandomActivation
```python
from mesa.time import RandomActivation
self.schedule = RandomActivation(self)
```
Activa agentes en orden aleatorio cada step.

### SimultaneousActivation
```python
from mesa.time import SimultaneousActivation
self.schedule = SimultaneousActivation(self)
```
Primero llama a `step()` de todos, luego `advance()` para aplicar cambios simultáneos.

### StagedActivation
```python
from mesa.time import StagedActivation
self.schedule = StagedActivation(self, stage_list=["stage1", "stage2"])
```
Ejecuta métodos de agentes por etapas definidas.

### BaseScheduler
```python
from mesa.time import BaseScheduler
self.schedule = BaseScheduler(self)
```
Activa agentes en el orden en que fueron agregados.

## Espacios (Space)

### MultiGrid
```python
from mesa.space import MultiGrid
self.grid = MultiGrid(width, height, torus=True)
```
Permite múltiples agentes por celda.

### SingleGrid
```python
from mesa.space import SingleGrid
self.grid = SingleGrid(width, height, torus=False)
```
Solo un agente por celda.

### ContinuousSpace
```python
from mesa.space import ContinuousSpace
self.space = ContinuousSpace(x_max, y_max, torus=True, 
                             x_min=0, y_min=0)
```
Espacio continuo con coordenadas flotantes.

### NetworkGrid
```python
from mesa.space import NetworkGrid
import networkx as nx

G = nx.erdos_renyi_graph(n=30, p=0.2)
self.grid = NetworkGrid(G)
```
Para modelos basados en redes/grafos.

## Métodos de Grid

### Colocar y Mover Agentes
```python
# Colocar agente
self.grid.place_agent(agent, (x, y))

# Mover agente
self.grid.move_agent(agent, (new_x, new_y))

# Remover agente
self.grid.remove_agent(agent)

# Mover a celda vacía
self.grid.move_to_empty(agent)
```

### Consultar Grid
```python
# Obtener agentes en posición
agents = self.grid.get_cell_list_contents([(x, y)])

# Obtener vecindad (Moore: 8 vecinos, Von Neumann: 4 vecinos)
neighbors = self.grid.get_neighborhood(
    pos=(x, y),
    moore=True,  # False para Von Neumann
    include_center=False,
    radius=1
)

# Obtener vecinos (agentes)
neighbor_agents = self.grid.get_neighbors(
    pos=(x, y),
    moore=True,
    include_center=False,
    radius=1
)

# Verificar si celda está vacía
is_empty = self.grid.is_cell_empty((x, y))

# Obtener todas las celdas vacías
empty_cells = self.grid.empties
```

## DataCollector (Recolección de Datos)

```python
from mesa.datacollection import DataCollector

self.datacollector = DataCollector(
    # Métricas del modelo
    model_reporters={
        "Total Agents": lambda m: m.schedule.get_agent_count(),
        "Avg Wealth": lambda m: sum([a.wealth for a in m.schedule.agents]) / m.schedule.get_agent_count()
    },
    # Métricas por agente
    agent_reporters={
        "Wealth": "wealth",  # Atributo directo
        "Position": lambda a: a.pos  # Función
    }
)

# Recolectar datos en cada step
self.datacollector.collect(self)

# Obtener datos como DataFrame
model_data = self.datacollector.get_model_vars_dataframe()
agent_data = self.datacollector.get_agent_vars_dataframe()
```

## Visualización

### Servidor de Visualización
```python
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "Color": "red",
        "r": 0.5
    }
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

chart = ChartModule([
    {"Label": "Total", "Color": "Black"}
], data_collector_name='datacollector')

server = ModularServer(
    MiModelo,
    [grid, chart],
    "Mi Modelo",
    {"N": 10, "width": 10, "height": 10}
)

server.port = 8521
server.launch()
```

### Shapes Disponibles para Portrayal
```python
# Círculo
{"Shape": "circle", "r": 0.5, "Filled": "true", "Color": "red"}

# Rectángulo
{"Shape": "rect", "w": 0.8, "h": 0.8, "Filled": "true", "Color": "blue"}

# Arrowhead (flecha)
{"Shape": "arrowHead", "scale": 0.8, "heading_x": 1, "heading_y": 0, "Color": "green"}
```

## Batch Run (Experimentos)

```python
from mesa.batchrunner import batch_run
import pandas as pd

params = {
    "N": range(10, 100, 10),
    "width": 10,
    "height": 10
}

results = batch_run(
    MiModelo,
    parameters=params,
    iterations=5,
    max_steps=100,
    number_processes=1,
    data_collection_period=1,
    display_progress=True
)

df = pd.DataFrame(results)
```

## Acceso Aleatorio (Random)

```python
# En el modelo o agente
self.random.random()  # Float entre 0 y 1
self.random.randrange(start, stop)  # Entero
self.random.choice(sequence)  # Elemento aleatorio
self.random.shuffle(list)  # Mezclar lista
self.random.sample(population, k)  # k elementos sin reemplazo
```

## Métodos Útiles del Schedule

```python
# Agregar agente
self.schedule.add(agent)

# Remover agente
self.schedule.remove(agent)

# Avanzar un step
self.schedule.step()

# Obtener todos los agentes
all_agents = self.schedule.agents

# Contar agentes
count = self.schedule.get_agent_count()

# Obtener agente por ID
agent = self.schedule._agents[unique_id]
```

## Remover Agentes Durante Simulación

```python
# En el método step del agente
def step(self):
    if self.should_die():
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)
```

## Propiedades Útiles

```python
# En el agente
self.unique_id  # ID único del agente
self.model  # Referencia al modelo
self.pos  # Posición actual (si usa grid)

# En el modelo
self.running  # Boolean para controlar la simulación
self.schedule.steps  # Número de steps ejecutados
```

## Ejemplo Completo: Modelo de Boloney

```python
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class MoneyAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1
    
    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_money()
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
    
    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1

class MoneyModel(Model):
    def __init__(self, N, width, height):
        super().__init__()
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        
        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Wealth": "wealth"}
        )
        
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
    
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B
```

## Tips y Buenas Prácticas

1. **Siempre usa `super().__init__()`** al crear Model o Agent
2. **`self.running = True`** en el modelo para controlar la simulación
3. **Usa `self.random`** en lugar de `random` global para reproducibilidad
4. **DataCollector.collect()** debe llamarse ANTES de `schedule.step()`
5. **Para quitar agentes**, elimínalos del schedule Y del grid
6. **Usa `torus=True`** en grids para wrap-around (mundo toroidal)
7. **Moore=True** son 8 vecinos, **Moore=False** (Von Neumann) son 4
8. **batch_run** es mejor que loops manuales para experimentos

## Referencias

- Documentación oficial: https://mesa.readthedocs.io/
- Ejemplos: https://github.com/projectmesa/mesa-examples
- Tutorial introductorio: https://mesa.readthedocs.io/en/stable/tutorials/intro_tutorial.html
