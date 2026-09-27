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

## Limitações conhecidas

- Os exercícios de **Tkinter não abrem uma janela real** — o navegador não executa GUIs nativas. A correção neles é estrutural (verifica se o código tem os elementos certos). Para ver a janela de verdade, copie o código e rode localmente com `python arquivo.py`.
- O progresso é salvo por navegador/máquina (não sincroniza entre dispositivos). Veja [`docs/DOCUMENTACAO.md`](docs/DOCUMENTACAO.md) para as opções de persistir isso de forma mais robusta.

## Estrutura do projeto

```
.
├── index.html              # app completo (UI + engine + conteúdo dos exercícios)
├── README.md                # este arquivo
├── .gitignore
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

- [ ] Persistência de progresso em banco de dados (ver [`docs/DOCUMENTACAO.md`](docs/DOCUMENTACAO.md))
- [ ] Mais exercícios (ex: APIs, visualização com matplotlib)
- [ ] Exportar relatório de progresso em PDF/CSV

## Licença

Uso pessoal / educacional.
