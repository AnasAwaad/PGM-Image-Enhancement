import cmath
import math

from app.utils.pgm import read_pgm, write_pgm


def next_power_of_two(n):
    return 1 << (n - 1).bit_length() if n > 0 else 1


def pad_image_to_power_of_two(pixels, width, height):
    new_w = next_power_of_two(width)
    new_h = next_power_of_two(height)

    padded = [[0.0] * new_w for _ in range(new_h)]
    for y in range(height):
        for x in range(width):
            padded[y][x] = pixels[y][x]

    return padded, new_w, new_h


def fft_1d(x):
    n = len(x)
    if n <= 1:
        return x
    even = fft_1d(x[0::2])
    odd = fft_1d(x[1::2])
    t = [cmath.exp(-2j * cmath.pi * k / n) * odd[k] for k in range(n // 2)]
    return [even[k] + t[k] for k in range(n // 2)] + [
        even[k] - t[k] for k in range(n // 2)
    ]


def ifft_1d(x):
    n = len(x)
    x_conj = [c.conjugate() for c in x]
    x_fft = fft_1d(x_conj)
    return [c.conjugate() / n for c in x_fft]


def fft_2d(matrix):
    height = len(matrix)
    width = len(matrix[0])

    row_fft = [fft_1d(row) for row in matrix]

    col_fft = []
    for x in range(width):
        col = [row_fft[y][x] for y in range(height)]
        col_transformed = fft_1d(col)
        col_fft.append(col_transformed)

    final_fft = [[col_fft[x][y] for x in range(width)] for y in range(height)]
    return final_fft


def ifft_2d(matrix):
    height = len(matrix)
    width = len(matrix[0])

    row_ifft = [ifft_1d(row) for row in matrix]

    col_ifft = []
    for x in range(width):
        col = [row_ifft[y][x] for y in range(height)]
        col_transformed = ifft_1d(col)
        col_ifft.append(col_transformed)

    final_ifft = [[col_ifft[x][y] for x in range(width)] for y in range(height)]
    return final_ifft


def apply_hfe_filter(fft_matrix, d0=45, a=1.0, b=0.8, n=2):
    height = len(fft_matrix)
    width = len(fft_matrix[0])
    y_center = height / 2.0
    x_center = width / 2.0

    filtered = [[0j] * width for _ in range(height)]

    for u in range(height):
        for v in range(width):
            dist = math.sqrt((u - y_center) ** 2 + (v - x_center) ** 2)

            if dist == 0:
                h_hp = 0.0
            else:
                h_hp = 1.0 / (1.0 + (d0 / dist) ** (2 * n))

            h_hfe = a + b * h_hp
            filtered[u][v] = fft_matrix[u][v] * h_hfe

    return filtered


def enhance_pgm(input_filename, output_filename, d0=45, a=1.0, b=0.8):
    pixels, width, height, _max_val = read_pgm(input_filename)

    padded_img, pad_w, pad_h = pad_image_to_power_of_two(pixels, width, height)

    complex_input = []
    for y in range(pad_h):
        row = []
        for x in range(pad_w):
            val = padded_img[y][x] * ((-1) ** (x + y))
            row.append(complex(val, 0.0))
        complex_input.append(row)

    spectrum = fft_2d(complex_input)
    filtered_spectrum = apply_hfe_filter(spectrum, d0=d0, a=a, b=b, n=2)
    ifft_result = ifft_2d(filtered_spectrum)

    uncentered_spatial = [[0.0] * pad_w for _ in range(pad_h)]
    for y in range(pad_h):
        for x in range(pad_w):
            val = ifft_result[y][x].real * ((-1) ** (x + y))
            uncentered_spatial[y][x] = val

    cropped_spatial = [[0.0] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            cropped_spatial[y][x] = uncentered_spatial[y][x]

    final_pixels = []
    for row in cropped_spatial:
        clamped_row = []
        for p in row:
            val = int(round(p))
            val = max(0, min(255, val))
            clamped_row.append(val)
        final_pixels.append(clamped_row)

    write_pgm(output_filename, final_pixels, width, height, max_val=255)
