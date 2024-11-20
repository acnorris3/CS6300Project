import pandas as pd
import matplotlib.pyplot as plt

def generate_burndown_chart(file_path):
    # Load data
    data = pd.read_csv(file_path)

    # Parse date columns
    data['date_created'] = pd.to_datetime(data['date_created'])
    data['date_finished'] = pd.to_datetime(data['date_finished'], errors='coerce')  # Handle NaN for unfinished tasks

    # Calculate the timeline
    start_date = data['date_created'].min()
    end_date = max(data['date_finished'].max(), pd.Timestamp.today())
    timeline = pd.date_range(start=start_date, end=end_date)

    # Calculate remaining effort per day
    remaining_effort = []
    for day in timeline:
        # Sum estimates for tasks not finished by the given day
        effort = data.loc[
            (data['date_created'] <= day) & 
            ((data['date_finished'].isna()) | (data['date_finished'] > day)),
            'estimate'
        ].sum()
        remaining_effort.append(effort)

    # Ideal burndown line
    max_effort = sum(data['estimate'])
    ideal_burndown = [max_effort - (max_effort / (len(timeline) - 1)) * i for i in range(len(timeline))]

    # Plot the burndown chart
    plt.figure(figsize=(10, 6))
    plt.plot(timeline, remaining_effort, label="Actual Remaining Effort", marker="o", color="blue")
    plt.plot(timeline, ideal_burndown, label="Ideal Burndown", linestyle="--", color="orange")
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)  # Line at zero
    plt.title("Burndown Chart")
    plt.xlabel("Date")
    plt.ylabel("Remaining Effort")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()

generate_burndown_chart('scrum/BurndownData.csv')
