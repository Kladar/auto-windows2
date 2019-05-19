import pandas as pd
import requests
# import darksky
# import pendulum
import seaborn as sns

def simple_house_no_windows(data):
    df = pd.read_csv(data)

    indoor_real_temps = [60]
    furnace_bools = []
    ac_bools = []

    for index, row in df.iterrows():
        if indoor_real_temps[index] == row['Indoor Temp Goal']:
            furnace_bools.append(0)
            ac_bools.append(0)

            increment = indoor_real_temps[index]
            indoor_real_temps.append(increment)

        if indoor_real_temps[index] > row['Indoor Temp Goal']:
            furnace_bools.append(0)
            ac_bools.append(1)

            increment = indoor_real_temps[index] - 0.5
            indoor_real_temps.append(increment)

        if indoor_real_temps[index] < row['Indoor Temp Goal']:
            furnace_bools.append(1)
            ac_bools.append(0)

            increment = indoor_real_temps[index] + 0.5
            indoor_real_temps.append(increment)

    df['Indoor Real Temps'] = indoor_real_temps[:289]
    df['Furnace ON'] = furnace_bools
    df['AC ON'] = ac_bools

    cost_ac = 5/(24*12)
    cost_furnace = 9/(24*12)

    df['AC Cost'] = df['AC ON']*cost_ac
    df['Heater Cost'] = df['Furnace ON']*cost_furnace
    df['Total Cost'] = df['AC Cost']+df['Heater Cost']

    return df


def simple_house_windows(data):
    df = pd.read_csv(data)

    indoor_real_temps = [60]
    furnace_bools = []
    ac_bools = []
    window_bools = []

    for index, row in df.iterrows():
        if indoor_real_temps[index] == row['Indoor Temp Goal']:
            if row['Outdoor Temp'] <= indoor_real_temps[index]:
                window_bools.append(0)
                furnace_bools.append(0)
                ac_bools.append(0)

                increment = indoor_real_temps[index]
                indoor_real_temps.append(increment)

            if row['Outdoor Temp'] > indoor_real_temps[index]:
                window_bools.append(0)
                furnace_bools.append(0)
                ac_bools.append(0)

                increment = indoor_real_temps[index]
                indoor_real_temps.append(increment)


        if indoor_real_temps[index] > row['Indoor Temp Goal']:
            if row['Outdoor Temp'] <= indoor_real_temps[index]:

                window_bools.append(1)
                furnace_bools.append(0)
                ac_bools.append(0)

                increment = indoor_real_temps[index] - 0.25
                indoor_real_temps.append(increment)


        if indoor_real_temps[index] > row['Indoor Temp Goal']:
            if row['Outdoor Temp'] > indoor_real_temps[index]:

                window_bools.append(0)
                furnace_bools.append(0)
                ac_bools.append(1)

                increment = indoor_real_temps[index] - 0.5
                indoor_real_temps.append(increment)

        if indoor_real_temps[index] < row['Indoor Temp Goal']:
            if row['Outdoor Temp'] >= indoor_real_temps[index]:
                window_bools.append(1)
                furnace_bools.append(0)
                ac_bools.append(0)

                increment = indoor_real_temps[index] + 0.25
                indoor_real_temps.append(increment)

        if indoor_real_temps[index] < row['Indoor Temp Goal']:
            if row['Outdoor Temp'] < indoor_real_temps[index]:

                window_bools.append(0)
                furnace_bools.append(1)
                ac_bools.append(0)

                increment = indoor_real_temps[index] + 0.5
                indoor_real_temps.append(increment)




    df['Indoor Real Temps'] = indoor_real_temps[:289]
    df['Windows Open'] = window_bools
    df['Furnace ON'] = furnace_bools
    df['AC ON'] = ac_bools

    cost_ac = 5 / (24 * 12)
    cost_furnace = 9 / (24 * 12)

    df['AC Cost'] = df['AC ON'] * cost_ac
    df['Heater Cost'] = df['Furnace ON'] * cost_furnace
    df['Total Cost'] = df['AC Cost'] + df['Heater Cost']

    return df



if __name__ == '__main__':

    # output_no_windows = simple_house_no_windows('constant_temp.csv')
    output_windows = simple_house_windows('constant_temp.csv')

    output_windows.to_csv('outputs/constant_temp_windows_output.csv')
    # output_no_windows.to_csv('outputs/constant_temp_no_windows_output.csv')

    # output_no_windows = simple_house_no_windows('cold_outside.csv')
    # output_windows = simple_house_windows('cold_outside.csv')
    #
    # output_windows.to_csv('outputs/cold_outside_windows_output.csv')
    # output_no_windows.to_csv('outputs/cold_outside_no_windows_output.csv')
    #
    # output_no_windows = simple_house_no_windows('hot_outside.csv')
    # output_windows = simple_house_windows('hot_outside.csv')
    #
    # output_windows.to_csv('outputs/hot_outside_windows_output.csv')
    # output_no_windows.to_csv('outputs/hot_outside_no_windows_output.csv')



# class HouseModel(object):
#     def __init__(self, data):
#         self.df_data = pd.read_csv(data)
#         self.timestep = pendulum.parse(0)
#         self.indoor_temp = 22
#         self.outdoor_temp = 15
#         self.weather = None
#
#
#         self.furnace_condition = False #either on or off
#         self.ac_condition = True # either on or off
#         self.window_condition = 0 # gradient for 0, 0.5, 1
#
#     def time_stepper(self):
#
#         self.timestep = self.timestep.add(minutes=5)
#
#     def set_outdoor_temp(self):
#
#
#
#     def set_indoor_temp(self):
#
#         if self.furnace_condition:
#             self.indoor_temp =+ 1
#
#         if self.ac_condition:
#             self.indoor_temp =- 1
#
#         if self.window_condition == 0:
#             self.indoor_temp = self.indoor_temp
#
#         elif self.window_condition == 0.5:
#             if self.outdoor_temp > self.indoor_temp:
#                 self.indoor_temp =+ 0.5
#             if self.outdoor_temp < self.indoor_temp:
#                 self.indoor_temp =- 0.5
#             if self.outdoor_temp == self.indoor_temp:
#                 self.indoor_temp = self.indoor_temp
#
#         elif self.window_condition == 1:
#             if self.outdoor_temp > self.indoor_temp:
#                 self.indoor_temp =+ 1
#             if self.outdoor_temp < self.indoor_temp:
#                 self.indoor_temp =- 1
#             if self.outdoor_temp == self.indoor_temp:
#                 self.indoor_temp = self.indoor_temp
#
#
#     def set_weather(self):
#
#
#
#     def set_window_state(self):
#
#
#
#     def cost_logic(self):
        


# With auto windows
""" if indoor temp is not equal to goal
        do something
        
        if indoor temp < goal
            if outdoor temp > indoor temp
                open windows
                increment indoor temp 
            if outdoor temp < indoor temp
                close windows
                turn on furnace
                
        
        if indoor temp > goal
            if outdoor temp < indoor temp
                open windows
            if outdoor temp > indoor temp
                close windows
                turn on furnace
        
    else
        close windows
        
        
"""
# Without auto windows
""" if indoor temp is not equal to goal
        do something
        
        if indoor temp < goal
            turn on furnace
            update indoor temp =+.25
        if indoor temp > goal
            turn on AC
            update indoor temp =-0.25
            


"""

# Cost
"""
intervals_furnace * cost_furnace = tot_heating_bill
intervals_ac * cost_ac = tot_cooling_bill

tot_cooling_bill + tot_heating_bill = tot_bill
"""
