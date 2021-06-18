import os
import sys

import pandas as pd


if __name__ == "__main__":
    input_dir = data_path = sys.argv[1]
    output_dir = data_path = sys.argv[2]

    kbr_file_r1 = 'Etap V - 2_Pomiary nat®Ąenia ruchu drogowego_ring 1.xlsx'
    kbr_file_r2 = 'Etap V - 2_Pomiary nat®Ąenia ruchu drogowego_ring 2.xlsx'
    kbr_file_r3 = 'Etap V - 2_Pomiary nat®Ąenia ruchu drogowego_ring 3.xlsx'

    file_path_r1 = os.path.join(input_dir, kbr_file_r1)
    file_path_r2 = os.path.join(input_dir, kbr_file_r2)
    file_path_r3 = os.path.join(input_dir, kbr_file_r3)

    # dfs = []
    for file_path in [file_path_r1, file_path_r2, file_path_r3]:
        # BAZA_DANYCH_AGREGACJA
        header = 0 if file_path == file_path_r3 else 1
        df = pd.read_excel(
            file_path, 
            'BAZA_DANYCH_AGREGACJA', 
            header=[header],
            engine='openpyxl',
            parse_dates=['Godziny pomiarowe']
        )
        # leave only valid rows
        last_valid_index = df['Godziny pomiarowe'].last_valid_index()
        df = df.iloc[:last_valid_index+1]

        # fill values
        df['Przekrój pomiarowy'].fillna(method='ffill', inplace=True)

        # strip column names (to unify them)
        cols = list(df.columns)
        new_cols = [col.strip() for col in cols]
        df.columns = new_cols

        # extract hour from date
        df.rename(
            columns={'Godziny pomiarowe': 'date'}, 
            inplace=True
        )
        df['hour'] = df['date'].dt.hour

        # extract id and street name from 'Przekrój pomiarowy' column
        df['id'] = df['Przekrój pomiarowy'].apply(
        lambda x: x.split(' ')[0].strip()
        )
        df['street'] = df['Przekrój pomiarowy'].apply(
            lambda x: x.split('-')[1].strip()
        )

        # get counts
        df['n_cars'] = df['samochody osobowe (do 9 miejsc z kierowcą) [C] - SKALA GŁÓWNA'] + df['motocykle (także quady), skutery, motorowery [B] - SKALA POMOCNICZA']
        df['n_buses'] = df['autobusy (więcej niż 24 miejsca z kierowcą) [G] - SKALA POMOCNICZA']
        df['n_bicycles'] = df['rowery [A] - SKALA POMOCNICZA']

        chosen_cols = [
            'id', 'street', 'hour',
            'n_cars', 'n_buses', 'n_bicycles'
        ]
        df = df[chosen_cols]
        df = df.groupby(
            by=['id', 'street', 'hour']
        ).sum().reset_index()
        
        out_file_name = 'ring_' + file_path.split(' ')[-1].replace('xlsx', 'csv')
        df.to_csv(os.path.join(output_dir, out_file_name))
        # dfs.append(df.reset_index(drop=True))

    # dfs[0].to_csv(os.path.join(output_dir, 'ring_1.csv'))
    # dfs[1].to_csv(os.path.join(output_dir, 'ring_2.csv'))
    # dfs[2].to_csv(os.path.join(output_dir, 'ring_3.csv'))
