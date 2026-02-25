import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import ast

def plot_neighborhoods(csv="agents/plots/data_agents.csv", grid_size=400, num_snapshots=6):
    df = pd.read_csv(csv)
    df['pos'] = df['pos'].apply(ast.literal_eval)  # Parse "(x, y)" strings to tuples
    df['x'] = df['pos'].apply(lambda p: p[0])
    df['y'] = df['pos'].apply(lambda p: p[1])

    steps = sorted(df['Step'].unique())
    # Pick evenly spaced steps for snapshots
    indices = [int(i * (len(steps) - 1) / (num_snapshots - 1)) for i in range(num_snapshots)]
    selected_steps = [steps[i] for i in indices]

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    colors = {"White": "#2ecc71", "Black": "#2c3e50"}

    for idx, step in enumerate(selected_steps):
        ax = axes[idx]
        step_data = df[df['Step'] == step]

        # Draw grid
        ax.set_xlim(-0.5, grid_size - 0.5)
        ax.set_ylim(-0.5, grid_size - 0.5)
        ax.set_aspect('equal')
        ax.set_xticks(range(0, grid_size, 5))
        ax.set_yticks(range(0, grid_size, 5))
        ax.grid(True, alpha=0.2, linewidth=0.5)

        # Plot agents
        for _, row in step_data.iterrows():
            color = colors.get(row['agent_type'], 'gray')
            ax.scatter(row['x'], row['y'], c=color, s=40, alpha=0.8, edgecolors='white', linewidth=0.5)

        white_count = len(step_data[step_data['agent_type'] == 'White'])
        black_count = len(step_data[step_data['agent_type'] == 'Black'])
        ax.set_title(f"Step {int(step)} (W:{white_count} B:{black_count})", fontsize=11)

    # Legend
    legend_patches = [
        mpatches.Patch(color=colors["White"], label="White"),
        mpatches.Patch(color=colors["Black"], label="Black"),
    ]
    fig.legend(handles=legend_patches, loc='lower center', ncol=2, fontsize=12)
    fig.suptitle("Neighborhood Segregation Over Time", fontsize=14, fontweight='bold')
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    plot_neighborhoods()
