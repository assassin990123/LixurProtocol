#!/bin/bash

pdflatex report_attack.tex 
pdflatex report_attack.tex 
bibtex report_attack
pdflatex report_attack.tex 
evince report_attack.pdf &
