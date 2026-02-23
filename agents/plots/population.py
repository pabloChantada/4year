import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_population(csv="agents/plots/data_model.csv", title="Population Distribution"):
    if csv:
        df = pd.read_csv(csv)
        population = df['Total residents'].tolist()
        whites = df['White residents'].tolist()
        blacks = df['Black residents'].tolist()
        agents_eliminated = df['Agents eliminated'].tolist()
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(population)), population, color='blue')
    plt.plot(range(len(population)), whites, 'o', color='green')
    plt.plot(range(len(population)), blacks, 'o', color='black')
    plt.plot(range(len(population)), agents_eliminated, 'o', color='red')

    plt.xlabel('Steps')
    plt.ylabel('Population Count')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.legend(["Total ", "White residents", "Black residents", "Agents eliminated"])
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_population()