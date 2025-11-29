# Unificador de Dados - Guia de Uso

## Executável Criado com Sucesso! 🎉

O arquivo **Unificador.exe** foi gerado na pasta `dist/`.

### Como Usar:

1. **Localize o executável:**
   - Navegue até a pasta: `d:\unificador\dist\`
   - Você encontrará o arquivo: **Unificador.exe**

2. **Execute o programa:**
   - Clique duas vezes em **Unificador.exe**
   - Uma janela com interface gráfica será aberta

3. **Processar seus dados:**
   - Clique no botão **"Selecionar Arquivo"**
   - Escolha seu arquivo **unificador.xlsm** (ou qualquer outro arquivo .xlsx/.xlsm)
   - Clique no botão **"PROCESSAR DADOS"**
   - Acompanhe o progresso na área de log

4. **Resultado:**
   - O arquivo processado será salvo no mesmo diretório do arquivo original
   - Arquivos gerados:
     - `unificador_processado.xlsx` - Excel processado
     - `mix.parquet` - Dados em formato Parquet
     - `historico.parquet` - Histórico em formato Parquet

### Recursos da Interface:

✅ **Interface amigável** - Sem necessidade de terminal ou VS Code
✅ **Seleção de arquivo** - Escolha facilmente o arquivo Excel
✅ **Log em tempo real** - Acompanhe cada etapa do processamento
✅ **Mensagens de sucesso/erro** - Feedback claro sobre o resultado
✅ **Processamento em thread** - A interface não trava durante o processo

### Distribuição:

Você pode copiar o arquivo **Unificador.exe** para qualquer computador Windows e executá-lo sem precisar instalar Python ou qualquer dependência!

### Arquivos do Projeto:

- `gui.py` - Código fonte da interface gráfica
- `ap.py` - Lógica de processamento original
- `requirements.txt` - Dependências Python
- `Unificador.spec` - Configuração do PyInstaller
- `dist/Unificador.exe` - **Executável standalone pronto para uso!**
