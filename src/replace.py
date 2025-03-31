import re

def extrair_nome_e_ultimo_numero(texto):
    texto = texto.lstrip('+').strip()
    
    partes = texto.split('-')
    if len(partes) >= 2:
        nome_cidade = partes[0].strip() 
        ultimo_numero = partes[1].strip().rstrip(',') 
        return f"{nome_cidade},{ultimo_numero},"
    return None

def processar_arquivo(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        linhas = file.readlines()

    resultados = []
    for linha in linhas:
        linha = linha.strip()  
        if linha and "--------------------------" not in linha:  
            resultado = extrair_nome_e_ultimo_numero(linha)
            if resultado:
                resultados.append(resultado)

    with open(output_file, 'w', encoding='utf-8') as file:
        for resultado in resultados:
            file.write(resultado + '\n')

input_file = 'resultados'
output_file = 'resultados-final'
processar_arquivo(input_file, output_file)

print(f"Os resultados foram gravados no arquivo {output_file}.")
