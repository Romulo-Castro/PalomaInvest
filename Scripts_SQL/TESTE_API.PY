import fundamentus

tickers = 'BBDC3'


df = fundamentus.get_papel('BBDC3')
nome_empresa = df['Empresa'].iloc[0]
dataCot = df['Data_ult_cot'].iloc[0]
print(nome_empresa, dataCot)