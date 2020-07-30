.PHONY: all clean

all: level2.pdf hastoc.pdf onepage.pdf hardmode.pdf

%.pdf: %.tex
	latexmk -pdf $<

clean:
	rm -f *.aux *.dvi *.fdb_latexmk *.fls *.log *.out

nuke: clean
	rm -f *.pdf
