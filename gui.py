import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import pandas as pd
import os
import sys


class UnificadorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Unificador de Dados")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        
        self.arquivo_selecionado = None
        
        # Frame principal
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = tk.Label(main_frame, text="Processador de Dados Unificador", 
                        font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # Frame para seleção de arquivo
        file_frame = tk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(file_frame, text="Arquivo Excel:", font=("Arial", 10)).pack(anchor=tk.W)
        
        input_frame = tk.Frame(file_frame)
        input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.file_entry = tk.Entry(input_frame, font=("Arial", 10), state='readonly')
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.btn_browse = tk.Button(input_frame, text="Selecionar Arquivo", 
                                    command=self.selecionar_arquivo,
                                    font=("Arial", 10), bg="#4CAF50", fg="white",
                                    cursor="hand2", padx=10)
        self.btn_browse.pack(side=tk.RIGHT)
        
        # Botão processar
        self.btn_processar = tk.Button(main_frame, text="PROCESSAR DADOS", 
                                       command=self.processar_dados,
                                       font=("Arial", 12, "bold"), bg="#2196F3", 
                                       fg="white", cursor="hand2", pady=10,
                                       state=tk.DISABLED)
        self.btn_processar.pack(fill=tk.X, pady=(0, 20))
        
        # Área de log
        tk.Label(main_frame, text="Log de Processamento:", 
                font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, 
                                                   font=("Courier", 9),
                                                   state='disabled', wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
    def log(self, mensagem):
        """Adiciona mensagem ao log"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, mensagem + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update()
    
    def selecionar_arquivo(self):
        """Abre diálogo para selecionar arquivo Excel"""
        arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo Excel",
            filetypes=[("Excel files", "*.xlsm *.xlsx"), ("All files", "*.*")]
        )
        if arquivo:
            self.arquivo_selecionado = arquivo
            self.file_entry.config(state='normal')
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, arquivo)
            self.file_entry.config(state='readonly')
            self.btn_processar.config(state=tk.NORMAL)
            self.log(f"✓ Arquivo selecionado: {os.path.basename(arquivo)}")
    
    def processar_dados(self):
        """Executa o processamento em uma thread separada"""
        if not self.arquivo_selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um arquivo primeiro!")
            return
        
        # Desabilita botões durante processamento
        self.btn_processar.config(state=tk.DISABLED)
        self.btn_browse.config(state=tk.DISABLED)
        
        # Limpa log
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        # Inicia thread de processamento
        thread = threading.Thread(target=self.executar_processamento)
        thread.daemon = True
        thread.start()
    
    def executar_processamento(self):
        """Lógica de processamento (baseada em ap.py)"""
        try:
            input_file = self.arquivo_selecionado
            output_dir = os.path.dirname(input_file)
            output_file = os.path.join(output_dir, 'unificador_processado.xlsx')
            
            self.log("="*60)
            self.log("INICIANDO PROCESSAMENTO")
            self.log("="*60)
            self.log(f"Arquivo de entrada: {os.path.basename(input_file)}")
            self.log(f"Diretório de saída: {output_dir}")
            self.log("")
            
            # Carregar dados
            self.log("⏳ Carregando planilhas...")
            df_mix = pd.read_excel(input_file, sheet_name='mix')
            self.log(f"  ✓ 'mix' carregada ({len(df_mix)} linhas)")
            
            df_ativo = pd.read_excel(input_file, sheet_name='item_ativo')
            self.log(f"  ✓ 'item_ativo' carregada ({len(df_ativo)} linhas)")
            
            df_wms = pd.read_excel(input_file, sheet_name='wms')
            self.log(f"  ✓ 'wms' carregada ({len(df_wms)} linhas)")
            
            try:
                df_historico = pd.read_excel(input_file, sheet_name='historico')
                self.log(f"  ✓ 'historico' carregada ({len(df_historico)} linhas)")
            except ValueError:
                self.log("  ⚠ Planilha 'historico' não encontrada")
                df_historico = pd.DataFrame()
            
            self.log("")
            
            # Formatar codigo_ean
            self.log("⏳ Formatando 'codigo_ean'...")
            if 'codigo_ean' in df_mix.columns:
                df_mix['codigo_ean'] = pd.to_numeric(df_mix['codigo_ean'], errors='coerce').fillna(0).astype(int).astype(str).str.zfill(13)
                self.log("  ✓ Códigos EAN formatados para 13 dígitos")
            else:
                self.log("  ⚠ Coluna 'codigo_ean' não encontrada")
            
            # Formatar historico
            if not df_historico.empty:
                if 'loja' in df_historico.columns:
                    self.log("⏳ Formatando 'loja' no histórico...")
                    df_historico['loja'] = pd.to_numeric(df_historico['loja'], errors='coerce').fillna(0).astype(int).astype(str).str.zfill(3)
                    self.log("  ✓ Lojas formatadas para 3 dígitos")
                
                if 'data_pedido' in df_historico.columns:
                    self.log("⏳ Formatando 'data_pedido' no histórico...")
                    df_historico['data_pedido'] = pd.to_datetime(df_historico['data_pedido'], errors='coerce').dt.strftime('%d/%m/%y')
                    self.log("  ✓ Datas formatadas (DD/MM/AA)")
                
                if 'situacao' in df_historico.columns:
                    self.log("⏳ Mapeando 'situacao' no histórico...")
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
                    self.log("  ✓ Situações mapeadas")
            
            self.log("")
            
            # Processar loja_ativa_mix
            self.log("⏳ Processando 'loja_ativa_mix'...")
            active_items = df_ativo[df_ativo['status'] == 'A'].copy()
            active_items['loja'] = pd.to_numeric(active_items['loja'], errors='coerce').fillna(0).astype(int).astype(str).str.zfill(3)
            lojas_ativas = active_items.groupby('codigo_interno')['loja'].apply(lambda x: '-'.join(x)).reset_index()
            lojas_ativas.rename(columns={'loja': 'loja_ativa_mix_calculated'}, inplace=True)
            df_mix = pd.merge(df_mix, lojas_ativas, on='codigo_interno', how='left')
            df_mix['loja_ativa_mix'] = df_mix['loja_ativa_mix_calculated']
            df_mix.drop(columns=['loja_ativa_mix_calculated'], inplace=True)
            self.log("  ✓ Lojas ativas consolidadas")
            
            self.log("")
            
            # Processar estoque_cd
            self.log("⏳ Processando 'estoque_cd'...")
            qty_col = None
            possible_qty_cols = ['qtde', 'quantidade', 'saldo', 'estoque', 'total']
            for col in df_wms.columns:
                if col.lower() in possible_qty_cols:
                    qty_col = col
                    break
            
            if qty_col:
                self.log(f"  ✓ Coluna de quantidade encontrada: '{qty_col}'")
                wms_sum = df_wms.groupby('codigo_interno')[qty_col].sum().reset_index()
                wms_sum.rename(columns={qty_col: 'total_estoque'}, inplace=True)
                
                if 'total_estoque' in df_mix.columns:
                    df_mix.drop(columns=['total_estoque'], inplace=True)
                
                df_mix = pd.merge(df_mix, wms_sum, on='codigo_interno', how='left')
                df_mix['total_estoque'] = pd.to_numeric(df_mix['total_estoque'], errors='coerce').fillna(0)
                df_mix['embalagem'] = pd.to_numeric(df_mix['embalagem'], errors='coerce').fillna(1)
                df_mix['estoque_cd'] = df_mix['total_estoque'] / df_mix['embalagem']
                self.log("  ✓ Estoque CD calculado (em caixas)")
            else:
                self.log("  ⚠ Coluna de quantidade não identificada no WMS")
            
            self.log("")
            
            # Salvar Excel
            self.log("⏳ Salvando arquivo Excel...")
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                df_mix.to_excel(writer, sheet_name='mix', index=False)
                if not df_historico.empty:
                    df_historico.to_excel(writer, sheet_name='historico', index=False)
            self.log(f"  ✓ Salvo: {os.path.basename(output_file)}")
            
            self.log("")
            
            # Salvar Parquet
            self.log("⏳ Salvando arquivos Parquet...")
            try:
                mix_parquet = os.path.join(output_dir, 'mix.parquet')
                df_mix.to_parquet(mix_parquet, index=False)
                self.log(f"  ✓ Salvo: mix.parquet")
                
                if not df_historico.empty:
                    hist_parquet = os.path.join(output_dir, 'historico.parquet')
                    df_historico.to_parquet(hist_parquet, index=False)
                    self.log(f"  ✓ Salvo: historico.parquet")
            except Exception as e:
                self.log(f"  ⚠ Erro ao salvar Parquet: {e}")
            
            self.log("")
            self.log("="*60)
            self.log("✓ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
            self.log("="*60)
            
            # Mostrar mensagem de sucesso
            self.root.after(0, lambda: messagebox.showinfo(
                "Sucesso", 
                f"Processamento concluído!\n\nArquivo salvo em:\n{output_file}"
            ))
            
        except Exception as e:
            self.log("")
            self.log("="*60)
            self.log(f"✗ ERRO NO PROCESSAMENTO: {str(e)}")
            self.log("="*60)
            self.root.after(0, lambda: messagebox.showerror(
                "Erro", 
                f"Erro durante o processamento:\n\n{str(e)}"
            ))
        
        finally:
            # Reabilita botões
            self.root.after(0, lambda: self.btn_processar.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_browse.config(state=tk.NORMAL))


def main():
    root = tk.Tk()
    app = UnificadorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
