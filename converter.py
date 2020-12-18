def format_fields(model):
    return [f'{field.modifier} {field.name}: {field.type.name}' for field in model.fields]

def format_init_parameters(model):
    return [f'{field.name}: {field.type.name}' for field in model.fields]

def format_init_assignments(model):
    return [f'self.{field.name} = {field.name}' for field in model.fields]

def format_constructor(model):
    constructor_lines = []
    parameters = format_init_parameters(model)
    prefixes = [f'{" " * 4}init('] + [' ' * 9] * (len(parameters) - 1)
    sufixes = [','] * (len(parameters) - 1) + [') {']
    constructor_lines.extend([''.join(line) for line in zip(prefixes, parameters, sufixes)])

    assignments = format_init_assignments(model)
    constructor_lines.extend([f'{" " * 8}{assignment}' for assignment in assignments])

    constructor_lines.append(f'{" " * 4}}}')

    return constructor_lines

def format_clone_parameters(model):
    return [f'{field.name}: {field.type.optional_name} = nil' for field in model.fields]

def format_clone_assignments(model):
    return [f'{field.name}: {field.name} ?? self.{field.name}' for field in model.fields]

def format_clone_method(model):
    clone_lines = []
    parameters = format_clone_parameters(model)
    prefixes = [f'{" " * 4}func clone('] + ['               '] * (len(parameters) - 1)
    sufixes = [','] * (len(parameters) - 1) + [f') -> {model.name} {{']

    clone_lines.extend([''.join(line) for line in zip(prefixes, parameters, sufixes)])

    assignments = format_clone_assignments(model)
    assignment_first_prefix = f'{" " * 8}return {model.name}('
    assignment_first_prefix_length = len(assignment_first_prefix)
    assignment_prefixes = [assignment_first_prefix] + [' ' * assignment_first_prefix_length] * (len(assignments) - 1)
    assignment_sufixes = [','] * (len(assignments) - 1) + [')']
    clone_lines.extend([''.join(line) for line in zip(assignment_prefixes, assignments, assignment_sufixes)])

    clone_lines.append(f'    }}')

    return clone_lines

def format_decode_method(model):
    lines = []
    lines.append(f'    static func from(json: Json) throws -> {model.name} {{')

    lines.append('    }')

    return lines
    
def format_encode_method(model):
    lines = []
    # func toJson() -> Json
    lines.append(f'    func toJson() -> Json {{')
    if len(model.fields) == 0:
        lines.append(f'{" " * 8}return [:]')
    else:
        lines.append(f'{" " * 8}return [')

        map_fields = [f'"{field.name}": {field.name} as AnyObject?' for field in model.fields]
        map_prefixes = [" " * 12] * len(map_fields)
        map_sufixes = [','] * (len(map_fields) - 1) + ['']

        lines.extend([''.join(line) for line in zip(map_prefixes, map_fields, map_sufixes)])

        lines.append(f'{" " * 8}].filter {{ $0.value != nil }}')

    lines.append('    }')

    return lines

class TypeConverter:
    EMPTY_LINE = ""
    def convert(self, model):
        lines = []
        lines.append(self.generate_header(model))

        fields = format_fields(model)
        for field in fields:
            lines.append(f'    {field}')
        lines.append(self.EMPTY_LINE)

        lines.extend(format_constructor(model))
        lines.append(self.EMPTY_LINE)

        lines.extend(format_clone_method(model))
        lines.append(self.EMPTY_LINE)
        
        lines.extend(format_decode_method(model))
        lines.append(self.EMPTY_LINE)

        lines.extend(format_encode_method(model))

        lines.append(self.generate_end())
        
        return lines

    def generate_header(self, model):
        access_modifier_prefix = '' if model.access_modifier is None else f'{model.access_modifier} '
        return f'{access_modifier_prefix}{model.type} {model.name} {{'

    def generate_end(self):
        return '}'