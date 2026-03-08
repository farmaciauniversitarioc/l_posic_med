import pandas as pd

def processar_r84(arquivo):
    df = pd.read_excel(arquivo, header=None, engine="xlrd")

    estabelecimento_atual = None
    medicamento_atual = None
    registros = []

    for _, row in df.iterrows():
        col_texto = str(row[1]).strip() if pd.notna(row[1]) else ""

        # Detectar estabelecimento
        if "Estabelecimento de Saúde:" in col_texto:
            estabelecimento_atual = col_texto.split(":", 1)[1].strip()
            medicamento_atual = None
            continue

        # Detectar medicamento
        if col_texto.startswith("BR"):
            partes = col_texto.split(" ", 1)
            catmat = partes[0]
            medicamento = partes[1] if len(partes) > 1 else ""
            medicamento_atual = (catmat, medicamento)
            continue

        # Detectar linha Total
        if "Total:" in col_texto and estabelecimento_atual and medicamento_atual:
            qtd = row[12]

            if pd.notna(qtd):
                registros.append({
                    "estabelecimento_saude": estabelecimento_atual,
                    "catmat": medicamento_atual[0],
                    "medicamento": medicamento_atual[1],
                    "quantidade_total": float(qtd)
                })

    resultado = pd.DataFrame(registros)

    if resultado.empty:
        return resultado

    resultado = (
        resultado
        .groupby(
            ["estabelecimento_saude", "catmat", "medicamento"],
            as_index=False
        )["quantidade_total"]
        .sum()
        .sort_values(["estabelecimento_saude", "medicamento"])
    )

    return resultado