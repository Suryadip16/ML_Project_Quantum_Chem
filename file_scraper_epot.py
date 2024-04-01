import glob
import linecache
import statistics
import matplotlib.pyplot as plt
import os


def get_files(filename):
    currdir = os.getcwd()
    files = glob.iglob(filename, root_dir=currdir)  # This creates an iterator object containing the filenames for all the required files in the path format.
    return files


# The following piece of code iterates over all the files, opens each of them and based on a particular pattern extracts out
# the required values and appends them to the respective lists and dictionaries.

def get_file_data(files):
    e_pot_dict = {}
    time_step_dict = {}

    for i, file in enumerate(files, 1):
        e_pot_list = []
        time_step_list = []
        with open(file=file) as f:
            for i, line in enumerate(f):
                if line.find('Ekin') > -1:
                    line_num = i
                    pot_line = linecache.getline(filename=file, lineno=line_num + 2)
                    e_pot = pot_line.strip().split()[3]
                    e_pot = float(e_pot)
                    e_pot_list.append(e_pot)
                elif line.find('TIME') > -1:
                    line_num = i
                    time_line = linecache.getline(filename=file, lineno=line_num + 1)
                    time_step = time_line.strip().split()[9]
                    time_step = float(time_step)
                    time_step_list.append(time_step)

        e_pot_dict[file] = e_pot_list
        time_step_dict[file] = time_step_list
    return e_pot_dict, time_step_dict


# At this stage of the code, we have 2 dictionaries. Each dictionary has the file names in the format
# "traj_results/TRAJ*/RESULTS/dyn.out" where * is 1 to 97 as the keys. The e_pot_dict contains the associated e_pot values
# with each file at each time step in ascending order of time steps. The time_step_dict contains the associated time step values
# in ascending order.

# the following piece of code iterates over the 2 dictionaries and keeps only those keys(files) that have a time step of 0.5fs.
# The ones that have a time step of 0.5fs all start with the 1st time step as 0.5fs. that is the condition I am checking for here.

def filter_data(e_pot_dict, time_step_dict):
    time_step_filtered_dict = {}
    e_pot_filtered_dict = {}
    for file_name1, file_name2 in zip(time_step_dict, e_pot_dict):
        if time_step_dict[file_name1][0] == 0.5:
            time_step_filtered_dict[file_name1] = time_step_dict[file_name1]
            e_pot_filtered_dict[file_name2] = e_pot_dict[file_name2]

    # print(len(time_step_filtered_dict))
    # print(len(e_pot_filtered_dict))
    # print(time_step_filtered_dict["traj_results/TRAJ26/RESULTS/dyn.out"])

    # print(len(e_pot_dict))
    # print(len(time_step_dict))
    min_length = 200000000
    for key in time_step_filtered_dict:
        size = len(time_step_filtered_dict[key])
        if size < min_length:
            min_length = size
            final_key = key
    # print(min_length)
    # print(final_key)
    for key1, key2 in zip(e_pot_filtered_dict, time_step_filtered_dict):
        e_pot_filtered_dict[key1] = e_pot_filtered_dict[key1][:min_length + 2]
        time_step_filtered_dict[key2] = time_step_filtered_dict[key2][:min_length + 2]
    #     print(len(time_step_filtered_dict[key2]))
    # print("DONE")

    # print(len(e_pot_dict))
    # print(len(time_step_filtered_dict["traj_results/TRAJ45/RESULTS/dyn.out"]))
    # print(time_step_filtered_dict["traj_results/TRAJ45/RESULTS/dyn.out"][818])
    return e_pot_filtered_dict, time_step_filtered_dict


# the next piece of code calculates the projection of each potential energy on the initial potential energy at time step 0.5fs and appends it to a dictionary
# with keys as file names and values as the list of all the projections associated with each file.

def calculate_projection(e_pot_filtered_dict):
    traj_epot_calculated_dict = {}
    for key3 in e_pot_filtered_dict:
        traj_epot = e_pot_filtered_dict[key3]
        traj_epot_calculated_list = []
        for k in range(len(traj_epot)):
            val = traj_epot[0] * traj_epot[k]
            traj_epot_calculated_list.append(val)
        traj_epot_calculated_dict[key3] = traj_epot_calculated_list

    # print(traj_epot_calculated_dict['traj_results/TRAJ3/RESULTS/dyn.out'])

    # At this point once again, we have 2 dictionaries. One with the keys as file names and values as the list of all respective projections.
    # Another with the keys as file names and values as the list of all respective time steps going from 0.5fs to 408.5fs.
    # Now instead of this, I want a dictionary having 819 keys with each key being designated as "e_pot_n". Each key will contain a list of values
    # from the nth time step across all the 91 files, so that we can average the e_pot at the 1st time step over all files, average e_pot over the 2nd time step over all files,
    # and generally average e_pot over the nth step across all file,

    traj_epot_transformed_dict = {}
    for key, values in traj_epot_calculated_dict.items():
        for i, value in enumerate(values):
            new_key = f"e_pot_{i}"
            if new_key not in traj_epot_transformed_dict:
                traj_epot_transformed_dict[new_key] = []
            traj_epot_transformed_dict[new_key].append(value)

    # print(len(traj_epot_transformed_dict))
    # for each_key in traj_epot_transformed_dict:
    #     print(len(traj_epot_transformed_dict[each_key]))

    epot_avg = []
    for each_key in traj_epot_transformed_dict:
        avg_val = statistics.mean(traj_epot_transformed_dict[each_key])
        epot_avg.append(avg_val)
    return epot_avg, traj_epot_calculated_dict
    # print(len(epot_avg))


def plot(x, y):
    y_axis = []
    for h in range(len(y)):
        res = y[0] / y[h]
        y_axis.append(res)
    plt.plot(x, y_axis, marker="o")
    plt.show()


def main():
    file_matcher = "traj_results/TRAJ*/RESULTS/dyn.out"
    files = get_files(file_matcher)
    e_pot_dict, time_step_dict = get_file_data(files)
    e_pot_filtered_dict, time_step_filtered_dict = filter_data(e_pot_dict, time_step_dict)
    e_pot_avg, traj_epot_individual_file = calculate_projection(e_pot_filtered_dict)
    y = e_pot_avg
    # or for File Wise Comparison
    # y = traj_epot_individual_file["traj_results/TRAJ45/RESULTS/dyn.out"]  # enter file name in the following format "traj_results/TRAJ(n)/RESULTS/dyn.out" (here n is the trajectory number)
    x = time_step_filtered_dict[
        "traj_results/TRAJ45/RESULTS/dyn.out"]  # enter file name in the following format "traj_results/TRAJ(n)/RESULTS/dyn.out" (here n is the trajectory number)
    plot(x, y)


if __name__ == '__main__':
    main()
