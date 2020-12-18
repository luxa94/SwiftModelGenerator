class SimpleFieldType:
    def __init__(self, name, optional):
        self.name = f'{name}{optional}'
        self.optional_name = f'{name}?'
        self.cast_name = name

class ArrayFieldType:
    def __init__(self, name, optional):
        self.name = f'[{name}]{optional}'
        self.optional_name = f'[{name}]?'
        self.cast_name = f'[{name}]'

class Field:
    def __init__(self):
        self.deserialization_type = None
        self.modifier = None
        self.name = None
        self.type = None
        self.optional = None
        self.initial_value = None

    def interpret(self, model):
        self.deserialization_type = model.deserialization_type
        self.modifier = model.modifier
        self.name = model.name
        self.optional = model.optional == '?'
        self.initial_value = model.initial_value

        type_name = model.type.__class__.__name__
        if type_name == 'SimpleFieldType':
            self.type = SimpleFieldType(model.type.name, model.optional)
        elif type_name == 'ArrayFieldType':
            self.type = ArrayFieldType(model.type.name, model.optional)
        else:
            print(f'Unsupported field type: {type_name}')

        return self

class Type:
    def __init__(self):
        self.access_modifier = None
        self.type = None
        self.name = None
        self.protocol = None
        self.fields = []

    def interpret(self, model):
        self.access_modifier = model.access_modifier
        self.type = model.type
        self.name = model.name

        if model.protocol == 'codable':
            self.protocol = 'JsonCodable'
        elif model.protocol == 'encodable':
            self.protocol = 'JsonEncodable'
        elif model.protocol == 'decodable':
            self.protocol = 'JsonDecodable'

        for field in model.fields:
            self.fields.append(Field().interpret(field))

        return self
