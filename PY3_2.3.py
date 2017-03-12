import json
import yaml
import csv


def get_menu(fname) :
    with open(fname ) as f:
        if fname == "dishes.yaml" : cook_book = yaml.load(f)
        else: cook_book = json.load(f)
    return cook_book

def get_shop_list_by_dishes(dishes, person_count, cook_book):
    shop_list = {}
    for dish in dishes:
        for ingridient in cook_book[dish]:
            new_shop_list_item = dict(ingridient)
            new_shop_list_item['quantity'] *= person_count
            if new_shop_list_item['ingridient_name'] not in shop_list:
                shop_list[new_shop_list_item['ingridient_name']] = new_shop_list_item
            else:
                shop_list[new_shop_list_item['ingridient_name']]['quantity'] += new_shop_list_item['quantity']
    return shop_list


def print_shop_list(shop_list):
    for shop_list_item in shop_list.values():
        print('{ingridient_name} {quantity} {measure}'.format(**shop_list_item))

def write_shop_list(shop_list, finput):
    if finput == "dishes.json" :
        with open("out.json", 'w', encoding="utf8") as f:
            json.dump(shop_list, f, ensure_ascii=False, indent=2)
    else:
        with open("out.yaml", 'w' , encoding="utf8") as f:
            yaml.dump(shop_list, f , allow_unicode=True, default_flow_style=False)



def create_shop_list(f):
    cook_book = get_menu(f)
    person_count = int(input('Введите количество человек: '))
    dishes = input('Введите блюда в расчете на одного человека (через запятую и пробел): ').lower().split(', ')
    shop_list = get_shop_list_by_dishes(dishes, person_count, cook_book)
    print_shop_list(shop_list)
    write_shop_list(shop_list, f)

def choose_format(lfd):       # выбор формата JSON или YAML
    ## соспоставление элементов списка lfd расширениям json и yaml
    for l in lfd:
        lst = l.split('.')
        if lst[1] == 'json' : js = l
        elif lst[1] == 'yaml' : ya =l

    print("Выберите формат JSON или YAML , введите J или Y")
    while True:
        frmt = input().upper()
        if frmt == 'J' or frmt == 'Y': break
    print("Расчет необходимых ингредиентов будет сохранен в файле out.{}".format("json" if frmt == 'J' else "yaml"))
    return js if frmt == 'J' else ya

def get_files_dif_formats(fn):
    with open(fn) as f:
        lfdishes = csv.reader(f, delimiter=';')
        lfd =[]
        for l in lfdishes:     # можно обойтись без цикла , так как одна строка в файле
            lfd.extend(l)
    return lfd



lfd = get_files_dif_formats("list_frmts.csv")

create_shop_list(choose_format(lfd))

# print(check_encoding('dishes.txt'))

