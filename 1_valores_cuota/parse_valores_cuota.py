import datetime
import pandas as pd
import pyodbc
import sqlite3

FONDOS = ['A', 'B', 'C', 'D', 'E']

DB_PATH = 'valores_cuota.db'

CONN = sqlite3.connect(DB_PATH)


def parse_file(file, fondo):
    
    f = open(file)
    
    aux_list = []
    for line in f:

        data = line.strip().split(';')

        if len(data) < 3:
            continue
        
        if data[0] == 'Fecha':
            start = True
            names = data[1::2]
            f.readline()
            continue
            
        fecha = data[0]
        valores = data[1::2]

        for i, name in enumerate(names):
            vc = valores[i]
            
            if not vc:
                continue
            vc_f = float(vc.replace('.', '$').replace(',', '.').replace('$', '').strip())

            aux_list.append((fecha, name + "_" + fondo, vc_f))

    df = pd.DataFrame.from_records(aux_list, columns=['fecha_dia', 'ticker', 'valor'])
    
    df['valor'] = df['valor'].astype(float)
    
    f.close()
    
    return df

if __name__ == '__main__':
    print('Started at: ', datetime.datetime.now())

    first = True
    for fondo in FONDOS:
        data = parse_file('vcf{}2010-2020.csv'.format(fondo), fondo)
        if first:
            data.to_sql('VALORES_CUOTA', con=CONN, if_exists='replace')
            first = False
        else:
            data.to_sql('VALORES_CUOTA', con=CONN, if_exists='append')

    print('Finished at:', datetime.datetime.now())