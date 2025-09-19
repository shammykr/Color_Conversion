import math

def rgb_to_hsi(r, g, b):
    """
    Converts RGB to HSI.
    RGB: [0, 255]
    Returns H in [0, 360], S in [0, 1], I in [0, 1]
    """
    # Normalize RGB
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0

    # Intensity
    i = (r_norm + g_norm + b_norm) / 3.0

    # Saturation
    min_rgb = min(r_norm, g_norm, b_norm)
    s = 0 if i == 0 else 1 - min_rgb / i

    # Hue
    if s == 0:
        h = 0.0
    else:
        numerator = 0.5 * ((r_norm - g_norm) + (r_norm - b_norm))
        denominator = math.sqrt((r_norm - g_norm)**2 + (r_norm - b_norm)*(g_norm - b_norm))
        # Clamp to avoid floating-point errors
        denominator = max(1e-10, denominator)
        theta = math.acos(max(-1, min(1, numerator / denominator)))
        if b_norm <= g_norm:
            h = math.degrees(theta)
        else:
            h = 360 - math.degrees(theta)

    return h, s, i

def hsi_to_rgb(h, s, i):
    """
    Converts HSI to RGB.
    H: [0, 360], S: [0, 1], I: [0, 1]
    Returns RGB: [0, 255]
    """
    if s == 0:
        # Grayscale
        r = g = b = round(i * 255)
        return r, g, b

    h = h % 360  # Ensure H in [0, 360]
    h_rad = math.radians(h)

    if 0 <= h < 120:
        # Sector 0°–120°: R-G-B
        b_norm = i * (1 - s)
        r_norm = i * (1 + s * math.cos(h_rad) / math.cos(math.radians(60) - h_rad))
        g_norm = 3 * i - (r_norm + b_norm)
    elif 120 <= h < 240:
        # Sector 120°–240°: G-B-R
        h_rad = math.radians(h - 120)
        r_norm = i * (1 - s)
        g_norm = i * (1 + s * math.cos(h_rad) / math.cos(math.radians(60) - h_rad))
        b_norm = 3 * i - (r_norm + g_norm)
    else:
        # Sector 240°–360°: B-R-G
        h_rad = math.radians(h - 240)
        g_norm = i * (1 - s)
        b_norm = i * (1 + s * math.cos(h_rad) / math.cos(math.radians(60) - h_rad))
        r_norm = 3 * i - (g_norm + b_norm)

    # Clamp and convert to [0,255]
    r = round(255 * max(0, min(r_norm, 1)))
    g = round(255 * max(0, min(g_norm, 1)))
    b = round(255 * max(0, min(b_norm, 1)))

    return r, g, b

if __name__ == "__main__":
    examples = [
        ("Red", (255, 0, 0)),
        ("Cyan", (0, 255, 255)),
        ("Mid-Gray", (128, 128, 128)),
        ("Complex", (150, 75, 200)),
    ]

    for name, rgb_color in examples:
        print(f"--- {name} ---")
        print(f"Original RGB: {rgb_color}")
        h, s, i = rgb_to_hsi(*rgb_color)
        print(f"Converted to HSI: H={h:.2f}°, S={s:.2f}, I={i:.2f}")
        r, g, b = hsi_to_rgb(h, s, i)
        print(f"Converted back to RGB: ({r}, {g}, {b})\n")

