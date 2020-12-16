from lark import Lark

__all__ = ['parse']


LogicalExpressionParser = Lark(r"""
    COMPARISON: "=" | "!=" | "<" | ">" | "<=" | "=>"
    OPERATOR: "AND" | "OR"
    ID: /\w+/
    STRING: "\""/.*?/"\""
    leaf: ID COMPARISON (STRING | INT | DECIMAL)
    ?node: block | node OPERATOR block
    ?block: leaf | "(" node ")"
    
    %import common.INT
    %import common.DECIMAL
    %ignore /\s+/
""", start='node', parser='lalr')


def transform(node, parsed_dict):
    parsed_dict['type'] = node.data
    parsed_dict['op'] = node.children[1]
    if node.data == 'leaf':
        parsed_dict['id'] = node.children[0]
        literal_token = node.children[2]
        literal_val = literal_token
        if literal_token.type == 'STRING':
            literal_val = literal_token[1:-1]
        elif literal_token.type == 'DECIMAL':
            literal_val = float(literal_token)
        elif literal_token.type == 'INT':
            literal_val = int(literal_token)
        parsed_dict['literal'] = literal_val
    else:
        parsed_dict['left'] = {}
        transform(node.children[0], parsed_dict['left'])
        parsed_dict['right'] = {}
        transform(node.children[2], parsed_dict['right'])
    return


def parse(query: str) -> dict:
    """
    Parameters
    ----------
    query : str
        логический запрос вида 'Пол="М" AND (Возраст>25 OR Стаж>5)'.

    Returns
    -------
    parsed_dict : dict
        словарь, содержащий дерево операций.

    Notes
    -----
        Поддерживаемые операции сравнения: = != > < >= <=.

        Поддерживаемые логические операции: AND OR, приоритет одинаковый, группировка скобками.

        Поддерживаемые типы литералов: int float str (двойные кавычки внутри строки не допускаются).

        Поддерживаемые типы узлов (type):
           leaf - узел, представляющий операцию сравнения

           node - узел, представляющий логическую операцию, имеет два подузла - left, right
    """
    tree = LogicalExpressionParser.parse(query)
    parsed_dict = {}
    transform(tree, parsed_dict)
    return parsed_dict
