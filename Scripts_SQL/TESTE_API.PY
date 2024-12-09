import fundamentus

tickers = 'BBDC3'


df = fundamentus.get_papel('BBDC3')
print(df)
nome_empresa = df['Empresa'].iloc[0]
dataCot = df['Data_ult_cot'].iloc[0]
pl = df['PL'].iloc[0]
pvp = df['PVP'].iloc[0]
giro1 = df['Receita_Liquida_12m'].iloc[0]
pl = float(pl.replace('.', '').replace(',', '.'))  # Remove formatação brasileira e converte para float
pvp = float(pvp.replace('.', '').replace(',', '.'))

print(f"{nome_empresa}, {dataCot}, PL: {pl:.2f}, PVP: {pvp:.2f} GIRO02:")
