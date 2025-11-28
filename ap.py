import pandas as pd
import os

def process_data():
    input_file = os.path.join('data', 'unificador.xlsm')
    output_file = os.path.join('data', 'unificador_processado.xlsx')

    print(f"Loading data from {input_file}...")
    try:
        # Load sheets
        df_mix = pd.read_excel(input_file, sheet_name='mix')
        df_ativo = pd.read_excel(input_file, sheet_name='item_ativo')
        df_wms = pd.read_excel(input_file, sheet_name='wms')
        try:
            df_historico = pd.read_excel(input_file, sheet_name='historico')
        except ValueError:
            print("WARNING: 'historico' sheet not found in input file.")
            df_historico = pd.DataFrame() # Empty DF if missing
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    print("Formatting 'codigo_ean'...")
    if 'codigo_ean' in df_mix.columns:
        # Convert to numeric, fill NaNs with 0, convert to int, then string, then zfill
        # zfill(13) will NOT truncate strings longer than 13, so 14-digit EANs are preserved.
        df_mix['codigo_ean'] = pd.to_numeric(df_mix['codigo_ean'], errors='coerce').fillna(0).astype(int).astype(str).str.zfill(13)
    else:
        print("WARNING: 'codigo_ean' column not found in 'mix' sheet.")

    # Format 'loja' in historico if exists
    if not df_historico.empty and 'loja' in df_historico.columns:
        print("Formatting 'loja' in 'historico'...")
        df_historico['loja'] = pd.to_numeric(df_historico['loja'], errors='coerce').fillna(0).astype(int).astype(str).str.zfill(3)
    
    # Format 'data_pedido' in historico if exists
    if not df_historico.empty and 'data_pedido' in df_historico.columns:
        print("Formatting 'data_pedido' in 'historico'...")
        df_historico['data_pedido'] = pd.to_datetime(df_historico['data_pedido'], errors='coerce').dt.strftime('%d/%m/%y')

    # Map 'situacao' in historico if exists
    if not df_historico.empty and 'situacao' in df_historico.columns:
        print("Mapping 'situacao' in 'historico'...")
        def map_situacao(x):
            try:
                val = int(x)
                if val == 1: return "aguardando"
                if 2 <= val <= 5: return "processando"
                if val == 6: return "enviado"
                if val == 7: return "em falta"
                return x
            except:
                return x
        df_historico['situacao'] = df_historico['situacao'].apply(map_situacao)

    print("Processing 'loja_ativa_mix'...")
    # Filter active items
    active_items = df_ativo[df_ativo['status'] == 'A'].copy()
    
    # Group by codigo_interno and join lojas with hyphen
    # Ensure 'loja' is string and formatted to 3 digits
    active_items['loja'] = pd.to_numeric(active_items['loja'], errors='coerce').fillna(0).astype(int).astype(str).str.zfill(3)
    lojas_ativas = active_items.groupby('codigo_interno')['loja'].apply(lambda x: '-'.join(x)).reset_index()
    lojas_ativas.rename(columns={'loja': 'loja_ativa_mix_calculated'}, inplace=True)

    # Merge into mix
    df_mix = pd.merge(df_mix, lojas_ativas, on='codigo_interno', how='left')
    
    # Update the column 'loja_ativa_mix'
    df_mix['loja_ativa_mix'] = df_mix['loja_ativa_mix_calculated']
    df_mix.drop(columns=['loja_ativa_mix_calculated'], inplace=True)

    print("Processing 'estoque_cd'...")
    
    # Placeholder for WMS logic until we see columns
    qty_col = None
    possible_qty_cols = ['qtde', 'quantidade', 'saldo', 'estoque', 'total']
    for col in df_wms.columns:
        if col.lower() in possible_qty_cols:
            qty_col = col
            break
    
    if qty_col:
        print(f"Found quantity column: {qty_col}")
        wms_sum = df_wms.groupby('codigo_interno')[qty_col].sum().reset_index()
        wms_sum.rename(columns={qty_col: 'total_estoque'}, inplace=True)
        
        # Drop 'total_estoque' from mix if it exists to avoid suffixes
        if 'total_estoque' in df_mix.columns:
            df_mix.drop(columns=['total_estoque'], inplace=True)
            
        df_mix = pd.merge(df_mix, wms_sum, on='codigo_interno', how='left')
        
        # Calculate boxes
        # Ensure numeric
        df_mix['total_estoque'] = pd.to_numeric(df_mix['total_estoque'], errors='coerce').fillna(0)
        df_mix['embalagem'] = pd.to_numeric(df_mix['embalagem'], errors='coerce').fillna(1) # Avoid div by zero
        
        df_mix['estoque_cd'] = df_mix['total_estoque'] / df_mix['embalagem']
    else:
        print("WARNING: Could not find a clear quantity column in 'wms'.")
        # Fallback
        if 'endereco' in df_wms.columns and pd.api.types.is_numeric_dtype(df_wms['endereco']):
             print("Summing 'endereco' column as requested...")
             wms_sum = df_wms.groupby('codigo_interno')['endereco'].sum().reset_index()
             # ... (rest of logic would go here if needed, but we found 'estoque')
        else:
             print("Column 'endereco' is not numeric or not found. Cannot sum.")

    print(f"Saving to {output_file}...")
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_mix.to_excel(writer, sheet_name='mix', index=False)
        if not df_historico.empty:
            df_historico.to_excel(writer, sheet_name='historico', index=False)
        else:
            print("Skipping 'historico' sheet as it is empty or missing.")
    
    # Save as Parquet
    print("Saving to Parquet...")
    try:
        mix_parquet = os.path.join('data', 'mix.parquet')
        df_mix.to_parquet(mix_parquet, index=False)
        print(f"Saved {mix_parquet}")
        
        if not df_historico.empty:
            hist_parquet = os.path.join('data', 'historico.parquet')
            df_historico.to_parquet(hist_parquet, index=False)
            print(f"Saved {hist_parquet}")
    except Exception as e:
        print(f"Error saving Parquet files: {e}")
        print("Ensure you have 'pyarrow' or 'fastparquet' installed (pip install pyarrow).")

    print("Done.")

if __name__ == "__main__":
    process_data()
