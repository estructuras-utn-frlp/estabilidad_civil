if False:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    from mpl_toolkits.mplot3d import Axes3D
    import os

    os.makedirs('tp4/img', exist_ok=True)

    A = np.array([0,  0, 0])
    B = np.array([0,  0, 6])
    D = np.array([-2, 3, 0])
    E = np.array([-3, -3, 0])
    C = np.array([0,  0, 4])
    P_vec = np.array([7.9, -7.9, 4.1])
    escala = 0.25

    puntos = {'A': A, 'B': B, 'D': D, 'E': E}
    colores = {'A': 'black', 'B': 'black', 'D': 'steelblue', 'E': 'firebrick'}
    offsets = {
        'A': (-0.3, -0.3, -0.4),
        'B': (-0.3, -0.3,  0.3),
        'D': (-0.3,  0.2,  0.1),
        'E': (-0.3, -0.4,  0.1),
    }
    coords = {
        'A': '(0,0,0)', 'B': '(0,0,6)',
        'D': '(-2,3,0)', 'E': '(-3,-3,0)',
    }


    def draw_scene(ax, elev, azim, title, legend=False, fs_label=8):
        xx, yy = np.meshgrid([-4, 4], [-4, 4])
        ax.plot_surface(xx, yy, np.zeros_like(xx),
                        alpha=0.06, color='gray')

        ax.plot([A[0], B[0]], [A[1], B[1]], [A[2], B[2]],
                'k-', lw=2.5, label='Puntal AB')
        ax.plot([B[0], D[0]], [B[1], D[1]], [B[2], D[2]],
                color='steelblue', lw=2, label='Cable BD')
        ax.plot([B[0], E[0]], [B[1], E[1]], [B[2], E[2]],
                color='firebrick', lw=2, label='Cable BE')

        ax.scatter(*C, color='darkorange', s=30, marker='s', zorder=5)
        ax.text(C[0]+0.15, C[1]+0.1, C[2]+0.1,
                r'$C$', fontsize=fs_label, color='darkorange')
        ax.plot([B[0], C[0]], [B[1], C[1]], [B[2], C[2]],
                color='darkorange', lw=1, ls='--', alpha=0.6)

        for nombre, pt in puntos.items():
            ax.scatter(*pt, color=colores[nombre], s=30, zorder=5)
            ox, oy, oz = offsets[nombre]
            ax.text(pt[0]+ox, pt[1]+oy, pt[2]+oz,
                    f'${nombre}$', fontsize=fs_label+1,
                    fontweight='bold', color=colores[nombre])
            ax.text(pt[0]+ox, pt[1]+oy, pt[2]+oz-0.6,
                    coords[nombre], fontsize=fs_label-1, color='gray')

        for pt, col in [(D, 'steelblue'), (E, 'firebrick')]:
            ax.scatter(*pt, color=col, s=60, marker='s', zorder=5)
        ax.scatter(*A, color='black', s=100, marker='^', zorder=6)

        for pt, col in [(D, 'steelblue'), (E, 'firebrick'), (B, 'gray')]:
            ax.plot([pt[0], pt[0]], [pt[1], pt[1]], [0, pt[2]],
                    color=col, lw=0.7, ls=':', alpha=0.4)

        ax.quiver(B[0], B[1], B[2],
                  P_vec[0]*escala, P_vec[1]*escala, P_vec[2]*escala,
                  color='#8b008b', lw=2, arrow_length_ratio=0.18)
        ax.text(B[0]+P_vec[0]*escala+0.1,
                B[1]+P_vec[1]*escala-0.2,
                B[2]+P_vec[2]*escala+0.15,
                r'$\vec{P}$', fontsize=fs_label+1,
                color='#8b008b', fontweight='bold')

        L = 3.8
        for d, lbl in [((L, 0, 0), '$x$'), ((0, L, 0), '$y$'), ((0, 0, L), '$z$')]:
            ax.quiver(0, 0, 0, *d, color='gray', lw=0.8,
                      arrow_length_ratio=0.07)
            ax.text(d[0]+0.1, d[1]+0.1, d[2]+0.15,
                    lbl, fontsize=fs_label, color='gray')

        ax.set_xlim(-3.5, 3.5)
        ax.set_ylim(-3.5, 3.5)
        ax.set_zlim(0, 6.5)

        # Eliminar tick labels para limpiar
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])
        ax.set_xlabel('x', labelpad=2, fontsize=fs_label)
        ax.set_ylabel('y', labelpad=2, fontsize=fs_label)
        ax.set_zlabel('z', labelpad=2, fontsize=fs_label)
        ax.set_title(title, fontsize=fs_label+1, pad=4)
        ax.view_init(elev=elev, azim=azim)

        # Reducir espacio interno del subplot 3D
        ax.set_box_aspect([1, 1, 1.2])

        if legend:
            ax.legend(loc='upper left', fontsize=7, framealpha=0.7)


    # ── Layout ────────────────────────────────────────────────────
    fig = plt.figure(figsize=(13, 9))
    fig.patch.set_facecolor('white')

    gs = GridSpec(2, 2, figure=fig,
                  height_ratios=[1.5, 1],
                  hspace=0.05,
                  wspace=0.0,
                  left=0.02, right=0.98,
                  top=0.93,  bottom=0.02)

    ax1 = fig.add_subplot(gs[0, :], projection='3d')
    draw_scene(ax1, elev=15, azim=-35,
               title='Vista perspectiva', legend=False, fs_label=9)

    ax2 = fig.add_subplot(gs[1, 0], projection='3d')
    draw_scene(ax2, elev=90, azim=-90,
               title='Vista superior — plano XY', fs_label=8)

    ax3 = fig.add_subplot(gs[1, 1], projection='3d')
    draw_scene(ax3, elev=0, azim=0,
               title='Vista lateral — plano XZ', fs_label=8)

    plt.suptitle('Ejercicio 1 — Mástil con dos cables y puntal',
                 fontsize=12, y=0.97)

    plt.savefig('tp4/img/tp4_ej1.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print('tp4_ej1.png generado')

if False:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import os

    os.makedirs('tp4/img', exist_ok=True)

    # ── Datos geométricos ─────────────────────────────────────────
    a = 5.0   # ancho cartel
    h = 3.0   # alto cartel
    e = 0.30  # espesor cartel
    d = h * np.tan(np.radians(30)) * np.cos(np.radians(45))  # 1.225 m

    # Esquinas del cartel (cara frontal y=0, cara posterior y=e)
    A = np.array([0,   0, 0])
    B = np.array([a,   0, 0])
    C = np.array([0,   0, h])
    D = np.array([a,   0, h])

    # Anclajes en el terreno
    E = np.array([0-d,   -d, 0])
    F = np.array([0-d,   +d, 0])
    G = np.array([a+d,   -d, 0])
    H = np.array([a+d,   +d, 0])

    # ── Función principal de dibujo ───────────────────────────────


    def draw_scene(ax, elev, azim, title, legend=False, fs=8):

        # Plano terreno
        xx, yy = np.meshgrid([-2.5, 8], [-2.5, 2.5])
        ax.plot_surface(xx, yy, np.zeros_like(xx),
                        alpha=0.06, color='saddlebrown')

        # ── Cartel (prisma) ───────────────────────────────────────
        # Vértices de la cara frontal (y=0) y posterior (y=e)
        vf = np.array([[0, 0, 0], [a, 0, 0], [a, 0, h], [0, 0, h]])
        vp = np.array([[0, e, 0], [a, e, 0], [a, e, h], [0, e, h]])

        caras = [
            [vf[0], vf[1], vf[2], vf[3]],          # frontal
            [vp[0], vp[1], vp[2], vp[3]],          # posterior
            [vf[0], vp[0], vp[3], vf[3]],          # izquierda
            [vf[1], vp[1], vp[2], vf[2]],          # derecha
            [vf[0], vp[0], vp[1], vf[1]],          # inferior
            [vf[3], vp[3], vp[2], vf[2]],          # superior
        ]
        colores_cara = ['#d0d8e8', '#b0b8c8', '#c0c8d8',
                        '#c0c8d8', '#a8b0c0', '#a8b0c0']
        poly = Poly3DCollection(caras, alpha=0.35,
                                facecolor=colores_cara,
                                edgecolor='#445566', lw=0.8)
        ax.add_collection3d(poly)

        # ── Columnas ──────────────────────────────────────────────
        for xc in [0, a]:
            ax.bar3d(xc - 0.15, -0.15, -0.5,
                     0.30, 0.30, 0.5,
                     color='#888', alpha=0.8, shade=True)

        # ── Cables ────────────────────────────────────────────────
        cable_pairs = [(C, E), (C, F), (D, G), (D, H)]
        cable_labels = ['$T_E$', '$T_F$', '$T_G$', '$T_H$']
        cable_colors = ['steelblue', 'steelblue', 'firebrick', 'firebrick']

        for (p1, p2), lbl, col in zip(cable_pairs, cable_labels, cable_colors):
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
                    color=col, lw=1.8, ls='-', label=lbl if legend else '')
            mid = (p1 + p2) / 2
            ax.text(mid[0], mid[1], mid[2]+0.1, lbl,
                    fontsize=fs, color=col, fontweight='bold')

        # ── Anclajes ──────────────────────────────────────────────
        for pt, lbl, col in [(E, '$E$', 'steelblue'), (F, '$F$', 'steelblue'),
                             (G, '$G$', 'firebrick'), (H, '$H$', 'firebrick')]:
            ax.scatter(*pt, color=col, s=60, marker='s', zorder=5)
            ax.text(pt[0]+0.1, pt[1]+0.1, pt[2]+0.15,
                    lbl, fontsize=fs, color=col, fontweight='bold')

        # ── Puntos esquina del cartel ─────────────────────────────
        for pt, lbl, ox, oy, oz in [
            (A, '$A$', -0.3, -0.2, -0.4),
            (B, '$B$', 0.1, -0.2, -0.4),
            (C, '$C$', -0.4, -0.2, 0.2),
            (D, '$D$', 0.1, -0.2, 0.2),
        ]:
            ax.scatter(*pt, color='black', s=25, zorder=6)
            ax.text(pt[0]+ox, pt[1]+oy, pt[2]+oz,
                    lbl, fontsize=fs+1, fontweight='bold', color='black')

        # ── Fuerza de viento (cara frontal) ───────────────────────
        n_flechas = 6
        for i in range(3):
            for j in range(2):
                zw = h * (i + 0.5) / 3
                yw = a * (j + 0.5) / 2 - 0.3
                ax.quiver(yw - 1.0, 0, zw,
                          0, 1.0, 0,
                          color='#8b008b', lw=1.5,
                          arrow_length_ratio=0.2, length=0.8)
        ax.text(-1.6, 0, h/2,
                r'$p_w$', fontsize=fs+1, color='#8b008b', fontweight='bold')

        # ── Peso W (flecha hacia abajo desde centroide) ───────────
        ax.quiver(a/2, e/2, h,
                  0, 0, -0.8,
                  color='darkgreen', lw=2,
                  arrow_length_ratio=0.25)
        ax.text(a/2+0.1, e/2, h+0.1,
                r'$W$', fontsize=fs+1, color='darkgreen', fontweight='bold')

        # ── Cotas ─────────────────────────────────────────────────
        # Ancho a
        ax.plot([0, a], [-0.8, -0.8], [0, 0],
                color='dimgray', lw=0.8, ls='-')
        ax.text(a/2, -1.1, 0,
                r'$a = 5{,}0$ m', fontsize=fs-1,
                color='dimgray', ha='center')

        # Alto h
        ax.plot([-0.8, -0.8], [0, 0], [0, h],
                color='dimgray', lw=0.8, ls='-')
        ax.text(-1.2, 0, h/2,
                r'$h = 3{,}0$ m', fontsize=fs-1,
                color='dimgray', ha='center', rotation=90)

        # ── Ejes ──────────────────────────────────────────────────
        L = 2.0
        ax.quiver(0, 0, 0, L, 0, 0, color='gray', lw=0.8,
                  arrow_length_ratio=0.1)
        ax.quiver(0, 0, 0, 0, L, 0, color='gray', lw=0.8,
                  arrow_length_ratio=0.1)
        ax.quiver(0, 0, 0, 0, 0, L, color='gray', lw=0.8,
                  arrow_length_ratio=0.1)
        ax.text(L+0.1, 0, 0,    '$x$', fontsize=fs, color='gray')
        ax.text(0, L+0.1, 0,    '$y$', fontsize=fs, color='gray')
        ax.text(0, 0,    L+0.1, '$z$', fontsize=fs, color='gray')

        # ── Formato ───────────────────────────────────────────────
        ax.set_xlim(-2, 7)
        ax.set_ylim(-2, 2)
        ax.set_zlim(-0.6, 4)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])
        ax.set_xlabel('x', labelpad=2, fontsize=fs)
        ax.set_ylabel('y', labelpad=2, fontsize=fs)
        ax.set_zlabel('z', labelpad=2, fontsize=fs)
        ax.set_title(title, fontsize=fs+1, pad=6)
        ax.set_box_aspect([1.8, 0.8, 1.0])
        ax.view_init(elev=elev, azim=azim)


    # ── Layout ────────────────────────────────────────────────────
    fig = plt.figure(figsize=(14, 9))
    fig.patch.set_facecolor('white')

    gs = GridSpec(2, 2, figure=fig,
                  height_ratios=[1.5, 1],
                  hspace=0.05, wspace=0.0,
                  left=0.02, right=0.98,
                  top=0.93,  bottom=0.02)

    ax1 = fig.add_subplot(gs[0, :], projection='3d')
    draw_scene(ax1, elev=18, azim=-50,
               title='Vista perspectiva', legend=True, fs=9)

    ax2 = fig.add_subplot(gs[1, 0], projection='3d')
    draw_scene(ax2, elev=90, azim=-90,
               title='Vista superior — plano XY', fs=8)

    ax3 = fig.add_subplot(gs[1, 1], projection='3d')
    draw_scene(ax3, elev=0, azim=-90,
               title='Vista frontal — plano XZ', fs=8)

    plt.suptitle('Ejercicio 3 — Cartel prismático con columnas y cables',
                 fontsize=12, y=0.97)

    plt.savefig('tp4/img/tp4_ej3.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print('tp4_ej3.png generado')


if False:
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import os

    os.makedirs('tp4/img', exist_ok=True)

    # ── Datos ─────────────────────────────────────────────────────
    a = 3.0   # ancho
    b = 2.0   # largo
    P_mag = 8.0
    Q_mag = 4.0

    # Vértices de la placa (z = 1.0 para visualizar las barras debajo)
    z_placa = 1.2
    A = np.array([0,   0,   z_placa])
    B = np.array([a,   0,   z_placa])
    C = np.array([0,   b,   z_placa])
    D = np.array([a,   b,   z_placa])

    # Puntos de apoyo en el suelo (z = 0)
    E = np.array([0,   0,   0])
    F = np.array([a,   0,   0])
    G = np.array([0,   b,   0])

    # Carga puntual H
    H = np.array([2.0, 1.5, z_placa])

    # ── Figura ────────────────────────────────────────────────────
    fig = plt.figure(figsize=(9, 8))
    ax = fig.add_subplot(111, projection='3d')

    # ── Plano de referencia ───────────────────────────────────────
    xx, yy = np.meshgrid([-0.5, 4], [-0.5, 3])
    ax.plot_surface(xx, yy, np.zeros_like(xx),
                    alpha=0.05, color='gray')

    # ── Placa ─────────────────────────────────────────────────────
    cara = [[A, B, D, C]]
    poly = Poly3DCollection(cara, alpha=0.30,
                            facecolor='#aabbdd',
                            edgecolor='#334466', lw=1.5)
    ax.add_collection3d(poly)

    # Borde de la placa
    for p1, p2 in [(A, B), (B, D), (D, C), (C, A)]:
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
                'k-', lw=1.5)

    # ── Barras verticales E, F, G ─────────────────────────────────
    barras = [
        (E, np.array([0,   0,   z_placa]), 'steelblue', '$P_E$'),
        (F, np.array([a,   0,   z_placa]), 'firebrick', '$P_F$'),
        (G, np.array([0,   b,   z_placa]), 'seagreen',  '$P_G$'),
    ]
    for base, top, col, lbl in barras:
        ax.plot([base[0], top[0]], [base[1], top[1]], [base[2], top[2]],
                color=col, lw=3)
        # Flecha hacia arriba (reacción de la barra)
        ax.quiver(top[0], top[1], top[2],
                  0, 0, 0.4,
                  color=col, lw=2, arrow_length_ratio=0.3)
        ax.text(top[0]+0.08, top[1]+0.08, top[2]+0.55,
                lbl, fontsize=11, color=col, fontweight='bold')
        # Anclaje en el suelo
        ax.scatter(*base, color=col, s=80, marker='s', zorder=5)

    # ── Etiquetas vértices de la placa ───────────────────────────
    for pt, lbl, ox, oy in [
        (A, '$A$', -0.25, -0.20),
        (B, '$B$',  0.10, -0.20),
        (C, '$C$', -0.30,  0.10),
        (D, '$D$',  0.10,  0.10),
    ]:
        ax.scatter(*pt, color='black', s=20, zorder=6)
        ax.text(pt[0]+ox, pt[1]+oy, pt[2]+0.05,
                lbl, fontsize=11, fontweight='bold', color='black')

    # ── Etiquetas apoyos ──────────────────────────────────────────
    for pt, lbl, col in [(E, '$E$', 'steelblue'),
                         (F, '$F$', 'firebrick'),
                         (G, '$G$', 'seagreen')]:
        ax.text(pt[0]+0.08, pt[1]+0.08, pt[2]-0.25,
                lbl, fontsize=11, fontweight='bold', color=col)

    # ── Peso P (centroide de la placa) ────────────────────────────
    centroide = np.array([a/2, b/2, z_placa])
    ax.quiver(centroide[0], centroide[1], centroide[2]+0.6,
              0, 0, -0.55,
              color='darkgreen', lw=2.5, arrow_length_ratio=0.25)
    ax.text(centroide[0]+0.1, centroide[1], centroide[2]+0.75,
            r'$P = 8$ kN', fontsize=10, color='darkgreen', fontweight='bold')

    # ── Carga puntual Q en H ──────────────────────────────────────
    ax.quiver(H[0], H[1], H[2]+0.6,
              0, 0, -0.55,
              color='#8b008b', lw=2.5, arrow_length_ratio=0.25)
    ax.scatter(*H, color='#8b008b', s=40, zorder=6)
    ax.text(H[0]+0.1, H[1], H[2]+0.75,
            r'$Q = 4$ kN', fontsize=10, color='#8b008b', fontweight='bold')
    ax.text(H[0]+0.1, H[1]-0.2, H[2]-0.15,
            r'$H(2{,}0;\,1{,}5)$', fontsize=8, color='#8b008b')

    # ── Cotas ─────────────────────────────────────────────────────
    # Cota a (ancho)
    ax.plot([0, a], [-0.5, -0.5], [0, 0],
            color='dimgray', lw=0.8)
    ax.annotate('', xy=(a, 0), xytext=(0, 0),
                xycoords='data', textcoords='data')
    ax.text(a/2, -0.75, 0,
            r'$a = 3{,}0$ m', fontsize=8,
            color='dimgray', ha='center')

    # Cota b (largo)
    ax.plot([-0.5, -0.5], [0, b], [0, 0],
            color='dimgray', lw=0.8)
    ax.text(-0.9, b/2, 0,
            r'$b = 2{,}0$ m', fontsize=8,
            color='dimgray', ha='center', rotation=90)

    # ── Ejes ──────────────────────────────────────────────────────
    L = 1.5
    ax.quiver(0, 0, 0, L, 0, 0, color='gray', lw=0.8, arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, L, 0, color='gray', lw=0.8, arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 0, L, color='gray', lw=0.8, arrow_length_ratio=0.1)
    ax.text(L+0.1, 0,    0,    '$x$', fontsize=9, color='gray')
    ax.text(0,     L+0.1, 0,    '$y$', fontsize=9, color='gray')
    ax.text(0,     0,    L+0.1, '$z$', fontsize=9, color='gray')

    # ── Formato ───────────────────────────────────────────────────
    ax.set_xlim(-0.8, 4.0)
    ax.set_ylim(-0.8, 3.0)
    ax.set_zlim(0, 2.2)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.set_xlabel('x', labelpad=4, fontsize=9)
    ax.set_ylabel('y', labelpad=4, fontsize=9)
    ax.set_zlabel('z', labelpad=4, fontsize=9)
    ax.set_box_aspect([1.5, 1.0, 0.8])
    ax.set_title('Ejercicio 3 — Placa rectangular con tres barras',
                 fontsize=11, pad=12)
    ax.view_init(elev=22, azim=-55)

    plt.tight_layout()
    plt.savefig('tp4/img/tp4_ej4.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print('tp4_ej3_placa.png generado')
