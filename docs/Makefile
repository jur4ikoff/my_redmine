ifeq ($(OS),Windows_NT)
	RM = del /Q
	NULLDEV = NUL
else
	RM = rm -f
	NULLDEV = /dev/null 2>&1 || true
endif

PDF      = index.pdf
MAIN     = main
TEX      = $(MAIN).tex
CC       = pdflatex
FLAGS    = -shell-escape -interaction=batchmode -halt-on-error
TEX = $(wildcard *.tex) $(wildcard report/*.tex)
BIB      = bibliography.bib

all: $(PDF)

# $(PDF): $(TEX) *.tex report/*.tex $(BIB)
$(PDF): $(TEX) $(BIB)
	$(CC) $(FLAGS) $(MAIN)
	bibtex $(MAIN) >$(NULLDEV) 
	$(CC) $(FLAGS) $(MAIN)
	$(CC) $(FLAGS) $(MAIN)

clean:
	$(RM) $(PDF) main.pdf *.aux *.log *.out *.toc *.bbl *.blg *.lof *.lot *.idx *.ind *.ilg *.fls *.fdb_latexmk *.aux
	$(RM) report/*.aux
	# rm -rf out/

.PHONY: all clean
