import os
import pandas as pd

directory_path = '../data/raw_results_from_tara/'

file_name1 = 'raw_energy_fcitc_results.csv'
file_name2 = 'raw_capacity_deliverability_results.csv'
file_path1 = os.path.join(directory_path, file_name1)
file_path2 = os.path.join(directory_path, file_name2)

energy_df = pd.read_csv(file_path1).rename(columns=str.strip)
capacity_df = pd.read_csv(file_path2).rename(columns=str.strip)

# Concatenate vertically the studied bus numbers from both energy and capacity studies into a single DataFrame
study_bus_final_df = pd.concat([energy_df['Sending System'].str.extract(r'^(\d+)', expand=False),
    capacity_df['Study Bus'].str.extract(r'^(\d+)', expand=False)
], axis=0, ignore_index=True).astype(int).to_frame(name='study_bus')

# Concatenate vertically the 'Monitored Facility' columns from both energy and capacity studies into a single DataFrame
monitored_facility_final_df = pd.concat([energy_df['Monitored Facility'].str.strip(),capacity_df['Monitored Facility'].str.strip()], axis=0, ignore_index=True)

# Concatenate vertically the 'Cont Name' columns from both energy and capacity studies into a single DataFrame
contingency_name_final_df = pd.concat([energy_df['Cont Name'].str.strip(),capacity_df['Cont Name'].str.strip()], axis=0, ignore_index=True)

def applicable_rating(row):
    return row['Rate Base'] if row['Cont Name'] == 'Base Case' else row['Rate Cont']

energy_df['applicable_rating'] = energy_df.apply(applicable_rating, axis=1).astype(float)
capacity_df['applicable_rating'] = capacity_df.apply(applicable_rating, axis=1).astype(float)

# Concatenate vertically the 'applicable_rating' columns into a single DataFrame
applicable_rating_final_df = pd.concat([energy_df['applicable_rating'],capacity_df['applicable_rating']], axis=0, ignore_index=True)

# Calculate injection threshold for energy
energy_df['injection_threshold'] = energy_df['TrLim'].apply(lambda x: max(0, x)).astype(float)

# Define the function to calculate injection threshold for capacity
def calculate_injection_threshold_capacity(row):
    if row['Cont Name'] == 'Base Case':
        return 2000+((row['Rate Base'] - row['Final DC Loading'] - row['Study Bus MW Impact']) / (row['Study Bus MW Impact'] / 2000))
    else:
        return 2000+((row['Rate Cont'] - row['Final DC Loading'] - row['Study Bus MW Impact']) / (row['Study Bus MW Impact'] / 2000))


# Apply the function to calculate injection threshold for capacity DataFrame
capacity_df['injection_threshold'] = capacity_df.apply(calculate_injection_threshold_capacity, axis=1).astype(float)

# Concatenate vertically the 'injection_threshold' for energy and capacity into a single DataFrame
Injection_threshold_final_df = pd.concat([energy_df['injection_threshold'], capacity_df['injection_threshold']], axis=0, ignore_index=True).to_frame(name='Injection_threshold')

# Concatenate all final DataFrames horizontally
final_df = pd.concat([study_bus_final_df, monitored_facility_final_df, Injection_threshold_final_df,contingency_name_final_df, applicable_rating_final_df], axis=1)

# Add a new column 'resource_type' to final_df
final_df['resource_type'] = ['energy'] * len(energy_df) + ['capacity'] * len(capacity_df)

# Group by unique combination of study bus, monitored facility, and resource type
grouped_df = final_df.groupby(['study_bus', 'Monitored Facility', 'resource_type'])

# Get the index of the row with the lowest injection threshold for each group
min_indices = grouped_df['Injection_threshold'].idxmin()

# Filter the DataFrame to keep only the rows with the lowest injection threshold for each group
filtered_df = final_df.loc[min_indices]

filtered_df.to_csv(r'../outputs/constraints.csv', index=False)

rows = []
for bus in filtered_df['study_bus'].unique():
    filtered_subset = filtered_df[filtered_df['study_bus'] == bus]

    for size in range(0, 1001, 10):
        num_constraints_energy = ((filtered_subset['Injection_threshold'] >= ((size-10)+0.1)) &
                                  (filtered_subset['Injection_threshold'] <= size ) &
                                  (filtered_subset['resource_type'] == 'energy')).sum()
#Note:Iterating the filtered_subset over the resource type is less optimized but more efficient for accessing the number of constraints
#for capacity_size and energy_size individually if needed

        rows.append(
            {'study_bus': bus, 'size': size, 'number_of_constraints_energy': num_constraints_energy})

# Create the DataFrame from the list of rows
energy_constraints_df = pd.DataFrame(rows)

rows_capacity = []
for bus in filtered_df['study_bus'].unique():
    filtered_subset_capacity = filtered_df[filtered_df['study_bus'] == bus]

    for size in range(0, 1001, 10):
        num_constraints_capacity = ((filtered_subset_capacity['Injection_threshold'] >= ((size-10)+0.1)) &
                                    (filtered_subset_capacity['Injection_threshold'] <= size) &
                                    (filtered_subset_capacity['resource_type'] == 'capacity')).sum()

        rows_capacity.append({'study_bus': bus, 'size': size,
                              'number_of_constraints_capacity': num_constraints_capacity})
capacity_constraints_df = pd.DataFrame(rows_capacity)

# Merge energy_constraints_df and capacity_constraints_df on 'study_bus' and 'size'
summary_results = pd.merge(energy_constraints_df, capacity_constraints_df, on=['study_bus', 'size'], how='outer')

summary_results['number_of_constraints'] = summary_results['number_of_constraints_energy'] + summary_results['number_of_constraints_capacity']
# Note:The number_of_constraints column counts the energy and capacity constraints present within the range of the previous size excluded and the current size included.

summary_results.drop(['number_of_constraints_capacity', 'number_of_constraints_energy'], axis=1, inplace=True)

summary_results['energy_size'] = summary_results['size']

summary_results['capacity_size'] = summary_results['size']

summary_results.drop('size', axis=1, inplace=True)

# Move the 'number_of_constraints' column to the last position
cols = list(summary_results.columns)
cols.remove('number_of_constraints')
cols.append('number_of_constraints')
summary_results = summary_results[cols]

summary_results.to_csv(r'../outputs/summary_results.csv', index=False)

