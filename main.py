import os

from compiler.lex import LexicalAnalyzer


lex = LexicalAnalyzer()
lex.build()

directory = 'cool_programs'
cool_program_file_list = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith('.cl')]

for cool_program_file in cool_program_file_list:
    with open(cool_program_file, 'r') as cool_program:
        lex.parse(cool_program.read())
