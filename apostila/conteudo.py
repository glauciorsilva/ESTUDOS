# -*- coding: utf-8 -*-
"""
Conteúdo teórico da apostila.

Blocos suportados (cada capítulo é uma lista de seções; cada seção, uma lista de blocos):
  ("p", "texto com <b>negrito</b> e <i>itálico</i>")
  ("lista", ["item", ...])
  ("passos", ["passo 1", ...])              lista numerada
  ("code", "código")                        só exibe (não executa)
  ("run", "código", "legenda")              executa e mostra a SAÍDA REAL
  ("runc", "código", "legenda")             igual a run, mas continua o namespace do bloco anterior
  ("dica", "texto")  ("cuidado", "texto")  ("lembre", "texto")
  ("tabela", [[cab...], [linha...]], [larguras em %])
"""

CAP = {}

# ═════════════════════════════════════════════════════════════════════════
# CAPÍTULO 1 — PYTHON BÁSICO
# ═════════════════════════════════════════════════════════════════════════
CAP[1] = dict(
    titulo="Python básico",
    intro=("Tudo nos capítulos seguintes (classes, pandas, SQL) é construído sobre este "
           "alicerce: guardar valores, escolher caminhos, repetir tarefas e empacotar lógica "
           "em funções. Se você dominar estas páginas, o resto vira combinação de peças."),
    secoes=[
        ("1.1  Variáveis e tipos de dados", [
            ("p", "Uma <b>variável</b> é um nome que aponta para um valor. Em Python você não "
                  "declara o tipo: ele vem do valor. Os tipos básicos são <b>int</b> (inteiro), "
                  "<b>float</b> (decimal), <b>str</b> (texto), <b>bool</b> (verdadeiro/falso) e "
                  "<b>None</b> (ausência de valor)."),
            ("run", '''pao_unidade = 0.75        # float
quantidade = 12           # int
padaria = "Pão Quente"    # str
aberta = True             # bool
cliente = None            # None: ainda não temos cliente

print(type(pao_unidade), type(quantidade), type(padaria))
total = pao_unidade * quantidade
print(f"{padaria}: {quantidade} pães = R$ {total:.2f}")
print(int("42") + 1, float("3.5") * 2, str(7) + "!")''',
             "Tipos e conversões"),
            ("lembre", "Conversões: <b>int()</b>, <b>float()</b>, <b>str()</b>. O resultado de "
                       "input() é sempre texto: converta antes de fazer conta."),
            ("cuidado", "<b>=</b> atribui um valor; <b>==</b> compara dois valores. "
                        "Confundir os dois é um dos erros mais comuns de quem está começando."),
        ]),
        ("1.2  Listas, tuplas, dicionários e conjuntos", [
            ("p", "São as quatro formas de guardar <i>coleções</i>. Escolha pela pergunta que você "
                  "vai fazer aos dados:"),
            ("tabela", [
                ["Tipo", "Sintaxe", "Use quando…", "Mutável?"],
                ["list", "[1, 2, 3]", "ordem importa e pode repetir", "sim"],
                ["tuple", "(1, 2)", "grupo fixo (ex.: par nome/valor)", "não"],
                ["dict", '{"a": 1}', "buscar valor por uma chave", "sim"],
                ["set", "{1, 2, 3}", "sem repetidos / testar pertencimento", "sim"],
            ], [14, 22, 46, 18]),
            ("run", '''padaria = {"nome": "Pão Quente", "horario": (6, 20)}
paes = ["francês", "integral", "brioche"]

paes.append("baguete")        # adiciona no fim
print(paes[0], paes[-1])      # primeiro e último
print(paes[1:3])              # fatia: posições 1 e 2
print(padaria["nome"], padaria.get("telefone", "sem telefone"))

padaria["telefone"] = "9999-0000"      # adiciona/atualiza chave
for chave, valor in padaria.items():   # percorre pares
    print(chave, "->", valor)

print(set([1, 2, 2, 3, 3, 3]))         # remove repetidos''',
             "Operações essenciais"),
            ("dica", "dict.get(chave, padrao) não dá erro se a chave não existir; "
                     "dict[chave] dá KeyError. Use get quando a chave pode faltar."),
        ]),
        ("1.3  Condicionais e laços", [
            ("p", "<b>if / elif / else</b> escolhem um caminho. <b>for</b> repete para cada item "
                  "de uma sequência; <b>while</b> repete enquanto uma condição for verdadeira. A "
                  "<b>indentação</b> (4 espaços) define o que está dentro do bloco."),
            ("run", '''vendas_dia = [120.0, 85.5, 0, 240.0, 60.0]

for i, valor in enumerate(vendas_dia, start=1):   # i começa em 1
    if valor == 0:
        print(f"Dia {i}: loja fechada")
        continue                                   # pula para o próximo
    elif valor >= 100:
        faixa = "bom"
    else:
        faixa = "fraco"
    print(f"Dia {i}: R$ {valor:.2f} ({faixa})")

nomes = ["Ana", "Bia"]
notas = [9, 7]
for nome, nota in zip(nomes, notas):               # percorre em paralelo
    print(nome, nota)''',
             "if/elif/else, for, enumerate, zip"),
            ("lista", [
                "<b>range(n)</b>: 0 até n-1 (range(1, 6) vai de 1 a 5).",
                "<b>break</b> sai do laço; <b>continue</b> pula para a próxima volta.",
                "<b>and / or / not</b> combinam condições; <b>in</b> testa pertencimento "
                "(<i>if 'Ana' in nomes</i>).",
            ]),
        ]),
        ("1.4  Comprehensions e funções embutidas", [
            ("p", "Uma <b>list comprehension</b> cria uma lista nova a partir de outra em uma linha: "
                  "<i>[expressão for item in sequência if condição]</i>. As funções embutidas "
                  "<b>sum, min, max, len, sorted, any, all</b> resolvem a maioria dos laços simples."),
            ("run", '''pecas = [
    {"nome": "Filtro de óleo", "preco": 35.0, "qtd": 10},
    {"nome": "Pastilha de freio", "preco": 120.0, "qtd": 4},
    {"nome": "Lâmpada", "preco": 12.5, "qtd": 30},
]

valor_total = sum(p["preco"] * p["qtd"] for p in pecas)
mais_cara = max(pecas, key=lambda p: p["preco"])
baratas = [p["nome"] for p in pecas if p["preco"] < 40]
por_qtd = sorted(pecas, key=lambda p: p["qtd"], reverse=True)

print(valor_total, mais_cara["nome"], baratas)
print([p["nome"] for p in por_qtd])
print(any(p["qtd"] < 5 for p in pecas), all(p["preco"] > 10 for p in pecas))
quadrados = {n: n ** 2 for n in range(1, 5)}      # dict comprehension
print(quadrados)''',
             "sum, max(key=), sorted(key=), any/all"),
            ("lembre", "<b>key=</b> diz <i>por qual critério</i> comparar. "
                       "<b>lambda p: p['preco']</b> é uma função de uma linha que devolve o preço."),
        ]),
        ("1.5  Funções", [
            ("p", "Uma função empacota uma lógica com nome, recebe <b>parâmetros</b> e devolve um "
                  "resultado com <b>return</b>. Sem return, devolve None. Parâmetros podem ter "
                  "<b>valor padrão</b>, e dá para devolver vários valores (na verdade, uma tupla)."),
            ("run", '''def calcula_frete(peso_kg, expresso=False):
    """Frete: R$ 8 por kg; expresso custa 50% a mais."""
    valor = peso_kg * 8
    if expresso:
        valor *= 1.5
    return round(valor, 2)

def resumo(valores):
    return min(valores), max(valores), sum(valores) / len(valores)

print(calcula_frete(2))                    # usa o padrão (expresso=False)
print(calcula_frete(2, expresso=True))     # argumento nomeado
menor, maior, media = resumo([10, 20, 60])  # desempacotamento
print(menor, maior, round(media, 1))''',
             "def, return, parâmetro padrão, múltiplos retornos"),
            ("cuidado", "Variáveis criadas <i>dentro</i> da função só existem lá (escopo local). Para "
                        "usar um valor de fora, passe-o como parâmetro; evite <i>global</i>."),
        ]),
        ("1.6  Textos (strings) e f-strings", [
            ("p", "Strings têm dezenas de métodos prontos. Os que mais aparecem em tratamento de "
                  "dados: <b>strip, lower, upper, title, replace, split, join, startswith, "
                  "endswith, isdigit, in</b>. As <b>f-strings</b> inserem valores no texto, com "
                  "formatação depois dos dois pontos."),
            ("run", '''codigo = "  pet-2024-0087 "
limpo = codigo.strip().upper()
print(limpo, limpo.startswith("PET"), limpo.split("-"))
print("-".join(["a", "b", "c"]), "gato preto".title(), "2024".isdigit())

preco, qtd = 1234.5, 3
print(f"Total: R$ {preco * qtd:,.2f}")     # milhar e 2 casas
print(f"{'Item':<10}|{'Qtd':>5}")           # alinhar à esq./dir.
print(f"{0.256:.1%}  {7:03d}")               # percentual e zeros à esquerda''',
             "Métodos de texto e formatação"),
            ("tabela", [
                ["Formato", "Efeito", "Exemplo → resultado"],
                [":.2f", "2 casas decimais", "f'{3.14159:.2f}' → 3.14"],
                [":,", "separador de milhar", "f'{1234567:,}' → 1,234,567"],
                [":>8", "alinha à direita em 8 espaços", "f'{42:>8}' → '      42'"],
                [":.1%", "percentual", "f'{0.256:.1%}' → 25.6%"],
            ], [20, 36, 44]),
        ]),
        ("1.7  Erros e exceções", [
            ("p", "Quando algo dá errado, Python <i>levanta uma exceção</i>. Você pode antecipar "
                  "com <b>try/except</b> e também <b>levantar</b> a sua própria com <b>raise</b> "
                  "para recusar dados inválidos."),
            ("run", '''def divide(a, b):
    if b == 0:
        raise ValueError("divisor não pode ser zero")
    return a / b

for dado in [(10, 2), (1, 0)]:
    try:
        print("resultado:", divide(*dado))
    except ValueError as erro:
        print("recusado:", erro)
    finally:
        print("-- fim da tentativa --")''',
             "try / except / finally e raise"),
            ("tabela", [
                ["Erro", "Quase sempre significa…"],
                ["SyntaxError / IndentationError", "falta ':' , parêntese aberto ou indentação errada"],
                ["NameError", "usou um nome que ainda não existe (ou escreveu errado)"],
                ["TypeError", "misturou tipos (ex.: texto + número)"],
                ["KeyError", "a chave do dicionário/coluna não existe"],
                ["IndexError", "posição fora da lista"],
                ["ValueError", "valor com tipo certo, mas conteúdo inválido (int('abc'))"],
                ["ZeroDivisionError", "divisão por zero"],
            ], [38, 62]),
        ]),
    ],
    resolvido=dict(
        titulo="Exemplo resolvido — fechamento do caixa da padaria",
        enunciado=("A lista abaixo tem as vendas do dia (item, preço, quantidade). Descubra o faturamento "
                   "total, o item mais vendido (em quantidade) e a lista de itens que venderam menos de "
                   "5 unidades, em ordem alfabética."),
        passos=[
            "<b>Entender os dados:</b> lista de dicionários; cada venda tem 3 campos.",
            "<b>Faturamento:</b> soma de preço × quantidade → sum() com expressão geradora.",
            "<b>Mais vendido:</b> max() com key=quantidade, depois pegar o campo 'item'.",
            "<b>Poucos vendidos:</b> comprehension com if, e sorted() para ordenar.",
        ],
        codigo='''vendas = [
    {"item": "pão francês", "preco": 0.75, "qtd": 200},
    {"item": "bolo de milho", "preco": 18.0, "qtd": 3},
    {"item": "café", "preco": 4.5, "qtd": 60},
    {"item": "croissant", "preco": 7.0, "qtd": 4},
]

faturamento = sum(v["preco"] * v["qtd"] for v in vendas)
mais_vendido = max(vendas, key=lambda v: v["qtd"])["item"]
poucos = sorted(v["item"] for v in vendas if v["qtd"] < 5)

print(f"Faturamento: R$ {faturamento:.2f}")
print("Mais vendido:", mais_vendido)
print("Poucos vendidos:", poucos)''',
    ),
    armadilhas=[
        "Esquecer o <b>:</b> no fim de if/for/def/while.",
        "Alterar uma lista enquanto percorre a mesma lista (crie uma nova no lugar).",
        "Comparar texto com número ('5' == 5 é False). Converta com int()/float().",
        "Usar <b>round()</b> no meio dos cálculos: arredonde só no resultado final.",
    ],
    cola=[
        ["Quero…", "Use…"],
        ["somar / contar / maior", "sum(...) / len(...) / max(..., key=...)"],
        ["filtrar e transformar", "[expr for x in lista if cond]"],
        ["ordenar por um campo", "sorted(lista, key=lambda x: x['campo'])"],
        ["percorrer com posição", "for i, x in enumerate(lista):"],
        ["valor com padrão", "dicionario.get(chave, padrao)"],
        ["limpar texto", "texto.strip().lower()"],
        ["recusar dado inválido", "raise ValueError('mensagem')"],
    ],
    exercicios=["ap_acervo", "ap_matricula", "ap_boletim"],
)

# ═════════════════════════════════════════════════════════════════════════
# CAPÍTULO 2 — POO
# ═════════════════════════════════════════════════════════════════════════
CAP[2] = dict(
    titulo="Programação orientada a objetos",
    intro=("POO organiza o programa em <b>objetos</b> que juntam dados (atributos) e ações "
           "(métodos). Em vez de funções soltas manipulando dicionários, você cria o conceito "
           "(Animal, Pedido, Conta) uma vez e gera quantos exemplares precisar."),
    secoes=[
        ("2.1  Classe, objeto, __init__ e self", [
            ("p", "A <b>classe</b> é o molde; o <b>objeto</b> é cada peça fabricada com ele. "
                  "O método <b>__init__</b> roda quando o objeto nasce e guarda os dados iniciais. "
                  "<b>self</b> é o próprio objeto: todo método recebe self como primeiro parâmetro."),
            ("run", '''class Paciente:
    """Um animal atendido na clínica veterinária."""

    def __init__(self, nome, especie, peso_kg):
        self.nome = nome              # atributos de instância
        self.especie = especie
        self.peso_kg = peso_kg
        self.vacinas = []

    def vacinar(self, vacina):
        self.vacinas.append(vacina)

    def dose_diaria(self):
        return round(self.peso_kg * 0.5, 1)    # 0,5 mg por kg

    def __str__(self):                          # usado por print()
        return f"{self.nome} ({self.especie}, {self.peso_kg} kg)"

rex = Paciente("Rex", "cão", 12.0)
mia = Paciente("Mia", "gato", 4.2)
rex.vacinar("raiva")
print(rex, "| vacinas:", rex.vacinas)
print(mia, "| dose:", mia.dose_diaria(), "mg")
print(mia.vacinas)         # cada objeto tem a sua própria lista''',
             "Classe Paciente"),
            ("cuidado", "Esqueceu o <b>self</b> no def, ou o <b>self.</b> antes do atributo? "
                        "Vai aparecer TypeError ou NameError. Dentro da classe, atributos sempre "
                        "levam self."),
        ]),
        ("2.2  Atributos de classe e métodos especiais", [
            ("p", "Um <b>atributo de classe</b> é compartilhado por todos os objetos (ex.: uma taxa "
                  "fixa). <b>@classmethod</b> cria objetos por caminhos alternativos; "
                  "<b>@staticmethod</b> é uma função utilitária dentro da classe. Métodos "
                  "<i>dunder</i> (__str__, __repr__, __eq__, __lt__, __len__) ensinam o Python a "
                  "imprimir, comparar e medir seus objetos."),
            ("run", '''class Consulta:
    taxa_clinica = 15.0                      # atributo de CLASSE

    def __init__(self, paciente, valor):
        self.paciente = paciente
        self.valor = valor

    @classmethod
    def de_texto(cls, texto):                # "Rex;120"
        paciente, valor = texto.split(";")
        return cls(paciente, float(valor))

    def total(self):
        return self.valor + self.taxa_clinica

    def __lt__(self, outro):                 # permite sorted()/min()/max()
        return self.total() < outro.total()

    def __repr__(self):
        return f"Consulta({self.paciente!r}, {self.total()})"

consultas = [Consulta.de_texto("Rex;120"), Consulta("Mia", 80)]
print(sorted(consultas))
print(max(consultas))''',
             "@classmethod, atributo de classe, __lt__ e __repr__"),
        ]),
        ("2.3  Herança e polimorfismo", [
            ("p", "<b>Herança</b>: uma classe-filha reaproveita tudo da classe-mãe e acrescenta ou "
                  "<i>sobrescreve</i> o que for diferente. <b>super()</b> chama a versão da mãe. "
                  "<b>Polimorfismo</b>: você chama o mesmo método em objetos de tipos diferentes e "
                  "cada um responde do seu jeito."),
            ("run", '''class Atendimento:
    def __init__(self, paciente, base):
        self.paciente = paciente
        self.base = base

    def valor(self):
        return self.base

class Emergencia(Atendimento):
    def valor(self):
        return super().valor() * 2          # dobro do valor base

class Retorno(Atendimento):
    def valor(self):
        return super().valor() * 0.5        # metade

fila = [Atendimento("Rex", 100), Emergencia("Mia", 100), Retorno("Bob", 100)]
for a in fila:                              # polimorfismo em ação
    print(f"{a.paciente:<4} {type(a).__name__:<12} R$ {a.valor():.2f}")
print("Total:", sum(a.valor() for a in fila))
print(isinstance(fila[1], Atendimento), issubclass(Retorno, Emergencia))''',
             "Atendimento → Emergencia e Retorno"),
            ("lembre", "<b>Quando usar herança?</b> Quando existe a relação <i>'é um tipo de'</i> "
                       "(Emergência é um tipo de Atendimento). Se for 'tem um' (Clínica tem "
                       "pacientes), use composição: um atributo guardando outros objetos."),
        ]),
        ("2.4  Encapsulamento: proteger o estado", [
            ("p", "Encapsular é controlar <i>como</i> os dados mudam. Por convenção, nomes com "
                  "underscore (<b>_saldo</b>) são de uso interno. Uma <b>@property</b> expõe o "
                  "valor como se fosse atributo (somente leitura). Com um <b>setter</b> você valida "
                  "antes de aceitar a mudança."),
            ("run", '''class Termometro:
    def __init__(self, temp):
        self._temp = None
        self.temperatura = temp          # passa pelo setter (valida)

    @property
    def temperatura(self):
        return self._temp

    @temperatura.setter
    def temperatura(self, valor):
        if not -50 <= valor <= 150:
            raise ValueError("temperatura fora da faixa")
        self._temp = valor

    @property
    def fahrenheit(self):                # propriedade calculada
        return self._temp * 9 / 5 + 32

t = Termometro(36.5)
print(t.temperatura, round(t.fahrenheit, 1))
t.temperatura = 40
try:
    t.temperatura = 900
except ValueError as erro:
    print("recusado:", erro, "| continua:", t.temperatura)''',
             "property com setter e validação"),
            ("dica", "Valide <b>antes</b> de alterar o estado. Assim, uma operação recusada nunca "
                     "deixa o objeto 'pela metade'."),
        ]),
    ],
    resolvido=dict(
        titulo="Exemplo resolvido — fila do banco de sangue",
        enunciado=("Crie a classe Doador(nome, tipo, litros_doados) com o método "
                   "pode_doar_para(tipo_receptor) usando a regra simplificada: 'O' doa para todos, "
                   "'A' doa para A e AB, 'B' para B e AB, 'AB' só para AB. Depois, dada uma lista "
                   "de doadores, mostre quantos litros são compatíveis com um receptor tipo 'A'."),
        passos=[
            "<b>Modelar:</b> o que um Doador sabe (nome, tipo, litros) e faz (checar compatibilidade).",
            "<b>Regra em dados:</b> um dicionário tipo → conjunto de receptores evita if em cascata.",
            "<b>Usar:</b> filtrar com comprehension chamando o método do objeto.",
        ],
        codigo='''class Doador:
    COMPATIVEL = {"O": {"O", "A", "B", "AB"}, "A": {"A", "AB"},
                  "B": {"B", "AB"}, "AB": {"AB"}}

    def __init__(self, nome, tipo, litros_doados):
        self.nome = nome
        self.tipo = tipo
        self.litros_doados = litros_doados

    def pode_doar_para(self, tipo_receptor):
        return tipo_receptor in self.COMPATIVEL[self.tipo]

doadores = [Doador("Lia", "O", 0.45), Doador("Davi", "B", 0.40),
            Doador("Iara", "A", 0.50), Doador("Teo", "AB", 0.45)]

aptos = [d for d in doadores if d.pode_doar_para("A")]
print([d.nome for d in aptos], round(sum(d.litros_doados for d in aptos), 2))''',
    ),
    armadilhas=[
        "Atributo mutável como valor padrão: <i>def __init__(self, itens=[])</i> compartilha a "
        "MESMA lista entre objetos. Use <i>itens=None</i> e crie a lista dentro.",
        "Esquecer <b>super().__init__(...)</b> numa subclasse que define o seu próprio __init__.",
        "Chamar um método sem parênteses (<i>obj.total</i> em vez de <i>obj.total()</i>).",
        "Misturar impressão e cálculo no mesmo método: devolva o valor com return e imprima fora.",
    ],
    cola=[
        ["Quero…", "Use…"],
        ["guardar dados iniciais", "def __init__(self, ...): self.x = x"],
        ["texto bonito no print()", "def __str__(self): return f'...'"],
        ["reaproveitar a classe-mãe", "class Filha(Mae):  /  super().metodo()"],
        ["atributo somente leitura", "@property + atributo _interno"],
        ["recusar valor inválido", "raise ValueError('mensagem')"],
        ["ordenar objetos", "sorted(objs, key=lambda o: o.campo)"],
        ["checar o tipo", "isinstance(obj, Classe)"],
    ],
    exercicios=["ap_livro_classe", "ap_planos_heranca", "ap_carteirinha"],
)

# ═════════════════════════════════════════════════════════════════════════
# CAPÍTULO 3 — PANDAS
# ═════════════════════════════════════════════════════════════════════════
CAP[3] = dict(
    titulo="Pandas — análise de dados",
    intro=("Pandas trabalha com tabelas: o <b>DataFrame</b> (linhas × colunas) e a <b>Series</b> "
           "(uma coluna). A ideia central é <i>operar na coluna inteira de uma vez</i>, sem escrever "
           "laços. Convenção universal: <i>import pandas as pd</i>."),
    secoes=[
        ("3.1  Criar e inspecionar um DataFrame", [
            ("run", '''import pandas as pd

jogos = pd.DataFrame({
    "time":   ["Tigres", "Águias", "Lobos", "Tigres", "Águias", "Lobos"],
    "rodada": [1, 1, 1, 2, 2, 2],
    "gols":   [3, 1, 0, 2, 2, 4],
    "sofridos": [1, 1, 3, 2, 0, 1],
})

print(jogos.head(3))           # primeiras linhas
print(jogos.shape)             # (linhas, colunas)
print(jogos[["rodada", "gols"]].dtypes.astype(str).to_dict())  # tipos
print(jogos["gols"].agg(["min", "max", "mean"]).to_dict())''',
             "Criando e inspecionando"),
            ("lista", [
                "De arquivo: <b>pd.read_csv('arquivo.csv')</b>, <b>pd.read_excel(...)</b>.",
                "Inspeção rápida: <b>.head()</b>, <b>.info()</b>, <b>.describe()</b>, <b>.shape</b>, "
                "<b>.columns</b>, <b>.dtypes</b>.",
                "Para salvar: <b>df.to_csv('saida.csv', index=False)</b>.",
            ]),
        ]),
        ("3.2  Selecionar e filtrar", [
            ("p", "Colunas: <b>df['gols']</b> (uma coluna → Series) ou <b>df[['time','gols']]</b> "
                  "(várias → DataFrame). Linhas por condição: uma <i>máscara booleana</i> dentro de "
                  "colchetes. Combine condições com <b>&amp;</b> (e), <b>|</b> (ou), <b>~</b> (não), "
                  "<b>sempre com parênteses</b> em cada condição."),
            ("runc", '''goleadas = jogos[jogos["gols"] >= 3]
print(goleadas)

so_tigres_e_lobos = jogos[jogos["time"].isin(["Tigres", "Lobos"])]
print(len(so_tigres_e_lobos))

bons = jogos[(jogos["gols"] > 1) & (jogos["sofridos"] <= 1)]
print(bons[["time", "rodada"]])

print(jogos.loc[0, "gols"], jogos.iloc[1, 2])   # por rótulo / por posição''',
             "Filtros, isin, &, loc e iloc"),
            ("cuidado", "Escrever <i>df[df.a > 1 and df.b < 5]</i> dá erro. Em pandas use "
                        "<b>&amp;</b>/<b>|</b> e parenteses: <i>df[(df.a &gt; 1) &amp; (df.b &lt; 5)]</i>."),
            ("tabela", [
                ["Quero…", "Código"],
                ["texto que contém", "df[df['nome'].str.contains('ana', case=False)]"],
                ["entre dois valores", "df[df['gols'].between(2, 4)]"],
                ["valores de uma lista", "df[df['time'].isin(['Lobos', 'Águias'])]"],
                ["negar uma condição", "df[~(df['gols'] == 0)]"],
            ], [30, 70]),
        ]),
        ("3.3  Colunas novas, ordenar e renomear", [
            ("runc", '''jogos["saldo"] = jogos["gols"] - jogos["sofridos"]          # coluna nova
jogos["resultado"] = jogos["saldo"].apply(
    lambda s: "vitória" if s > 0 else ("empate" if s == 0 else "derrota"))

ordenado = jogos.sort_values(["saldo", "gols"], ascending=[False, False])
print(ordenado[["time", "rodada", "saldo", "resultado"]].to_string(index=False))

renomeado = jogos.rename(columns={"sofridos": "gols_contra"})
print(list(renomeado.columns))''',
             "Colunas derivadas, apply, sort_values e rename"),
            ("dica", "Prefira operações entre colunas (<i>df.a - df.b</i>) a <i>apply</i>: são muito "
                     "mais rápidas. Use apply quando a regra for complexa demais para uma expressão."),
        ]),
        ("3.4  Agrupar e resumir (groupby)", [
            ("p", "Receita universal: <b>divida</b> a tabela em grupos, <b>aplique</b> uma "
                  "agregação em cada um (soma, média, contagem…) e <b>combine</b> o resultado."),
            ("runc", '''classificacao = jogos.groupby("time").agg(
    jogos=("rodada", "count"),
    pontos=("saldo", lambda s: (s > 0).sum() * 3 + (s == 0).sum()),
    gols_pro=("gols", "sum"),
    media_saldo=("saldo", "mean"),
).sort_values("pontos", ascending=False)
print(classificacao)

print(jogos["resultado"].value_counts().to_dict())   # contagem por categoria
print(jogos["time"].nunique(), "times diferentes")''',
             "agg com nomes, value_counts e nunique"),
            ("lembre", "groupby('coluna')['valor'].sum() devolve uma <b>Series</b> cujo índice são os "
                       "grupos. Use <b>.reset_index()</b> para transformar de volta em tabela comum."),
        ]),
        ("3.5  Limpeza de dados", [
            ("p", "Dados reais vêm sujos. As ferramentas de sempre:"),
            ("run", '''import pandas as pd

sujo = pd.DataFrame({
    "cliente": ["  marcos ", "LUCIA", "marcos", None, "Paulo"],
    "idade": ["31", "28", "31", "40", "x"],
    "compra": ["R$ 10,50", "R$ 20,00", "R$ 10,50", "R$ 5,00", None],
})

print(sujo.isna().sum().to_dict())                      # nulos por coluna

s = sujo.copy()
s["cliente"] = s["cliente"].str.strip().str.title()      # texto padronizado
s = s.dropna(subset=["cliente"])                         # sem nome, descarta
s["idade"] = pd.to_numeric(s["idade"], errors="coerce")  # 'x' vira NaN
s["idade"] = s["idade"].fillna(s["idade"].median())
s["compra"] = (s["compra"].str.replace("R$ ", "", regex=False)
                          .str.replace(",", ".", regex=False).astype(float))
s["compra"] = s["compra"].fillna(0.0)
s = s.drop_duplicates()
print(s.reset_index(drop=True))''',
             "isna, strip/title, dropna, to_numeric, fillna, drop_duplicates"),
            ("tabela", [
                ["Problema", "Ferramenta"],
                ["valores vazios (NaN)", "isna() · dropna() · fillna(valor)"],
                ["linhas repetidas", "drop_duplicates(subset=[...])"],
                ["texto sujo", ".str.strip() .str.lower() .str.title() .str.replace()"],
                ["tipo errado", ".astype(int) · pd.to_numeric(errors='coerce') · pd.to_datetime()"],
                ["valores impossíveis", "df[df['idade'].between(0, 120)]"],
            ], [34, 66]),
        ]),
        ("3.6  Tabela dinâmica (pivot_table)", [
            ("p", "É o <i>groupby</i> em duas dimensões, já com cara de planilha: uma variável nas "
                  "linhas, outra nas colunas e uma agregação nas células."),
            ("run", '''import pandas as pd

ingressos = pd.DataFrame({
    "sala":  ["1", "1", "2", "2", "1", "2", "2"],
    "dia":   ["sex", "sáb", "sex", "sáb", "sáb", "sex", "sáb"],
    "vendidos": [80, 120, 60, 90, 30, 25, 40],
})
tabela = pd.pivot_table(ingressos, values="vendidos", index="sala",
                        columns="dia", aggfunc="sum", fill_value=0,
                        margins=True, margins_name="Total")
print(tabela)''',
             "pivot_table com totais (margins)"),
        ]),
        ("3.7  Juntar tabelas (merge e concat)", [
            ("p", "<b>merge</b> junta tabelas por uma chave (como o JOIN do SQL). O parâmetro "
                  "<b>how</b> decide quem fica: <i>inner</i> (só quem tem par nos dois lados), "
                  "<i>left</i> (tudo da esquerda), <i>right</i>, <i>outer</i> (tudo). "
                  "<b>concat</b> empilha tabelas de mesmo formato."),
            ("run", '''import pandas as pd

alunos = pd.DataFrame({"id": [1, 2, 3], "nome": ["Lara", "Caio", "Rui"]})
provas = pd.DataFrame({"aluno_id": [1, 1, 3], "nota": [8.0, 9.0, 5.5]})

inner = alunos.merge(provas, left_on="id", right_on="aluno_id")          # só com prova
left = alunos.merge(provas, left_on="id", right_on="aluno_id", how="left")
print(len(inner), len(left))
print(left[["nome", "nota"]])

mais = pd.DataFrame({"id": [4], "nome": ["Eva"]})
print(pd.concat([alunos, mais], ignore_index=True)["nome"].tolist())''',
             "merge inner vs left, e concat"),
            ("cuidado", "Depois de um merge <i>left</i>, quem não tem par fica com <b>NaN</b>. "
                        "Conte as linhas antes e depois: se o número cresceu, havia chaves repetidas "
                        "do outro lado (um aluno com 2 provas vira 2 linhas)."),
        ]),
    ],
    resolvido=dict(
        titulo="Exemplo resolvido — a artilharia do campeonato",
        enunciado=("Com a tabela de jogos abaixo, descubra: (a) o total de gols de cada time, "
                   "(b) o time com mais gols, (c) a média de gols por jogo de cada time arredondada "
                   "em 2 casas, (d) quantos jogos tiveram 3 gols ou mais."),
        passos=[
            "<b>Entender:</b> uma linha = um time em um jogo.",
            "<b>(a)</b> groupby('time')['gols'].sum().",
            "<b>(b)</b> idxmax() sobre a Series do passo (a).",
            "<b>(c)</b> groupby + mean() + round(2).   <b>(d)</b> filtro e len().",
        ],
        codigo='''import pandas as pd

jogos = pd.DataFrame({
    "time": ["Tigres", "Águias", "Lobos", "Tigres", "Águias", "Lobos", "Tigres"],
    "gols": [3, 1, 0, 2, 2, 4, 1],
})

gols_por_time = jogos.groupby("time")["gols"].sum()
artilheiro = gols_por_time.idxmax()
media = jogos.groupby("time")["gols"].mean().round(2)
jogos_3mais = len(jogos[jogos["gols"] >= 3])

print(gols_por_time.to_dict())
print(artilheiro, media.to_dict(), jogos_3mais)''',
    ),
    armadilhas=[
        "Usar <b>and / or</b> em filtros (precisa de <b>&amp;</b> e <b>|</b> com parênteses).",
        "<b>SettingWithCopyWarning</b>: ao alterar uma fatia, trabalhe numa cópia (<i>df.copy()</i>).",
        "Esquecer que <i>sum()</i> ignora NaN e <i>mean()</i> também (a média é só dos preenchidos).",
        "Comparar texto com espaços escondidos: padronize com <i>.str.strip()</i> antes de agrupar ou juntar.",
        "Esquecer o <b>reset_index()</b> depois de um groupby e estranhar que o grupo virou índice.",
    ],
    cola=[
        ["Quero…", "Use…"],
        ["ver o formato dos dados", "df.head()  df.info()  df.describe()"],
        ["filtrar linhas", "df[(df.a > 1) & (df.b == 'x')]"],
        ["coluna nova", "df['nova'] = df['a'] * df['b']"],
        ["soma por categoria", "df.groupby('cat')['valor'].sum()"],
        ["maior/menor (rótulo)", "serie.idxmax()   serie.idxmin()"],
        ["tabela cruzada", "pd.pivot_table(df, values=, index=, columns=, aggfunc=)"],
        ["juntar tabelas", "a.merge(b, on='chave', how='left')"],
        ["limpar", "dropna · fillna · drop_duplicates · astype · str.strip"],
    ],
    exercicios=["ap_cafeteria_df", "ap_limpeza_alunos", "ap_pivot_faltas", "ap_merge_pacientes"],
)

# ═════════════════════════════════════════════════════════════════════════
# CAPÍTULO 4 — SQLITE E SQL
# ═════════════════════════════════════════════════════════════════════════
CAP[4] = dict(
    titulo="SQLite e SQL — banco de dados",
    intro=("Um <b>banco de dados relacional</b> guarda dados em tabelas ligadas por chaves. "
           "<b>SQL</b> é a linguagem para perguntar e alterar esses dados. O <b>SQLite</b> é um banco "
           "completo dentro de um único arquivo (ou da memória), já incluído no Python: perfeito "
           "para estudar e para apps pequenos."),
    secoes=[
        ("4.1  Conceitos e o módulo sqlite3", [
            ("lista", [
                "<b>Tabela</b>: conjunto de linhas (registros) e colunas (campos).",
                "<b>Chave primária (PRIMARY KEY)</b>: identifica cada linha de forma única.",
                "<b>Chave estrangeira</b>: coluna que aponta para a chave primária de outra tabela.",
                "Tipos do SQLite: INTEGER, REAL, TEXT, BLOB (e NULL para ausência).",
            ]),
            ("p", "Fluxo no Python: <b>connect</b> → <b>execute</b> (comandos) → <b>commit</b> "
                  "(grava alterações) → <b>fetchall/fetchone</b> (lê resultados) → <b>close</b>."),
            ("run", '''import sqlite3

conn = sqlite3.connect(":memory:")      # ou sqlite3.connect("oficina.db")
conn.execute("""
    CREATE TABLE servicos (
        id      INTEGER PRIMARY KEY,
        placa   TEXT NOT NULL,
        tipo    TEXT,
        valor   REAL
    )""")
conn.executemany(
    "INSERT INTO servicos (placa, tipo, valor) VALUES (?, ?, ?)",
    [("ABC1D23", "revisão", 450.0), ("XYZ9K88", "freio", 280.0),
     ("ABC1D23", "óleo", 120.0), ("QWE4R56", "revisão", 520.0)])
conn.commit()

print(conn.execute("SELECT COUNT(*) FROM servicos").fetchone())
for linha in conn.execute("SELECT placa, tipo FROM servicos LIMIT 2"):
    print(linha)''',
             "Criar tabela, inserir e ler"),
            ("lembre", "Sem <b>commit()</b> as alterações (INSERT/UPDATE/DELETE) não são gravadas "
                       "no arquivo. Em bancos em memória isso não aparece, mas em arquivo faz toda a diferença."),
        ]),
        ("4.2  Consultar: SELECT, WHERE, ORDER BY, LIMIT", [
            ("tabela", [
                ["Cláusula", "Função", "Exemplo"],
                ["SELECT", "quais colunas", "SELECT placa, valor"],
                ["WHERE", "filtra linhas", "WHERE valor >= 300"],
                ["ORDER BY", "ordena", "ORDER BY valor DESC"],
                ["LIMIT", "limita a quantidade", "LIMIT 3"],
                ["LIKE / IN / BETWEEN", "padrão / lista / faixa", "WHERE tipo LIKE 'rev%'"],
                ["IS NULL", "testa ausência", "WHERE valor IS NULL"],
            ], [22, 30, 48]),
            ("runc", '''caros = conn.execute(
    "SELECT placa, tipo, valor FROM servicos "
    "WHERE valor >= ? AND tipo != ? ORDER BY valor DESC", (300, "freio")
).fetchall()
print(caros)

print(conn.execute(
    "SELECT tipo FROM servicos WHERE tipo LIKE 'rev%' OR valor BETWEEN 100 AND 150"
).fetchall())''',
             "WHERE com parâmetros, LIKE, BETWEEN"),
            ("cuidado", "<b>Nunca</b> monte SQL juntando texto com f-string "
                        "(<i>f\"... WHERE nome = '{nome}'\"</i>): abre brecha para SQL injection e quebra com "
                        "aspas. Use <b>?</b> e passe os valores numa tupla."),
        ]),
        ("4.3  Alterar dados: UPDATE e DELETE", [
            ("runc", '''conn.execute("UPDATE servicos SET valor = valor * 1.10 WHERE tipo = ?", ("revisão",))
conn.execute("DELETE FROM servicos WHERE valor < ?", (150,))
conn.commit()
print(conn.execute("SELECT tipo, ROUND(valor, 2) FROM servicos ORDER BY id").fetchall())''',
             "Reajuste de 10% e remoção"),
            ("cuidado", "UPDATE ou DELETE <b>sem WHERE</b> atinge a tabela inteira. Escreva primeiro "
                        "o SELECT com o mesmo WHERE para conferir o que será afetado."),
        ]),
        ("4.4  Agregações: COUNT, SUM, AVG, GROUP BY e HAVING", [
            ("p", "As funções de agregação resumem várias linhas em uma: <b>COUNT, SUM, AVG, MIN, MAX</b>. "
                  "Com <b>GROUP BY</b> você resume por grupo; com <b>HAVING</b> filtra os grupos "
                  "(WHERE filtra as linhas <i>antes</i> de agrupar)."),
            ("run", '''import sqlite3

conn = sqlite3.connect(":memory:")
conn.executescript("""
CREATE TABLE servicos (placa TEXT, tipo TEXT, valor REAL);
INSERT INTO servicos VALUES
  ('ABC1D23','revisão',450), ('XYZ9K88','freio',280),
  ('ABC1D23','óleo',120),    ('QWE4R56','revisão',520),
  ('ABC1D23','freio',300);
""")
q = """
SELECT placa, COUNT(*) AS qtd, SUM(valor) AS total
FROM servicos
GROUP BY placa
HAVING COUNT(*) >= 2
ORDER BY total DESC
"""
print(conn.execute(q).fetchall())
print(conn.execute("SELECT tipo, AVG(valor) FROM servicos GROUP BY tipo").fetchall())''',
             "GROUP BY + HAVING"),
            ("lembre", "Ordem de escrita: <b>SELECT → FROM → JOIN → WHERE → GROUP BY → HAVING → "
                       "ORDER BY → LIMIT</b>."),
        ]),
        ("4.5  Juntar tabelas: JOIN", [
            ("p", "Dados bem organizados ficam em tabelas separadas (um cliente, vários pedidos). "
                  "<b>JOIN</b> as combina pela chave. <b>INNER JOIN</b> traz só quem tem par; "
                  "<b>LEFT JOIN</b> traz tudo da tabela da esquerda, com NULL onde não há par."),
            ("run", '''import sqlite3

conn = sqlite3.connect(":memory:")
conn.executescript("""
CREATE TABLE donos (id INTEGER PRIMARY KEY, nome TEXT);
CREATE TABLE carros (id INTEGER PRIMARY KEY, dono_id INTEGER, modelo TEXT);
INSERT INTO donos VALUES (1,'Marta'), (2,'Otávio'), (3,'Sônia');
INSERT INTO carros (dono_id, modelo) VALUES (1,'Gol'), (1,'Onix'), (2,'Argo');
""")
print(conn.execute("""
    SELECT d.nome, c.modelo FROM donos d
    INNER JOIN carros c ON c.dono_id = d.id ORDER BY d.nome""").fetchall())
print(conn.execute("""
    SELECT d.nome, COUNT(c.id) AS carros FROM donos d
    LEFT JOIN carros c ON c.dono_id = d.id
    GROUP BY d.id ORDER BY d.nome""").fetchall())''',
             "INNER JOIN vs LEFT JOIN (Sônia só aparece no LEFT)"),
            ("dica", "Use <b>COUNT(c.id)</b> (coluna da tabela da direita) e não COUNT(*) no LEFT JOIN: "
                     "assim quem não tem par conta 0, e não 1."),
        ]),
        ("4.6  Pandas + SQL", [
            ("run", '''import sqlite3
import pandas as pd

conn = sqlite3.connect(":memory:")
df = pd.DataFrame({"peca": ["filtro", "pastilha", "filtro"], "qtd": [4, 2, 6]})
df.to_sql("consumo", conn, index=False, if_exists="replace")     # DataFrame -> tabela

resumo = pd.read_sql(
    "SELECT peca, SUM(qtd) AS total FROM consumo GROUP BY peca", conn)  # SQL -> DataFrame
print(resumo)''',
             "to_sql e read_sql"),
            ("lembre", "Regra prática: <b>filtrar e agregar</b> volumes grandes no SQL; "
                       "<b>explorar e transformar</b> o resultado no pandas."),
        ]),
    ],
    resolvido=dict(
        titulo="Exemplo resolvido — ranking de peças da oficina",
        enunciado=("Dada a tabela pecas(nome, categoria, preco, estoque), liste, por categoria, o "
                   "valor total em estoque (preco × estoque) mostrando apenas categorias cujo total "
                   "passe de R$ 1.000, da maior para a menor."),
        passos=[
            "<b>Pergunta → SQL:</b> 'por categoria' = GROUP BY categoria.",
            "<b>Valor em estoque</b> = SUM(preco * estoque).",
            "<b>'só as que passam de 1000'</b> é filtro de GRUPO → HAVING (não WHERE).",
            "<b>Ordem</b> = ORDER BY total DESC.",
        ],
        codigo='''import sqlite3

conn = sqlite3.connect(":memory:")
conn.executescript("""
CREATE TABLE pecas (nome TEXT, categoria TEXT, preco REAL, estoque INTEGER);
INSERT INTO pecas VALUES
 ('Filtro de ar','motor',40,30), ('Vela','motor',25,100),
 ('Pastilha','freio',120,12),    ('Disco','freio',200,8),
 ('Lâmpada','elétrica',12,40);
""")
print(conn.execute("""
    SELECT categoria, SUM(preco * estoque) AS total
    FROM pecas
    GROUP BY categoria
    HAVING SUM(preco * estoque) > 1000
    ORDER BY total DESC""").fetchall())''',
    ),
    armadilhas=[
        "Esquecer o <b>commit()</b> depois de INSERT/UPDATE/DELETE em banco de arquivo.",
        "Formatar SQL com f-string em vez de usar <b>?</b> com parâmetros.",
        "Passar um valor só como parâmetro sem tupla: <i>execute(sql, (valor,))</i> — repare na vírgula.",
        "Usar <b>WHERE</b> para filtrar resultado de agregação (o certo é HAVING).",
        "No LEFT JOIN, filtrar a tabela da direita no WHERE transforma o LEFT em INNER sem querer; "
        "coloque a condição no ON.",
    ],
    cola=[
        ["Quero…", "SQL"],
        ["criar tabela", "CREATE TABLE t (id INTEGER PRIMARY KEY, nome TEXT)"],
        ["inserir (seguro)", "INSERT INTO t (nome) VALUES (?)"],
        ["filtrar e ordenar", "SELECT ... WHERE ... ORDER BY col DESC LIMIT n"],
        ["total por grupo", "SELECT g, SUM(v) FROM t GROUP BY g"],
        ["filtrar grupos", "... GROUP BY g HAVING SUM(v) > 100"],
        ["juntar tabelas", "FROM a JOIN b ON b.a_id = a.id   (LEFT JOIN p/ manter tudo de a)"],
        ["alterar / apagar", "UPDATE t SET c = ? WHERE id = ?   ·   DELETE FROM t WHERE id = ?"],
    ],
    exercicios=["ap_filmes_sql", "ap_join_pedidos", "ap_pandas_sql"],
)

# ═════════════════════════════════════════════════════════════════════════
# CAPÍTULO 5 — TKINTER
# ═════════════════════════════════════════════════════════════════════════
CAP[5] = dict(
    titulo="Tkinter — interfaces gráficas",
    intro=("Tkinter vem instalado com o Python e cria janelas com botões, campos de texto e listas. "
           "A lógica é sempre a mesma: <b>criar a janela</b>, <b>criar widgets</b>, <b>posicioná-los</b>, "
           "<b>ligar eventos a funções</b> e chamar <b>mainloop()</b>."),
    secoes=[
        ("5.1  Estrutura mínima de uma janela", [
            ("code", '''import tkinter as tk

janela = tk.Tk()                 # janela principal
janela.title("Meu app")
janela.geometry("300x150")       # largura x altura

rotulo = tk.Label(janela, text="Olá, mundo!")
rotulo.pack(pady=10)             # posiciona (empilha) na janela

janela.mainloop()                # mantém a janela aberta e atenta a eventos'''),
            ("lembre", "O código depois de <b>mainloop()</b> só roda quando a janela fecha. Tudo o "
                       "que o app faz acontece dentro de <i>callbacks</i> (funções chamadas por eventos)."),
            ("cuidado", "Tkinter precisa de uma tela. Ele <b>não abre</b> em navegador, em servidor sem "
                        "interface nem na aba Apostila do app: lá validamos a estrutura. Para ver a "
                        "janela de verdade, rode o arquivo .py no seu computador."),
        ]),
        ("5.2  Widgets mais usados", [
            ("tabela", [
                ["Widget", "Para quê", "Pontos-chave"],
                ["Label", "mostrar texto", "label.config(text='novo texto')"],
                ["Button", "disparar uma ação", "Button(janela, text='OK', command=funcao)"],
                ["Entry", "uma linha de texto", "entrada.get()  ·  entrada.delete(0, tk.END)"],
                ["Listbox", "lista de itens", "lista.insert(tk.END, item)  ·  lista.curselection()"],
                ["Frame", "agrupar widgets", "Frame(janela).pack()  (container)"],
                ["messagebox", "avisos e perguntas", "from tkinter import messagebox"],
            ], [16, 26, 58]),
        ]),
        ("5.3  Posicionamento: pack, grid e place", [
            ("lista", [
                "<b>pack()</b>: empilha um widget embaixo do outro (rápido para telas simples). "
                "Opções: side, padx, pady, fill, expand.",
                "<b>grid(row=, column=)</b>: posiciona em linhas e colunas, ideal para formulários. "
                "Não misture pack e grid no mesmo container.",
                "<b>place(x=, y=)</b>: posição absoluta em pixels (evite; não se adapta ao redimensionar).",
            ]),
            ("code", '''# formulário com grid
tk.Label(janela, text="Nome:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
nome = tk.Entry(janela)
nome.grid(row=0, column=1, padx=5, pady=5)
tk.Label(janela, text="Idade:").grid(row=1, column=0, sticky="e", padx=5)
idade = tk.Entry(janela)
idade.grid(row=1, column=1, padx=5)'''),
        ]),
        ("5.4  Eventos e callbacks", [
            ("p", "O botão recebe a função em <b>command=</b>, <b>sem parênteses</b>: quem a chama é o "
                  "Tkinter, no clique. Para outros eventos (tecla Enter, clique duplo) use "
                  "<b>widget.bind('&lt;Return&gt;', funcao)</b> — nesse caso a função recebe o parâmetro "
                  "<i>evento</i>."),
            ("code", '''import tkinter as tk
from tkinter import messagebox

def converter():
    try:
        reais = float(entrada.get().replace(",", "."))
    except ValueError:
        messagebox.showerror("Erro", "Digite um número válido")
        return
    resultado.config(text=f"US$ {reais / 5.0:.2f}")     # cotação fixa de exemplo

janela = tk.Tk()
janela.title("Conversor")
entrada = tk.Entry(janela)
entrada.pack(padx=10, pady=5)
entrada.bind("<Return>", lambda evento: converter())    # Enter também converte
tk.Button(janela, text="Converter R$ → US$", command=converter).pack()
resultado = tk.Label(janela, text="")
resultado.pack(pady=8)
janela.mainloop()'''),
            ("dica", "Sempre valide o que vem do <b>Entry</b>: ele devolve texto. Converta com "
                     "float()/int() dentro de try/except e avise o usuário em vez de deixar o app quebrar."),
        ]),
        ("5.5  Organizando o app em uma classe", [
            ("p", "Variáveis globais viram bagunça rápido. Herdando de <b>tk.Tk</b> (ou usando um "
                  "Frame), widgets e dados viram atributos de <i>self</i> e cada ação, um método."),
            ("code", '''import tkinter as tk

class AppContador(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Contador")
        self.total = 0
        self.rotulo = tk.Label(self, text="0", font=("Arial", 24))
        self.rotulo.pack(padx=30, pady=10)
        tk.Button(self, text="+1", command=self.somar).pack(pady=(0, 10))

    def somar(self):
        self.total += 1
        self.rotulo.config(text=str(self.total))

if __name__ == "__main__":
    AppContador().mainloop()'''),
        ]),
    ],
    resolvido=dict(
        titulo="Exemplo resolvido — checklist de viagem",
        enunciado=("Uma janela com um Entry, o botão 'Adicionar' e um Listbox. Ao adicionar, o item vai "
                   "para a lista e o campo é limpo; um segundo botão 'Remover selecionado' apaga o item "
                   "escolhido."),
        passos=[
            "<b>Widgets:</b> Entry, 2 Buttons, Listbox.",
            "<b>Callback adicionar:</b> get() → insert(END, ...) → delete(0, END).",
            "<b>Callback remover:</b> curselection() devolve as posições selecionadas; delete(posição).",
        ],
        codigo=None,
        codigo_estatico='''import tkinter as tk

def adicionar():
    item = entrada.get().strip()
    if item:
        lista.insert(tk.END, item)
        entrada.delete(0, tk.END)

def remover():
    for posicao in reversed(lista.curselection()):
        lista.delete(posicao)

janela = tk.Tk()
janela.title("Checklist")
entrada = tk.Entry(janela, width=28)
entrada.pack(padx=10, pady=5)
tk.Button(janela, text="Adicionar", command=adicionar).pack()
lista = tk.Listbox(janela, width=32, height=8)
lista.pack(padx=10, pady=8)
tk.Button(janela, text="Remover selecionado", command=remover).pack(pady=(0, 8))
janela.mainloop()''',
    ),
    armadilhas=[
        "<b>command=funcao()</b> com parênteses executa a função na hora de criar o botão. Use "
        "<b>command=funcao</b> (ou <i>lambda: funcao(x)</i> para passar argumentos).",
        "Misturar <b>pack</b> e <b>grid</b> no mesmo container trava a janela.",
        "Fazer algo demorado dentro de um callback congela a janela (ela só responde entre callbacks).",
        "Esquecer de guardar o widget numa variável antes de chamar <b>.pack()</b>: "
        "<i>x = tk.Label(...).pack()</i> faz x valer None.",
    ],
    cola=[
        ["Quero…", "Tkinter"],
        ["criar janela", "janela = tk.Tk(); janela.title('...'); janela.mainloop()"],
        ["ler / limpar campo", "entrada.get()   entrada.delete(0, tk.END)"],
        ["trocar texto", "label.config(text='...')"],
        ["adicionar na lista", "lista.insert(tk.END, texto)"],
        ["ligar botão a função", "tk.Button(janela, text='OK', command=funcao)"],
        ["avisar o usuário", "messagebox.showinfo('Título', 'Mensagem')"],
    ],
    exercicios=["ap_tk_contador", "ap_tk_tarefas"],
)

# ═════════════════════════════════════════════════════════════════════════
# CAPÍTULO 6 — PROJETO INTEGRADOR
# ═════════════════════════════════════════════════════════════════════════
CAP[6] = dict(
    titulo="Projeto integrador",
    intro=("Aqui as peças se encontram: <b>classes</b> para as regras, <b>SQLite</b> para guardar, "
           "<b>pandas</b> para analisar e, opcionalmente, <b>Tkinter</b> para a tela. O segredo não é "
           "código novo, e sim <i>onde cada coisa mora</i>."),
    secoes=[
        ("6.1  Arquitetura em camadas", [
            ("tabela", [
                ["Camada", "Responsabilidade", "Ferramenta"],
                ["Dados", "guardar e buscar registros", "sqlite3 (CREATE, INSERT, SELECT)"],
                ["Regras", "o que pode e o que não pode", "classes + exceções"],
                ["Análise", "relatórios e números", "pandas (groupby, pivot)"],
                ["Interface", "falar com o usuário", "print/input ou Tkinter"],
            ], [18, 42, 40]),
            ("lembre", "Uma camada só conversa com a vizinha. A interface não escreve SQL; "
                       "o banco não conhece a interface. Assim você troca Tkinter por uma página "
                       "web depois sem mexer nas regras."),
        ]),
        ("6.2  Roteiro para qualquer projeto novo", [
            ("passos", [
                "<b>Descreva o problema</b> em 3 frases (quem usa, o que registra, que relatório quer).",
                "<b>Liste as entidades</b> (substantivos): ex.: Aluno, Turma, Presença.",
                "<b>Desenhe as tabelas</b>: uma por entidade, com chave primária e as chaves "
                "estrangeiras que ligam uma à outra.",
                "<b>Crie as classes</b>: uma por entidade, com as regras (validações) como métodos.",
                "<b>Escreva a camada de dados</b>: métodos adicionar / buscar / listar.",
                "<b>Faça os relatórios</b> com SQL (agregações) e pandas (apresentação).",
                "<b>Só então</b> monte a interface. Teste cada camada isolada antes de ligar tudo.",
            ]),
        ]),
        ("6.3  Esqueleto completo (estúdio de música)", [
            ("p", "Um agendamento de salas de ensaio: classe com a regra, banco guardando, pandas "
                  "resumindo. Leia de cima para baixo: cada bloco é uma camada."),
            ("run", '''import sqlite3
import pandas as pd

class Estudio:
    """Camada de dados + regras de agendamento."""

    def __init__(self, caminho=":memory:"):
        self.conn = sqlite3.connect(caminho)
        self.conn.execute("""CREATE TABLE IF NOT EXISTS ensaios (
            id INTEGER PRIMARY KEY, banda TEXT, sala INTEGER,
            horas INTEGER, valor_hora REAL)""")

    def agendar(self, banda, sala, horas, valor_hora=60.0):
        if horas <= 0:
            raise ValueError("horas deve ser positivo")
        self.conn.execute(
            "INSERT INTO ensaios (banda, sala, horas, valor_hora) VALUES (?, ?, ?, ?)",
            (banda, sala, horas, valor_hora))
        self.conn.commit()

    def relatorio(self):
        """Camada de análise: SQL entrega a tabela, pandas organiza."""
        df = pd.read_sql(
            "SELECT banda, horas * valor_hora AS valor FROM ensaios", self.conn)
        total = df.groupby("banda", as_index=False)["valor"].sum()
        return total.sort_values("valor", ascending=False)

est = Estudio()
est.agendar("Trio Maré", 1, 2)
est.agendar("Banda Aurora", 2, 3, valor_hora=80.0)
est.agendar("Trio Maré", 1, 1)
print(est.relatorio().to_string(index=False))
try:
    est.agendar("Solo", 1, 0)
except ValueError as erro:
    print("recusado:", erro)''',
             "Classe + SQLite + pandas trabalhando juntos"),
            ("dica", "Desafio para praticar: implemente a regra de conflito de horário (duas bandas "
                     "não podem ocupar a mesma sala no mesmo horário). Comece escrevendo o SELECT que "
                     "detecta o conflito, depois use o resultado dentro de agendar()."),
        ]),
    ],
    resolvido=None,
    armadilhas=[
        "Começar pela interface: sem as regras e os dados funcionando, a tela só esconde os erros.",
        "Misturar SQL espalhado pelo programa todo: concentre numa classe/arquivo de dados.",
        "Guardar dados calculados no banco (ex.: total) em vez de calcular na consulta; "
        "eles ficam desatualizados.",
        "Não testar com dados vazios (sem reservas, sem alunos): é aí que SUM() devolve NULL.",
    ],
    cola=[
        ["Quero…", "Faça…"],
        ["guardar dados", "tabela + classe de acesso com adicionar/listar"],
        ["proteger uma regra", "método da classe que levanta ValueError"],
        ["relatório rápido", "SQL agrega → pandas apresenta"],
        ["tela", "Tkinter chamando os métodos da classe (nunca SQL direto)"],
        ["testar", "rode a classe sozinha com dados de exemplo antes da tela"],
    ],
    exercicios=["ap_reservas_hotel"],
)

# ═════════════════════════════════════════════════════════════════════════
# APÊNDICES
# ═════════════════════════════════════════════════════════════════════════
COMO_RESOLVER = [
    "<b>Leia o enunciado duas vezes</b> e sublinhe o que ele PEDE: nomes de variáveis, de funções, formato do resultado.",
    "<b>Anote a entrada e a saída</b> em uma linha cada: 'recebo uma lista de dicts → devolvo um número'.",
    "<b>Resolva um exemplo à mão</b> com os dados fornecidos. O resultado é o seu teste.",
    "<b>Escreva a versão mais simples</b> que funcione (pode ser com for). Funcionar vem antes de ficar bonito.",
    "<b>Rode e compare</b> com o resultado à mão. Divergiu? Imprima os passos intermediários com print().",
    "<b>Só então melhore</b>: troque o for por comprehension, nomeie melhor, remova repetição.",
    "<b>Confira os casos de borda</b>: lista vazia, valor zero, texto com espaços, letra maiúscula.",
]

COMO_USAR_APP = [
    "Abra <b>estudogr.vercel.app</b> e escolha a <b>pílula vermelha</b> (login com Google) para que "
    "seu progresso e seu código fiquem salvos no banco de dados.",
    "No topo da barra lateral há duas abas: <b>Exercícios</b> (os 16 do ambiente) e <b>Apostila</b> "
    "(os 16 exercícios deste material, na mesma ordem dos capítulos).",
    "Clique em um exercício, leia o enunciado, escreva no editor e use <b>Executar</b> para ver a "
    "saída e <b>Verificar</b> para a correção automática.",
    "Ao acertar, aparece a solução comentada ('versão otimizada') para você comparar com a sua.",
    "O código que você escreve é salvo sozinho (e no banco, se estiver logado). Pode fechar e voltar depois.",
    "O botão <b>Baixar apostila (PDF)</b> no cabeçalho baixa este material.",
]

ERROS_COMUNS = [
    ["Mensagem", "O que olhar primeiro"],
    ["IndentationError: unexpected indent", "linha com espaços a mais/menos que o bloco"],
    ["SyntaxError: invalid syntax", "falta ':' ou parêntese; confira a linha de cima também"],
    ["NameError: name 'x' is not defined", "escreveu o nome diferente ou usou antes de criar"],
    ["KeyError: 'preco'", "chave/coluna inexistente (acentos e maiúsculas contam)"],
    ["TypeError: unsupported operand", "somando/multiplicando tipos incompatíveis (texto × número)"],
    ["AttributeError: 'list' has no attribute ...", "método não existe nesse tipo de objeto"],
    ["ValueError: invalid literal for int()", "texto que não é número (ex.: 'abc' ou '3,5')"],
    ["sqlite3.OperationalError: no such table", "tabela não criada nesta conexão (ou nome errado)"],
    ["sqlite3.ProgrammingError: Incorrect number of bindings", "quantidade de ? diferente da de valores"],
]
