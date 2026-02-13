import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Gestão 4° Pelotão - Carnaval 2026", layout="wide")

# 1. Base de Dados Logística e Alterações Pré-definidas
escala_dados = {
    'Dia': ['14 (Sáb)', '15 (Dom)', '16 (Seg)', '17 (Ter)'],
    'Bloco': ['Então Brilha', 'Bloco do Wando', 'Baianas Ozadas', 'Baianeiros'],
    'Endereço': ['AV. CONTORNO, 160', 'AV. BRASIL, 1145', 'AV. AFONSO PENA, 996', 'AV. AMAZONAS, 686'],
    'Comando Geral': ['CAP Madureira', 'CAP Romeu', 'CAP Madureira', 'TEN Queiroga'],
    'Chamada': ['04:00', '08:00', '07:00', '12:00'],
    'Bus Ida': ['A, B, C, D', 'G, H', 'A, B, C', 'A, B, E, X'],
    'Bus Volta': ['B, D, H, I', 'G, H', 'R, S, T', 'B, C, D, E'],
    'Previstos': [27, 27, 27, 27],
    'Alteracoes_Fixas': [
        "• Al Sd Maria Luiza – Auxiliar de transporte 03h as 10h30min\n• Al Sd Ryan Soares – Sentinela 07h as 19h",
        "• Al Sd Karen – SAT 08h as 16h",
        "• Efetivo Completo (27 presentes)",
        "• Al Sd Amado – Auxiliar de transporte 06h a 12h"
    ]
}
df_escala = pd.DataFrame(escala_dados)

# 2. Base de Dados do Efetivo
patrulhas_dados = {
    'Patrulha': [
        'Cmt/Sub Pel', 'Cmt/Sub Pel',
        'P1. CMD', 'P1. CMD', 'P1. CMD', 'P1. CMD', 'P1. CMD',
        'Patrulha 02', 'Patrulha 02', 'Patrulha 02', 'Patrulha 02', 'Patrulha 02',
        'Patrulha 03', 'Patrulha 03', 'Patrulha 03', 'Patrulha 03', 'Patrulha 03',
        'Patrulha 04', 'Patrulha 04', 'Patrulha 04', 'Patrulha 04', 'Patrulha 04',
        'Patrulha 05', 'Patrulha 05', 'Patrulha 05', 'Patrulha 05', 'Patrulha 05'
    ],
    'Militar': [
        'CAD PM Tiago Oliveira', 'CAD PM Jean Reis',
        'CAD PM Caroline Ribeiro', 'Al Sgt Leonardo Melo', 'Al Sd Bruno Henrique', 'Al Sd Samuel Santos Cesar', 'Al Sd Breno Rodrigues',
        'AL OF PM Fábio Fernando', 'Al Sgt José Roberto', 'Al Sd Ryan Deusmar', 'Al Sd Samuel Gomes', 'Al Sd Karen Christina',
        'AL OF PM Filipi Coimbra', 'Al Sgt Willis Eugênio', 'Al Sd Brunno Kaic', 'Al Sd Thamires Luz', 'Al Sd Amanda Gonçalves',
        'CAD PM Cosme', 'Al Sd Amado Rodrigues Lima', 'Al Sd Maria Luiza', 'Al Sd João Guilherme', 'Al Sd Brandon Hiago Henrique',
        'CAD PM Thadeu Junior', 'Al Sgt Lucas Dias', 'Al Sd Higor Vinicius', 'Al Sd Jonathan Fellipe', 'Al Sd Janine Paiva'
    ]
}
df_efetivo = pd.DataFrame(patrulhas_dados)

# --- INICIALIZAÇÃO DO ESTADO ---
if 'checklist_data' not in st.session_state:
    st.session_state.checklist_data = df_efetivo.copy()
    for d in df_escala['Dia']:
        st.session_state.checklist_data[f'Presente {d}'] = False

# --- INTERFACE ---
st.title("🔺 Sistema de Gestão 4° Pel / 1ª Cia")
st.subheader("📍 LOCAL DE CHAMADA: Pátio Principal da APM")

# Seleção do Dia
st.sidebar.header("Calendário Operacional")
dia_selecionado = st.sidebar.selectbox("Selecione o Dia:", df_escala['Dia'])
info = df_escala[df_escala['Dia'] == dia_selecionado].iloc[0]

# --- PAINEL DE INFORMAÇÕES ---
c1, c2, c3 = st.columns([1.2, 1, 1.2])

with c1:
    st.info(f"👮 **Comando do Dia:** {info['Comando Geral']}")
    st.success(f"🚌 **Transporte:**\n\n**Ida:** {info['Bus Ida']}\n\n**Volta:** {info['Bus Volta']}")

with c2:
    st.info(f"🎭 **Bloco:** {info['Bloco']}\n\n📍 **Endereço:** {info['Endereço']}")
    st.error(f"⏰ **Chamada na APM:** {info['Chamada']}")

with c3:
    st.warning(f"📝 **Alterações Pré-definidas:**\n\n{info['Alteracoes_Fixas']}")
    st.text_area("Notas extras da chamada:", key=f"notes_{dia_selecionado}", placeholder="Digite aqui atrasos ou outras baixas...")

st.divider()

# --- CHECKLIST ---
st.subheader(f"✅ Checklist de Chamada - {info['Bloco']}")
col_presenca = f'Presente {dia_selecionado}'

df_editado = st.data_editor(
    st.session_state.checklist_data[['Patrulha', 'Militar', col_presenca]],
    column_config={
        col_presenca: st.column_config.CheckboxColumn("Presente", default=False),
        "Patrulha": st.column_config.TextColumn("Patrulha", width="medium"),
        "Militar": st.column_config.TextColumn("Militar", width="large"),
    },
    disabled=["Patrulha", "Militar"],
    hide_index=True,
    use_container_width=True
)

st.session_state.checklist_data.update(df_editado)

# --- MÉTRICAS ---
presentes_total = df_editado[col_presenca].sum()
previstos = info['Previstos']

m1, m2 = st.columns(2)
m1.metric("Conferência de Efetivo", f"{presentes_total} / {previstos}")
m2.progress(presentes_total / previstos)

# Botão de Relatório
if st.button("Listar Faltas e Gerar Relatório"):
    faltosos = df_editado[df_editado[col_presenca] == False]['Militar'].tolist()
    if faltosos:
        st.error(f"Militares Ausentes na Fila: {', '.join(faltosos)}")
        st.write("*(Lembre-se de conferir se estão nas alterações pré-definidas acima)*")
    else:
        st.success("Tropa em forma! Nenhum militar ausente.")
# --- FUNÇÃO PARA SALVAR OS DADOS ---
st.divider()
st.subheader("💾 Exportar Resultados")

if st.button("📥 Baixar Relatório de Presença (Excel)"):
    # Prepara os dados para exportação
    df_resultado = st.session_state.checklist_data[['Patrulha', 'Militar', col_presenca]]
    
    # Converte para Excel (usando memória)
    import io
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_resultado.to_excel(writer, index=False, sheet_name='Chamada')
    
    # Botão de download real
    st.download_button(
        label="Clique aqui para baixar o arquivo .xlsx",
        data=output.getvalue(),
        file_name=f"chamada_{info['Bloco']}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )