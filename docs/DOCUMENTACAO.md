# Documentação Técnica — Prática Python para Dados

Este documento explica como o app funciona por dentro, para você conseguir dar manutenção, adicionar exercícios novos ou evoluir o projeto (ex: adicionar um banco de dados de verdade).

## 1. Visão geral da arquitetura

O projeto é **um único arquivo HTML** (`index.html`) sem build step. Tudo roda no navegador:

```
┌─────────────────────────────────────────────┐
│                index.html                     │
│                                                │
│  ┌──────────────┐   ┌────────────────────┐   │
│  │  CodeMirror   │   │      Pyodide        │   │
│  │  (editor de   │   │  (Python real via   │   │
│  │   código)     │   │   WebAssembly)       │   │
│  └──────────────┘   │  + pandas + sqlite3  │   │
│                      └────────────────────┘   │
│                                                │
│  EXERCISES[] (array JS com todo o conteúdo)   │
│  localStorage (progresso do usuário)          │
│  fetch() → PyPI (botão "Buscar novidades")    │
└─────────────────────────────────────────────┘
```

Não existe backend, servidor, nem build. Abrir o HTML é suficiente porque o Python que roda os exercícios é o **Pyodide**: CPython compilado para WebAssembly, carregado via CDN (`cdn.jsdelivr.net/pyodide`) na primeira execução.

## 2. Como cada exercício é definido

Cada exercício é um objeto dentro do array `EXERCISES` (dentro da tag `<script>`, no fim do `index.html`). Campos:

| Campo | Obrigatório | Descrição |
|---|---|---|
| `id` | sim | identificador único (usado no `localStorage` e no progresso) |
| `nivel` | sim | `"Iniciante"` \| `"Intermediário"` \| `"Avançado"` \| `"Profissional"` |
| `topico` | sim | rótulo mostrado como badge (ex: `"Pandas"`, `"POO"`) |
| `titulo` | sim | título do exercício |
| `caso` | sim | enunciado (texto do caso real) |
| `starter` | sim | código inicial que aparece no editor |
| `mode` | não | se omitido, o exercício é executado normalmente. Use `"structural"` para exercícios que **não podem ser executados** (caso do Tkinter — ver seção 4) |
| `check` | apenas se `mode` for omitido | código Python que roda **depois** do código do usuário, no mesmo namespace, e deve terminar com uma expressão `{"ok": bool, "message": str}` |
| `structuralRules` | apenas se `mode === "structural"` | lista de `{re: /regex/, desc: "..."}` — cada regex precisa dar match no código digitado |
| `otimizado` ou `otimizadoReal` | sim | código de referência mostrado após acertar |
| `melhorias` | sim | lista de strings (bullets) explicando o que a versão otimizada melhora |

### Exemplo mínimo de um novo exercício

```js
{
  id: "meu_exercicio_novo",
  nivel: "Iniciante",
  topico: "Python Básico",
  titulo: "Título do exercício",
  caso: "Descrição do problema real...",
  starter: `numeros = [1, 2, 3]\nsoma = 0  # TODO: calcule a soma\n`,
  check: `
_ok = True
_msgs = []
if soma != 6:
    _ok = False
    _msgs.append(f"soma deveria ser 6, veio {soma}")
{"ok": _ok, "message": "Tudo certo! 🎉" if _ok else " | ".join(_msgs)}
`,
  otimizado: `numeros = [1, 2, 3]\nsoma = sum(numeros)\n`,
  melhorias: ["sum() substitui o loop manual"]
}
```

Basta adicionar esse objeto ao array `EXERCISES` e ele aparece automaticamente na barra lateral (a UI é gerada dinamicamente a partir do array — não precisa mexer em HTML/CSS).

## 3. Como funciona a correção automática (`check`)

1. Ao clicar em **Verificar solução**, o app cria um **namespace Python isolado** (`pyodide.globals.get("dict")()`), para o código de um exercício não vazar variáveis para outro.
2. O código do usuário (`editor.getValue()`) é executado nesse namespace com `pyodide.runPython(code, {globals: ns})`.
3. Se não der erro, o código de `check` roda **no mesmo namespace** — por isso ele enxerga as variáveis/funções/classes que o usuário criou.
4. `check` sempre termina em uma expressão `{"ok": ..., "message": ...}` (sem `return`, sem `print`) — o Pyodide devolve o valor dessa última expressão para o JavaScript, como um REPL.
5. O JS lê `ok`/`message` e decide: mostra "Tudo certo 🎉" (e marca como concluído) ou mostra o que falta.

Isso é o mesmo princípio de um "judge" automático (tipo LeetCode/HackerRank), só que rodando 100% no navegador.

## 4. Por que os exercícios de Tkinter são diferentes

O Pyodide roda Python via WebAssembly **dentro do navegador**, que não tem um sistema de janelas (display server). O módulo `tkinter` depende de `_tkinter`, uma extensão C que nem existe compilada para WebAssembly. Ou seja: **não é uma limitação de configuração, é uma impossibilidade estrutural** — não dá para abrir uma janela GTK/Tk dentro de uma aba do Chrome.

Por isso, os exercícios de Tkinter usam `mode: "structural"`: em vez de executar o código, o app aplica uma lista de expressões regulares (`structuralRules`) sobre o **texto** do código digitado, checando se elementos esperados estão presentes (`import tkinter`, `Button(`, `command=`, etc.). Isso valida a estrutura do código sem executá-lo.

Para ver a janela de verdade, o próprio app avisa: copie o código e rode localmente com `python arquivo.py` (com Python instalado no seu computador).

## 5. Tratamento de erros

Quando o código do usuário lança uma exceção, o Pyodide propaga um erro JS (`PythonError`) contendo o traceback completo do Python. O app:

1. Mostra o traceback bruto no console de saída (`#saida-console`)
2. Passa a última linha do erro (`SyntaxError: ...`, `KeyError: ...` etc.) por uma função `errorHint()` que faz match por palavra-chave e devolve uma dica em português (ex: "IndentationError → confira se todas as linhas usam o mesmo número de espaços")

Essa lógica está em `errorHint()`, dentro do `<script>` do `index.html`. Para adicionar uma dica nova, basta acrescentar um par `[regex, texto]` no array `rules` dessa função.

## 6. Persistência do progresso (estado atual)

Hoje o progresso (quais exercícios foram concluídos + o código que você escreveu em cada um) é salvo em `localStorage`, sob a chave `praticapython_progress_v1`, como um JSON:

```json
{
  "completed": ["estoque_total", "analise_vendas_df", ...],
  "code": { "estoque_total": "produtos = [...]" }
}
```

**Limitações dessa abordagem:**
- Fica preso a um navegador específico, numa máquina específica
- Se o usuário limpar dados de navegação, o progresso some
- Não dá para consultar/analisar seu histórico de tentativas (ex: "quantas vezes errei antes de acertar")
- Não é literalmente "um banco de dados" — é um blob JSON

Para evoluir isso para um banco de dados de verdade, veja a seção 7.

## 7. Evoluindo para um banco de dados real

Existem três caminhos, dependendo do que você quer resolver. Nenhum deles está implementado ainda — são as opções recomendadas para o próximo passo do projeto.

### Opção A — Banco local simples, sem servidor (SQLite em arquivo, via script auxiliar)
Um script Python separado (fora do navegador) lê o JSON exportado do `localStorage` e grava num arquivo `.db` SQLite local. Simples, mas manual (sem sincronização automática).

### Opção B — Backend mínimo (Flask/FastAPI + SQLite) — recomendado para aprendizado
Sobe um servidor local (`python app.py`) com um banco SQLite real em disco (`progresso.db`). O `index.html` passa a fazer `fetch()` para esse backend em vez de usar só `localStorage`. Essa é a opção mais alinhada com o objetivo de "aprender banco de dados do iniciante ao profissional", porque pratica: schema de banco, API REST simples, e separação frontend/backend — habilidades reais de cientista/engenheiro de dados.

### Opção C — Banco na nuvem (Supabase/Postgres, Firebase, etc.)
Permite sincronizar progresso entre dispositivos. Mais complexo (autenticação, variáveis de ambiente, deploy), mas é o caminho profissional se a ideia é o projeto virar algo acessível de qualquer lugar.

> Antes de implementar qualquer uma dessas opções, é importante confirmar **para que exatamente** o banco vai servir (ver conversa/próximos passos do projeto) — o desenho do schema muda dependendo do objetivo.

## 8. Convenções de commit (sugestão)

Como o projeto passou a ser versionado com git, sugestão de padrão para mensagens de commit:

```
feat: adiciona exercício de agregação com pandas
fix: corrige checagem do exercício de SQLite
docs: atualiza README com instruções de uso
chore: configura .gitignore
```
