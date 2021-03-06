#!/usr/bin/python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  - Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------

import ply.lex as lex
from core import Context, ColorDef
from core import MeshGenerationOptions

import ply.yacc as yacc

reserved = {
    'Default': 'DEFAULT_ID',
    'MAKEPLY': 'MAKEPLY_ID',
    'Include': 'INCLUDE_ID',
    'RegionColor': 'REGIONCOLOR_ID',
    'IGNORE': 'IGNORE_ID',
    'COLOR_ALIASES': 'COLOR_ALIASES_ID',
    'COLOR_DEFAULTS': 'COLOR_DEFAULTS_ID',
    'TRIM': 'TRIM_ID',
    'OFFSET': 'OFFSET_ID',
    'OPTION_DEFAULTS': 'OPTION_DEFAULTS_ID',
    'MIN_DIAMETER': 'MIN_DIAMETER_ID',
    }

tokens = [
    'FILENAME',
    'COMMA',
    'FLOAT',
    'INT',
    'COLON',
    'LBRACE',
    'RBRACE',
    'RPAREN',
    'LPAREN',
    'SEMICOLON',
    'STAR',
    'ID',
    ] + list(reserved.values())


def t_ID(t):
    r'''[a-zA-Z_][a-zA-Z_0-9]*'''

    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t



def t_FLOAT(t):
    r"""[-+]?[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?"""

    t.value = float(t.value)
    return t


def t_INT(t):
    r'''\d+'''
    t.value = int(t.value)
    return t


def t_FILENAME(t):
    r'''".*"'''
    t.value = str(t.value[1:-1])
    return t


def t_COMMENT(t):
    r'''\#.*'''
    pass


t_COMMA = r','
t_SEMICOLON = r';'
t_COLON = r':'

t_STAR = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'


# Define a rule so we can track line numbers
def t_newline(t):
    r'''\n+'''
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

from errors import MultiMeshParseError


# Error handling rule

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    raise MultiMeshParseError("Lexer couldn't parse: '%s'" % t.value[0])


# Build the lexer
lexer = lex.lex()



# Overall File:

def p_config_completeB(p):
    r"""config :  config config_block
               |  config_block"""
    # Don't need to do anything.


## Blocks
## -------------
def p_configblocksA(p):
    """config_block : color_defaults_block
                    | color_aliases_block
                    | options_block
                    | makeply_block """
    # Don't need to do anything.




#Options:
def p_option_defaults_block(p):
    r"""options_block :  OPTION_DEFAULTS_ID LBRACE option_block_stmts RBRACE """

def p_option_defaults_block_stmts(p):
    r"""option_block_stmts : empty
                           | option_block_stmts option_block_stmt"""
    # Don't need to do anything.

def p_option_block_block_stmt(p):
    r"""option_block_stmt : MIN_DIAMETER_ID COLON FLOAT SEMICOLON """
    # Set the option
    p.parser.context.global_options[MeshGenerationOptions.minimum_diameter] = float(p[3])







# COLOR_ALIASES
# =============
def p_color_aliases_block(p):
    r"""color_aliases_block :  COLOR_ALIASES_ID LBRACE color_aliases_block_stmts RBRACE """
    # Don't need to do anything.

def p_color_aliases_block_stmts(p):
    r"""color_aliases_block_stmts : empty
                                   | color_aliases_block_stmts color_aliases_block_stmt"""
    # Don't need to do anything.

def p_color_aliases_block_stmt(p):
    r"""color_aliases_block_stmt : ID COLON color_rgb SEMICOLON """
    # Register the alias:
    p[0] = p.parser.context.add_alias(id=p[1], color=p[3])



# COLOR_DEFAULTS:
# ================
def p_color_defaults_block(p):
    r"""color_defaults_block :  COLOR_DEFAULTS_ID LBRACE color_defaults_block_stmts RBRACE """
    # Don't need to do anything.

def p_color_defaults_block_stmts(p):
    r"""color_defaults_block_stmts : empty
                                   | color_defaults_block_stmts color_defaults_block_stmt"""
    # Don't need to do anything.


def p_color_defaults_block_stmt(p):
    r"""color_defaults_block_stmt : region_color_def """
    rgns, color = p[1]
    for rgn_id in rgns:
        p.parser.context.set_default_region_color(rgn_id=rgn_id, color=color)






# MAKEPLY Block
# ==============

def p_ply_block(p):
    r"""makeply_block :  MAKEPLY_ID FILENAME ply_block_open LBRACE makeply_block_stmts  RBRACE """
    p.parser.context.close_ply_block(plyfilename=p[2])


def p_ply_block_open(p):
    r"""ply_block_open : empty"""
    p.parser.context.new_ply_block()


def p_ply_block_stmts(p):
    r"""makeply_block_stmts : empty
                            | makeply_block_stmts makeply_block_stmt
    """
    # Don't need to do anything.

def p_ply_block_stmt(p):
    """makeply_block_stmt : makeply_block_stmt_color
                          | makeply_block_stmt_include  """
    # Don't need to do anything.


def p_ply_block_stmt_color(p):
    """makeply_block_stmt_color : region_color_def"""
    rgns, color = p[1]
    for rgn in rgns:
        p.parser.context.currentplyscope.set_region_color(region=rgn, color=color)


def p_ply_block_stmt_include(p):
    """makeply_block_stmt_include : INCLUDE_ID  FILENAME include_option_set SEMICOLON"""
    p.parser.context.currentplyscope.include_file(filename= p[2], options = p[3])


def p_include_option_set(p):
    """include_option_set : empty
                          | LBRACE include_options RBRACE"""
    if len(p) == 2:
        p[0] =  {}
    elif len(p) == 4:
        p[0] =  p[2]
    else:
        assert False


def p_include_option_trim(p):
    """include_option : TRIM_ID COLON INT"""
    p[0] = {'trim': p[3]}


def p_include_option_offset(p):
    """include_option : OFFSET_ID COLON LPAREN INT COMMA INT COMMA INT RPAREN """
    p[0] = {'offset': (p[4], p[6], p[8])}


def p_include_optionsA(p):
    """include_options : empty"""
    p[0] = {}


def p_include_optionsB(p):
    """include_options : include_option
                       | include_options COMMA include_option"""

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1].copy()
        p[0].update(p[3])


def p_region_color_def_stmt(p):
    r"""region_color_def : REGIONCOLOR_ID int_list COLON color SEMICOLON """
    p[0] = (p[2], p[4])


def p_color(p):
    r"""color : color_rgb
              | color_alias"""
    p[0] = p[1]

def p_color3(p):
    r"""color : IGNORE_ID """
    p[0] = None

def p_color1(p):
    r"""color_rgb : LPAREN INT COMMA INT COMMA INT RPAREN"""
    p[0] = ColorDef(r=p[2], g=p[4], b=p[6])

def p_color2(p):
    r"""color_alias : ID"""
    p[0] = p.parser.context.get_color(p[1])


def p_int_list(p):
    r"""int_list : INT
                 | int_list COMMA INT """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_int_list_star(p):
    r"""int_list : STAR"""
    p[0] = [None]


def p_empty(p):
    '''empty : '''

    pass






# Error rule for syntax errors

def p_error(p):
    raise MultiMeshParseError("Yacc Error on line: %d Token: '%s'"%(p.lineno, p.type))





from zipfile import ZipFile


def parse_mesh_config(t):
    # Build the parser
    parser = yacc.yacc()
    parser.context = Context()
    parser.parse(t, lexer=lex)

    print 'Parsed OK'
    return parser.context


def parse_zip_file(zip_in, zip_out):
    # Build the parser
    parser = yacc.yacc()

    fIn = ZipFile(zip_in, 'r')
    fOut = ZipFile(zip_out, 'w')
    parser.context = Context(src_zip_file=fIn, dst_zip_file=fOut)

    try:
        conf = fIn.open('config.txt').read()
    except:
        conf = fIn.open('src/config.txt').read()

    parser.parse(conf, lexer=lex)

    fIn.close()
    fOut.close()

    print 'Parsed OK'
    return parser.context


