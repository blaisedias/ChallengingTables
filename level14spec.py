#!/usr/bin/python
# -*- coding: utf-8 -*-
# python script specifying number ranges for sums and the distributions
# of sums for test level.
# This is for level 14
#
level = '14-beta'
# A number range is specified as (start, end, step)
# for example:
#   (1, 8, 1) gives 1, 2, 3, 4, 5, 6, 7, 8
#   (1, 8, 2) gives 1, 3, 5, 7
test_spec = [
    {
        'type': 'Multiply2',
        'count': 11,
        'ranges': [
            # a × b
            (11, 19),       # a
            (11, 19, 1),    # b
        ],
    },

    {
        'type': 'Multiply3',
        'count': 11,
        'ranges': [
            # a × b × c
            (2, 9, 1),      # a
            (2, 9, 1),      # b
            (2, 9, 1),      # c
        ],
    },

    {
        'type': 'Divide2',
        'count': 1,
        'ranges': [
            # A ÷ b  where A = (a  × b)
            (2, 20, 1),     # a
            (11, 20, 1),    # b
            # A = (22 ... 400)
        ],
    },

    {
        'type': 'FractionOf',
        'count': 8,
        'ranges': [
            # a/b of C where C = (b × c) to get a whole number
            (1, 8, 1),      # a
            (2, 10, 1),     # b
            (2, 12, 1),     # c
            # C = (4 ... 120)
        ],
    },

    {
        'type': 'PercentOf',
        'count': 13,
        'ranges': [
            # a % of b
            (10, 200, 5),   # a = (10, 15, 20, 25, ... 100)
            (1, 200, 1),    # b
        ],
    },

    {
        'type': 'FractionOfFraction',
        'count': 7,
        'ranges': [
            # (a/b) × (c/d)
            (1, 3, 1),      # a
            (2, 4, 1),      # b
            (1, 3, 1),      # c
            (2, 4, 1),      # d
        ],
    },

    {
        'type': 'PowerOf',
        'count': 18,
        'ranges': [
            # a raised to b, squares, cubes ...
            (2, 20, 1),     # a
            (2, 3, 1),      # b squares, cubes
        ],
    },

    {
        'type': 'SquareRoot',
        'count': 0,
        'ranges': [
            # 2√a
            (2, 20, 1),   # expanded to (4, 9, 25, ... 400)
        ],
    },

    {
        'type': 'CubeRoot',
        'count': 1,
        'ranges': [
            # 3√a
            (2, 20, 1),   # expanded to (8, 27, 125, ... 8000)
        ],
    },

    # ### 80 tests upto here
    {
        'type': 'Divide2',
        'count': 10,
        'ranges': [
            # A ÷ b  where A = (a  × b)
            (2, 20, 1),     # a
            (11, 20, 1),    # b
            # A = (22 ... 400)
        ],
    },

    {
        'type': 'SquareRoot',
        'count': 10,
        'ranges': [
            # 2√a
            (2, 20, 1),   # expanded to (4, 9, 25, ... 400)
        ],
    },

    {
        'type': 'CubeRoot',
        'count': 10,
        'ranges': [
            # 3√a
            (2, 20, 1),   # expanded to (8, 27, 125, ... 8000)
        ],
    },
]
