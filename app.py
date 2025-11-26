import streamlit as st
import random
import time

# --- Configuração da Página ---
st.set_page_config(
    page_title="LotoTurbo Admin",
    page_icon="🎱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Constantes ---
ADMIN_EMAIL = "admin@lototurbo.com"
NEON_GREEN = "#39FF14"
DARK_BG = "#0E1117"
DARK_SEC = "#262730"

# --- CSS Personalizado (Dark Mode Forçado + Neon) ---
def local_css():
    st.markdown(f"""
        <style>
        /* Força fundo escuro geral */
        .stApp {{
            background-color: {DARK_BG};
            color: white;
        }}
        
        /* Inputs de texto e áreas */
        .stTextInput > div > div > input {{
            background-color: {DARK_SEC};
            color: white;
            border-color: #444;
        }}
        
        /* Estilização dos Botões (Neon Green) */
        div.stButton > button {{
            background-color: {NEON_GREEN} !important;
            color: black !important;
            font-weight: bold !important;
            border: none !important;
            border-radius: 8px !important;
            box-shadow: 0px 0px 10px {NEON_GREEN}80 !important; /* Glow effect */
            transition: all 0.3s ease;
        }}
        
        div.stButton > button:hover {{
            box-shadow: 0px 0px 20px {NEON_GREEN} !important;
            transform: scale(1.02);
        }}
        
        /* Headers e Textos */
        h1, h2, h3, p, label {{
            color: white !important;
        }}
        
        /* Ajuste de Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            white-space: pre-wrap;
            background-color: {DARK_SEC};
            border-radius: 5px;
            color: white;
            border: 1px solid #444;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {NEON_GREEN} !important;
            color: black !important;
            font-weight: bold;
        }}
        
        /* Cards de Resultado */
        .result-card {{
            background-color: {DARK_SEC};
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #444;
            margin-top: 20px;
            text-align: center;
        }}
        
        .number-ball {{
            display: inline-block;
            width: 35px;
            height: 35px;
            line-height: 35px;
            border-radius: 50%;
            background-color: {NEON_GREEN};
            color: black;
            font-weight: bold;
            text-align: center;
            margin: 3px;
            font-size: 14px;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- Funções Lógicas ---

def verificar_soma(numeros):
    """Verifica se a soma está entre 180 e 220."""
    total = sum(numeros)
    return 180 <= total <= 220, total

def gerar_jogo_otimizado():
    """Gera 15 números (1-25) com soma entre 180-220."""
    max_tentativas = 1000
    for _ in range(max_tentativas):
        jogo = sorted(random.sample(range(1, 26), 15))
        soma = sum(jogo)
        if 180 <= soma <= 220:
            return jogo, soma
    return None, 0

def render_bolas(numeros):
    """Renderiza os números como 'bolas' de loteria via HTML."""
    html = '<div style="margin-top: 10px;">'
    for num in sorted(numeros):
        html += f'<span class="number-ball">{num:02d}</span>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# --- Gerenciamento de Sessão ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- Aplicação Principal ---
def main():
    local_css() # Injeta o CSS
    
    # TELA DE LOGIN
    if not st.session_state['logged_in']:
        st.markdown("<h1 style='text-align: center; color: #39FF14 !important;'>🎱 LotoTurbo Admin</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Acesso Restrito</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            email = st.text_input("E-mail de Acesso", placeholder="admin@lototurbo.com")
            if st.button("ENTRAR", use_container_width=True):
                if email.strip() == ADMIN_EMAIL:
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("Acesso Negado. E-mail não autorizado.")
        return

    # TELA PRINCIPAL (Pós-Login)
    st.markdown(f"<h2 style='color: {NEON_GREEN} !important;'>Painel de Controle Lotofácil</h2>", unsafe_allow_html=True)
    
    # Botão de Logout no canto
    if st.sidebar.button("Sair"):
        st.session_state['logged_in'] = False
        st.rerun()

    tab1, tab2 = st.tabs(["📊 Analisador de Jogo", "🎲 Gerador Automático"])

    # --- ABA 1: ANALISADOR ---
    with tab1:
        st.markdown("### Verificar Jogo Existente")
        st.info("Digite 15 números separados por espaço ou vírgula (1 a 25).")
        
        input_nums = st.text_input("Números do jogo:", placeholder="Ex: 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15")
        
        if st.button("ANALISAR JOGO", use_container_width=True):
            if not input_nums:
                st.warning("Por favor, digite os números.")
            else:
                try:
                    # Tratamento de string para lista de inteiros (aceita vírgula ou espaço)
                    raw_nums = input_nums.replace(',', ' ').split()
                    numeros = [int(n) for n in raw_nums]
                    
                    # Validações básicas
                    if len(numeros) != 15:
                        st.error(f"Você digitou {len(numeros)} números. É necessário digitar exatamente 15.")
                    elif any(n < 1 or n > 25 for n in numeros):
                        st.error("Os números devem ser entre 1 e 25.")
                    elif len(set(numeros)) != 15:
                        st.error("Existem números repetidos.")
                    else:
                        # Lógica Principal
                        valido, soma = verificar_soma(numeros)
                        
                        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                        render_bolas(numeros)
                        st.markdown(f"<h4>Soma Total: {soma}</h4>", unsafe_allow_html=True)
                        
                        if valido:
                            st.markdown(f"<h3 style='color: {NEON_GREEN} !important;'>✅ APROVADO</h3>", unsafe_allow_html=True)
                            st.success("A soma está dentro do padrão estatístico (180-220).")
                        else:
                            st.markdown("<h3 style='color: #FF4B4B !important;'>❌ REPROVADO</h3>", unsafe_allow_html=True)
                            st.error("A soma está fora do padrão (180-220).")
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                except ValueError:
                    st.error("Entrada inválida. Digite apenas números inteiros.")

    # --- ABA 2: GERADOR ---
    with tab2:
        st.markdown("### Inteligência Artificial Geradora")
        st.write("O sistema irá gerar um jogo aleatório respeitando a regra de soma (180-220).")
        
        if st.button("GERAR PALPITE OTIMIZADO", use_container_width=True):
            with st.spinner("Calculando probabilidades..."):
                time.sleep(0.5) # Efeito visual de processamento
                jogo, soma = gerar_jogo_otimizado()
            
            if jogo:
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown("<p>Palpite Gerado:</p>", unsafe_allow_html=True)
                render_bolas(jogo)
                st.markdown(f"<h4 style='margin-top:15px;'>Soma: {soma}</h4>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: {NEON_GREEN}; font-size: 0.8em;'>Padrão de Soma Válido</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Texto para copiar fácil
                lista_txt = str(jogo).replace('[', '').replace(']', '')
                st.text_area("Copiar números:", value=lista_txt, height=70)
            else:
                st.error("Erro ao gerar combinação. Tente novamente.")

if __name__ == "__main__":
    main()
