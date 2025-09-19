import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import math

# --- RGB <-> HSI functions ---
def rgb_to_hsi(r, g, b):
    r_norm, g_norm, b_norm = r/255.0, g/255.0, b/255.0
    i = (r_norm + g_norm + b_norm)/3
    min_rgb = min(r_norm, g_norm, b_norm)
    s = 0 if i==0 else 1 - min_rgb/i
    if s == 0:
        h = 0.0
    else:
        numerator = 0.5*((r_norm - g_norm) + (r_norm - b_norm))
        denominator = max(1e-10, math.sqrt((r_norm - g_norm)**2 + (r_norm - b_norm)*(g_norm - b_norm)))
        theta = math.acos(max(-1, min(1, numerator/denominator)))
        h = math.degrees(theta) if b_norm <= g_norm else 360 - math.degrees(theta)
    return h, s, i

def hsi_to_rgb(h, s, i):
    if s == 0:
        r = g = b = round(i*255)
        return r, g, b
    h = h % 360
    h_rad = math.radians(h)
    if 0 <= h < 120:
        b_norm = i*(1-s)
        r_norm = i*(1 + s*math.cos(h_rad)/math.cos(math.radians(60) - h_rad))
        g_norm = 3*i - (r_norm + b_norm)
    elif 120 <= h < 240:
        h_rad = math.radians(h - 120)
        r_norm = i*(1-s)
        g_norm = i*(1 + s*math.cos(h_rad)/math.cos(math.radians(60) - h_rad))
        b_norm = 3*i - (r_norm + g_norm)
    else:
        h_rad = math.radians(h - 240)
        g_norm = i*(1-s)
        b_norm = i*(1 + s*math.cos(h_rad)/math.cos(math.radians(60) - h_rad))
        r_norm = 3*i - (g_norm + b_norm)
    r = round(255*max(0, min(r_norm,1)))
    g = round(255*max(0, min(g_norm,1)))
    b = round(255*max(0, min(b_norm,1)))
    return r, g, b

# --- Interactive Visualization ---
fig, ax = plt.subplots(figsize=(6,4))
plt.subplots_adjust(left=0.1, bottom=0.35)
rgb_patch = ax.imshow(np.zeros((100,100,3), dtype=np.uint8))
ax.set_axis_off()
ax.set_title("HSI → RGB Interactive Color")

# Slider axes
ax_h = plt.axes([0.1, 0.25, 0.8, 0.03])
ax_s = plt.axes([0.1, 0.18, 0.8, 0.03])
ax_i = plt.axes([0.1, 0.11, 0.8, 0.03])

slider_h = Slider(ax_h, 'Hue (°)', 0, 360, valinit=0)
slider_s = Slider(ax_s, 'Saturation', 0, 1, valinit=1)
slider_i = Slider(ax_i, 'Intensity', 0, 1, valinit=0.5)

def update(val):
    h = slider_h.val
    s = slider_s.val
    i = slider_i.val
    r, g, b = hsi_to_rgb(h, s, i)
    color = np.zeros((100,100,3), dtype=np.uint8)
    color[:,:,:] = [r,g,b]
    rgb_patch.set_data(color)
    fig.canvas.draw_idle()

slider_h.on_changed(update)
slider_s.on_changed(update)
slider_i.on_changed(update)

# Initialize display
update(None)
plt.show()