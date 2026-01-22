import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

creds = service_account.Credentials.from_service_account_info(st.secrets["firebase"])
db = firestore.Client(credentials=creds)

st.title("Criar Usuário")

# Formulário de Cadastro
with st.form("formFirebase"):
    nome = st.text_input("Nome:", placeholder="Informe seu nome...")
    apelido = st.text_input("Apelido:", placeholder="Informe seu apelido...")
    idade = st.number_input("Idade:", step=1, min_value=8, max_value=100)
    senha = st.text_input("Senha:", placeholder="Informe sua senha...", type="password")
    btnSalvarUsuario = st.form_submit_button("Salvar", use_container_width=True)

    if btnSalvarUsuario:
        if nome and idade and senha and apelido:
            novoUsuario = db.collection("usuarios").document(apelido)
            novoUsuario.set(
                {
                    "nome": nome,
                    "apelido": apelido,
                    "idade": idade,
                    "senha": senha
                }
            )
            st.success("Usuário criado!")
        else:
            st.error("Informe seu nome, apelido, idade e senha por gentileza")

"---"

usuarios = db.collection("usuarios").stream()

for usuarioRef in usuarios:
    usuario = usuarioRef.to_dict()
    nomeUsuario = usuario["nome"]
    idadeUsuario = usuario["idade"]
    apelidoUsuario = usuario["apelido"]
    st.subheader(f"Usuário {apelidoUsuario}")
    st.write(f":material/person: Nome: {nomeUsuario} com {idadeUsuario} anos")