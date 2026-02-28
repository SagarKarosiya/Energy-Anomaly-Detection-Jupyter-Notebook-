import pandas as pd
import os

def load_data(data_path):

    print(" Loading Data...")

    file_path = os.path.join(data_path, "building_energy_800k.csv")
    df = pd.read_csv(file_path)

    print("Raw Shape:", df.shape)

    return df