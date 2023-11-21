import matplotlib
from matplotlib_venn import venn2
import matplotlib.pyplot as plt
import io

def plot_venn(genes_a, genes_b):
    matplotlib.use('agg')
    stream = io.BytesIO()

    plt.figure(figsize=(10, 8), dpi=400)

    venn2([set(genes_a), set(genes_b)])
    plt.title("Significant Genes Venn Chart")

    plt.savefig(stream, format='png')
    stream.seek(0)
    plt.close()
    return stream.getvalue()
    