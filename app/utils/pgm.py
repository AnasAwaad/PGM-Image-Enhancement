def read_pgm(filename):
    """Reads both ASCII PGM (P2) and Binary PGM (P5) files safely."""
    with open(filename, "rb") as f:
        data = f.read()

    cleaned_data = bytearray()
    i = 0
    while i < len(data):
        if data[i : i + 1] == b"#":
            while i < len(data) and data[i : i + 1] != b"\n":
                i += 1
            i += 1
        else:
            cleaned_data.append(data[i])
            i += 1

    tokens = cleaned_data.split()
    if not tokens:
        raise ValueError("The provided file is empty.")

    magic = tokens[0].decode("latin-1", errors="ignore")
    if magic not in ("P2", "P5"):
        raise ValueError(
            f"Unsupported PGM format: {magic}. Only P2 and P5 are supported."
        )

    width = int(tokens[1].decode("latin-1"))
    height = int(tokens[2].decode("latin-1"))
    max_val = int(tokens[3].decode("latin-1"))

    pixels = []

    if magic == "P2":
        pixel_data = tokens[4:]
        if len(pixel_data) < width * height:
            raise ValueError("Incomplete pixel data in ASCII PGM.")

        idx = 0
        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(int(pixel_data[idx].decode("latin-1")))
                idx += 1
            pixels.append(row)

    elif magic == "P5":
        raw_pixels = data[-width * height :]
        if len(raw_pixels) < width * height:
            raise ValueError("Incomplete pixel data in Binary PGM.")

        idx = 0
        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(raw_pixels[idx])
                idx += 1
            pixels.append(row)

    return pixels, width, height, max_val


def write_pgm(filename, pixels, width, height, max_val=255):
    """Writes a 2D list of integer pixels into an ASCII PGM file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("P2\n")
        f.write(f"{width} {height}\n")
        f.write(f"{max_val}\n")
        for row in pixels:
            line = " ".join(str(min(max(0, int(round(p))), max_val)) for p in row)
            f.write(line + "\n")
