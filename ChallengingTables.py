#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) <2016>, <Blaise Dias>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Simple python program to generate Challenging times table test sheets
# uses random number generator to select the numbers for each test.
# The Algorithms to avoid generation of duplicates individual tests in a
# single test sheet are simple, but deemed good enough for a test set of size
# 100.
# Quite simply for each type of sum generated, and place in the sum,
# a list of possible and used numbers is maintained,
# and random selection is retried until an unused number is found in the list.
# At the start of number selection for a place in the sum, the list of
# numbers is checked for availability.
# If all numbers have been used before, the list is reset,
# so a number will eventually be reused  in a place in a type of sum.
# Additionally if the generated sum is found in the existing list of sums,
# the sum is discarded, and generation is restarted.
# Theoretically this could lead to the program hanging, due to an infinite
# loop, when all possible sums have been generated before.
# This is unlikely give the size of the test sets, so the algorithms are
# "good enough" for the required purpose.

# Tests sheets are generated by pattern matching and substituting lines in
# an OpenDocument Flat XML (.fodt) template file.
# Note for the pattern matching to work XML formatting information must match.
# This is fragile, editting the template file even trivially in LibreOffice
# changes all sorts of formatting!
# Be warned that it is highly likely that the regular expressions will have to
# be updated if the template file is changed.
# If not matching and substitution will fail.
# Also the formatting strings for individual sums will have to change.
# There is probably a better way to do this, but I've deemed that it is a lot
# of work, and not worth my while.
#
# Generates .pdf files if LibreOffice/OpenOffice is installed,
# else generates .fodt files.
#
import sys
from random import randint
from random import shuffle as random_shuffle
import math
import os
import uuid
import time
import re

# flat open document XLM format support text.
fodt_fmt = {}
fodt_lines = {}
fodt_re = {}
fmt_warn_gt_100_tests = 'WARNING: number of test specifed is {}, which exceeds slots in template'
debug = False


def reset(arr):
    if debug:
        print >> sys.stderr, '** reset **', arr
    for ix in range(len(arr)):
        arr[ix][1] = False


def check_and_reset(arr):
    for ix in range(len(arr)):
        if not arr[ix][1]:
            return
    reset(arr)


class NumberSelector:
    def __init__(self, spec):
        if isinstance(spec, tuple):
            try:
                step = spec[2]
            except Exception:
                if debug:
                    print >> sys.stderr, 'Defaulting step to 1 for {}'.format(spec)
                step = 1
            self.numbers = [
                [x, False] for x in range(
                    spec[0], spec[1] + 1, step
                )
            ]
        elif isinstance(spec, list):
            self.numbers = [[x, False] for x in spec]
        else:
            raise RuntimeError('Invalid number selector spec {}'.format(spec))

    def reset(self):
        reset(self.numbers)

    def select(self):
        check_and_reset(self.numbers)
        ix = randint(0, len(self.numbers) - 1)
        while self.numbers[ix][1]:
            ix = randint(0, len(self.numbers) - 1)
        self.numbers[ix][1] = True
        return self.numbers[ix][0]

    def select_gt_nc(self, v):
        ix = randint(0, len(self.numbers) - 1)
        while self.numbers[ix][0] <= v:
            ix = randint(0, len(self.numbers) - 1)
        return self.numbers[ix][0]


class SumBase:
    def __init__(self, *args):
        # Subclasses take a number of range specifications
        # store an array of NumberSelectors one for each
        # range specification.
        self.m = []
        for arg in args:
            self.m.append(NumberSelector(arg))


class SquareRoot(SumBase):

    def text(self, sums):
        m1 = self.m[0].select()
        the_sum = fodt_fmt['sqrt'].format("{}", m1, '')
        if the_sum in sums:
            return self.text(sums)
        sums.append(the_sum)
        return {
            'sum': the_sum,
            'ans': fodt_fmt['sqrt'].format("{}", m1, int(math.sqrt(m1))),
        }


class CubeRoot(SumBase):

    def text(self, sums):
        m1 = self.m[0].select()
        the_sum = fodt_fmt['cubert'].format("{}", m1 ** 3, '')
        if the_sum in sums:
            return self.text(sums)
        sums.append(the_sum)
        return {
            'sum': the_sum,
            'ans': fodt_fmt['cubert'].format("{}", m1 ** 3, m1),
        }


class Multiply2(SumBase):

    def text(self, sums):
        m1 = self.m[0].select()
        m2 = self.m[1].select()
        the_sum = fodt_fmt['mul2'].format("{}", m1, m2, '')
        if the_sum in sums:
            return self.text(sums)
        sums.append(the_sum)
        return {
            'sum': the_sum,
            'ans': fodt_fmt['mul2'].format("{}", m1, m2, m1 * m2),
        }


class Multiply3(SumBase):

    def text(self, sums):
        m1 = self.m[0].select()
        m2 = self.m[1].select()
        m3 = self.m[2].select()
        the_sum = fodt_fmt['mul3'].format("{}", m1, m2, m3, '')
        if the_sum in sums:
            return self.text(sums)
        sums.append(the_sum)
        return {
            'sum': the_sum,
            'ans': fodt_fmt['mul3'].format("{}", m1, m2, m3,  m1 * m2 * m3),
        }


class Divide2(SumBase):

    def text(self, sums):
        m1 = self.m[0].select()
        m2 = self.m[1].select()
        the_sum = fodt_fmt['div'].format("{}", m1 * m2, m2, '')
        if the_sum in sums:
            return self.text(sums)
        sums.append(the_sum)
        return {
            'sum': the_sum,
            'ans': fodt_fmt['div'].format("{}", m1 * m2, m2, m1),
        }


class FractionOf(SumBase):

    def text(self, sums):
        m1 = self.m[0].select()
        m2 = self.m[1].select_gt_nc(m1)
        m3 = randint(m2 * 2, m2 * 12)       # FIXME: derive from param
        while m3 % m2:
            m3 = randint(m2 * 2, m2 * 12)
        # randomly multiply by 10
        if (randint(0, 100) % 2):
            m3 *= 10
        if debug:
            print >> sys.stderr, "{}/{} of {}".format(m1, m2, m3)
        a = m1 * m3 * 1.0
        a /= m2
        a = int(a)
        the_sum = fodt_fmt['frac_of'].format("{}", m1, m2, m3, '')
        if the_sum in sums:
            return self.text(sums)
        sums.append(the_sum)
        return {
            'sum': the_sum,
            'ans': fodt_fmt['frac_of'].format("{}", m1, m2, m3, a)
        }


class PercentOf(SumBase):

    def text(self, sums):
        m1 = self.m[0].select()
        m2 = randint(1, 200)  # FIXME: derive from param
        while True:
            if 0 == ((m1 * m2) % 100):
                if (m2 < 100):
                    break
                if ((m2 % 10) == 0):
                    break
            m2 = randint(1, 200)  # FIXME: derive from param

        if debug:
            print >> sys.stderr, "{}% of {} {}".format(m1, m2, ((m1 * m2) / 100))

        the_sum = fodt_fmt['percent_of'].format("{}", m1, m2, '')
        if the_sum in sums:
            return self.text(sums)
        sums.append(the_sum)
        return {
            'sum': the_sum,
            'ans': fodt_fmt['percent_of'].format("{}", m1, m2, (m1 * m2) / 100),
        }


class FractionOfFraction(SumBase):

    def text(self, sums):
        m1 = self.m[0].select()
        m2 = self.m[1].select_gt_nc(m1)
        m3 = self.m[2].select()
        m4 = self.m[3].select_gt_nc(m3)

        n = m1 * m3
        d = m2 * m4

        if d % n == 0:
            d = d / n
            n = 1

        for x in range(4, 1, -1):
            if n % x == 0 and d % x == 0:
                n = n / x
                d = d / x

        the_sum = fodt_fmt['frac_frac'].format("{}", m1, m2, m3, m4, '')
        the_ans = fodt_fmt['ans_frac_frac'].format(n, d)
        if the_sum in sums:
            return self.text(sums)
        sums.append(the_sum)
        return {
            'sum': the_sum,
            'ans': fodt_fmt['frac_frac'].format("{}", m1, m2, m3, m4, the_ans)
        }


class PowerOf(SumBase):

    def text(self, sums):
        m1 = self.m[0].select()
        m2 = self.m[1].select()
        if debug:
            print >> sys.stderr, "{}^{}".format(m1, m2)
        the_sum = fodt_fmt['power'].format("{}", m1, m2, '')
        if the_sum in sums:
            return self.text(sums)
        sums.append(the_sum)
        return {
            'sum': the_sum,
            'ans': fodt_fmt['power'].format("{}", m1, m2, int(math.pow(m1, m2))),
        }


class Squared(SumBase):

    def text(self, sums):
        m1 = self.m[0].select()
        m2 = 2
        if debug:
            print >> sys.stderr, "{}^{}".format(m1, m2)
        the_sum = fodt_fmt['power'].format("{}", m1, m2, '')
        if the_sum in sums:
            return self.text(sums)
        sums.append(the_sum)
        return {
            'sum': the_sum,
            'ans': fodt_fmt['power'].format("{}", m1, m2, int(math.pow(m1, m2))),
        }


class Cubed(SumBase):

    def text(self, sums):
        m1 = self.m[0].select()
        m2 = 3
        if debug:
            print >> sys.stderr, "{}^{}".format(m1, m2)
        the_sum = fodt_fmt['power'].format("{}", m1, m2, '')
        if the_sum in sums:
            return self.text(sums)
        sums.append(the_sum)
        return {
            'sum': the_sum,
            'ans': fodt_fmt['power'].format("{}", m1, m2, int(math.pow(m1, m2))),
        }


class Blank(SumBase):

    def text(self, sums):
        return {
            'sum': fodt_fmt['empty'],
            'ans': fodt_fmt['empty']
        }


def substitute(line, test_lst, key, ix):
    def do_subst(regex):
        ixtxt = fodt_fmt['count'].format(ix + 1)
        txt = regex.sub(test_lst[ix][key].format(ixtxt), line)
        if debug:
            print >> sys.stderr, txt
        return txt.encode('utf8')

    if fodt_re['SUM'].search(line):
        return do_subst(fodt_re['SUM']), ix + 1
    elif fodt_re['sig'].match(line):
        return sig, ix
    elif fodt_re['footer'].match(line):
        return footer, ix
    elif fodt_re['level'].match(line):
        if leveltext is not None:
            return leveltext, ix
    return line, ix


def read_spec(spec_name):
    re_comment = re.compile('#.*$')
    # Read text, strip comments.
    with open(spec_name, "rb") as fp:
        lines = [y for y in [re_comment.sub(r'', xx) for xx in [x.strip() for x in fp.readlines()]]
                 if len(y)]
    sum_names = [
        'Multiply2',
        'Multiply3',
        'Divide2',
        'FractionOf',
        'PercentOf',
        'FractionOfFraction',
        'Squared',
        'Cubed',
        'PowerOf',
        'SquareRoot',
        'CubeRoot',
    ]
    re_level = re.compile('(?i)level[:=\s]+(?P<LEVEL>.*)')
    hr_label = '((\w+[\s=:]+)?)'
    re_p = re.compile('(?i){}(?P<SUM>{})[,\s]+{}(?P<COUNT>\d+)[,\s]+{}(?P<NUMBERS>.*)'.format(
        hr_label,
        '|'.join(sum_names),
        hr_label,
        hr_label))

    re_range3 = re.compile('(?i){}(?P<RANGE>(\(\d+[,\s]+\d+[,\s]+\d+[,\s]*\)))'.format(
        hr_label))
    re_range2 = re.compile('(?i){}(?P<RANGE>(\(\d+[,\s]+\d+[,\s]*\)))'.format(
        hr_label))
    re_list = re.compile('(?i){}(?P<RANGE>(\[((\d+[,\s]+)*)(\d+[,\s]*)\]))'.format(
        hr_label))

    test_spec = []
    level = None
    for line in lines:
        s = re_level.match(line)
        if s:
            level = s.groupdict()['LEVEL']
            continue
        s = re_p.match(line)
        if s:
            gd = s.groupdict()
            if debug:
                print >> sys.stderr, line
                print >> sys.stderr, '{SUM} {COUNT} {NUMBERS}'.format(**gd)
            spec = {
                'type': gd['SUM'],
                'count': int(gd['COUNT'].strip()),
                'ranges': []
            }
            n = gd['NUMBERS']
            while True:
                m = re_range3.match(n)
                if m:
                    spec['ranges'].append(eval(m.groupdict()['RANGE']))
                    n = re_range3.sub(r'', n, count=1).strip()
                    continue
                m = re_range2.match(n)
                if m:
                    spec['ranges'].append(eval(m.groupdict()['RANGE']))
                    n = re_range2.sub(r'', n, count=1).strip()
                    continue
                m = re_list.match(n)
                if m:
                    spec['ranges'].append(eval(m.groupdict()['RANGE']))
                    n = re_list.sub(r'', n, count=1).strip()
                    continue
                break
            test_spec.append(spec)
            if debug:
                print >> sys.stderr, '{type} {count} {ranges}\n'.format(**spec)

    return test_spec, level


if __name__ == '__main__':

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("names", nargs='*', action="store", default=['L14_{}'.format(str(int(time.time())))])
    parser.add_argument("-p", "--print", dest="do_print", action="store_true", default=False,
                        help="Print to default printer")
    parser.add_argument("-s", "--series", dest="series", action="store", type=int, default=0,
                        help="Generate a series of tests")
    parser.add_argument("--template", dest="template", action="store", default="ChallengingTables_template.fodt",
                        help="Name of test template file, (change with care)")
    parser.add_argument("--shuffle", dest="shuffle", action="store_true", default=False,
                        help="Shuffle the list of tests")
    parser.add_argument("--date", dest="printdate", action="store_true", default=False,
                        help="Print creation date")
    parser.add_argument("--specification", dest="spec", action="store",
                        required=True, help="Test specification text, e.g. level14spec.txt")

    options = parser.parse_args()

    if options.series:
        fnames = ['{}_{}'.format(options.names[0], x + 1) for x in
                  range(options.series)]
    else:
        fnames = options.names[:]

    with open(options.template) as fp:
        lines = [x.rstrip() for x in fp.readlines()]

    thismodule = sys.modules[__name__]
    test_spec, level = read_spec(options.spec)
    if debug:
        for spec in test_spec:
            print >> sys.stderr, '{type} repeated={count} number ranges={ranges}'.format(**spec)

    import json
    with open('ChallengingTables_template.json', "rb") as fp:
        fodt = json.load(fp, encoding="utf-8")

    fodt_fmt = fodt['fmt']
    fodt_lines = fodt['lines']
    fodt_re = {k: re.compile(re.escape(fodt_lines[k])) for k in fodt_lines}

    for fname in fnames:

        testfile = '{}.fodt'.format(fname)
        ansfile = 'ANS.{}.fodt'.format(fname)
        uuidv = str(uuid.uuid4())
        dt = ''
        if options.printdate:
            dt = 'Created on {}'.format(time.ctime())
        sig = fodt_fmt['sig'].format(uuidv)
        footer = fodt_fmt['footer'].format(uuidv, fname, dt)
        try:
            leveltext = fodt_fmt['level'].format(level)
        except:
            leveltext = None

        sums = []
        tests = []
        for spec in test_spec:
            obj = getattr(thismodule, spec['type'])(*spec['ranges'])
            tests.extend([obj.text(sums) for i in range(spec['count'])])

        if options.shuffle:
            random_shuffle(tests)

        if (len(tests) > 100):
            print >> sys.stderr,  fmt_warn_gt_100_tests.format(len(tests))

        blank = Blank()
        tests.extend([blank.text(sums) for x in range(len(tests), 100)])

        ix = 0
        with open(testfile, 'wb') as fp:
            for line in lines:
                sline, ix = substitute(line, tests, 'sum', ix)
                fp.write(sline)

        ix = 0
        with open(ansfile, "wb") as fp:
            for line in lines:
                sline, ix = substitute(line, tests, 'ans', ix)
                fp.write(sline)

        if options.do_print:
            os.system("soffice --headless -p {}".format(testfile))

        if 0 == os.system("soffice --headless --convert-to pdf {}".format(testfile)) \
                and 0 == os.system("soffice --headless --convert-to pdf {}".format(ansfile)):
            os.system("rm {}".format(testfile))
            os.system("rm {}".format(ansfile))
