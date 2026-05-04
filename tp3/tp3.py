import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np
import os

os.makedirs('img', exist_ok=True)


def cota(ax, x1, x2, y, label, offset=0.15, fontsize=9):
    """Dibuja una cota horizontal con flechas y etiqueta."""
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='<->', color='dimgray', lw=1))
    ax.text((x1 + x2) / 2, y + offset, label,
            ha='center', va='bottom', fontsize=fontsize, color='dimgray')


def cota_v(ax, x, y1, y2, label, offset=0.15, fontsize=9):
    """Dibuja una cota vertical."""
    ax.annotate('', xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle='<->', color='dimgray', lw=1))
    ax.text(x + offset, (y1 + y2) / 2, label,
            ha='left', va='center', fontsize=fontsize, color='dimgray')


def hatch_fill(ax, x, y, w, h, hatch='///', color='lightgray', ec='gray'):
    rect = mpatches.Rectangle((x, y), w, h,
                               hatch=hatch, facecolor=color,
                               edgecolor=ec, linewidth=0.8)
    ax.add_patch(rect)


def arrow_force(ax, x, y, dx, dy, color, label, fontsize=10,
                lx=0.15, ly=0.15):
    ax.annotate('', xy=(x + dx, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=2, mutation_scale=15))
    ax.text(x + dx + lx, y + dy + ly, label,
            color=color, fontsize=fontsize, fontweight='bold')


# ═══════════════════════════════════════════════════════════════
# FIGURA 1 — Muro de contención con contrafuerte
# ═══════════════════════════════════════════════════════════════
def figura_muro():
    fig, ax = plt.subplots(figsize=(9, 10))
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-3.5, 8)
    ax.set_ylim(-1.5, 10)

    # Dimensiones base
    h1    = 6.0    # altura de relleno
    h2    = 1.5    # altura lado pasivo
    em    = 0.40   # espesor muro
    ez    = 0.50   # espesor zapata
    ec    = 0.30   # espesor contrafuerte
    a_ref = 4.0    # ancho base referencial (incógnita)

    # Coordenadas base
    x0, y0 = 0.0, 0.0   # esquina inferior izquierda de la zapata

    # ── Zapata ────────────────────────────────────────────────
    hatch_fill(ax, x0, y0, a_ref, ez, hatch='', color='#d0d0d0', ec='black')
    ax.add_patch(mpatches.Rectangle((x0, y0), a_ref, ez,
                 fill=False, edgecolor='black', lw=1.5))

    # ── Muro vertical ─────────────────────────────────────────
    # El muro está en el extremo izquierdo de la zapata
    hatch_fill(ax, x0, ez, em, h1, hatch='', color='#b0b0b0', ec='black')
    ax.add_patch(mpatches.Rectangle((x0, ez), em, h1,
                 fill=False, edgecolor='black', lw=1.5))

    # ── Contrafuerte ──────────────────────────────────────────
    # Triángulo desde la base del muro hasta la parte superior
    xc = em
    contrafuerte = plt.Polygon(
        [(xc, ez), (xc + ec, ez), (xc, ez + h1)],
        closed=True, facecolor='#909090', edgecolor='black', lw=1.5)
    ax.add_patch(contrafuerte)

    # ── Relleno de suelo (lado activo) ────────────────────────
    hatch_fill(ax, -2.5, ez, 2.5, h1,
               hatch='..', color='#e8dcc8', ec='#a08060')
    ax.text(-1.25, ez + h1 / 2, 'Suelo\nrelleno',
            ha='center', va='center', fontsize=8,
            color='#604020', style='italic')

    # ── Suelo lado pasivo ─────────────────────────────────────
    hatch_fill(ax, a_ref, ez, 2.0, h2,
               hatch='..', color='#e8dcc8', ec='#a08060')

    # ── Nivel de terreno ──────────────────────────────────────
    ax.axhline(ez + h1, xmin=0.05, xmax=0.55,
               color='saddlebrown', lw=1, ls='--', alpha=0.6)
    ax.axhline(ez + h2, xmin=0.6, xmax=0.85,
               color='saddlebrown', lw=1, ls='--', alpha=0.6)

    # ── Presión activa (triángulo de presiones) ────────────────
    pa_max = 1.8   # longitud visual máxima de la flecha
    n = 6
    for i in range(n):
        yi = ez + h1 * i / (n - 1)
        scale = (h1 - (yi - ez)) / h1
        ax.annotate('', xy=(x0, yi), xytext=(x0 - pa_max * scale, yi),
                    arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.2))
    # Contorno triángulo
    ax.plot([-pa_max, 0, 0, -pa_max],
            [ez, ez, ez + h1, ez],
            color='#c0392b', lw=1.5, ls='-', alpha=0.5)
    ax.text(-pa_max / 2 - 0.3, ez + h1 / 2,
            'Presión\nActiva $E_a$',
            ha='center', va='center', fontsize=8,
            color='#c0392b', fontweight='bold')

    # ── Presión pasiva ────────────────────────────────────────
    pp_max = 1.2
    n2 = 4
    for i in range(n2):
        yi = ez + h2 * i / (n2 - 1)
        scale = (yi - ez) / h2
        ax.annotate('', xy=(a_ref, yi), xytext=(a_ref + pp_max * scale, yi),
                    arrowprops=dict(arrowstyle='->', color='#27ae60', lw=1.2))
    ax.plot([a_ref, a_ref + pp_max, a_ref, a_ref],
            [ez, ez, ez + h2, ez],
            color='#27ae60', lw=1.5, ls='-', alpha=0.5)
    ax.text(a_ref + pp_max / 2 + 0.4, ez + h2 / 2,
            'Presión\nPasiva $E_p$',
            ha='center', va='center', fontsize=8,
            color='#27ae60', fontweight='bold')

    # ── Peso del sistema (Ws) ─────────────────────────────────
    arrow_force(ax, a_ref / 2, ez + h1 + 0.8,
                0, -0.7, '#2c5f8a', '$W_s$', lx=0.1, ly=0.05)

    # ── Reacción del suelo (Rs) ───────────────────────────────
    arrow_force(ax, a_ref / 2, -0.1,
                0, -0.7, '#8e44ad', '$R_s$', lx=0.1, ly=-0.3)
    ax.text(a_ref / 2 + 0.15, -0.9,
            r'$\alpha$', fontsize=11, color='#8e44ad')

    # ── Cotas ────────────────────────────────────────────────
    # Ancho base (incógnita)
    cota(ax, x0, a_ref, -0.8, '$a$ = ?', offset=0.12)
    # h1
    cota_v(ax, -3.0, ez, ez + h1, '$h_1 = 6{,}0$ m', offset=0.12)
    # h2
    cota_v(ax, a_ref + 2.3, ez, ez + h2, '$h_2 = 1{,}5$ m', offset=0.12)
    # Espesor zapata
    cota_v(ax, a_ref + 0.6, y0, ez, '$e_z$', offset=0.1)
    # Espesor muro
    cota(ax, x0, x0 + em, ez + h1 + 0.3, '$e_m$', offset=0.1)

    # ── Etiquetas ────────────────────────────────────────────
    ax.text(x0 + em / 2, ez + h1 / 2, 'Muro',
            ha='center', va='center', fontsize=8,
            color='white', fontweight='bold', rotation=90)
    ax.text(x0 + em + ec / 3, ez + h1 * 0.3, 'C',
            ha='center', va='center', fontsize=8, color='white',
            fontweight='bold')
    ax.text(a_ref / 2, ez / 2, 'Zapata',
            ha='center', va='center', fontsize=9, color='#333')

    # ── Pivote de volcamiento ─────────────────────────────────
    ax.plot(a_ref, y0, 'v', color='black', ms=10, zorder=5)
    ax.text(a_ref + 0.1, y0 - 0.2, 'Pivote\nvolteo',
            fontsize=8, color='black')

    ax.set_title('Ejercicio 1 — Muro de contención con contrafuerte',
                 fontsize=11, pad=12)
    plt.tight_layout()
    plt.savefig('img/tp3_ej1.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('tp3_ej1.png generado')


# ═══════════════════════════════════════════════════════════════
# FIGURA 2 — Tanque elevado sobre cuatro patas
# ═══════════════════════════════════════════════════════════════
def figura_tanque():
    fig, ax = plt.subplots(figsize=(9, 11))
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-3, 9)
    ax.set_ylim(-1.5, 12)

    # Dimensiones
    de   = 3.0    # lado interior tanque
    e    = 0.15   # espesor pared
    ht   = 2.0    # altura tanque
    hp   = 4.0    # altura patas
    ef   = 0.20   # losa fondo
    etp  = 0.15   # losa tapa
    sp   = 0.30   # sección pata
    L    = 3.6    # separación entre patas (referencial)

    # Dimensión exterior del tanque
    d_ext = de + 2 * e

    # Posición base
    x0_tank = (L - d_ext) / 2
    y0_pata = 0.0
    y0_tank = hp

    # ── Terreno ───────────────────────────────────────────────
    hatch_fill(ax, -0.5, -0.4, L + 1, 0.4,
               hatch='///', color='#e8dcc8', ec='#a08060')
    ax.axhline(0, color='saddlebrown', lw=1.5, xmin=0.05, xmax=0.85)

    # ── Zapatas de fundación ──────────────────────────────────
    zap_w, zap_h = 0.8, 0.3
    for xp in [0, L]:
        ax.add_patch(mpatches.Rectangle(
            (xp - zap_w / 2, -zap_h), zap_w, zap_h,
            facecolor='#909090', edgecolor='black', lw=1.2))

    # ── Patas ─────────────────────────────────────────────────
    for xp in [0, L]:
        ax.add_patch(mpatches.Rectangle(
            (xp - sp / 2, y0_pata), sp, hp,
            facecolor='#b0b0b0', edgecolor='black', lw=1.2))

    # ── Losa de fondo del tanque ───────────────────────────────
    ax.add_patch(mpatches.Rectangle(
        (x0_tank, y0_tank), d_ext, ef,
        facecolor='#909090', edgecolor='black', lw=1.2))

    # ── Paredes del tanque ────────────────────────────────────
    # Pared izquierda
    ax.add_patch(mpatches.Rectangle(
        (x0_tank, y0_tank + ef), e, ht - ef - etp,
        facecolor='#b0b0b0', edgecolor='black', lw=1.2))
    # Pared derecha
    ax.add_patch(mpatches.Rectangle(
        (x0_tank + d_ext - e, y0_tank + ef), e, ht - ef - etp,
        facecolor='#b0b0b0', edgecolor='black', lw=1.2))

    # ── Agua ─────────────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle(
        (x0_tank + e, y0_tank + ef), de, ht - ef - etp - 0.1,
        facecolor='#aed6f1', edgecolor='#2980b9', lw=0.8, alpha=0.7))
    ax.text(x0_tank + e + de / 2, y0_tank + ef + (ht - ef - etp) / 2,
            'Agua', ha='center', va='center',
            fontsize=9, color='#1a5276')

    # ── Losa de tapa ─────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle(
        (x0_tank, y0_tank + ht - etp), d_ext, etp,
        facecolor='#909090', edgecolor='black', lw=1.2))

    # ── Viento ────────────────────────────────────────────────
    # Presión (lado izquierdo → hacia la derecha)
    n_v = 4
    for i in range(n_v):
        yi = y0_tank + ef + (ht - ef - etp) * i / (n_v - 1)
        ax.annotate('', xy=(x0_tank, yi),
                    xytext=(x0_tank - 1.0, yi),
                    arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=1.5))
    ax.text(x0_tank - 1.3, y0_tank + ht / 2,
            'Presión\n$p_w$', ha='center', va='center',
            fontsize=8, color='#e74c3c', fontweight='bold')

    # Succión (lado derecho → hacia la derecha, saliendo)
    for i in range(n_v):
        yi = y0_tank + ef + (ht - ef - etp) * i / (n_v - 1)
        ax.annotate('', xy=(x0_tank + d_ext + 1.0, yi),
                    xytext=(x0_tank + d_ext, yi),
                    arrowprops=dict(arrowstyle='->', color='#e67e22', lw=1.5))
    ax.text(x0_tank + d_ext + 1.4, y0_tank + ht / 2,
            'Succión\n$p_w$', ha='center', va='center',
            fontsize=8, color='#e67e22', fontweight='bold')

    # ── Peso total (Wt) ───────────────────────────────────────
    arrow_force(ax, L / 2, y0_tank + ht + 0.6,
                0, -0.5, '#2c5f8a', '$W_t$', lx=0.1, ly=0.05)

    # ── Reacción del suelo ────────────────────────────────────
    arrow_force(ax, L / 2, -0.15, 0, -0.6,
                '#8e44ad', '$R_s$', lx=0.1, ly=-0.3)

    # ── Cotas ────────────────────────────────────────────────
    # L (separación entre patas)
    cota(ax, 0, L, -1.0, '$L$ = ?', offset=0.12)
    # hp
    cota_v(ax, -1.5, 0, hp, '$h_p = 4{,}0$ m', offset=0.12)
    # ht
    cota_v(ax, -1.5, hp, hp + ht, '$h_t = 2{,}0$ m', offset=0.12)
    # de
    cota(ax, x0_tank + e, x0_tank + e + de,
         y0_tank + ht + 0.3, '$d_e = 3{,}0$ m', offset=0.1)
    # espesor pared
    cota(ax, x0_tank, x0_tank + e,
         y0_tank + ht + 0.7, '$e$', offset=0.1)
    # sección pata
    cota(ax, -sp / 2, sp / 2, hp / 2,
         '$s_p$', offset=0.1)

    # ── Pivote de volcamiento ─────────────────────────────────
    ax.plot(L, y0_pata, 'v', color='black', ms=10, zorder=5)
    ax.text(L + 0.15, -0.3, 'Pivote\nvolteo',
            fontsize=8, color='black')

    # ── Etiquetas ────────────────────────────────────────────
    for xp, lbl in [(0, 'Pata 1'), (L, 'Pata 2')]:
        ax.text(xp, hp / 2, lbl, ha='center', va='center',
                fontsize=7, color='white', fontweight='bold', rotation=90)

    ax.set_title('Ejercicio 2 — Tanque elevado sobre cuatro patas\n'
                 '(vista de elevación, sección transversal)',
                 fontsize=11, pad=12)
    plt.tight_layout()
    plt.savefig('img/tp3_ej2.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('tp3_ej2.png generado')


# ── Main ──────────────────────────────────────────────────────
figura_muro()
figura_tanque()