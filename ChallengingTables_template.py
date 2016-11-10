#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) <2016>, <Blaise Dias>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#  this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#  may be used to endorse or promote products derived from this software without
#  specific prior written permission.
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
# ChallengingTables .fodt formatting strings
# TODO: move to a text/JSON file which is read by ChallengingTables.py
fodt = {
    'fmt': {
        'mul2': '<text:p text:style-name="P4">{}{} × {} = {}</text:p>',
        'mul3': '<text:p text:style-name="P4">{}{} × {} × {} = {} </text:p>',
        'div': '<text:p text:style-name="P4">{}{} ÷ {} = {}</text:p>',
        'percent_of': '<text:p text:style-name="P5">{}{}%<text:span text:style-name="T11"> of </text:span>{} = {}</text:p>',
        'frac_of': '<text:p text:style-name="P5">{}<text:span text:style-name="T1">{}</text:span>/<text:span text:style-name="T7">{}</text:span><text:span text:style-name="T11"> of </text:span>{} = {}</text:p>',
        'frac_frac': '<text:p text:style-name="P5">{}<text:span text:style-name="T1">{}</text:span><text:span text:style-name="T3">/</text:span><text:span text:style-name="T8">{}</text:span><text:span text:style-name="T4"> of </text:span><text:span text:style-name="T10"><text:span text:style-name="T1">{}</text:span></text:span><text:span text:style-name="T3">/</text:span><text:span text:style-name="T8">{}</text:span><text:span text:style-name="T3">  = {}</text:span></text:p>',
        'ans_frac_frac': '<text:span text:style-name="T1">{}</text:span><text:span text:style-name="T3">/</text:span><text:span text:style-name="T8">{}</text:span>',
        'power': '<text:p text:style-name="P4">{}{}<text:span text:style-name="T1">{}</text:span><text:span text:style-name="T2"> = {}</text:span></text:p>',
        'sqrt': '<text:p text:style-name="P2">{}√{} = {}</text:p>',
        'cubert': '<text:p text:style-name="P5">{}<text:span text:style-name="T1">3</text:span>√{} = {}</text:p>',

        'sig': '      <text:p text:style-name="P24">{}</text:p>',
        'footer': '    <text:p text:style-name="P1">ID: {} <text:s text:c="10"/>Filename: {}<text:s text:c="10"/>{}</text:p>',
        'level': '      <text:p text:style-name="P20"><text:span text:style-name="T13">Challenging Tables– Stage {}</text:span> <text:s text:c="19"/>Will you get a bronze silver or gold award?</text:p>',
        'count': '<text:span text:style-name="T11">{}) </text:span>',
        'empty': '<text:p text:style-name="P2"></text:p>',
    },

# signature text
    'lines': {
# Regular expression to match lines that must be replaced with text.
#    'SUM': '<text:p text:style-name="P2"\>__SUM__</text:p\>',
        'SUM': '<text:p text:style-name="P2">__SUM__</text:p>',
# level name
#    'level': '<text:p text:style-name="P20"><text:span text:style-name="T13">Challenging Tables– Stage ',
        'level': r'      <text:p text:style-name="P20"><text:span text:style-name="T13">Challenging Tables– Stage #</text:span> <text:s text:c="19"/>Will you get a bronze silver or gold award\?</text:p>',
        'sig': '      <text:p text:style-name="P24">XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX</text:p>',
# page footer line
        'footer': '    <text:p text:style-name="P1">XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX</text:p>',

    }
}
