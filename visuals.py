import matplotlib.pyplot as plt


def chart(data, chart_name):
    curve, sec_derivation, eq_point = data
    x1 = [curve[i][0] for i in range(len(curve))]
    y1 = [curve[i][1] for i in range(len(curve))]
    x2 = [sec_derivation[i][0] for i in range(len(sec_derivation))]
    y2 = [sec_derivation[i][1] for i in range(len(sec_derivation))]
    # vytvoří dvě křivky dle indexů jak jsou data v listu vycházejícího z finkce "x"
    plt.plot(x1, y1, label='Titration Curve', color='blue')
    plt.plot(x2, y2, color='green', label='Second Derivative')
    plt.scatter(eq_point, 0, color="red", zorder=5, s=100, marker="x")
    plt.grid(True, linestyle="--", linewidth=0.5)
    plt.title(f"{chart_name}")
    plt.xlabel("Volume")
    plt.ylabel("pH")
    # Přidá popisek do grafu s informací o bodu ekvivalence; indexově vybráno z listu vycházejícího z funkce "x"
    plt.annotate(f"Equivalence point by volume: {eq_point} ml",
                 xy=(eq_point, 0),
                 xytext=(0, - 15),
                 arrowprops=None,
                 fontsize=12, color="red")
    plt.legend()
    plt.show()


def titration_chart(data, chart_name):
    if not data:
        pass
    else:
        x, y = zip(*data)
        x = list(x)
        y = list(y)
        plt.plot(x, y, label='Titration Curve', color='blue')
        plt.grid(True, linestyle="--", linewidth=0.5)
        plt.title(f"{chart_name}")
        plt.legend()
        plt.show()
