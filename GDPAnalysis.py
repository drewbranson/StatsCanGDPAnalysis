import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Function to read industries from a file
def read_industries(file_path):
    with open(file_path, 'r') as file:
        industries = [line.strip() for line in file.readlines()]
    return industries

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Plot industry values over time.')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file containing the data.')
    parser.add_argument('industries_file', type=str, help='Path to the text file containing the list of industries.')
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Load the data into a pandas DataFrame
    df = pd.read_csv(args.csv_file)

    # Strip any whitespace from the column names
    df.columns = df.columns.str.strip()

    # Convert the 'REF_DATE' column to datetime format
    df['REF_DATE'] = pd.to_datetime(df['REF_DATE'], format='%Y-%m')

    # Filter relevant columns
    df_filtered = df[['REF_DATE', 'North American Industry Classification System (NAICS)', 'VALUE']]

    # Rename columns for easier access
    df_filtered.columns = ['Date', 'Industry', 'Value']

    # Extract unique industries
    unique_industries = df_filtered['Industry'].unique()

    # Save the unique industries to a text file
    with open('unique_industries.txt', 'w') as f:
        for industry in unique_industries:
            f.write(f"{industry}\n")

    print("Unique industries have been saved to 'unique_industries.txt'.")

    # Read the list of industries from the specified text file
    selected_industries = read_industries(args.industries_file)

    # Filter the DataFrame to include only the selected industries
    df_filtered_industries = df_filtered[df_filtered['Industry'].isin(selected_industries)]

    # Group by 'Date' and 'Industry' and sum the values to handle duplicates
    df_grouped = df_filtered_industries.groupby(['Date', 'Industry']).sum().reset_index()

    # Pivot the DataFrame to have industries as columns and dates as rows
    df_pivot = df_grouped.pivot(index='Date', columns='Industry', values='Value')

    # Calculate the final value for each industry
    final_values = df_pivot.iloc[-1].sort_values(ascending=False)

    # Plotting the data
    plt.figure(figsize=(14, 8))

    # Plot each industry, sorted by final value
    for industry in final_values.index:
        plt.plot(df_pivot.index, df_pivot[industry], label=f"{industry} (${final_values[industry]:.2f})")

    # Customize the plot
    plt.title('Industry Values Over Time')
    plt.xlabel('Date')
    plt.ylabel('Value (millions of dollars)')
    plt.legend(loc='upper left')  # Move the legend to the top left
    plt.grid(True)

    # Show the plot
    plt.show()

if __name__ == '__main__':
    main()