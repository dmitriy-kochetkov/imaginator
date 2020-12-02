import json


def generate_config(x0=275, y0=90, width=9, height=24, step=60, window_w=50, window_h=50):
    matrix_list = []

    for i in range(height):
        row = []
        for j in range(width):
            coords = {'x0': x0 + step * j,
                      'y0': y0 + step * i,
                      'x1': x0 + window_w + step * j,
                      'y1': y0 + window_h + step * i}
            row.append(coords)
        matrix_list.append(row)

    return matrix_list


def save_config(matrix, name='config.txt'):
    try:
        json_str = json.dumps(matrix, sort_keys=True, indent=4)
    except Exception as e:
        print('Matrix converting failed\n', e)
        return False

    try:
        conf = open(name, 'w')
        conf.write(json_str)
        conf.close()
    except Exception as e:
        print('Config saving failed\n', e)
        return False

    return True
