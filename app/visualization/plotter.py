import matplotlib.pyplot as plt


def plot_bar(columns, results):
    x = [row[0] for row in results]
    y = [row[1] for row in results]

    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set_xlabel(columns[0])
    ax.set_ylabel(columns[1])
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=45)

    return fig


def plot_line(columns, results):
    x = [row[0] for row in results]
    y = [row[1] for row in results]

    fig, ax = plt.subplots()
    ax.plot(x, y, marker="o")
    ax.set_xlabel(columns[0])
    ax.set_ylabel(columns[1])
    ax.tick_params(axis='x', rotation=45)

    return fig


def plot_scatter(columns, results):
    x = [row[0] for row in results]
    y = [row[1] for row in results]

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_xlabel(columns[0])
    ax.set_ylabel(columns[1])

    return fig