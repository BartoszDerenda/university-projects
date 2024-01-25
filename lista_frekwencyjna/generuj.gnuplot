#!/usr/bin/gnuplot

set terminal pngcairo size 1024,768
set output 'plot.png'

#unset key

maks = 19763
slow = 30175

set xrange [1:slow]
set yrange [1:maks]
set logscale x
set logscale y

set datafile separator " "
plot \
        'result.csv' using 1:3 pt 7 ps 1 title 'csv', \
        maks/x, \
        maks/x**2, \
        maks/x**0.5
