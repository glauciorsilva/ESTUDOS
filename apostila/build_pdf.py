# -*- coding: utf-8 -*-
"""Gera a apostila em PDF: python3 build_pdf.py  ->  Apostila_Dados_com_Python.pdf"""
import html
import os
import random
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, KeepTogether,
                                PageBreak, PageTemplate, Paragraph, XPreformatted,
                                Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

from conteudo import (CAP, COMO_RESOLVER, COMO_USAR_APP, ERROS_COMUNS)
from exercicios import CAPITULOS, EXERCICIOS
from executor import processar

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "Apostila_Dados_com_Python.pdf")
EX = {e["id"]: e for e in EXERCICIOS}

# ───────────────────────── fontes ─────────────────────────
LIB = "/usr/share/fonts/truetype/liberation/"
DJV = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Corpo", LIB + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Corpo-Bold", LIB + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Corpo-Italic", LIB + "LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Corpo-BoldItalic", LIB + "LiberationSans-BoldItalic.ttf"))
pdfmetrics.registerFontFamily("Corpo", normal="Corpo", bold="Corpo-Bold",
                              italic="Corpo-Italic", boldItalic="Corpo-BoldItalic")
pdfmetrics.registerFont(TTFont("Mono", DJV + "DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("Mono-Bold", DJV + "DejaVuSansMono-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono-Italic", DJV + "DejaVuSansMono-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("Mono-BoldItalic", DJV + "DejaVuSansMono-BoldOblique.ttf"))
pdfmetrics.registerFontFamily("Mono", normal="Mono", bold="Mono-Bold",
                              italic="Mono-Italic", boldItalic="Mono-BoldItalic")

# ───────────────────────── paleta ─────────────────────────
NEON = colors.HexColor("#00ff41")
VERDE = colors.HexColor("#0a8a2e")       # títulos em fundo branco
VERDE_ESC = colors.HexColor("#06501c")
PRETO = colors.HexColor("#050805")
TEXTO = colors.HexColor("#1b221d")
CINZA = colors.HexColor("#5b675f")
FUNDO_COD = colors.HexColor("#f0f5f1")
BORDA_COD = colors.HexColor("#bcd9c4")
LARG, ALT = A4
MARG = 1.9 * cm
LARG_UTIL = LARG - 2 * MARG

# ───────────────────────── estilos ─────────────────────────
def estilo(nome, **kw):
    base = dict(fontName="Corpo", fontSize=10, leading=14.2, textColor=TEXTO)
    base.update(kw)
    return ParagraphStyle(nome, **base)


S = {
    "p": estilo("p", spaceAfter=6, alignment=TA_LEFT),
    "intro": estilo("intro", fontSize=11, leading=16, textColor=VERDE_ESC, spaceAfter=10),
    "h1": estilo("h1", fontName="Corpo-Bold", fontSize=20, leading=24, textColor=VERDE_ESC,
                 spaceBefore=4, spaceAfter=8),
    "h2": estilo("h2", fontName="Corpo-Bold", fontSize=13.5, leading=17, textColor=VERDE,
                 spaceBefore=12, spaceAfter=5, keepWithNext=1),
    "h3": estilo("h3", fontName="Corpo-Bold", fontSize=11, leading=14, textColor=VERDE_ESC,
                 spaceBefore=8, spaceAfter=3, keepWithNext=1),
    "legenda": estilo("legenda", fontName="Corpo-Italic", fontSize=8.5, leading=11,
                      textColor=CINZA, spaceBefore=4, spaceAfter=2, keepWithNext=1),
    "item": estilo("item", leftIndent=14, bulletIndent=3, spaceAfter=3),
    "cel": estilo("cel", fontSize=8.8, leading=11.2),
    "celh": estilo("celh", fontName="Corpo-Bold", fontSize=8.8, leading=11.2, textColor=colors.white),
    "celm": estilo("celm", fontName="Mono", fontSize=7.9, leading=10),
    "caixa": estilo("caixa", fontSize=9.4, leading=13),
    "cod": ParagraphStyle("cod", fontName="Mono", fontSize=7.9, leading=10.1, textColor=colors.HexColor("#14301c"),
                          backColor=FUNDO_COD, borderColor=BORDA_COD, borderWidth=0.6,
                          borderPadding=(5, 6, 5, 6), leftIndent=8, rightIndent=8,
                          spaceBefore=9, spaceAfter=9),
    "saida": ParagraphStyle("saida", fontName="Mono", fontSize=7.9, leading=10.1,
                            textColor=colors.HexColor("#8dffb0"), backColor=PRETO,
                            borderColor=PRETO, borderWidth=0.6, borderPadding=(5, 6, 5, 6),
                            leftIndent=8, rightIndent=8, spaceBefore=1, spaceAfter=9),
    "rot_saida": estilo("rot_saida", fontName="Mono-Bold", fontSize=7, leading=9, textColor=VERDE,
                        spaceBefore=1, spaceAfter=4, leftIndent=8, keepWithNext=1),
    "toc1": estilo("toc1", fontName="Corpo-Bold", fontSize=11, leading=16, leftIndent=0,
                   textColor=VERDE_ESC, spaceBefore=6),
    "toc2": estilo("toc2", fontSize=9.5, leading=13, leftIndent=16, textColor=TEXTO),
    "ex_t": estilo("ex_t", fontName="Corpo-Bold", fontSize=11.5, leading=15, textColor=colors.white),
    "ex_id": estilo("ex_id", fontName="Mono", fontSize=7.8, leading=10, textColor=NEON),
}

LIMITE_COL = 94


def esc(t):
    return html.escape(t, quote=False)


def paragrafo(txt, estilo_="p"):
    return Paragraph(txt, S[estilo_])


# ───────────────────────── flowables personalizados ─────────────────────────
class Banner(Flowable):
    """Faixa preta de abertura de capítulo."""

    def __init__(self, numero, titulo):
        super().__init__()
        self.numero, self.titulo = numero, titulo
        self.width, self.height = LARG_UTIL, 3.1 * cm

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(PRETO)
        c.roundRect(0, 0, self.width, self.height, 8, fill=1, stroke=0)
        rnd = random.Random(self.numero * 11)
        c.setFont("Mono", 9)
        for i in range(34):
            x = 8 + i * (self.width - 16) / 33
            for k in range(rnd.randint(2, 6)):
                c.setFillColor(colors.Color(0, 1, 0.25, alpha=max(0.06, 0.55 - k * 0.1)))
                c.drawString(x, self.height - 12 - k * 10, rnd.choice("01{}[]<>=+*/#$%&"))
        c.setFillColor(PRETO)
        c.setFillAlpha(0.78)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        c.setFillAlpha(1)
        c.setFillColor(NEON)
        c.setFont("Mono-Bold", 11)
        c.drawString(18, self.height - 26, f"CAPÍTULO {self.numero:02d}")
        c.setFillColor(colors.white)
        c.setFont("Corpo-Bold", 22)
        c.drawString(18, self.height - 54, self.titulo)
        c.setStrokeColor(NEON)
        c.setLineWidth(1.2)
        c.line(18, 12, 18 + 90, 12)


class Rascunho(Flowable):
    """Área pautada para anotar a abordagem à mão."""

    def __init__(self, linhas=5):
        super().__init__()
        self.linhas = linhas
        self.width, self.height = LARG_UTIL, 0.62 * cm * linhas + 0.9 * cm

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setStrokeColor(BORDA_COD)
        c.setLineWidth(0.6)
        c.roundRect(0, 0, self.width, self.height, 5, fill=0, stroke=1)
        c.setFillColor(CINZA)
        c.setFont("Corpo-Italic", 7.5)
        c.drawString(8, self.height - 11, "Rascunho — escreva a entrada, a saída esperada e os passos antes de programar")
        c.setStrokeColor(colors.HexColor("#d6e6da"))
        for i in range(self.linhas):
            y = self.height - 0.9 * cm - i * 0.62 * cm
            c.line(8, y, self.width - 8, y)


class Marcador(Flowable):
    """Invisível: avisa a numeração de página em qual capítulo estamos."""

    def __init__(self, doc_attr, valor):
        super().__init__()
        self.doc_attr, self.valor = doc_attr, valor
        self.width = self.height = 0

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        setattr(self.canv, self.doc_attr, self.valor)


class TituloTOC(Paragraph):
    def __init__(self, texto, estilo_, nivel, chave):
        super().__init__(texto, estilo_)
        self.nivel, self.chave, self.texto_toc = nivel, chave, re.sub(r"<[^>]+>", "", texto)


# ───────────────────────── documento ─────────────────────────
class Doc(BaseDocTemplate):
    def __init__(self, nome, **kw):
        super().__init__(nome, pagesize=A4, leftMargin=MARG, rightMargin=MARG,
                         topMargin=2.0 * cm, bottomMargin=1.8 * cm,
                         title="Dados com Python — Apostila de bolso",
                         author="Estudo GR", subject="Python, POO, pandas, SQLite e Tkinter", **kw)
        frame = Frame(MARG, 1.8 * cm, LARG_UTIL, ALT - 3.8 * cm, id="f", leftPadding=0,
                      rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="capa", frames=[Frame(0, 0, 1, 1, id="x")], onPage=desenha_capa, autoNextPageTemplate="miolo"),
            PageTemplate(id="miolo", frames=[frame], onPageEnd=cabecalho_rodape),
        ])

    def afterFlowable(self, fl):
        if isinstance(fl, TituloTOC):
            self.notify("TOCEntry", (fl.nivel, fl.texto_toc, self.page, fl.chave))
            self.canv.bookmarkPage(fl.chave)
            self.canv.addOutlineEntry(fl.texto_toc, fl.chave, level=fl.nivel, closed=fl.nivel == 0)


def cabecalho_rodape(canv, doc):
    canv.saveState()
    cap = getattr(canv, "cap_atual", "")
    canv.setStrokeColor(colors.HexColor("#cfe3d5"))
    canv.setLineWidth(0.6)
    canv.line(MARG, ALT - 1.45 * cm, LARG - MARG, ALT - 1.45 * cm)
    canv.setFont("Mono-Bold", 7.5)
    canv.setFillColor(VERDE)
    canv.drawString(MARG, ALT - 1.25 * cm, "DADOS COM PYTHON")
    canv.setFont("Corpo", 7.8)
    canv.setFillColor(CINZA)
    canv.drawRightString(LARG - MARG, ALT - 1.25 * cm, cap)
    canv.line(MARG, 1.35 * cm, LARG - MARG, 1.35 * cm)
    canv.drawString(MARG, 0.9 * cm, "Estudo · GR — para relembrar na frente da máquina")
    canv.setFont("Mono-Bold", 8.5)
    canv.setFillColor(VERDE_ESC)
    canv.drawRightString(LARG - MARG, 0.9 * cm, str(doc.page))
    canv.restoreState()


# ───────────────────────── capa ─────────────────────────
def desenha_capa(canv, doc):
    W, H = A4
    canv.saveState()
    canv.setFillColor(colors.black)
    canv.rect(0, 0, W, H, fill=1, stroke=0)

    # chuva de código
    rnd = random.Random(2026)
    glifos = "01{}[]<>=+*/#$%&@;:()_|?!ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    canv.setFont("Mono", 11)
    passo = 15
    for i in range(int(W / passo) + 1):
        x = i * passo + 3
        topo = rnd.uniform(H * 0.45, H + 40)
        comp = rnd.randint(8, 34)
        for k in range(comp):
            y = topo - k * 14
            if y < -10 or y > H + 10:
                continue
            a = max(0.05, 0.85 - k * (0.85 / comp))
            canv.setFillColor(colors.Color(0.85, 1, 0.9, alpha=min(1, a + 0.2)) if k == 0
                              else colors.Color(0, 1, 0.25, alpha=a * 0.75))
            canv.drawString(x, y, rnd.choice(glifos))

    # halo atrás do boneco
    cx, cy = W / 2, H * 0.50
    for r, al in [(230, 0.10), (190, 0.16), (150, 0.26), (115, 0.5)]:
        canv.setFillColor(colors.Color(0, 0, 0, alpha=al + 0.25))
        canv.circle(cx, cy, r, fill=1, stroke=0)
    canv.setStrokeColor(colors.Color(0, 1, 0.25, alpha=0.55))
    canv.setLineWidth(1)
    canv.circle(cx, cy, 168, fill=0, stroke=1)
    canv.setStrokeColor(colors.Color(0, 1, 0.25, alpha=0.25))
    canv.circle(cx, cy, 180, fill=0, stroke=1)

    desenha_boneco(canv, cx, cy + 6, 0.98)

    # título
    canv.setFillColor(colors.Color(0, 0, 0, alpha=0.8))
    canv.rect(0, H - 235, W, 150, fill=1, stroke=0)
    canv.setFillColor(NEON)
    canv.setFont("Mono-Bold", 12)
    canv.drawCentredString(W / 2, H - 112, "ESTUDO · GR   //   APOSTILA DE BOLSO")
    for dx, al in [(0, 1), (1.2, 0.35), (-1.2, 0.35), (0, 0.2)]:
        canv.setFillColor(colors.Color(0, 1, 0.25, alpha=al))
        canv.setFont("Mono-Bold", 50)
        canv.drawCentredString(W / 2 + dx, H - 168 + (dx and 0.8), "DADOS COM")
        canv.drawCentredString(W / 2 + dx, H - 222 + (dx and 0.8), "PYTHON")
    # nota: a 2ª linha fica sobre a faixa; ajusta abaixo
    canv.setStrokeColor(NEON)
    canv.setLineWidth(1.5)
    canv.line(W / 2 - 120, H - 244, W / 2 + 120, H - 244)

    # rodapé da capa
    canv.setFillColor(colors.Color(0, 0, 0, alpha=0.82))
    canv.rect(0, 0, W, 170, fill=1, stroke=0)
    canv.setFillColor(colors.white)
    canv.setFont("Corpo-Bold", 15)
    canv.drawCentredString(W / 2, 130, "Teoria, receitas e exercícios para relembrar")
    canv.setFont("Corpo", 11)
    canv.setFillColor(colors.Color(0.78, 1, 0.84))
    canv.drawCentredString(W / 2, 110, "como obter resultados com código — sem decorar, entendendo.")
    topicos = ["Python básico", "POO", "Pandas", "SQLite & SQL", "Tkinter", "Projeto integrador"]
    x0, y0 = MARG, 72
    larg_t = (W - 2 * MARG) / 3
    canv.setFont("Mono-Bold", 9)
    for i, t in enumerate(topicos):
        xx = x0 + (i % 3) * larg_t
        yy = y0 - (i // 3) * 20
        canv.setFillColor(NEON)
        canv.drawString(xx, yy, f"{i + 1:02d}")
        canv.setFillColor(colors.white)
        canv.setFont("Corpo-Bold", 10.5)
        canv.drawString(xx + 20, yy, t)
        canv.setFont("Mono-Bold", 9)
    canv.setFillColor(colors.Color(0, 1, 0.25, alpha=0.8))
    canv.setFont("Mono", 8)
    canv.drawCentredString(W / 2, 22, "estudogr.vercel.app   ·   16 exercícios práticos com correção automática")

    # moldura neon
    canv.setStrokeColor(NEON)
    canv.setLineWidth(2)
    canv.rect(14, 14, W - 28, H - 28, fill=0, stroke=1)
    canv.setStrokeColor(colors.Color(0, 1, 0.25, alpha=0.35))
    canv.setLineWidth(0.6)
    canv.rect(20, 20, W - 40, H - 40, fill=0, stroke=1)
    canv.restoreState()


def desenha_boneco(c, ox, oy, s):
    """Boneco de óculos escuros oferecendo duas pílulas (coordenadas do SVG do app)."""
    def X(x):
        return ox + (x - 160) * s

    def Y(y):
        return oy - (y - 175) * s

    def elipse(cx, cy, rx, ry, cor, borda=None, alpha=1):
        c.setFillColor(cor)
        c.setFillAlpha(alpha)
        if borda:
            c.setStrokeColor(borda)
            c.setLineWidth(1)
        c.ellipse(X(cx - rx), Y(cy + ry), X(cx + rx), Y(cy - ry), fill=1, stroke=1 if borda else 0)
        c.setFillAlpha(1)

    def rrect(x, y, w, h, r, cor, borda=None):
        c.setFillColor(cor)
        if borda:
            c.setStrokeColor(borda)
            c.setLineWidth(1.2)
        c.roundRect(X(x), Y(y + h), w * s, h * s, r * s, fill=1, stroke=1 if borda else 0)

    def traco(p0, p1, p2, larg, cor):
        """curva quadrática do SVG com ponta redonda"""
        c.setStrokeColor(cor)
        c.setLineWidth(larg * s)
        c.setLineCap(1)
        (x0, y0), (qx, qy), (x1, y1) = p0, p1, p2
        c1 = (x0 + 2 / 3 * (qx - x0), y0 + 2 / 3 * (qy - y0))
        c2 = (x1 + 2 / 3 * (qx - x1), y1 + 2 / 3 * (qy - y1))
        p = c.beginPath()
        p.moveTo(X(x0), Y(y0))
        p.curveTo(X(c1[0]), Y(c1[1]), X(c2[0]), Y(c2[1]), X(x1), Y(y1))
        c.drawPath(p, fill=0, stroke=1)

    pele = colors.HexColor("#7a4a2b")
    pele_esc = colors.HexColor("#5b3419")
    preto = colors.HexColor("#0a0a0a")
    verde = colors.HexColor("#00ff41")

    # base
    elipse(160, 330, 108, 16, colors.HexColor("#06280f"), borda=verde)
    elipse(160, 324, 90, 10, verde, alpha=0.18)
    # pernas e sapatos
    rrect(121, 262, 34, 58, 14, preto)
    rrect(165, 262, 34, 58, 14, preto)
    elipse(136, 321, 23, 9, colors.black)
    elipse(184, 321, 23, 9, colors.black)
    # braços
    traco((104, 176), (66, 190), (50, 226), 30, preto)
    traco((216, 176), (254, 190), (270, 226), 30, preto)
    traco((104, 176), (68, 188), (52, 222), 6, colors.HexColor("#2a2a2a"))
    traco((216, 176), (252, 188), (268, 222), 6, colors.HexColor("#2a2a2a"))
    # casaco
    c.setFillColor(colors.HexColor("#111111"))
    p = c.beginPath()
    p.moveTo(X(100), Y(168))
    p.curveTo(X(130), Y(150), X(190), Y(150), X(220), Y(168))
    p.lineTo(X(238), Y(278))
    p.curveTo(X(190), Y(292), X(130), Y(292), X(82), Y(278))
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor("#303030"))
    c.setLineWidth(1.3)
    c.line(X(160), Y(168), X(160), Y(284))
    c.setFillColor(colors.HexColor("#1d1d1d"))
    p = c.beginPath()
    p.moveTo(X(128), Y(160))
    p.lineTo(X(160), Y(214))
    p.lineTo(X(192), Y(160))
    p.close()
    c.drawPath(p, fill=1, stroke=1)
    for yy in (236, 258):
        elipse(150, yy, 3, 3, colors.HexColor("#3a3a3a"))
    # pescoço, cabeça, orelhas
    rrect(143, 138, 34, 26, 10, pele_esc)
    elipse(160, 90, 58, 56, pele)
    elipse(102, 94, 11, 11, colors.HexColor("#6e4222"))
    elipse(218, 94, 11, 11, colors.HexColor("#6e4222"))
    elipse(136, 55, 22, 12, colors.white, alpha=0.16)
    # óculos
    rrect(112, 76, 46, 26, 12, colors.HexColor("#050505"), borda=colors.HexColor("#2b2b2b"))
    rrect(162, 76, 46, 26, 12, colors.HexColor("#050505"), borda=colors.HexColor("#2b2b2b"))
    c.setStrokeColor(colors.HexColor("#2b2b2b"))
    c.setLineWidth(2.5 * s)
    c.line(X(158), Y(87), X(162), Y(87))
    c.setStrokeColor(verde)
    c.setLineWidth(2.6 * s)
    c.setLineCap(1)
    c.line(X(120), Y(82), X(134), Y(80))
    c.line(X(170), Y(82), X(184), Y(80))
    # sobrancelhas, nariz, sorriso
    traco((116, 68), (135, 60), (152, 68), 3.5, colors.HexColor("#2a1608"))
    traco((168, 68), (185, 60), (204, 68), 3.5, colors.HexColor("#2a1608"))
    traco((156, 108), (160, 114), (164, 108), 3, colors.HexColor("#3b200d"))
    traco((138, 124), (160, 138), (182, 124), 4, colors.HexColor("#2a1608"))
    # mãos
    elipse(50, 232, 16, 16, pele)
    elipse(270, 232, 16, 16, pele)

    # pílulas com brilho
    def pilula(cx, cy, ang, cor, claro, escuro):
        c.saveState()
        c.translate(X(cx), Y(cy))
        c.rotate(-ang)
        for r, al in [(34, 0.10), (27, 0.18)]:
            c.setFillColor(colors.Color(cor.red, cor.green, cor.blue, alpha=al))
            c.circle(0, 0, r * s, fill=1, stroke=0)
        c.setFillColor(cor)
        c.setStrokeColor(escuro)
        c.setLineWidth(1)
        c.roundRect(-24 * s, -11 * s, 48 * s, 22 * s, 11 * s, fill=1, stroke=1)
        c.setFillColor(claro)
        c.setFillAlpha(0.7)
        c.roundRect(-18 * s, 3 * s, 22 * s, 5 * s, 2.5 * s, fill=1, stroke=0)
        c.restoreState()

    pilula(50, 206, 24, colors.HexColor("#ff1d1d"), colors.white, colors.HexColor("#5a0000"))
    pilula(270, 206, -24, colors.HexColor("#2468ff"), colors.white, colors.HexColor("#00155a"))


# ───────────────────────── blocos ─────────────────────────
def caixa(txt, rotulo, cor_borda, cor_fundo):
    t = Table([[Paragraph(f"<b>{rotulo}</b>  {txt}", S["caixa"])]], colWidths=[LARG_UTIL])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), cor_fundo),
        ("LINEBEFORE", (0, 0), (0, -1), 3, cor_borda),
        ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#d5dfd8")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return [t, Spacer(1, 7)]


def tabela(linhas, larguras, mono_primeira=False):
    dados = []
    for i, lin in enumerate(linhas):
        row = []
        for j, cel in enumerate(lin):
            if i == 0:
                row.append(Paragraph(esc(cel), S["celh"]))
            elif j == len(lin) - 1 and len(lin) >= 2 and mono_primeira is False and _eh_codigo(cel):
                row.append(Paragraph(esc(cel), S["celm"]))
            else:
                row.append(Paragraph(esc(cel), S["cel"]))
        dados.append(row)
    cw = [LARG_UTIL * l / sum(larguras) for l in larguras]
    t = Table(dados, colWidths=cw, repeatRows=1)
    est = [
        ("BACKGROUND", (0, 0), (-1, 0), PRETO),
        ("LINEBELOW", (0, 0), (-1, 0), 1.2, NEON),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 1), (-1, -1), 0.3, colors.HexColor("#d3ded6")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(dados)):
        if i % 2 == 0:
            est.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f4f8f5")))
    t.setStyle(TableStyle(est))
    return [t, Spacer(1, 9)]


def _eh_codigo(txt):
    return bool(re.search(r"[(){}\[\]=_.]|SELECT|FROM|CREATE|INSERT|UPDATE|DELETE", txt)) and not txt[:1].isupper() or \
        bool(re.match(r"^(SELECT|CREATE|INSERT|UPDATE|DELETE|FROM|import|pd\.|df|tk\.|class|def)", txt))


avisos = []


def codigo(txt):
    for lin in txt.split("\n"):
        if len(lin) > LIMITE_COL:
            avisos.append(f"linha longa ({len(lin)}): {lin[:60]}…")
    return XPreformatted(esc(txt.expandtabs(4)), S["cod"])


def bloco_run(txt, legenda, saida):
    out = []
    if legenda:
        out.append(Paragraph(esc(legenda), S["legenda"]))
    out.append(codigo(txt))
    if saida:
        for lin in saida.split("\n"):
            if len(lin) > LIMITE_COL:
                avisos.append(f"saída longa ({len(lin)}): {lin[:60]}…")
        out.append(Paragraph("▶ SAÍDA", S["rot_saida"]))
        out.append(XPreformatted(esc(saida), S["saida"]))
    return out


def renderiza_secao_blocos(n, i, blocos, saidas):
    fl = []
    for j, b in enumerate(blocos):
        t = b[0]
        if t == "p":
            fl.append(paragrafo(b[1]))
        elif t == "lista":
            fl += [Paragraph(x, S["item"], bulletText="•") for x in b[1]]
            fl.append(Spacer(1, 4))
        elif t == "passos":
            fl += [Paragraph(x, S["item"], bulletText=f"{k}.") for k, x in enumerate(b[1], 1)]
            fl.append(Spacer(1, 4))
        elif t == "code":
            fl.append(codigo(b[1]))
        elif t in ("run", "runc"):
            fl += bloco_run(b[1], b[2] if len(b) > 2 else "", saidas.get((n, i, j), ""))
        elif t == "dica":
            fl += caixa(b[1], "DICA", colors.HexColor("#00b341"), colors.HexColor("#effaf2"))
        elif t == "cuidado":
            fl += caixa(b[1], "CUIDADO", colors.HexColor("#e0a100"), colors.HexColor("#fff8e6"))
        elif t == "lembre":
            fl += caixa(b[1], "LEMBRE", colors.HexColor("#1f7fbf"), colors.HexColor("#edf6fc"))
        elif t == "tabela":
            fl += tabela(b[1], b[2])
        else:
            raise ValueError(f"bloco desconhecido: {t}")
    return fl


def cartao_exercicio(num, e):
    cab = Table([[Paragraph(f"Exercício {num} — {esc(e['titulo'])}", S["ex_t"]),
                  Paragraph(f"Apostila ▸ {e['id']}", S["ex_id"])]],
                colWidths=[LARG_UTIL * 0.66, LARG_UTIL * 0.34])
    cab.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PRETO),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("LINEBELOW", (0, 0), (-1, -1), 1.4, NEON),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    enun = esc(e["caso"]).replace("\n\n", "<br/><br/>").replace("\n", "<br/>")
    corpo = [cab, Spacer(1, 6), Paragraph(enun, S["p"]), Paragraph("Ponto de partida (já vem pronto no editor do app):", S["legenda"]),
             codigo(e["starter"].rstrip("\n")), Rascunho(4), Spacer(1, 12)]
    return corpo


# ───────────────────────── montagem ─────────────────────────
def montar():
    saidas, erros = processar(CAP)
    if erros:
        print("ERROS no conteúdo:")
        for x in erros:
            print(" -", x)
        sys.exit(1)

    story = [Marcador("cap_atual", "")]          # capa já é desenhada no template

    # Como usar + sumário
    story.append(Marcador("cap_atual", "Como usar esta apostila"))
    story.append(TituloTOC("Como usar esta apostila", S["h1"], 0, "usar"))
    story.append(paragrafo(
        "Esta apostila foi feita para <b>relembrar como obter resultados</b> com Python: cada capítulo "
        "explica a teoria, mostra receitas com exemplos <i>diferentes</i> dos do ambiente de prática, "
        "traz um exemplo resolvido passo a passo e termina com exercícios para você resolver "
        "diante do computador, na aba <b>Apostila</b> do app.", "intro"))
    story.append(paragrafo("<b>Como cada capítulo está organizado</b>"))
    story += [Paragraph(x, S["item"], bulletText="•") for x in [
        "<b>Teoria e receitas</b> — conceito curto + código que você pode copiar e adaptar. "
        "Cada bloco com saída mostra o resultado <b>real</b> da execução.",
        "<b>Exemplo resolvido</b> — do enunciado ao código, pensando em voz alta.",
        "<b>Armadilhas</b> — os tropeços mais comuns.",
        "<b>Cola rápida</b> — tabela de consulta de bolso.",
        "<b>Exercícios</b> — enunciado, ponto de partida e um espaço de rascunho. "
        "As soluções comentadas estão no <b>gabarito</b> no fim (tente antes de olhar!).",
    ]]
    story.append(Spacer(1, 6))
    story.append(paragrafo("<b>Usando a aba Apostila do app</b>"))
    story += [Paragraph(x, S["item"], bulletText=f"{k}.") for k, x in enumerate(COMO_USAR_APP, 1)]
    story.append(Spacer(1, 10))
    story.append(Paragraph("Sumário", S["h2"]))
    toc = TableOfContents()
    toc.levelStyles = [S["toc1"], S["toc2"]]
    toc.dotsMinLevel = 0
    story += [toc, PageBreak()]

    # capítulos
    n_ex = 0
    for n in sorted(CAP):
        cap = CAP[n]
        nome = f"Capítulo {n} — {cap['titulo']}"
        story.append(Marcador("cap_atual", nome))
        story.append(Banner(n, cap["titulo"]))
        story.append(TituloTOC(f"{n}. {esc(cap['titulo'])}", ParagraphStyle("oculto", fontSize=0.1, leading=0.1, spaceAfter=6), 0, f"cap{n}"))
        story.append(paragrafo(cap["intro"], "intro"))
        for i, (titulo, blocos) in enumerate(cap["secoes"]):
            story.append(TituloTOC(esc(titulo), S["h2"], 1, f"cap{n}s{i}"))
            story += renderiza_secao_blocos(n, i, blocos, saidas)
        r = cap.get("resolvido")
        if r:
            story.append(TituloTOC(esc(r["titulo"]), S["h2"], 1, f"cap{n}res"))
            story += caixa(esc(r["enunciado"]), "ENUNCIADO", colors.HexColor("#00b341"), colors.HexColor("#effaf2"))
            story.append(Paragraph("<b>Como pensar:</b>", S["p"]))
            story += [Paragraph(x, S["item"], bulletText=f"{k}.") for k, x in enumerate(r["passos"], 1)]
            story.append(Spacer(1, 4))
            if r.get("codigo"):
                story += bloco_run(r["codigo"], "Solução completa", saidas.get((n, "res"), ""))
            else:
                story.append(Paragraph("Solução completa (rode no seu computador)", S["legenda"]))
                story.append(codigo(r["codigo_estatico"]))
        story.append(Paragraph("Armadilhas comuns", S["h3"]))
        story += [Paragraph(x, S["item"], bulletText="!") for x in cap["armadilhas"]]
        story.append(Paragraph("Cola rápida", S["h3"]))
        story += tabela(cap["cola"], [34, 66])
        story.append(TituloTOC(f"Exercícios do capítulo {n}", S["h2"], 1, f"cap{n}ex"))
        story.append(paragrafo("Resolva no app (aba <b>Apostila</b>) e confira com a correção automática. "
                               "Antes de digitar, use o rascunho para anotar entrada, saída e passos."))
        for ide in cap["exercicios"]:
            n_ex += 1
            story += cartao_exercicio(n_ex, EX[ide])
        story.append(PageBreak())

    # apêndices
    story.append(Marcador("cap_atual", "Apêndices"))
    story.append(TituloTOC("Apêndice A — Método para resolver qualquer exercício", S["h1"], 0, "apA"))
    story += [Paragraph(x, S["item"], bulletText=f"{k}.") for k, x in enumerate(COMO_RESOLVER, 1)]
    story.append(Spacer(1, 10))
    story.append(TituloTOC("Apêndice B — Mensagens de erro e o que fazer", S["h1"], 0, "apB"))
    story += tabela(ERROS_COMUNS, [44, 56])
    story.append(PageBreak())

    # gabarito
    story.append(Marcador("cap_atual", "Gabarito"))
    story.append(TituloTOC("Gabarito comentado", S["h1"], 0, "gab"))
    story += caixa("Só abra esta parte depois de tentar! Se o seu código passou na correção automática mas é "
                   "diferente do abaixo, está tudo bem: compare as <i>ideias</i> (lista de pontos ao final de cada solução).",
                   "ANTES DE LER", colors.HexColor("#e0a100"), colors.HexColor("#fff8e6"))
    n_ex = 0
    for n in sorted(CAP):
        story.append(TituloTOC(f"Capítulo {n} — {esc(CAP[n]['titulo'])}", S["h2"], 1, f"gab{n}"))
        for ide in CAP[n]["exercicios"]:
            n_ex += 1
            e = EX[ide]
            bloco = [Paragraph(f"Exercício {n_ex} — {esc(e['titulo'])}", S["h3"]), codigo(e["solucao"].rstrip("\n"))]
            bloco += [Paragraph(esc(m), S["item"], bulletText="›") for m in e["melhorias"]]
            bloco.append(Spacer(1, 6))
            story.append(KeepTogether(bloco[:2]))
            story += bloco[2:]

    doc = Doc(SAIDA)
    doc.multiBuild(story)
    print("PDF gerado:", SAIDA)
    if avisos:
        print(f"{len(avisos)} aviso(s):")
        for a in avisos:
            print("  -", a)


if __name__ == "__main__":
    montar()
