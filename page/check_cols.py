import pandas as pd

def check_columns():
    input_file = 'unificador.xlsm'
    try:
        xl = pd.ExcelFile(input_file)
        for sheet in xl.sheet_names:
            df = pd.read_excel(input_file, sheet_name=sheet, nrows=5)
            print(f"--- Sheet: {sheet} ---")
            print(df.columns.tolist())
            if 'data_pedido' in df.columns:
                print(f"FOUND 'data_pedido' in {sheet}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    check_columns()
