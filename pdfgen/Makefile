.PHONY: all clean

all: level2.pdf

%.pdf: %.tex
	latexmk $<

clean:
	rm -f *.aux *.dvi *.fdb_latexmk *.fls *.log *.pdf
