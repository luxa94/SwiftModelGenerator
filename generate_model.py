from textx.metamodel import metamodel_from_file
from textx.exceptions import TextXSyntaxError
from model import Type
from converter import TypeConverter

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_name', help='Specification to load.')
    args = parser.parse_args()

    try:
        meta_model = metamodel_from_file('model.tx')
        model = meta_model.model_from_file(args.input_file_name)
    except TextXSyntaxError as e:
        print(e)
        return

    stuff = Type()
    stuff.interpret(model)

    converter = TypeConverter()
    for line in converter.convert(stuff):
        print(line)


if __name__ == '__main__':
    main()
