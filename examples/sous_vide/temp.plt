#!/usr/bin/gnuplot -persist

set title "Temperature data"
set xlabel "Time (s)"
set ylabel "Temperature"
set grid
plot for [i=2:3] "temp.txt" using i:xtic(1) title col
