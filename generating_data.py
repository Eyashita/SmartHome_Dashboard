import serial
import time
import csv
from datetime import datetime
from pymongo import MongoClient
import os
import random


start_date = datetime(2021, 1, 1)
end_date = datetime(2023, 12, 31)
timestamp = start_date + (end_date - start_date) * random.random()
last_upload_time = timestamp

while True:
    try:
        voltage1 = round(random.uniform(209, 231), 2)
        frequency1 = random.randint(45, 55)
        current1 = round(random.uniform(40, 60), 2)
        power_factor1 = random.uniform(0.855, 0.945)
        power1 = round(voltage1 * current1 * power_factor1, 2)
        energy1 = round(power1 / 1000, 2)  # Energy in KWh
        
        voltage2 = round(random.uniform(209, 231), 2)
        frequency2 = random.randint(45, 55)
        current2 = round(random.uniform(40, 60), 2)
        power_factor2 = random.uniform(0.855, 0.945)
        power2 = round(voltage2 * current2 * power_factor2, 2)
        energy2 = round(power2 / 1000, 2)  # Energy in KWh
        
        voltage3 = round(random.uniform(209, 231), 2)
        frequency3 = random.randint(45, 55)
        current3 = round(random.uniform(40, 60), 2)
        power_factor3 = random.uniform(0.855, 0.945)
        power3 = round(voltage3 * current3 * power_factor3, 2)
        energy3 = round(power3 / 1000, 2)  # Energy in KWh
        
        voltage4 = round(random.uniform(209, 231), 2)
        frequency4 = random.randint(45, 55)
        current4 = round(random.uniform(40, 60), 2)
        power_factor4 = random.uniform(0.855, 0.945)
        power4 = round(voltage4 * current4 * power_factor4, 2)
        energy4 = round(power4 / 1000, 2)  # Energy in KWh
        
        voltage5 = round(random.uniform(209, 231), 2)
        frequency5 = random.randint(45, 55)
        current5 = round(random.uniform(40, 60), 2)
        power_factor5 = random.uniform(0.855, 0.945)
        power5 = round(voltage5 * current5 * power_factor5, 2)
        energy5 = round(power5 / 1000, 2)  # Energy in KWh
        
        voltage6 = round(random.uniform(209, 231), 2)
        frequency6 = random.randint(45, 55)
        current6 = round(random.uniform(40, 60), 2)
        power_factor6 = random.uniform(0.855, 0.945)
        power6 = round(voltage6 * current6 * power_factor6, 2)
        energy6 = round(power6 / 1000, 2)  # Energy in KWh
        
        voltage7 = round(random.uniform(209, 231), 2)
        frequency7 = random.randint(45, 55)
        current7 = round(random.uniform(40, 60), 2)
        power_factor7 = random.uniform(0.855, 0.945)
        power7 = round(voltage7 * current7 * power_factor7, 2)
        energy7 = round(power7 / 1000, 2)  # Energy in KWh
        
        voltage8 = round(random.uniform(209, 231), 2)
        frequency8 = random.randint(45, 55)
        current8 = round(random.uniform(40, 60), 2)
        power_factor8 = random.uniform(0.855, 0.945)
        power8 = round(voltage8 * current8 * power_factor8, 2)
        energy8 = round(power8 / 1000, 2)  # Energy in KWh
       

        print('voltage1')
        print(voltage1)
        print(current1)
        print(power1)
        print(energy1)
        print(frequency1)
        print(power_factor1)

        print('voltage2')
        print(voltage2)
        print(current2)
        print(power2)
        print(energy2)
        print(frequency2)
        print(power_factor2)

        print('voltage3')
        print(voltage3)
        print(current3)
        print(power3)
        print(energy3)
        print(frequency3)
        print(power_factor3)

        print('voltage4')
        print(voltage4)
        print(current4)
        print(power4)
        print(energy4)
        print(frequency4)
        print(power_factor4)

        print('voltage5')
        print(voltage5)
        print(current5)
        print(power5)
        print(energy5)
        print(frequency5)
        print(power_factor5)

        print('voltage6')
        print(voltage6)
        print(current6)
        print(power6)
        print(energy6)
        print(frequency6)
        print(power_factor6)

        print('voltage7')
        print(voltage7)
        print(current7)
        print(power7)
        print(energy7)
        print(frequency7)
        print(power_factor7)

        print('voltage8')
        print(voltage8)
        print(current8)
        print(power8)
        print(energy8)
        print(frequency8)
        print(power_factor8)

        data = [
           {'Voltage-1': voltage1, 'Current-1': current1, 'Power-1': power1, 'Energy-1': energy1, 'Frequency-1': frequency1, 'Powerfactor-1': power_factor1,
             'Voltage-2': voltage2, 'Current-2': current2, 'Power-2': power2, 'Energy-2': energy2, 'Frequency-2': frequency2, 'Powerfactor-2': power_factor2,
             'Voltage-3': voltage3, 'Current-3': current3, 'Power-3': power3, 'Energy-3': energy3, 'Frequency-3': frequency3, 'Powerfactor-3': power_factor3,
             'Voltage-4': voltage4, 'Current-4': current4, 'Power-4': power4, 'Energy-4': energy4, 'Frequency-4': frequency4, 'Powerfactor-4': power_factor4,
             'Voltage-5': voltage5, 'Current-5': current5, 'Power-5': power5, 'Energy-5': energy5, 'Frequency-5': frequency5, 'Powerfactor-5': power_factor5,
             'Voltage-6': voltage6, 'Current-6': current6, 'Power-6': power6, 'Energy-6': energy6, 'Frequency-6': frequency6, 'Powerfactor-6': power_factor6,
             'Voltage-7': voltage7, 'Current-7': current7, 'Power-7': power7, 'Energy-7': energy7, 'Frequency-7': frequency7, 'Powerfactor-7': power_factor7,
             'Voltage-8': voltage8, 'Current-8': current8, 'Power-8': power8, 'Energy-8': energy8, 'Frequency-8': frequency8, 'Powerfactor-8': power_factor8,} 
        ]

        # Specify the path and filename for the CSV file
        csv_file = 'data.csv'

        # Open the file in append mode
        with open(csv_file, mode='a') as file:
            # Define the fieldnames (column headers)
            fieldnames = ['Timestamp', 'Voltage-1', 'Current-1', 'Power-1', 'Energy-1', 'Frequency-1', 'Powerfactor-1',
                  'Voltage-2', 'Current-2', 'Power-2', 'Energy-2', 'Frequency-2', 'Powerfactor-2',
                  'Voltage-3', 'Current-3', 'Power-3', 'Energy-3', 'Frequency-3', 'Powerfactor-3',
                  'Voltage-4', 'Current-4', 'Power-4', 'Energy-4', 'Frequency-4', 'Powerfactor-4',
                  'Voltage-5', 'Current-5', 'Power-5', 'Energy-5', 'Frequency-5', 'Powerfactor-5',
                  'Voltage-6', 'Current-6', 'Power-6', 'Energy-6', 'Frequency-6', 'Powerfactor-6',
                  'Voltage-7', 'Current-7', 'Power-7', 'Energy-7', 'Frequency-7', 'Powerfactor-7',
                  'Voltage-8', 'Current-8', 'Power-8', 'Energy-8', 'Frequency-8', 'Powerfactor-8',]

            # Create a CSV writer object
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Check if the file is empty
            if file.tell() == 0:
               # Write the fieldnames as the header row
                writer.writeheader()

            # Get the current timestamp
            timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

            # Iterate over the data and write each row
            for row in data:
                row['Timestamp'] = timestamp
                writer.writerow(row)

        print('Data has been written to the CSV file.')

    except IndexError:
        print('index ERROR')
    except ValueError:
        print('value ERROR')
    
    # Short delay to avoid busy-waiting
    time.sleep(2) 
