# -*- coding: utf-8 -*-
"""Valida os exercícios: a solução PASSA na verificação e o starter NÃO passa."""
import ast, re, sys
from exercicios import EXERCICIOS


def rodar_check(codigo_check, ns):
    arvore = ast.parse(codigo_check)
    *corpo, ultimo = arvore.body
    exec(compile(ast.Module(corpo, []), "<check>", "exec"), ns)
    return eval(compile(ast.Expression(ultimo.value), "<check>", "eval"), ns)


def main():
    falhas = 0
    ids = set()
    for e in EXERCICIOS:
        assert e["id"] not in ids, f"id repetido {e['id']}"
        ids.add(e["id"])
        if e.get("mode") == "structural":
            sol_falta = [d for r, d in e["regras"] if not re.search(r, e["solucao"])]
            ini_falta = [d for r, d in e["regras"] if not re.search(r, e["starter"])]
            ok = not sol_falta and ini_falta
            print(("OK  " if ok else "FAIL"), e["id"], "(estrutural)",
                  "" if ok else f"solução sem: {sol_falta}; starter faltando {len(ini_falta)}")
            falhas += 0 if ok else 1
            continue
        # solução deve passar
        ns = {}
        try:
            exec(e["solucao"], ns)
            r = rodar_check(e["check"], ns)
            ok_sol = r["ok"]
            msg_sol = r["message"]
        except Exception as ex_:
            ok_sol, msg_sol = False, f"EXC {type(ex_).__name__}: {ex_}"
        # starter não deve passar
        ns2 = {}
        try:
            exec(e["starter"], ns2)
            r2 = rodar_check(e["check"], ns2)
            ok_ini = r2["ok"]
        except Exception:
            ok_ini = False
        ok = ok_sol and not ok_ini
        print(("OK  " if ok else "FAIL"), e["id"],
              "" if ok else f"solução ok={ok_sol} ({msg_sol}); starter passa={ok_ini}")
        falhas += 0 if ok else 1
    print(f"\n{len(EXERCICIOS)} exercícios, {falhas} falha(s)")
    sys.exit(1 if falhas else 0)


main()
