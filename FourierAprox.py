import numpy as np
from manim import *

class FourierAprox(Scene):
    def construct(self):
        self.camera.background_color = "#111317"
        ax = Axes(
            x_range=[-2, 6, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=7,
            y_length=4,
            axis_config={"color": WHITE}
        )

        text1 = Tex("Aproximación de una Serie de Fourier", font_size=50).next_to(ax, UP, buff=1.5)
        n = 0
        nTex = Tex(fr"n = {n}", font_size=40).next_to(text1, DOWN, buff=1.2)

        def fourier_coeficientes(f, t, T, N):
            a0 = (2/T) * np.trapz(f, t)
            an = [(2/T) * np.trapz(f * np.cos(2 * np.pi * n * t / T), t) for n in range(1, N+1)]
            bn = [(2/T) * np.trapz(f * np.sin(2 * np.pi * n * t / T), t) for n in range(1, N+1)]
            return a0, np.array(an), np.array(bn)

        def fourier_series(t, a0, an, bn, T, N):
            return a0 / 2 + sum(an[n-1] * np.cos(2 * np.pi * n * t / T) + bn[n-1] * np.sin(2 * np.pi * n * t / T) for n in range(1, N+1))

        T2 = 3
        t_periodo = np.linspace(0, T2, 250)
        f_period = np.piecewise(t_periodo, [t_periodo < 1, t_periodo >= 1], [lambda t: t, lambda t: -t + 2])
        N = 10
        a0, an, bn = fourier_coeficientes(f_period, t_periodo, T2, N)

        # Texto para la función principal
        func_text = MathTex(
            r"f(t) = \begin{cases} t & \text{si } 0 \leq t < 1 \\ -t + 2 & \text{si } 1 \leq t < 3 \end{cases}",
            font_size=30
        ).next_to(ax, DOWN, buff=1.0)

        # Texto inicial de la serie de Fourier
        fourier_series_text = (
            f"f(t) \\approx {a0/2:.3f} + "
            + r"\sum_{n=1}^{" + str(N) + r"} \left( "
            + f"{an[0]:.3f} \\cos\\left(\\frac{{2\\pi n t}}{{{T2}}}\\right) + {bn[0]:.3f} \\sin\\left(\\frac{{2\\pi n t}}{{{T2}}}\\right) \\right)"
        )
        fourier_text = MathTex(fourier_series_text, font_size=30).next_to(func_text, DOWN, buff=0.5)

        t_ext = np.linspace(-2*T2, 2*T2, 500)
        t_mod = t_ext % T2
        f_ext = np.interp(t_mod, t_periodo, f_period)
        fourierFunc = lambda x: fourier_series(x, a0, an, bn, T2, N)
        
        graph = ax.plot(lambda x: fourierFunc(x), color=BLUE)
        original_graph = ax.plot(lambda x: np.interp(x % T2, t_periodo, f_period), color=RED)

        self.wait(1)
        self.play(Write(text1))
        self.play(Create(ax))
        self.play(Write(nTex))
        self.play(Create(original_graph))
        self.play(Create(graph))
        self.play(Write(func_text), Write(fourier_text))

        # Animación de la serie de Fourier
        for i in range(1, N+1):
            # Actualizar la serie de Fourier con los términos hasta n = i
            actualizar_fourier_series_text = (
                f"f(t) \\approx {a0/2:.3f} + "
                + r"\sum_{n=1}^{" + str(i) + r"} \left( "
                + f"{an[i-1]:.3f} \\cos\\left(\\frac{{2\\pi n t}}{{{T2}}}\\right) + {bn[i-1]:.3f} \\sin\\left(\\frac{{2\\pi n t}}{{{T2}}}\\right) \\right)"
            )
            actualizar_fourier_text = MathTex(actualizar_fourier_series_text, font_size=30).next_to(func_text, DOWN, buff=0.5)

            # Actualizar la gráfica de la serie de Fourier
            actualizar_fourierFunc = lambda x: fourier_series(x, a0, an[:i], bn[:i], T2, i)
            
            text2 = Tex("CruzGV", font_size=30).move_to(ORIGIN)

            self.play(
                ReplacementTransform(nTex, nTex := Tex(fr"n = {i}", font_size=40).next_to(text1, DOWN, buff=1.2)),
                ReplacementTransform(graph, graph := ax.plot(lambda x: actualizar_fourierFunc(x), color=BLUE)),
                ReplacementTransform(fourier_text, actualizar_fourier_text)
            )
            fourier_text = actualizar_fourier_text  # Actualizar la referencia al texto de Fourier
            self.wait(0.1)

        self.wait(2)
        
        self.play(ReplacementTransform(graph, text2))  
        self.play(FadeOut(text1, ax, nTex, original_graph, func_text, fourier_text))  # Ocultar otros elementos
        self.wait(2)