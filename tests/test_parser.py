from main import parse


def test_one_operation():
    result = {
        'type': 'leaf',
        'op': '=',
        'id': 'Пол',
        'literal': 'М'
    }

    assert parse('Пол="М"') == result


def test_one_node():
    result = {
        'type': 'node',
        'op': 'OR',
        'left': {
            'type': 'node',
            'op': 'AND',
            'left': {
                'type': 'leaf',
                'op': '=',
                'id': 'Пол',
                'literal': "М"
            },
            'right': {
                'type': 'leaf',
                'op': '>',
                'id': 'Возраст',
                'literal': 25
            }
        },
        'right': {
            'type': 'leaf',
            'op': '>',
            'id': 'Стаж',
            'literal': 0.5
        },
    }

    assert parse('Пол="М" AND Возраст>25 OR Стаж>.5') == result


def test_two_nodes():
    result = {
        'type': 'node',
        'op': 'AND',
        'left': {
            'type': 'leaf',
            'op': '=',
            'id': 'Пол',
            'literal': "М"
        },
        'right': {
            'type': 'node',
            'op': 'OR',
            'left': {
                'type': 'leaf',
                'op': '>',
                'id': 'Возраст',
                'literal': 25
            },
            'right': {
                'type': 'leaf',
                'op': '>',
                'id': 'Стаж',
                'literal': 0.5
            }
        }
    }

    assert parse('Пол="М" AND (Возраст>25 OR Стаж>.5)') == result


def test_errors():
    try:
        parse('Пол="M" UND (Возраст>25 OR Стаж>.5)')
    except Exception:
        assert True

    try:
        parse('Пол=М AND (Возраст>25 OR Стаж>.5)')
    except Exception:
        assert True

    try:
        parse('Пол="М" AND Возраст>25 OR Стаж>.5)')
    except Exception:
        assert True

    try:
        parse('Пол="М" AND (Возраст>25 OR Стаж>.5')
    except Exception:
        assert True

    try:
        parse('Пол="М" AND ((Возраст>25 OR Стаж>.5)')
    except Exception:
        assert True

    try:
        parse('Пол="М AND (Возраст>25 OR Стаж>.5)')
    except Exception:
        assert True

    try:
        parse('Пол="М" and (Возраст>25 OR Стаж>.5)')
    except Exception:
        assert True

    try:
        parse('')
    except Exception:
        assert True

    try:
        parse('OR')
    except Exception:
        assert True
