def get_file_content(filename: str) -> dict[str, str]:
    """Returns content from a txt file in the form of a dict."""
    content = dict()
    with open(f'{filename}') as f:
        while (line:=f.readline()) != '':
            line = line.removesuffix('\n').split(';', 1)
            content[line[0]] = line[1]
    return content

def write_over_file(filename: str, field: str, new_info: str) -> None:
    """Overwrites information of a specific field in a file."""
    f = open(filename, 'r')
    new_file_content = ''
    for line in f:
        line = line.strip()
        if (field_in_line:=line.split(';', 1)[0]) == field:
            new_file_content += f'{field_in_line};{new_info}\n'
        else:
            new_file_content += line + '\n'
    f.close()
    f = open(filename, 'w')
    f.write(new_file_content)
    f.close()

def get_content_by_field(filename: str, field: str) -> str:
    with open(filename) as f:
        line = f.readline()
        while line!='' and line.split(';', 1)[0]!=field:
            line = f.readline()
        if line != '':
            return line.split(';', 1)[1].strip()
        else:
            raise Exception('La línea buscada no existe en este archivo.')
            