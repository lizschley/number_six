# defining a function return the current time

def print_line():
    genus = 'Lindera'
    species = 'benzoin'
    # plant_part = 'leaves_and_acorns'
    # plant_part = 'leaves'
    plant_part = 'bark'
    # plant_part = 'flowers'
    ext = 'jpg'
    # date = '2024-4-20'
    # activity = 'SFest'
    # photographer = 'Zhang'
    # desc = 'Caricature2'
    # desc = 'GreenLadies2'
    # return f'{date}.{activity}.{photographer}.{desc}'
    return f'{genus}.{species}.{plant_part}.{ext}'


if __name__ == '__main__':
    print(print_line())
