The objective of file_scraper_epot.py is to take in the file names as an input and extract the required Potential Energy values and Time stamps from the respective files. 
Based on some exploratory analysis of the data, a few filtering strategies were used to make sure unformity of the Potential Energies across time stamps across Trajectories.
In order to run the code, make sure to keep the code in the same directory as the root directory provided as a parameter to the glob.iglob function.
Also make sure to store the data files or the directory structure containing the data files in the same root directory as mentioned above and edit the filename parameter of the glob.iglob function utility. 
For eg; if your code is in the directory, 'My_Dir', keep the directory structure (eg; traj_results/TRAJ*/RESULTS/dyn.out  ['*' stands for any fle staring from1 to 97]) in the same directory and run the code. 
Here the file in question is dyn.out. 

The final objective is to calculate the projections of each Potential Energy at each time step on the Potential Energy at time step 1 of 0.5 fs. 
We then average all projections at the nth time step (n goes from 1 to 819) across all 91 files to obtain the average projection at a given time step.
We plot these Average projections against time to get an idea about the time stamp at which the Potential Energy at one time stamp stops influencing the potential energy at the next time stamp.
