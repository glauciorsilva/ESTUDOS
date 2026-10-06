# -*- coding: utf-8 -*-
"""
Exercícios da apostila (fonte única).

Esta lista alimenta DUAS coisas:
  - a aba "Apostila" do app (via gerar_js.py -> apostila-exercicios.js)
  - o PDF da apostila (via build_pdf.py): enunciados e gabarito

Cada exercício tem:
  id, cap, nivel, topico, titulo, caso, starter, check, solucao, melhorias
  (exercícios de Tkinter usam mode="structural" + regras em `regras`)
"""

# cabeçalho/rodapé comuns dos scripts de verificação
_HEAD = '''_msgs = []
def _exige(cond, msg):
    if not cond:
        _msgs.append(msg)
def _pega(nome):
    return globals().get(nome, "__AUSENTE__")
try:
'''
_TAIL = '''except Exception as _e:
    _msgs.append(f"erro ao testar seu código: {type(_e).__name__}: {_e}")
{"ok": not _msgs, "message": "Tudo certo! 🎉" if not _msgs else " | ".join(_msgs)}
'''


def _check(corpo):
    linhas = corpo.strip("\n").split("\n")
    return _HEAD + "\n".join("    " + l if l.strip() else l for l in linhas) + "\n" + _TAIL


EXERCICIOS = []


def ex(**kw):
    EXERCICIOS.append(kw)


# ───────────────────────── CAPÍTULO 1 — PYTHON BÁSICO ─────────────────────────
ex(
    id="ap_acervo", cap=1, nivel="Iniciante", topico="Python Básico",
    titulo="Acervo da biblioteca de bairro",
    caso="""Você cuida do acervo de uma biblioteca. A lista "livros" tem, para cada livro, 'titulo', 'paginas' e 'exemplares'.

Calcule:
• total_paginas: soma de paginas * exemplares de todos os livros;
• livro_mais_longo: título do livro com mais páginas;
• titulos_raros: lista com os títulos que têm apenas 1 exemplar (na ordem original).""",
    starter='''livros = [
    {"titulo": "Dom Casmurro", "paginas": 256, "exemplares": 3},
    {"titulo": "O Cortiço", "paginas": 320, "exemplares": 1},
    {"titulo": "Memórias Póstumas", "paginas": 288, "exemplares": 2},
    {"titulo": "Iracema", "paginas": 176, "exemplares": 1},
]

# TODO: soma de paginas * exemplares
total_paginas = 0

# TODO: título do livro com mais páginas
livro_mais_longo = ""

# TODO: lista de títulos com exatamente 1 exemplar
titulos_raros = []
''',
    check=_check('''
_exige(_pega("total_paginas") == 1840, f"total_paginas deveria ser 1840, veio {_pega('total_paginas')!r}")
_exige(_pega("livro_mais_longo") == "O Cortiço", f"livro_mais_longo deveria ser 'O Cortiço', veio {_pega('livro_mais_longo')!r}")
_exige(_pega("titulos_raros") == ["O Cortiço", "Iracema"], f"titulos_raros deveria ser ['O Cortiço', 'Iracema'], veio {_pega('titulos_raros')!r}")
'''),
    solucao='''livros = [
    {"titulo": "Dom Casmurro", "paginas": 256, "exemplares": 3},
    {"titulo": "O Cortiço", "paginas": 320, "exemplares": 1},
    {"titulo": "Memórias Póstumas", "paginas": 288, "exemplares": 2},
    {"titulo": "Iracema", "paginas": 176, "exemplares": 1},
]

total_paginas = sum(l["paginas"] * l["exemplares"] for l in livros)
livro_mais_longo = max(livros, key=lambda l: l["paginas"])["titulo"]
titulos_raros = [l["titulo"] for l in livros if l["exemplares"] == 1]
''',
    melhorias=[
        "sum() com expressão geradora no lugar do for + acumulador",
        "max(..., key=...) devolve o item inteiro; depois pegamos só o título",
        "List comprehension com if filtra e transforma em uma única linha",
    ],
)

ex(
    id="ap_matricula", cap=1, nivel="Iniciante", topico="Python Básico",
    titulo="Validador de matrícula escolar",
    caso="""Uma escola usa matrículas no formato 'MAT-2024-0153': prefixo MAT, ano com 4 dígitos e número com 4 dígitos, separados por hífen.

Escreva a função matricula_valida(texto) que devolve True ou False.
Regras: ignore espaços nas pontas e aceite minúsculas ('mat-2024-0153' é válida).""",
    starter='''def matricula_valida(texto):
    # TODO: devolva True se o texto seguir o formato MAT-AAAA-NNNN
    return False
''',
    check=_check('''
f = _pega("matricula_valida")
_exige(callable(f), "defina a função matricula_valida(texto)")
if callable(f):
    for bom in ["MAT-2024-0153", " mat-2023-0001 ", "Mat-1999-9999"]:
        _exige(f(bom) is True, f"{bom!r} deveria ser válida (True)")
    for ruim in ["MAT-24-0153", "MAT-2024-015", "ABC-2024-0153", "MAT-2024-01a3",
                 "MAT2024-0153", "MAT-2024-0153-9", ""]:
        _exige(f(ruim) is False, f"{ruim!r} deveria ser inválida (False)")
'''),
    solucao='''def matricula_valida(texto):
    partes = texto.strip().upper().split("-")
    if len(partes) != 3:
        return False
    prefixo, ano, numero = partes
    return (prefixo == "MAT"
            and len(ano) == 4 and ano.isdigit()
            and len(numero) == 4 and numero.isdigit())
''',
    melhorias=[
        "strip() + upper() normalizam a entrada antes de validar (uma regra só, sem duplicar casos)",
        "split('-') + desempacotamento deixa claro o que é cada pedaço",
        "isdigit() evita converter para int só para testar se é número",
    ],
)

ex(
    id="ap_boletim", cap=1, nivel="Iniciante", topico="Python Básico",
    titulo="Boletim escolar com funções e f-strings",
    caso="""Escreva a função situacao(notas) que recebe uma lista de notas e devolve a tupla (media, texto):
• media arredondada com 1 casa decimal;
• texto = "Aprovado" se media >= 7, "Recuperação" se media >= 5, senão "Reprovado".

Depois, usando o dicionário "alunos", monte o dicionário "boletim" no formato {nome: texto_da_situacao}.""",
    starter='''def situacao(notas):
    # TODO: calcule a média (1 casa decimal) e decida o texto
    return (0, "")


alunos = {
    "Ana": [8, 9, 7.5],
    "Bruno": [5, 6, 4],
    "Carla": [3, 4, 2],
}

# TODO: {nome: texto} usando a função situacao
boletim = {}
''',
    check=_check('''
f = _pega("situacao")
_exige(callable(f), "defina a função situacao(notas)")
if callable(f):
    _exige(f([7, 7]) == (7.0, "Aprovado"), f"situacao([7, 7]) deveria ser (7.0, 'Aprovado'), veio {f([7, 7])!r}")
    _exige(f([6.9, 6.9]) == (6.9, "Recuperação"), f"situacao([6.9, 6.9]) deveria ser (6.9, 'Recuperação'), veio {f([6.9, 6.9])!r}")
    _exige(f([2, 3]) == (2.5, "Reprovado"), f"situacao([2, 3]) deveria ser (2.5, 'Reprovado'), veio {f([2, 3])!r}")
esperado = {"Ana": "Aprovado", "Bruno": "Recuperação", "Carla": "Reprovado"}
_exige(_pega("boletim") == esperado, f"boletim deveria ser {esperado}, veio {_pega('boletim')!r}")
'''),
    solucao='''def situacao(notas):
    media = round(sum(notas) / len(notas), 1)
    if media >= 7:
        return (media, "Aprovado")
    if media >= 5:
        return (media, "Recuperação")
    return (media, "Reprovado")


alunos = {
    "Ana": [8, 9, 7.5],
    "Bruno": [5, 6, 4],
    "Carla": [3, 4, 2],
}

boletim = {nome: situacao(notas)[1] for nome, notas in alunos.items()}
''',
    melhorias=[
        "Retornos antecipados (return dentro do if) dispensam else/elif aninhados",
        "Dict comprehension monta o resultado direto, sem criar o dict vazio e preencher no loop",
        "A função faz uma coisa só (classificar); quem monta o boletim é outro trecho",
    ],
)

# ───────────────────────── CAPÍTULO 2 — POO ─────────────────────────
ex(
    id="ap_livro_classe", cap=2, nivel="Intermediário", topico="POO",
    titulo="Classe Livro com empréstimo e devolução",
    caso="""Crie a classe Livro com:
• __init__(self, titulo, exemplares) guardando os dois valores;
• emprestar(): diminui 1 exemplar; se não houver nenhum disponível, levanta ValueError("sem exemplares");
• devolver(): aumenta 1 exemplar;
• __str__: devolve "Título (N disponíveis)", por exemplo "Iracema (1 disponíveis)".""",
    starter='''class Livro:
    # TODO: __init__, emprestar, devolver e __str__
    pass
''',
    check=_check('''
L = _pega("Livro")
_exige(isinstance(L, type), "defina a classe Livro")
if isinstance(L, type):
    l = L("Iracema", 1)
    _exige(l.titulo == "Iracema" and l.exemplares == 1, "o __init__ deve guardar titulo e exemplares")
    l.emprestar()
    _exige(l.exemplares == 0, "emprestar() deveria diminuir 1 exemplar")
    try:
        l.emprestar()
        _msgs.append("emprestar() sem exemplares deveria levantar ValueError")
    except ValueError:
        pass
    l.devolver()
    _exige(l.exemplares == 1, "devolver() deveria aumentar 1 exemplar")
    _exige(str(l) == "Iracema (1 disponíveis)", f"str(livro) deveria ser 'Iracema (1 disponíveis)', veio {str(l)!r}")
'''),
    solucao='''class Livro:
    def __init__(self, titulo, exemplares):
        self.titulo = titulo
        self.exemplares = exemplares

    def emprestar(self):
        if self.exemplares == 0:
            raise ValueError("sem exemplares")
        self.exemplares -= 1

    def devolver(self):
        self.exemplares += 1

    def __str__(self):
        return f"{self.titulo} ({self.exemplares} disponíveis)"
''',
    melhorias=[
        "A regra de negócio (não emprestar sem estoque) fica DENTRO da classe, não espalhada pelo programa",
        "raise ValueError dá um erro claro; quem chama decide como tratar com try/except",
        "__str__ faz print(livro) ficar legível sem código extra",
    ],
)

ex(
    id="ap_planos_heranca", cap=2, nivel="Intermediário", topico="POO",
    titulo="Planos de academia com herança",
    caso="""A classe Plano já existe: guarda 'aluno' e 'base' e sua mensalidade() devolve a base.

Crie:
• PlanoAnual(Plano): mensalidade() com 20% de desconto sobre a base;
• PlanoPersonal(Plano): mensalidade() = base + 150 (taxa do personal).

Depois calcule total_mensal: soma de mensalidade() de todos os planos da lista "planos".""",
    starter='''class Plano:
    def __init__(self, aluno, base):
        self.aluno = aluno
        self.base = base

    def mensalidade(self):
        return self.base


# TODO: PlanoAnual (20% de desconto) e PlanoPersonal (base + 150)
class PlanoAnual(Plano):
    pass


class PlanoPersonal(Plano):
    pass


planos = [Plano("Rita", 120), PlanoAnual("Caio", 120), PlanoPersonal("Lia", 120)]

# TODO: some a mensalidade de todos os planos
total_mensal = 0
''',
    check=_check('''
PA, PP, P = _pega("PlanoAnual"), _pega("PlanoPersonal"), _pega("Plano")
_exige(isinstance(PA, type) and issubclass(PA, P), "PlanoAnual deve herdar de Plano")
_exige(isinstance(PP, type) and issubclass(PP, P), "PlanoPersonal deve herdar de Plano")
_exige(abs(PA("A", 100).mensalidade() - 80) < 0.01, "PlanoAnual(base=100).mensalidade() deveria ser 80")
_exige(abs(PP("B", 100).mensalidade() - 250) < 0.01, "PlanoPersonal(base=100).mensalidade() deveria ser 250")
_exige(abs(_pega("total_mensal") - 486) < 0.01, f"total_mensal deveria ser 486, veio {_pega('total_mensal')!r}")
'''),
    solucao='''class Plano:
    def __init__(self, aluno, base):
        self.aluno = aluno
        self.base = base

    def mensalidade(self):
        return self.base


class PlanoAnual(Plano):
    def mensalidade(self):
        return super().mensalidade() * 0.8


class PlanoPersonal(Plano):
    def mensalidade(self):
        return super().mensalidade() + 150


planos = [Plano("Rita", 120), PlanoAnual("Caio", 120), PlanoPersonal("Lia", 120)]

total_mensal = sum(p.mensalidade() for p in planos)
''',
    melhorias=[
        "super().mensalidade() reaproveita a regra da classe-mãe em vez de copiar self.base",
        "Polimorfismo: o loop chama p.mensalidade() sem saber qual é o tipo de plano",
        "Um novo tipo de plano é só mais uma subclasse; o cálculo do total não muda",
    ],
)

ex(
    id="ap_carteirinha", cap=2, nivel="Intermediário", topico="POO",
    titulo="Carteirinha de cafeteria (encapsulamento)",
    caso="""Crie a classe Carteirinha(dono, saldo=0) que guarda o saldo de forma protegida:
• o saldo fica em self._saldo e é lido pela property "saldo" (somente leitura: atribuir carteirinha.saldo = 10 deve dar erro);
• depositar(valor): valor deve ser > 0, senão ValueError;
• pagar(valor): se valor > saldo, levanta ValueError("saldo insuficiente"); senão desconta.""",
    starter='''class Carteirinha:
    # TODO: __init__, property saldo, depositar e pagar
    pass
''',
    check=_check('''
C = _pega("Carteirinha")
_exige(isinstance(C, type), "defina a classe Carteirinha")
if isinstance(C, type):
    c = C("Marta", 20)
    _exige(c.saldo == 20, "o saldo inicial deveria ser 20")
    c.depositar(30)
    _exige(c.saldo == 50, "depositar(30) deveria levar o saldo a 50")
    c.pagar(15)
    _exige(c.saldo == 35, "pagar(15) deveria levar o saldo a 35")
    for acao, msg in [(lambda: c.pagar(100), "pagar mais que o saldo deveria levantar ValueError"),
                      (lambda: c.depositar(0), "depositar(0) deveria levantar ValueError"),
                      (lambda: c.depositar(-5), "depositar(-5) deveria levantar ValueError")]:
        try:
            acao()
            _msgs.append(msg)
        except ValueError:
            pass
    try:
        c.saldo = 999
        _msgs.append("atribuir carteirinha.saldo = 999 deveria dar erro (property sem setter)")
    except AttributeError:
        pass
    _exige(c.saldo == 35, "o saldo não pode mudar quando uma operação é recusada")
'''),
    solucao='''class Carteirinha:
    def __init__(self, dono, saldo=0):
        self.dono = dono
        self._saldo = saldo

    @property
    def saldo(self):
        return self._saldo

    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("valor deve ser positivo")
        self._saldo += valor

    def pagar(self, valor):
        if valor > self._saldo:
            raise ValueError("saldo insuficiente")
        self._saldo -= valor
''',
    melhorias=[
        "Property sem setter impede alterações diretas: o saldo só muda por depositar/pagar",
        "Validar ANTES de alterar o estado garante que uma operação recusada não deixa o objeto pela metade",
        "O underscore (_saldo) é a convenção de 'uso interno da classe'",
    ],
)

# ───────────────────────── CAPÍTULO 3 — PANDAS ─────────────────────────
ex(
    id="ap_cafeteria_df", cap=3, nivel="Avançado", topico="Pandas",
    titulo="Vendas da cafeteria: coluna nova e groupby",
    caso="""O DataFrame "vendas" tem as colunas bebida, qtd e preco.

1) Crie a coluna "total" = qtd * preco;
2) receita_por_bebida: Series com a soma de "total" por bebida (use groupby);
3) bebida_campea: nome da bebida com maior receita.""",
    starter='''import pandas as pd

vendas = pd.DataFrame({
    "bebida": ["Café", "Cappuccino", "Café", "Chá", "Cappuccino", "Café"],
    "qtd":    [2, 1, 3, 1, 2, 1],
    "preco":  [6.0, 9.5, 6.0, 5.0, 9.5, 6.0],
})

# TODO 1: coluna "total"

# TODO 2: soma de total por bebida
receita_por_bebida = None

# TODO 3: nome da bebida campeã
bebida_campea = ""
''',
    check=_check('''
v = _pega("vendas")
_exige("total" in v.columns, "crie a coluna 'total' no DataFrame vendas")
if "total" in v.columns:
    _exige(v["total"].tolist() == [12.0, 9.5, 18.0, 5.0, 19.0, 6.0], f"coluna total incorreta: {v['total'].tolist()}")
r = _pega("receita_por_bebida")
_exige(r is not None and not isinstance(r, str) and dict(r) == {"Café": 36.0, "Cappuccino": 28.5, "Chá": 5.0},
       f"receita_por_bebida deveria ser Café=36.0, Cappuccino=28.5, Chá=5.0")
_exige(_pega("bebida_campea") == "Café", f"bebida_campea deveria ser 'Café', veio {_pega('bebida_campea')!r}")
'''),
    solucao='''import pandas as pd

vendas = pd.DataFrame({
    "bebida": ["Café", "Cappuccino", "Café", "Chá", "Cappuccino", "Café"],
    "qtd":    [2, 1, 3, 1, 2, 1],
    "preco":  [6.0, 9.5, 6.0, 5.0, 9.5, 6.0],
})

vendas["total"] = vendas["qtd"] * vendas["preco"]
receita_por_bebida = vendas.groupby("bebida")["total"].sum()
bebida_campea = receita_por_bebida.idxmax()
''',
    melhorias=[
        "Operações vetorizadas (coluna * coluna) dispensam loops linha a linha",
        "groupby(...)[coluna].sum() é o padrão 'agrupe e some'",
        "idxmax() devolve o RÓTULO do maior valor (max() devolveria o valor)",
    ],
)

ex(
    id="ap_limpeza_alunos", cap=3, nivel="Avançado", topico="Pandas",
    titulo="Limpeza do cadastro de alunos",
    caso="""O DataFrame "bruto" veio de uma planilha bagunçada. Gere o DataFrame "limpo" seguindo, nesta ordem:
1) nomes sem espaços nas pontas e com Iniciais Maiúsculas;
2) remova linhas sem nome;
3) remova linhas duplicadas;
4) converta "idade" para número inteiro;
5) nota ausente significa que o aluno faltou: preencha com 0.0.

Dica: use reset_index(drop=True) no final.""",
    starter='''import pandas as pd

bruto = pd.DataFrame({
    "nome":  ["  ana lima", "BRUNO souza", "Ana Lima ", "carla dias", None],
    "idade": ["20", "21", "20", "19", "22"],
    "nota":  [8.0, None, 8.0, 7.5, 6.0],
})

limpo = bruto.copy()
# TODO: aplique os 5 passos em "limpo"
''',
    check=_check('''
l = _pega("limpo").reset_index(drop=True)
_exige(l["nome"].tolist() == ["Ana Lima", "Bruno Souza", "Carla Dias"], f"nomes incorretos: {l['nome'].tolist()}")
_exige([int(x) for x in l["idade"].tolist()] == [20, 21, 19] and str(l["idade"].dtype).startswith("int"),
       f"idade deve ser inteira [20, 21, 19], veio {l['idade'].tolist()} ({l['idade'].dtype})")
_exige(l["nota"].tolist() == [8.0, 0.0, 7.5], f"notas incorretas: {l['nota'].tolist()}")
'''),
    solucao='''import pandas as pd

bruto = pd.DataFrame({
    "nome":  ["  ana lima", "BRUNO souza", "Ana Lima ", "carla dias", None],
    "idade": ["20", "21", "20", "19", "22"],
    "nota":  [8.0, None, 8.0, 7.5, 6.0],
})

limpo = bruto.copy()
limpo["nome"] = limpo["nome"].str.strip().str.title()
limpo = limpo.dropna(subset=["nome"])
limpo = limpo.drop_duplicates()
limpo["idade"] = limpo["idade"].astype(int)
limpo["nota"] = limpo["nota"].fillna(0.0)
limpo = limpo.reset_index(drop=True)
''',
    melhorias=[
        "A ordem importa: normalizar o nome ANTES de procurar duplicadas revela 'ana lima' = 'Ana Lima '",
        "dropna(subset=[...]) só olha as colunas que importam",
        "Sempre trabalhe numa cópia (bruto.copy()) para poder comparar antes/depois",
    ],
)

ex(
    id="ap_pivot_faltas", cap=3, nivel="Avançado", topico="Pandas",
    titulo="Pivot de faltas por turma e mês",
    caso="""O DataFrame "freq" registra faltas por turma e mês.

Crie:
• pivot: tabela com uma linha por turma, uma coluna por mês e a SOMA de faltas (células vazias = 0);
• turma_mais_faltas: nome da turma com o maior total de faltas (somando todos os meses).""",
    starter='''import pandas as pd

freq = pd.DataFrame({
    "turma":  ["A", "A", "B", "B", "A", "B"],
    "mes":    ["mar", "abr", "mar", "abr", "abr", "mar"],
    "faltas": [2, 1, 3, 0, 4, 1],
})

# TODO: pivot_table com soma de faltas
pivot = None

# TODO: turma com mais faltas no total
turma_mais_faltas = ""
''',
    check=_check('''
p = _pega("pivot")
_exige(p is not None and not isinstance(p, str), "crie a tabela 'pivot' com pd.pivot_table")
if p is not None and not isinstance(p, str):
    _exige(p.loc["A", "mar"] == 2 and p.loc["A", "abr"] == 5, "turma A: mar deveria ser 2 e abr deveria ser 5")
    _exige(p.loc["B", "mar"] == 4 and p.loc["B", "abr"] == 0, "turma B: mar deveria ser 4 e abr deveria ser 0")
_exige(_pega("turma_mais_faltas") == "A", f"turma_mais_faltas deveria ser 'A', veio {_pega('turma_mais_faltas')!r}")
'''),
    solucao='''import pandas as pd

freq = pd.DataFrame({
    "turma":  ["A", "A", "B", "B", "A", "B"],
    "mes":    ["mar", "abr", "mar", "abr", "abr", "mar"],
    "faltas": [2, 1, 3, 0, 4, 1],
})

pivot = pd.pivot_table(freq, values="faltas", index="turma",
                       columns="mes", aggfunc="sum", fill_value=0)
turma_mais_faltas = pivot.sum(axis=1).idxmax()
''',
    melhorias=[
        "pivot_table = groupby em duas dimensões, já formatado como planilha",
        "fill_value=0 troca as células sem dados por 0",
        "sum(axis=1) soma ao longo das colunas (por linha); axis=0 somaria por coluna",
    ],
)

ex(
    id="ap_merge_pacientes", cap=3, nivel="Avançado", topico="Pandas",
    titulo="Pacientes e consultas com merge",
    caso="""Há duas tabelas: "pacientes" (id, nome) e "consultas" (paciente_id, valor).

Crie:
• base: junção que mantém TODOS os pacientes, mesmo sem consulta (merge com how="left");
• gasto_por_paciente: Series com o total de "valor" por nome (quem não teve consulta soma 0);
• sem_consulta: lista com os nomes de quem não tem nenhuma consulta.""",
    starter='''import pandas as pd

pacientes = pd.DataFrame({"id": [1, 2, 3], "nome": ["Ana", "Bruno", "Carla"]})
consultas = pd.DataFrame({"paciente_id": [1, 1, 2], "valor": [150.0, 200.0, 180.0]})

# TODO: merge mantendo todos os pacientes
base = None

# TODO: total gasto por nome
gasto_por_paciente = None

# TODO: nomes sem consulta
sem_consulta = []
''',
    check=_check('''
g = _pega("gasto_por_paciente")
_exige(g is not None and not isinstance(g, str) and dict(g) == {"Ana": 350.0, "Bruno": 180.0, "Carla": 0.0},
       "gasto_por_paciente deveria ser Ana=350.0, Bruno=180.0, Carla=0.0")
_exige(_pega("sem_consulta") == ["Carla"], f"sem_consulta deveria ser ['Carla'], veio {_pega('sem_consulta')!r}")
b = _pega("base")
_exige(b is not None and not isinstance(b, str) and len(b) == 4, "base deveria ter 4 linhas (Ana 2x, Bruno 1x, Carla 1x)")
'''),
    solucao='''import pandas as pd

pacientes = pd.DataFrame({"id": [1, 2, 3], "nome": ["Ana", "Bruno", "Carla"]})
consultas = pd.DataFrame({"paciente_id": [1, 1, 2], "valor": [150.0, 200.0, 180.0]})

base = pacientes.merge(consultas, left_on="id", right_on="paciente_id", how="left")
gasto_por_paciente = base.groupby("nome")["valor"].sum()
sem_consulta = base[base["valor"].isna()]["nome"].tolist()
''',
    melhorias=[
        "how='left' preserva a tabela da esquerda inteira (é o LEFT JOIN do SQL)",
        "Nomes de chave diferentes nas tabelas? left_on/right_on resolvem",
        "isna() acha exatamente quem ficou sem par na junção",
    ],
)

# ───────────────────────── CAPÍTULO 4 — SQLITE ─────────────────────────
ex(
    id="ap_filmes_sql", cap=4, nivel="Avançado", topico="SQLite",
    titulo="Catálogo de filmes: CREATE, INSERT e SELECT",
    caso="""A conexão "conn" (banco em memória) já está aberta e a lista "catalogo" tem (titulo, nota).

1) Crie a tabela filmes(id INTEGER PRIMARY KEY, titulo TEXT, nota REAL);
2) Insira todos os itens de catalogo com executemany e parâmetros "?";
3) bem_avaliados: lista de títulos com nota >= 8, da maior para a menor nota (consulta SQL com ORDER BY).""",
    starter='''import sqlite3

conn = sqlite3.connect(":memory:")
catalogo = [
    ("Cidade de Deus", 8.6),
    ("Central do Brasil", 8.0),
    ("Tropa de Elite", 7.1),
    ("O Auto da Compadecida", 8.8),
]

# TODO 1: CREATE TABLE filmes (...)

# TODO 2: INSERT com executemany e "?"

# TODO 3: títulos com nota >= 8, maior nota primeiro
bem_avaliados = []
''',
    check=_check('''
_exige(_pega("bem_avaliados") == ["O Auto da Compadecida", "Cidade de Deus", "Central do Brasil"],
       f"bem_avaliados incorreto: {_pega('bem_avaliados')!r}")
n = _pega("conn").execute("SELECT COUNT(*) FROM filmes").fetchone()[0]
_exige(n == 4, f"a tabela filmes deveria ter 4 linhas, tem {n}")
'''),
    solucao='''import sqlite3

conn = sqlite3.connect(":memory:")
catalogo = [
    ("Cidade de Deus", 8.6),
    ("Central do Brasil", 8.0),
    ("Tropa de Elite", 7.1),
    ("O Auto da Compadecida", 8.8),
]

conn.execute("""CREATE TABLE filmes (
    id INTEGER PRIMARY KEY,
    titulo TEXT,
    nota REAL)""")
conn.executemany("INSERT INTO filmes (titulo, nota) VALUES (?, ?)", catalogo)
conn.commit()

linhas = conn.execute(
    "SELECT titulo FROM filmes WHERE nota >= ? ORDER BY nota DESC", (8,)
).fetchall()
bem_avaliados = [titulo for (titulo,) in linhas]
''',
    melhorias=[
        "Parâmetros '?' evitam SQL injection e problemas com aspas nos textos",
        "executemany insere a lista toda de uma vez",
        "fetchall() devolve tuplas; a comprehension com (titulo,) desembrulha cada uma",
    ],
)

ex(
    id="ap_join_pedidos", cap=4, nivel="Avançado", topico="SQLite",
    titulo="JOIN, GROUP BY e HAVING em pedidos de restaurante",
    caso="""As tabelas clientes(id, nome) e pedidos(id, cliente_id, valor) já estão criadas e preenchidas.

Escreva na variável "consulta" um SELECT que devolva, para cada cliente, três colunas NESTA ORDEM:
nome, total gasto (SUM do valor) e quantidade de pedidos (COUNT);
mostrando só clientes cujo total seja maior que 100, do maior total para o menor.""",
    starter='''import sqlite3

conn = sqlite3.connect(":memory:")
conn.executescript("""
CREATE TABLE clientes (id INTEGER PRIMARY KEY, nome TEXT);
CREATE TABLE pedidos  (id INTEGER PRIMARY KEY, cliente_id INTEGER, valor REAL);
INSERT INTO clientes VALUES (1, 'Ana'), (2, 'Bruno'), (3, 'Carla');
INSERT INTO pedidos (cliente_id, valor) VALUES (1, 60), (1, 70), (2, 40), (3, 200);
""")

# TODO: escreva o SELECT (nome, total, qtd) com JOIN + GROUP BY + HAVING + ORDER BY
consulta = ""

resultado = conn.execute(consulta).fetchall() if consulta else []
''',
    check=_check('''
c = _pega("consulta")
_exige(isinstance(c, str) and c.strip() != "", "escreva o SELECT na variável 'consulta'")
if isinstance(c, str) and c.strip():
    r = _pega("conn").execute(c).fetchall()
    esperado = [("Carla", 200.0, 1), ("Ana", 130.0, 2)]
    _exige(r == esperado, f"a consulta deveria devolver {esperado}, devolveu {r}")
'''),
    solucao='''import sqlite3

conn = sqlite3.connect(":memory:")
conn.executescript("""
CREATE TABLE clientes (id INTEGER PRIMARY KEY, nome TEXT);
CREATE TABLE pedidos  (id INTEGER PRIMARY KEY, cliente_id INTEGER, valor REAL);
INSERT INTO clientes VALUES (1, 'Ana'), (2, 'Bruno'), (3, 'Carla');
INSERT INTO pedidos (cliente_id, valor) VALUES (1, 60), (1, 70), (2, 40), (3, 200);
""")

consulta = """
SELECT c.nome, SUM(p.valor) AS total, COUNT(*) AS qtd
FROM clientes c
JOIN pedidos p ON p.cliente_id = c.id
GROUP BY c.id, c.nome
HAVING SUM(p.valor) > 100
ORDER BY total DESC
"""

resultado = conn.execute(consulta).fetchall() if consulta else []
''',
    melhorias=[
        "WHERE filtra LINHAS antes de agrupar; HAVING filtra GRUPOS depois de agregar",
        "Apelidos (c, p) deixam o JOIN curto e legível",
        "O banco faz a soma e a contagem; o Python só recebe o resultado pronto",
    ],
)

ex(
    id="ap_pandas_sql", cap=4, nivel="Avançado", topico="SQLite",
    titulo="Integração Pandas + SQLite (to_sql e read_sql)",
    caso="""O DataFrame "df" tem vendas de uma loja virtual.

1) Grave-o no banco com df.to_sql("vendas", conn, index=False, if_exists="replace");
2) Em df_sql, leia com pd.read_sql o total por categoria (colunas: categoria, total), do maior para o menor total.""",
    starter='''import sqlite3
import pandas as pd

conn = sqlite3.connect(":memory:")
df = pd.DataFrame({
    "categoria": ["Livros", "Games", "Livros", "Música"],
    "valor": [50.0, 200.0, 30.0, 20.0],
})

# TODO 1: df.to_sql(...)

# TODO 2: pd.read_sql("SELECT ...", conn)
df_sql = None
''',
    check=_check('''
d = _pega("df_sql")
_exige(d is not None and not isinstance(d, str), "crie df_sql com pd.read_sql(...)")
if d is not None and not isinstance(d, str):
    _exige(list(d.columns) == ["categoria", "total"], f"as colunas deveriam ser ['categoria', 'total'], vieram {list(d.columns)}")
    _exige(d["categoria"].tolist() == ["Games", "Livros", "Música"], f"ordem das categorias incorreta: {d['categoria'].tolist()}")
    _exige(d["total"].tolist() == [200.0, 80.0, 20.0], f"totais incorretos: {d['total'].tolist()}")
'''),
    solucao='''import sqlite3
import pandas as pd

conn = sqlite3.connect(":memory:")
df = pd.DataFrame({
    "categoria": ["Livros", "Games", "Livros", "Música"],
    "valor": [50.0, 200.0, 30.0, 20.0],
})

df.to_sql("vendas", conn, index=False, if_exists="replace")
df_sql = pd.read_sql(
    "SELECT categoria, SUM(valor) AS total FROM vendas "
    "GROUP BY categoria ORDER BY total DESC", conn)
''',
    melhorias=[
        "to_sql transforma um DataFrame em tabela sem escrever CREATE/INSERT",
        "read_sql devolve um DataFrame pronto para continuar a análise no pandas",
        "index=False evita gravar o índice do DataFrame como uma coluna extra",
    ],
)

# ───────────────────────── CAPÍTULO 5 — TKINTER ─────────────────────────
ex(
    id="ap_tk_contador", cap=5, nivel="Profissional", topico="Tkinter", mode="structural",
    titulo="Contador de cliques",
    caso="""Crie uma janela Tkinter com um Label que mostra "Cliques: 0" e um Button "Clicar". A cada clique, o número aumenta de 1 e o Label é atualizado.

⚠️ O navegador não abre janelas Tkinter. Aqui validamos a ESTRUTURA do código; copie e rode no seu computador para ver a janela de verdade.""",
    starter='''import tkinter as tk

contagem = 0

def clicar():
    # TODO: aumente a contagem e atualize o label
    pass

janela = tk.Tk()
janela.title("Contador")

# TODO: crie o Label "Cliques: 0" e o Button "Clicar" (command=clicar) e use pack()

# janela.mainloop()  # deixe comentado aqui; rode localmente
''',
    regras=[
        (r"import\s+tkinter", "Importe o módulo tkinter (import tkinter as tk)"),
        (r"tk\.Tk\(\)|(?<!\w)Tk\(\)", "Crie a janela principal com tk.Tk()"),
        (r"Label\(", "Crie um Label"),
        (r"Button\(", "Crie um Button"),
        (r"command\s*=", "Associe a função ao botão com command="),
        (r"global\s+\w+|self\.\w+\s*\+=\s*1", "Use 'global contagem' (ou um atributo self.contagem) para alterar a contagem dentro da função"),
        (r"\+=\s*1|=\s*\w+\s*\+\s*1", "Aumente a contagem em 1 (contagem += 1)"),
        (r"\.config\(|\.configure\(", "Atualize o texto do label com label.config(text=...)"),
        (r"\.pack\(|\.grid\(|\.place\(", "Adicione os widgets à janela com .pack(), .grid() ou .place()"),
    ],
    solucao='''import tkinter as tk

contagem = 0

def clicar():
    global contagem
    contagem += 1
    label.config(text=f"Cliques: {contagem}")

janela = tk.Tk()
janela.title("Contador")

label = tk.Label(janela, text="Cliques: 0")
label.pack(padx=20, pady=10)
tk.Button(janela, text="Clicar", command=clicar).pack(pady=(0, 10))

janela.mainloop()
''',
    melhorias=[
        "global é necessário para REATRIBUIR uma variável de fora da função",
        "Em apps maiores, prefira uma classe com self.contagem no lugar de variável global",
        "command=clicar passa a função SEM parênteses (quem chama é o Tkinter, no clique)",
    ],
)

ex(
    id="ap_tk_tarefas", cap=5, nivel="Profissional", topico="Tkinter", mode="structural",
    titulo="Lista de tarefas com Entry e Listbox",
    caso="""Monte uma janela com: um Entry para digitar uma tarefa, um Button "Adicionar" e um Listbox com as tarefas. Ao clicar, o texto do Entry vai para o fim do Listbox e o Entry é limpo.

⚠️ Validação estrutural (o navegador não abre janelas Tkinter). Rode no seu computador para ver funcionando.""",
    starter='''import tkinter as tk

def adicionar():
    # TODO: pegue o texto do Entry, insira no Listbox e limpe o Entry
    pass

janela = tk.Tk()
janela.title("Tarefas")

# TODO: Entry, Button (command=adicionar) e Listbox, todos com pack()

# janela.mainloop()
''',
    regras=[
        (r"import\s+tkinter", "Importe o módulo tkinter"),
        (r"tk\.Tk\(\)|(?<!\w)Tk\(\)", "Crie a janela principal com tk.Tk()"),
        (r"Entry\(", "Crie um Entry"),
        (r"Listbox\(", "Crie um Listbox"),
        (r"Button\(", "Crie um Button"),
        (r"command\s*=", "Associe a função ao botão com command="),
        (r"\.get\(\)", "Leia o texto digitado com entry.get()"),
        (r"\.insert\(", "Insira a tarefa no Listbox com lista.insert(tk.END, texto)"),
        (r"\.delete\(\s*0", "Limpe o Entry com entry.delete(0, tk.END)"),
        (r"\.pack\(|\.grid\(|\.place\(", "Adicione os widgets com .pack(), .grid() ou .place()"),
    ],
    solucao='''import tkinter as tk

def adicionar():
    texto = entrada.get().strip()
    if texto:
        lista.insert(tk.END, texto)
        entrada.delete(0, tk.END)

janela = tk.Tk()
janela.title("Tarefas")

entrada = tk.Entry(janela, width=30)
entrada.pack(padx=10, pady=(10, 5))
tk.Button(janela, text="Adicionar", command=adicionar).pack()
lista = tk.Listbox(janela, width=40, height=8)
lista.pack(padx=10, pady=10)

janela.mainloop()
''',
    melhorias=[
        "strip() + if texto impede adicionar tarefas vazias",
        "tk.END significa 'depois do último item' (para insert) e 'até o fim' (para delete)",
        "Entry.get() lê, Entry.delete(0, END) limpa: par de operações que você usará sempre",
    ],
)

# ───────────────────────── CAPÍTULO 6 — PROJETO INTEGRADOR ─────────────────────────
ex(
    id="ap_reservas_hotel", cap=6, nivel="Profissional", topico="Projeto Integrador",
    titulo="Sistema de reservas de hotel (POO + SQLite + pandas)",
    caso="""Crie a classe ReservaDB que usa um banco SQLite em memória:
• __init__: abre a conexão e cria a tabela reservas(id INTEGER PRIMARY KEY, hospede TEXT, noites INTEGER, diaria REAL);
• adicionar(hospede, noites, diaria): insere uma reserva;
• listar(): devolve um DataFrame com todas as reservas (pd.read_sql);
• faturamento(): soma de noites * diaria feita NO SQL (0.0 se não houver reservas);
• maior_reserva(): nome do hóspede com maior valor (noites * diaria).""",
    starter='''import sqlite3
import pandas as pd


class ReservaDB:
    # TODO: __init__, adicionar, listar, faturamento, maior_reserva
    pass


# Depois de implementar, teste assim:
# hotel = ReservaDB()
# hotel.adicionar("Marcos", 3, 200.0)
# print(hotel.listar())
''',
    check=_check('''
R = _pega("ReservaDB")
_exige(isinstance(R, type), "defina a classe ReservaDB")
if isinstance(R, type):
    h = R()
    _exige(h.faturamento() == 0, "sem reservas, faturamento() deveria ser 0")
    h.adicionar("Marcos", 3, 200.0)
    h.adicionar("Helena", 2, 450.0)
    h.adicionar("Paulo", 1, 300.0)
    d = h.listar()
    _exige(len(d) == 3, f"listar() deveria devolver 3 reservas, devolveu {len(d)}")
    _exige({"hospede", "noites", "diaria"} <= set(d.columns), "listar() deveria ter as colunas hospede, noites e diaria")
    _exige(abs(h.faturamento() - 1800.0) < 0.01, f"faturamento() deveria ser 1800.0, veio {h.faturamento()!r}")
    _exige(h.maior_reserva() == "Helena", f"maior_reserva() deveria ser 'Helena', veio {h.maior_reserva()!r}")
'''),
    solucao='''import sqlite3
import pandas as pd


class ReservaDB:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("""CREATE TABLE reservas (
            id INTEGER PRIMARY KEY,
            hospede TEXT,
            noites INTEGER,
            diaria REAL)""")

    def adicionar(self, hospede, noites, diaria):
        self.conn.execute(
            "INSERT INTO reservas (hospede, noites, diaria) VALUES (?, ?, ?)",
            (hospede, noites, diaria))
        self.conn.commit()

    def listar(self):
        return pd.read_sql("SELECT * FROM reservas", self.conn)

    def faturamento(self):
        total = self.conn.execute(
            "SELECT SUM(noites * diaria) FROM reservas").fetchone()[0]
        return total or 0.0

    def maior_reserva(self):
        linha = self.conn.execute(
            "SELECT hospede FROM reservas "
            "ORDER BY noites * diaria DESC LIMIT 1").fetchone()
        return linha[0] if linha else None
''',
    melhorias=[
        "Cada classe tem uma responsabilidade: ReservaDB cuida da persistência e dos relatórios",
        "A soma e o 'maior' são feitos pelo banco (SUM, ORDER BY ... LIMIT 1), não em loops Python",
        "'total or 0.0' trata o caso SUM() = NULL quando a tabela está vazia",
    ],
)

CAPITULOS = {
    1: "Python básico",
    2: "Programação orientada a objetos",
    3: "Pandas",
    4: "SQLite e SQL",
    5: "Tkinter",
    6: "Projeto integrador",
}
