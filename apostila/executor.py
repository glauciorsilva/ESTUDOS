# -*- coding: utf-8 -*-
"""Executa os blocos 'run'/'runc' do conteúdo e devolve a saída REAL de cada um."""
import ast, contextlib, io, textwrap


def executar(codigo, ns):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(codigo, "<apostila>", "exec"), ns)
    return buf.getvalue().rstrip("\n")


def processar(CAP):
    """Devolve {(cap, indice_secao, indice_bloco): saida} e valida a sintaxe dos blocos 'code'."""
    saidas, erros = {}, []
    for n, cap in CAP.items():
        ns = {}
        for i, (_, blocos) in enumerate(cap["secoes"]):
            for j, b in enumerate(blocos):
                tipo = b[0]
                if tipo in ("run", "runc"):
                    if tipo == "run":
                        ns = {}
                    try:
                        saidas[(n, i, j)] = executar(b[1], ns)
                    except Exception as e:  # noqa
                        erros.append(f"cap {n} seção {i} bloco {j}: {type(e).__name__}: {e}")
                elif tipo == "code":
                    try:
                        ast.parse(b[1])
                    except SyntaxError as e:
                        erros.append(f"cap {n} seção {i} bloco {j} (code): SyntaxError {e}")
        r = cap.get("resolvido")
        if r:
            if r.get("codigo"):
                try:
                    saidas[(n, "res")] = executar(r["codigo"], {})
                except Exception as e:  # noqa
                    erros.append(f"cap {n} resolvido: {type(e).__name__}: {e}")
            if r.get("codigo_estatico"):
                try:
                    ast.parse(r["codigo_estatico"])
                except SyntaxError as e:
                    erros.append(f"cap {n} resolvido estático: {e}")
    return saidas, erros


if __name__ == "__main__":
    from conteudo import CAP
    s, e = processar(CAP)
    print(len(s), "blocos executados;", len(e), "erro(s)")
    for x in e:
        print(" -", x)
    for k, v in s.items():
        print("\n==", k)
        print(v)
