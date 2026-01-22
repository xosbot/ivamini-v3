def read_input():
    print("Enter command (end with empty line):")

    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    if not lines:
        raise ValueError("No input provided")

    first_line = lines[0].strip()

    if not (first_line.startswith("[") and first_line.endswith("]")):
        raise ValueError("MODE required. Example: [PLAN], [COMMAND]")

    mode = first_line[1:-1].upper()
    content = "\n".join(lines[1:]).strip()

    return mode, content
