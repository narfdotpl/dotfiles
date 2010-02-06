#!/usr/bin/env python
# encoding: utf-8
"""
Enlarge the first page of an A4 PDF to an (almost) A2-sized poster
divided into four A4 pages.

Run this script like this

    python a2.py a4document.pdf

and you will get an `a2.pdf` file in your working directory.  The
original PDF should have proper margins (everything should be visible
after printing).
"""

from os.path import join, realpath
from pipes import quote
from shutil import rmtree
from string import Template
from subprocess import PIPE, Popen
from sys import argv, exit
from tempfile import mkdtemp


__author__ = 'Maciej Konieczny <hello@narf.pl>'


SCALE = 1.9  # > 0 and <= 2


def cm(fraction):
    return '{0:.2f}cm'.format(fraction)


def usage():
    print __doc__.lstrip('\n').rstrip('\n')


def _main():
    # take hostage
    try:
        pdf_to_enlarge = quote(realpath(argv[1]))
    except IndexError:
        usage()
        exit()

    # get your gun
    width = 10.5
    height = 14.85

    horizontal_margin = width * (2 - SCALE)
    vertical_margin = height * (2 - SCALE)

    horizontal_line = width * SCALE
    vertical_line = height * SCALE

    tex = Template(r"""
\documentclass{article}

% disable margins
\usepackage{geometry}
\geometry{
    a4paper,
    textheight = 29.7cm,
    textwidth = 21cm
}
\setlength{\parindent}{0}

% allow magic
\usepackage{tikz}

\begin{document}
    % left top
    \begin{tikzpicture}
        \node[inner sep=0pt, above right] {
            \includegraphics*[trim=0 $h $w 0, scale=$scale]{$a4}
        };
        \draw[dashed] (0,0) -- ($hl,0) -- ($hl,$vl);
    \end{tikzpicture}
    \newpage

    % right top
    \begin{tikzpicture}
        \hspace*{$hm}
        \node[inner sep=0pt, above right] {
            \includegraphics*[trim=$w $h 0 0, scale=$scale]{$a4}
        };
        \draw[dashed] (0,$vl) -- (0,0) -- ($hl,0);
    \end{tikzpicture}
    \newpage

    % left bottom
    \vspace*{$vm}
    \begin{tikzpicture}
        \node[inner sep=0pt, above right] {
            \includegraphics*[trim=0 0 $w $h, scale=$scale]{$a4}
        };
        \draw[dashed] (0,$vl) -- ($hl,$vl) -- ($hl,0);
    \end{tikzpicture}
    \newpage

    % right bottom
    \vspace*{$vm}
    \begin{tikzpicture}
        \hspace*{$hm}
        \node[inner sep=0pt, above right] {
            \includegraphics*[trim=$w 0 0 $h, scale=$scale]{$a4}
        };
        \draw[dashed] (0,0) -- (0,$vl) -- ($hl,$vl);
    \end{tikzpicture}
\end{document}
    """).substitute(
        a4=pdf_to_enlarge, scale=SCALE,
        w=cm(width), h=cm(height),
        hm=cm(horizontal_margin), vm=cm(vertical_margin),
        hl=cm(horizontal_line), vl=cm(vertical_line)
    )

    # avoid witnesses
    temp_dir = mkdtemp()

    # know your enemy
    source_pdf = join(temp_dir, 'texput.pdf')
    target_pdf = realpath('a2.pdf')

    # down rodeo
    command = ';'.join([
        'cd ' + temp_dir,
        'echo -n "{0}" | pdflatex'.format(tex),
        'mv {0} {1}'.format(source_pdf, target_pdf)
    ])

    # use silencer
    Popen(command, shell=True, stdout=PIPE).communicate()

    # burn the evidence
    rmtree(temp_dir)

if __name__ == '__main__':
    _main()
