import matplotlib.pyplot as plt
from matplotlib import rcParams
from io import BytesIO
from PIL import Image

def generate_tight_symbol(fontsize=48, font='Nimbus Sans Narrow', symbol=''):

    if font:
        rcParams['font.family'] = font  # Set the font explicitly

    # Create the figure
    fig, ax = plt.subplots(figsize=(1, 1))
    fig.patch.set_alpha(0)

    # Use `text` instead of math text
    ax.text(
        0.5, 0.5, symbol, fontsize=fontsize, 
        ha='center', va='center', color='white', 
        transform=ax.transAxes
    )

    ax.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    buf = BytesIO()
    plt.savefig(buf, format='png', transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    buf.seek(0)
    image = Image.open(buf)
    bbox = image.getbbox()
    return image.crop(bbox)

