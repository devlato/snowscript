from glob import glob
from snow_lexer import SnowLexer
from difflib import unified_diff
from termcolor import colored
from lexer.tokens.standard import tokens
import sys
import os
# Debug
from sys import exit as e

def lex_snow(code):
    """
    Prettylexes given snow code and returns colorized string.
    """
    lexer = SnowLexer()
    lexer.input(code, '')
    code_lines = code.split("\n")
    last_printed_pos = 0
    tokens_as_string = ''
    indent = 0
    has_newline = False
    no_prefix_next_time = False
    next_line = ''
    is_first_token = True
    for t in lexer:
        if t.type == 'INDENT':
            indent += 1
        elif t.type == 'DEDENT':
            indent -= 1
        elif t.type == 'NEWLINE':
            indention = " " * indent * 4
            linenob = colored(str(t.lexer.lineno) + '', 'white', 'on_grey') + ' '
            lineno = colored(str(t.lexer.lineno) + '', 'yellow', 'on_grey') + ' '
            if not has_newline: tokens_as_string += "\n"
            tokens_as_string += lineno
            tokens_as_string += colored(indention + code[last_printed_pos:t.lexpos].strip(), 'yellow')
            if not has_newline: tokens_as_string += "\n"
            tokens_as_string += linenob + indention + next_line.strip()
            next_line = ''
            last_printed_pos = t.lexpos + 1
            has_newline = True
        elif t.type == 'ENDMARKER':
            nl = "" if has_newline else "\n"
            linenob = colored(str(t.lineno+1) + '', 'white', 'on_grey') + ' '
            lineno = colored(str(t.lineno+1) + '', 'yellow', 'on_grey') + ' '
            tokens_as_string += "\n" + lineno
            tokens_as_string += colored(code[last_printed_pos:], 'yellow') + "\n"
            tokens_as_string += linenob + str(next_line)
            tokens_as_string += "%s%s" % (nl, t.type)            
            next_line = ''
        else:
            is_special = t.type in tokens and t.type not in ('STRING_WITH_CONCAT', )
            prefix = " " if not has_newline and not is_first_token else ""
            if no_prefix_next_time:
                prefix = ''
                no_prefix_next_time = False
            if t.value in "({[" and len(t.value) == 1:
                no_prefix_next_time = True
            if t.value in "({[)}]" and len(t.value) == 1:
                prefix = ''
            if t.value == ':':
                prefix = ''
            indention = (" " if has_newline else "") * indent * 4
            has_newline = False
            token = t.value if is_special else "%s{'%s'}" % (t.type, t.value)
            next_line += "%s%s%s" % (
                prefix, indention, token
            )
        is_first_token = False
    return tokens_as_string.strip()

# Parse args
glob_string = '*.test' if len(sys.argv) < 2 else sys.argv[1]

# Set dir
os.chdir(os.path.abspath(os.path.dirname(__file__)))

# Delete old .out files.
os.system('rm -f lexer/tests/*.out')

# Run test 'suite'
failure = succes = 0
for file in glob('lexer/tests/' + glob_string):
    print colored("Prettylexing file: %s" % file, 'cyan')
    code, tokens_expected = [_.strip() for _ in open(file).read().split('----')]
    print lex_snow(code)
