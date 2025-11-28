import pandas as pd
import os

def verify():
    # Assuming run from root, but if run from page/, we need to handle it.
    # Let's assume run from root for simplicity as per plan, OR handle both.
    # If run from root: data/unificador_processado.xlsx
    # If run from page: ../data/unificador_processado.xlsx
    
    if os.path.exists('data'):
        output_file = os.path.join('data', 'unificador_processado.xlsx')
    else:
        output_file = os.path.join('..', 'data', 'unificador_processado.xlsx')
        
    print(f"Checking {output_file}...")
    try:
        # Read sheet names
        xl = pd.ExcelFile(output_file)
        print("Sheets found:", xl.sheet_names)
        
        if 'mix' not in xl.sheet_names:
            print("ERROR: 'mix' sheet missing.")
            return
        
        if 'historico' not in xl.sheet_names:
            print("ERROR: 'historico' sheet missing.")
        
        # Read mix sheet for content verification
        df = pd.read_excel(output_file, sheet_name='mix', dtype={'codigo_ean': str})
        
        # Check historico
        if 'historico' in xl.sheet_names:
             df_hist = pd.read_excel(output_file, sheet_name='historico', dtype={'loja': str})
             if 'loja' in df_hist.columns:
                 print("\nSample 'loja' in historico:")
                 print(df_hist['loja'].head())
             if 'data_pedido' in df_hist.columns:
                 print("\nSample 'data_pedido' in historico:")
                 print(df_hist['data_pedido'].head())
             if 'situacao' in df_hist.columns:
                 print("\nSample 'situacao' in historico:")
                 print(df_hist['situacao'].head())
    except Exception as e:
        print(f"Could not read file: {e}")
        return

    print("\nChecking Parquet files...")
    mix_parquet = os.path.join(os.path.dirname(output_file), 'mix.parquet')
    hist_parquet = os.path.join(os.path.dirname(output_file), 'historico.parquet')
    
    if os.path.exists(mix_parquet):
        print(f"Found {mix_parquet}")
        try:
            df_p = pd.read_parquet(mix_parquet)
            print(f"Read {len(df_p)} rows from mix.parquet")
        except Exception as e:
            print(f"Error reading mix.parquet: {e}")
    else:
        print(f"MISSING {mix_parquet}")

    if os.path.exists(hist_parquet):
        print(f"Found {hist_parquet}")
        try:
            df_h = pd.read_parquet(hist_parquet)
            print(f"Read {len(df_h)} rows from historico.parquet")
        except Exception as e:
            print(f"Error reading historico.parquet: {e}")
    else:
        print(f"MISSING {hist_parquet}")

    print("Columns:", df.columns.tolist())
    
    if 'loja_ativa_mix' in df.columns:
        sample = df[['codigo_interno', 'loja_ativa_mix']].dropna().head()
        print("\nSample 'loja_ativa_mix':")
        print(sample)
    else:
        print("\nERROR: 'loja_ativa_mix' column missing.")

    if 'estoque_cd' in df.columns:
        sample_est = df[['codigo_interno', 'estoque_cd']].dropna().head()
        print("\nSample 'estoque_cd':")
        print(sample_est)
    else:
        print("\nERROR: 'estoque_cd' column missing.")

    if 'codigo_ean' in df.columns:
        sample_ean = df['codigo_ean'].dropna().head()
        print("\nSample 'codigo_ean':")
        print(sample_ean)
        # Check format
        invalid_eans = df[~df['codigo_ean'].astype(str).str.match(r'^\d{13}$')]
        if not invalid_eans.empty:
             print(f"\nWARNING: Found {len(invalid_eans)} invalid EANs (not 13 digits).")
             print(invalid_eans['codigo_ean'].head())
        else:
             print("\nAll EANs seem to be 13 digits.")
    else:
        print("\nERROR: 'codigo_ean' column missing.")

if __name__ == "__main__":
    verify()
