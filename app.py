import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import time

# --- Configuração da Página ---
st.set_page_config(page_title="LotoTurbo Admin", page_icon="🎱", layout="centered", initial_sidebar_state="collapsed")

# --- Constantes ---
NEON_GREEN = "#39FF14"
DARK_BG = "#0E1117"
DARK_SEC = "#262730"

# --- CSS (Design) ---
def local_css():
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {DARK_BG}; color: white; }}
        .stTextInput > div > div > input {{ background-color: {DARK_SEC}; color: white; border-color: #444; }}
        div.stButton > button {{ background-color: {NEON_GREEN} !important; color: black !important; font-weight: bold !important; border: none !important; border-radius: 8px !important; }}
        h1, h2, h3, p, label {{ color: white !important; }}
        .result-card {{ background-color: {DARK_SEC}; padding: 20px; border-radius: 10px; border: 1px solid #444; margin-top: 20px; text-align: center; }}
        .number-ball {{ display: inline-block; width: 35px; height: 35px; line-height: 35px; border-radius: 50%; background-color: {NEON_GREEN}; color: black; font-weight: bold; text-align: center; margin: 3px; font-size: 14px; }}
        </style>
    """, unsafe_allow_html=True)

# --- Funções Lógicas ---
def verificar_soma(numeros):
    return 180 <= sum(numeros) <= 220, sum(numeros)

def gerar_jogo_otimizado():
    for _ in range(1000):
        jogo = sorted(random.sample(range(1, 26), 15))
        if 180 <= sum(jogo) <= 220: return jogo, sum(jogo)
    return None, 0

def render_bolas(numeros):
    html = '<div style="margin-top: 10px;">'
    for num in sorted(numeros): html += f'<span class="number-ball">{num:02d}</span>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# --- SISTEMA DE LOGIN SEGURO ---
def check_login(email_input):
    # 1. Bypass para o dono (opcional, para teste rápido)
    if email_input == "admin@lototurbo.com":
        return True
        
    try:
        # 2. Conecta na Planilha
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
        
        # 3. Limpa os dados (remove espaços e converte pra string)
        # Garante que as colunas existem antes de processar
        if 'email' not in df.columns or 'status' not in df.columns:
            st.error("Erro na Planilha: Colunas 'email' ou 'status' não encontradas.")
            return False

        df['email'] = df['email'].astype(str).str.strip().str.lower()
        df['status'] = df['status'].astype(str).str.strip().str.upper()
        email_limpo = email_input.strip().lower()
        
        # 4. Verifica se existe e está ATIVO
        usuario = df[df['email'] == email_limpo]
        
        if not usuario.empty:
            status = usuario.iloc[0]['status']
            if status == "ATIVO":
                return True
            else:
                st.error("Sua assinatura está suspensa ou cancelada.")
                return False
        else:
            st.error("E-mail não encontrado na base de alunos.")
            return False
            
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return False

# --- APP PRINCIPAL ---
def main():
    local_css()
    
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        st.markdown(f"<h1 style='text-align: center; color: {NEON_GREEN};'>🎱 LotoTurbo IA</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            email = st.text_input("Digite seu E-mail de Compra")
            if st.button("ACESSAR SISTEMA", use_container_width=True):
                if check_login(email):
                    st.session_state['logged_in'] = True
                    st.rerun()
        return

    # PÓS LOGIN
    if st.sidebar.button("Sair"):
        st.session_state['logged_in'] = False
        st.rerun()

    st.markdown(f"<h3 style='color: {NEON_GREEN};'>Painel Oficial da Matriz</h3>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📊 Analisador", "🎲 Gerador Automático"])

    with tab1:
        st.info("Digite 15 números (separados por espaço ou vírgula)")
        input_nums = st.text_input("Seus Números:")
        if st.button("ANALISAR AGORA", use_container_width=True):
            try:
                raw = input_nums.replace(',', ' ').split()
                nums = [int(n) for n in raw]
                if len(set(nums)) != 15 or any(n>25 for n in nums): st.error("Erro: Digite 15 números únicos entre 1-25.")
                else:
                    valido, soma = verificar_soma(nums)
                    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                    render_bolas(nums)
                    st.markdown(f"<h4>Soma da Matriz: {soma}</h4>", unsafe_allow_html=True)
                    if valido: st.success("✅ APROVADO: Alta Probabilidade!")
                    else: st.error("❌ REPROVADO: Ajuste seus números.")
                    st.markdown("</div>", unsafe_allow_html=True)
            except: st.error("Digite apenas números.")

    with tab2:
        if st.button("GERAR PALPITE VENCEDOR 🚀", use_container_width=True):
            with st.spinner("A IA está calculando as zonas..."):
                time.sleep(1.5)
                jogo, soma = gerar_jogo_otimizado()
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                render_bolas(jogo)
                st.markdown(f"<p style='color:{NEON_GREEN}'>Soma Otimizada: {soma}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
