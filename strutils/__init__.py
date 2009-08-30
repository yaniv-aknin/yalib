"Utilities for the handling of strings"

# plural code based on Python recipe by Christopher Dunn, unspecified license

aberrant_plurals = {
                    'datum'     : 'data',
                    'knife'     : 'knives',
                    'self'      : 'selves',
                    'elf'       : 'elves',
                    'life'      : 'lives',
                    'hoof'      : 'hooves',
                    'leaf'      : 'leaves',
                    'echo'      : 'echoes',
                    'embargo'   : 'embargoes',
                    'hero'      : 'heroes',
                    'potato'    : 'potatoes',
                    'tomato'    : 'tomatoes',
                    'torpedo'   : 'torpedoes',
                    'veto'      : 'vetoes',
                    'child'     : 'children',
                    'woman'     : 'women',
                    'man'       : 'men',
                    'person'    : 'people',
                    'goose'     : 'geese',
                    'mouse'     : 'mice',
                    'barracks'  : 'barracks',
                    'deer'      : 'deer',
                    'nucleus'   : 'nuclei',
                    'syllabus'  : 'syllabi',
                    'focus'     : 'foci',
                    'fungus'    : 'fungi',
                    'cactus'    : 'cacti',
                    'phenomenon': 'phenomena',
                    'index'     : 'indices',
                    'appendix'  : 'appendices',
                    'criterion' : 'criteria'
                   }


def plural(singular):
    if singular in aberrant_plurals:
        return aberrant_plurals[singular]
    root = singular
    post = ''
    try:
        vowels = 'aeiou'
        if singular[-1] == 'y' and singular[-2] not in vowels:
            root = singular[:-1]; post = 'ies'
        elif singular[-1] == 's':
            if singular[-2] in vowels:
                if singular[-3:] == 'ius': root = singular[:-2]; post = 'i'
                else: root = singular[:-1]; post = 'ses'
            else: post = 'es'
        elif singular[-1] in 'o' or singular[-2:] in ('ch', 'sh'):
            post = 'es'
        else:
            post = 's'
    except:
        post = 's'
    return root + post
