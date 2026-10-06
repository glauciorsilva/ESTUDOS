# Prática Python para Dados 🐍

App single-file (HTML + JS + Python via Pyodide) para praticar Python aplicado a dados — do iniciante ao profissional — com casos reais, correção automática e sugestão de código mais enxuto.

Feito para quem está estudando para atuar como **Cientista de Dados**: cobre Python básico, Programação Orientada a Objetos, Pandas, SQLite e uma introdução a Tkinter, terminando num projeto integrador que junta tudo.

## Como usar

Não precisa instalar nada. Basta abrir o arquivo no navegador:

```
index.html
```

Dê duplo-clique nele (ou arraste para o Chrome/Edge). Na primeira execução, aguarde ~30-60s enquanto o ambiente Python (Pyodide + pandas + sqlite3) carrega — é necessário internet só nesse momento; depois fica em cache do navegador.

> Alternativa (evita eventuais bloqueios do navegador ao abrir via `file://`): sirva a pasta com um servidor local.
> ```bash
> python -m http.server 8000
> ```
> e acesse `http://localhost:8000`.

## O que o app faz

- **16 exercícios progressivos**: Python Básico → POO → Pandas → SQLite → Tkinter → Projeto Integrador (Profissional)
- Editor de código real (CodeMirror) com Python de verdade rodando **no navegador** (nenhum dado sai da sua máquina)
- **Executar**: roda seu código livremente e mostra a saída
- **Verificar solução**: corrige automaticamente e explica o que falta
- Em erro: traceback completo + dica traduzida do que provavelmente deu errado
- Ao acertar: mostra uma versão mais enxuta/idiomática do código, com a explicação de cada melhoria
- Progresso salvo automaticamente no navegador (`localStorage`)
- **Buscar novidades**: busca ao vivo na PyPI as versões mais recentes de pandas/numpy/scikit-learn
- **Banco de dados real (opcional)**: rodando o backend em `backend/`, o app passa a salvar progresso e histórico de tentativas num SQLite de verdade, além do navegador

## Banco de dados (opcional)

O app funciona sozinho, só com o navegador. Se você quiser persistir seu progresso e seu histórico de tentativas num **banco de dados de verdade** (não só no `localStorage`), suba o backend incluído:

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Isso sobe um servidor Flask em `http://localhost:5000` com um banco SQLite (`backend/progresso.db`). Com o backend rodando, abra (ou recarregue) o `index.html` — o indicador **"🗄️ Banco"** no cabeçalho muda para "conectado" e passa a sincronizar automaticamente. Sem o backend rodando, o app continua funcionando normalmente, só com `localStorage`.

Detalhes do schema, endpoints e consultas SQL de exemplo (inclusive sobre seu próprio histórico de tentativas) em [`docs/DOCUMENTACAO.md`](docs/DOCUMENTACAO.md#7-banco-de-dados-implementado).

## Limitações conhecidas

- Os exercícios de **Tkinter não abrem uma janela real** — o navegador não executa GUIs nativas. A correção neles é estrutural (verifica se o código tem os elementos certos). Para ver a janela de verdade, copie o código e rode localmente com `python arquivo.py`.
- O progresso só sincroniza com o banco enquanto o backend local (`backend/app.py`) estiver rodando na mesma máquina. Ele não funciona num deploy estático (ex: Vercel) — veja a nota abaixo.
- Se você publicar este app num host estático (Vercel, GitHub Pages, Netlify), **só o `index.html` funciona lá** (os exercícios em si, 100% client-side). O backend/banco de dados precisa continuar rodando local na sua máquina, ou ser adaptado para um serviço com banco persistente (fora do escopo deste projeto por enquanto).

## Estrutura do projeto

```
.
├── index.html              # app completo (UI + engine + conteúdo dos exercícios)
├── README.md                # este arquivo
├── .gitignore
├── backend/                 # opcional: API + banco SQLite para persistir progresso
│   ├── app.py
│   ├── schema.sql
│   └── requirements.txt
└── docs/
    └── DOCUMENTACAO.md       # arquitetura, como adicionar exercícios, decisões técnicas
```

## Requisitos

- Navegador moderno (Chrome ou Edge recomendados — testado nesses)
- Conexão com internet na primeira abertura (para baixar o Pyodide)

## Stack

- [Pyodide](https://pyodide.org/) — Python (com pandas e sqlite3) rodando via WebAssembly, direto no navegador
- [CodeMirror 5](https://codemirror.net/5/) — editor de código
- HTML/CSS/JS puro, sem build step, sem dependências de projeto (tudo via CDN)

## Roadmap

- [x] Persistência de progresso em banco de dados real (backend Flask + SQLite, ver acima e [`docs/DOCUMENTACAO.md`](docs/DOCUMENTACAO.md#7-banco-de-dados-implementado))
- [ ] Mais exercícios (ex: APIs, visualização com matplotlib)
- [ ] Exportar relatório de progresso em PDF/CSV
- [ ] Deploy do frontend em produção (Vercel) — pendente autorização da integração GitHub↔Vercel na conta do usuário

## Licença

Uso pessoal / educacional.

## ☁️ Nuvem (Firebase) — funciona na Vercel

O `index.html` tem login com Google e salva o progresso no Firestore (projeto `estudogrcs`),
em `usuarios/{uid}` (`completed`, `code`) e `usuarios/{uid}/tentativas`.

Configuração única no [console do Firebase](https://console.firebase.google.com/project/estudogrcs):

1. **Authentication → Sign-in method** → ativar **Google**.
2. **Authentication → Settings → Authorized domains** → adicionar `estudogr.vercel.app` (e `localhost`).
3. **Firestore Database** → criar o banco e publicar as regras do arquivo [`firestore.rules`](firestore.rules)
   (cole em *Firestore → Rules → Publish*, ou rode `firebase deploy --only firestore:rules`).
   Cada usuário só acessa `usuarios/{uid}`; o histórico em `tentativas` só aceita criação.

A `apiKey` do Firebase web é pública por design; a segurança vem das regras acima.

## 🕶️ Tema Matrix

Ao abrir, uma tela de entrada mostra um boneco de óculos escuros oferecendo duas pílulas:
**vermelha** = entrar com Google (progresso na nuvem) e **azul** = continuar sem login.
O app inteiro usa chuva de código verde, editor com tema próprio e fonte monoespaçada.
