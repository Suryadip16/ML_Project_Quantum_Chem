import glob
import linecache
import statistics
import matplotlib.pyplot as plt

files = glob.iglob("traj_results/TRAJ*/RESULTS/dyn.out", root_dir="/home/ibab/PycharmProjects/ML_Project_Semester2")

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
print(min_length)
print(final_key)
for key1, key2 in zip(e_pot_filtered_dict, time_step_filtered_dict):
    e_pot_filtered_dict[key1] = e_pot_filtered_dict[key1][:min_length + 2]
    time_step_filtered_dict[key2] = time_step_filtered_dict[key2][:min_length + 2]
#     print(len(time_step_filtered_dict[key2]))
# print("DONE")

# print(len(e_pot_dict))
print(len(time_step_filtered_dict["traj_results/TRAJ45/RESULTS/dyn.out"]))
print(len(e_pot_filtered_dict["traj_results/TRAJ45/RESULTS/dyn.out"]))

traj_epot_calculated_dict = {}
for key3 in e_pot_filtered_dict:
    traj_epot = e_pot_filtered_dict[key3]
    traj_epot_calculated_list = []
    items = len(traj_epot)
    for k in range(len(traj_epot)):
        val = traj_epot[0] * traj_epot[k]
        traj_epot_calculated_list.append(val)
    traj_epot_calculated_dict[key3] = traj_epot_calculated_list

#print(traj_epot_calculated_dict['traj_results/TRAJ3/RESULTS/dyn.out'])

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
# print(len(epot_avg))

y_axis = []
for h in range(len(epot_avg)):
    res = epot_avg[0] / epot_avg[h]
    y_axis.append(res)

# print(len(y_axis))
# print(y_axis[0])

x_axis = time_step_filtered_dict["traj_results/TRAJ45/RESULTS/dyn.out"]
# print(len(x_axis))
# print(x_axis)
print(x_axis)
print(y_axis)
# plt.plot(x_axis, y_axis, marker="o")
# plt.show()

# File Wise Comparison

time_axis = time_step_filtered_dict["traj_results/TRAJ45/RESULTS/dyn.out"]# enter file name in the following format "traj_results/TRAJ(n)/RESULTS/dyn.out" (here n is the trajectory number)
e_pot_individual = traj_epot_calculated_dict["traj_results/TRAJ45/RESULTS/dyn.out"]# enter same file name in the following format "traj_results/TRAJ(n)/RESULTS/dyn.out" (here n is the trajectory number)
e_pot_axis = []
for l in range(len(e_pot_individual)):
    res = e_pot_individual[0] / e_pot_individual[l]
    e_pot_axis.append(res)
print(e_pot_axis)
plt.plot(time_axis, e_pot_axis, marker="o")
plt.show()
















