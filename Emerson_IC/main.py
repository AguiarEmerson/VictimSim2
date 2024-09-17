import sys
import os
import time

## importa classes
from vs.environment import Env
from explorer import Explorer
from rescuer import Rescuer

def main(data_folder_name):
   
    # Set the path to config files and data files for the environment
    current_folder = os.path.abspath(os.getcwd())
    data_folder = os.path.abspath(os.path.join(current_folder, data_folder_name))

    
    # Instantiate the environment
    env = Env(data_folder)
    
    # config files for the agents
    rescuer_file = os.path.join(data_folder, "rescuer_config.txt")
    explorer_file1 = os.path.join(data_folder, "explorer_config1.txt")
    explorer_file2 = os.path.join(data_folder, "explorer_config2.txt")
    explorer_file3 = os.path.join(data_folder, "explorer_config3.txt")
    explorer_file4 = os.path.join(data_folder, "explorer_config4.txt")
    explorer_file5 = os.path.join(data_folder, "explorer_config5.txt")
    explorer_file6 = os.path.join(data_folder, "explorer_config6.txt")
    explorer_file7 = os.path.join(data_folder, "explorer_config7.txt")
    explorer_file8 = os.path.join(data_folder, "explorer_config8.txt")
    '''explorer_file9 = os.path.join(data_folder, "explorer_config9.txt")
    explorer_file10 = os.path.join(data_folder, "explorer_config10.txt")
    explorer_file11 = os.path.join(data_folder, "explorer_config11.txt")
    explorer_file12 = os.path.join(data_folder, "explorer_config12.txt")
    explorer_file13 = os.path.join(data_folder, "explorer_config13.txt")
    explorer_file14 = os.path.join(data_folder, "explorer_config14.txt")
    explorer_file15 = os.path.join(data_folder, "explorer_config15.txt")
    explorer_file16 = os.path.join(data_folder, "explorer_config16.txt")
    explorer_file17 = os.path.join(data_folder, "explorer_config17.txt")
    explorer_file18 = os.path.join(data_folder, "explorer_config18.txt")
    explorer_file19 = os.path.join(data_folder, "explorer_config19.txt")
    explorer_file20 = os.path.join(data_folder, "explorer_config20.txt")
    explorer_file21 = os.path.join(data_folder, "explorer_config21.txt")
    explorer_file22 = os.path.join(data_folder, "explorer_config22.txt")
    explorer_file23 = os.path.join(data_folder, "explorer_config23.txt")
    explorer_file24 = os.path.join(data_folder, "explorer_config24.txt")
    explorer_file25 = os.path.join(data_folder, "explorer_config25.txt")
    explorer_file26 = os.path.join(data_folder, "explorer_config26.txt")
    explorer_file27 = os.path.join(data_folder, "explorer_config27.txt")
    explorer_file28 = os.path.join(data_folder, "explorer_config28.txt")
    explorer_file29 = os.path.join(data_folder, "explorer_config29.txt")
    explorer_file30 = os.path.join(data_folder, "explorer_config30.txt")
    explorer_file31 = os.path.join(data_folder, "explorer_config31.txt")
    explorer_file32 = os.path.join(data_folder, "explorer_config32.txt")'''

    # Instantiate agents rescuer and explorer
    resc = Rescuer(env, rescuer_file)

    # Explorer needs to know rescuer to send the map
    # that's why rescuer is instatiated before
    exp1 = Explorer(env, explorer_file1, resc)
    exp2 = Explorer(env, explorer_file2, resc)
    exp3 = Explorer(env, explorer_file3, resc)
    exp4 = Explorer(env, explorer_file4, resc)
    exp5 = Explorer(env, explorer_file5, resc)
    exp6 = Explorer(env, explorer_file6, resc)
    exp7 = Explorer(env, explorer_file7, resc)
    exp8 = Explorer(env, explorer_file8, resc)
    '''exp9 = Explorer(env, explorer_file9, resc)
    exp10 = Explorer(env, explorer_file10, resc)
    exp11 = Explorer(env, explorer_file11, resc)
    exp12 = Explorer(env, explorer_file12, resc)
    exp13 = Explorer(env, explorer_file13, resc)
    exp14 = Explorer(env, explorer_file14, resc)
    exp15 = Explorer(env, explorer_file15, resc)
    exp16 = Explorer(env, explorer_file16, resc)
    exp17 = Explorer(env, explorer_file17, resc)
    exp18 = Explorer(env, explorer_file18, resc)
    exp19 = Explorer(env, explorer_file19, resc)
    exp20 = Explorer(env, explorer_file20, resc)
    exp21 = Explorer(env, explorer_file21, resc)
    exp22 = Explorer(env, explorer_file22, resc)
    exp23 = Explorer(env, explorer_file23, resc)
    exp24 = Explorer(env, explorer_file24, resc)
    exp25 = Explorer(env, explorer_file25, resc)
    exp26 = Explorer(env, explorer_file26, resc)
    exp27 = Explorer(env, explorer_file27, resc)
    exp28 = Explorer(env, explorer_file28, resc)
    exp29 = Explorer(env, explorer_file29, resc)
    exp30 = Explorer(env, explorer_file30, resc)
    exp31 = Explorer(env, explorer_file31, resc)
    exp32 = Explorer(env, explorer_file32, resc)'''
    
    # Run the environment simulator
    env.run()
    env.total_moves()
    
        
if __name__ == '__main__':
    """ To get data from a different folder than the default called data
    pass it by the argument line"""
    
    if len(sys.argv) > 1:
        data_folder_name = sys.argv[1]
    else:
        data_folder_name = os.path.join("datasets", "data_test")
        
    main(data_folder_name)
