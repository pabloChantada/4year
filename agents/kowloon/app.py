from model import KowloonModel
import argparse

def save_data(data_model, data_agents):
    data_model.to_csv("./agents/plots/data_model.csv")
    data_agents.to_csv("./agents/plots/data_agents.csv")   

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Kowloon model")
    parser.add_argument("--steps", type=int, default=5, help="Number of steps to run the model")
    args = parser.parse_args()

    model = KowloonModel()

    for _ in range(args.steps):
        model.step()

    data_model = model.datacollector.get_model_vars_dataframe()
    data_agents = model.datacollector.get_agent_vars_dataframe()

    print("Data Model: ", data_model)
    print("Data Agents: ", data_agents)
    print("Total residents: ", data_model["Total residents"].tolist()[-1])

    save_data(data_model, data_agents)
    