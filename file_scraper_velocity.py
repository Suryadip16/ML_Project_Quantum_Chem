import glob
import linecache
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def get_files(filename):
    currdir = os.getcwd()
    files = glob.iglob(filename,
                       root_dir=currdir)  # This creates an iterator object containing the filenames for all the required files in the path format
    return files


# The following piece of code iterates over all the files, opens each of them and based on a particular pattern extracts out
# the required values and appends them to the respective lists and dictionaries.

def get_file_data(files):
    vel_dict = {}
    time_step_dict = {}

    for i, file in enumerate(files):
        vel_list = []
        time_step_list = []
        with open(file) as f:
            for j, line in enumerate(f):
                if line.find('New velocity') > -1 or line.find('Initial velocity') > -1:
                    line_num = j
                    data = []

                    for x in range(2, 35):
                        vel_line = linecache.getline(filename=file, lineno=line_num + x)
                        vel = vel_line.strip().split()
                        vel = [float(v) for v in vel]
                        data.append(vel)
                    df = pd.DataFrame(data, columns=['v_x', 'v_y', 'v_z'])
                    vel_list.append(df)
                elif line.find('TIME') > -1:
                    line_num = j
                    time_line = linecache.getline(filename=file, lineno=line_num + 1)
                    time_step = time_line.strip().split()[9]
                    time_step = float(time_step)
                    time_step_list.append(time_step)
        vel_dict[file] = vel_list
        time_step_dict[file] = time_step_list
    return vel_dict, time_step_dict


# the following piece of code iterates over the 2 dictionaries and keeps only those keys(files) that have a time step of 0.5fs.
# The ones that have a time step of 0.5fs all start with the 1st time step as 0.5fs. that is the condition I am checking for here.


def filter_data(vel_dict, time_step_dict):
    final_key = None  # Initialize final_key as None
    time_step_filtered_dict = {}
    vel_filtered_dict = {}

    # Iterate through the keys of time_step_dict and vel_dict simultaneously
    for file_name1, file_name2 in zip(time_step_dict.keys(), vel_dict.keys()):
        # Check if the first value of the time_step_dict[file_name1] list is 0.5
        if time_step_dict[file_name1][0] == 0.5:
            time_step_filtered_dict[file_name1] = time_step_dict[file_name1]
            vel_filtered_dict[file_name2] = vel_dict[file_name2]

    print("Length of vel_filtered_dict:", len(vel_filtered_dict))
    print("Length of time_step_filtered_dict:", len(time_step_filtered_dict))

    min_length = float('inf')  # Use float('inf') as a large initial value for min_length
    for key in time_step_filtered_dict:
        size = len(time_step_filtered_dict[key])
        if size < min_length:
            min_length = size
            final_key = key

    print("Minimum length found:", min_length)
    print("Corresponding key with minimum length:", final_key)

    # Trim the lists in vel_filtered_dict and time_step_filtered_dict to min_length + 2
    for key1 in vel_filtered_dict:
        vel_filtered_dict[key1] = vel_filtered_dict[key1][:min_length + 2]

    for key2 in time_step_filtered_dict:
        time_step_filtered_dict[key2] = time_step_filtered_dict[key2][:min_length + 2]

    return vel_filtered_dict, time_step_filtered_dict


def atom_per_file(vel_filtered_dict):
    # Initialize a dictionary to store velocities for each file
    velocity_dict_per_file = {}

    # Iterate over each file and its corresponding list of DataFrames
    for file_name, df_list in vel_filtered_dict.items():
        # Initialize a list to store DataFrames for each atom
        atom_df_list = []

        # Iterate over each atom index
        for atom_index in range(33):
            # Initialize a list to store velocities for the current atom at different time steps
            velocity_list = []

            # Iterate over each DataFrame in df_list
            for data_frame in df_list:
                # Extract velocity of the current atom at the current time step
                velocity_of_atom = data_frame.iloc[atom_index].values.tolist()
                velocity_list.append(velocity_of_atom)  # Append velocity to the list

            # Convert the list of velocities into a DataFrame
            atom_df = pd.DataFrame(velocity_list, columns=['vx', 'vy', 'vz'])

            # Append the DataFrame for the current atom to the list
            atom_df_list.append(atom_df)

        # Store the list of DataFrames for each atom in the velocity dictionary for the current file
        velocity_dict_per_file[file_name] = atom_df_list
    return velocity_dict_per_file

    # Now velocity_dict_per_file contains DataFrames for each atom for each file


def compute_projections(dataframes):
    num_atoms = len(dataframes)
    num_time_steps = len(dataframes[0])  # Assuming all dataframes have the same length

    # Initialize DataFrame to store projections
    projections_df = pd.DataFrame(index=range(1, num_time_steps + 1))

    # Compute projections for each atom
    for atom_idx in range(num_atoms):
        atom_name = f'Atom {atom_idx + 1}'
        velocities = dataframes[atom_idx]  # DataFrame representing velocities of current atom

        # Take velocity vector at time step 1
        v1 = velocities.iloc[0].values

        # Compute dot products with velocity vector at time step 1
        dot_products = np.dot(velocities.values, v1)

        # Store dot products in projections DataFrame
        projections_df[atom_name] = dot_products

    return projections_df


def compute_all_projections(trajectory_data):
    projections_dict = {}

    # Process each trajectory in the input dictionary
    for trajectory, atom_dataframes in trajectory_data.items():
        projections_df = compute_projections(atom_dataframes)
        projections_dict[trajectory] = projections_df

    return projections_dict


# Averaging over all the trajectories for a single atom at a given time step


def average_projection(trajectory_dict):
    avg_projection_dict = {}
    for atom in range(33):
        avg_projection_dict[f'Atom{atom}'] = []
        for time_step in range(819):
            total_projection = 0
            num_trajectories = 0
            for trajectory in trajectory_dict:
                if time_step < len(trajectory_dict[trajectory]):
                    total_projection += trajectory_dict[trajectory].iloc[time_step][atom]
                    num_trajectories += 1
            if num_trajectories > 0:
                avg_projection_dict[f'Atom{atom}'].append(total_projection / num_trajectories)
            else:
                avg_projection_dict[f'Atom{atom}'].append(None)
    return avg_projection_dict


def plot_avg_projections(avg_projections_dict, time_step_filtered_dict):
    for atom in avg_projections_dict:
        y = avg_projections_dict[atom]
        x = time_step_filtered_dict["traj_results/TRAJ45/RESULTS/dyn.out"]
        plt.plot(x, y, marker="o")
        plt.xlabel("Time Step (fs)")
        plt.ylabel(f"Average Projection of Velocities of {atom} (averaged over all trajectories)")
        plt.title(f"Projection of Velocities of {atom} wrt Time Steps")
        plt.show()


def main():
    file_matcher = "traj_results/TRAJ*/RESULTS/dyn.out"
    files = get_files(file_matcher)
    vel_dict, time_step_dict = get_file_data(files)
    vel_filtered_dict, time_step_filtered_dict = filter_data(vel_dict, time_step_dict)
    vel_dict_per_file = atom_per_file(vel_filtered_dict)
    projections_result_dict = compute_all_projections(vel_dict_per_file)
    atom_avg_projections_over_traj = average_projection(projections_result_dict)
    print(len(atom_avg_projections_over_traj['Atom1']))
    print(len(time_step_filtered_dict["traj_results/TRAJ45/RESULTS/dyn.out"]))
    plot_avg_projections(atom_avg_projections_over_traj, time_step_filtered_dict)


if __name__ == '__main__':
    main()
