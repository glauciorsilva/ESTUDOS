# -*- coding: utf-8 -*-
"""Gera ../apostila-exercicios.js (exercícios da aba "Apostila" do app) a partir de exercicios.py."""
import json
import os

from exercicios import CAPITULOS, EXERCICIOS

DESTINO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "apostila-exercicios.js")


def js(v):
    return json.dumps(v, ensure_ascii=False)


def main():
    partes = []
    for e in EXERCICIOS:
        campos = [
            f"id:{js(e['id'])}", "apostila:true", f"cap:{e['cap']}",
            f"nivel:{js(e['nivel'])}", f"topico:{js(e['topico'])}",
            f"titulo:{js(e['titulo'])}", f"caso:{js(e['caso'])}",
            f"starter:{js(e['starter'])}",
            f"otimizado:{js(e['solucao'])}",
            f"melhorias:{js(e['melhorias'])}",
        ]
        if e.get("mode") == "structural":
            regras = ",\n    ".join(
                f"{{re:new RegExp({js(r)}), desc:{js(d)}}}" for r, d in e["regras"])
            campos.append('mode:"structural"')
            campos.append(f"structuralRules:[\n    {regras}\n  ]")
        else:
            campos.append(f"check:{js(e['check'])}")
        partes.append("{\n  " + ",\n  ".join(campos) + "\n}")
    saida = (
        "/* GERADO por apostila/gerar_js.py a partir de apostila/exercicios.py — não edite à mão. */\n"
        f"const APOSTILA_CAPITULOS = {js({str(k): v for k, v in CAPITULOS.items()})};\n"
        "const APOSTILA_EXERCISES = [\n" + ",\n".join(partes) + "\n];\n"
    )
    with open(DESTINO, "w", encoding="utf-8") as f:
        f.write(saida)
    print("gerado:", os.path.normpath(DESTINO), f"({len(EXERCICIOS)} exercícios)")


main()
