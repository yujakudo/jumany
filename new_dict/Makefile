prefix=

JUMAN_DIR = ../juman-7.01
MAKEINT = $(JUMAN_DIR)/makeint/makeint
MAKEMAT = $(JUMAN_DIR)/makemat/makemat
MAKEPAT = $(JUMAN_DIR)/makepat/makepat
DICSORT = $(JUMAN_DIR)/makepat/dicsort

GRM_FILES = JUMAN.grammar JUMAN.kankei JUMAN.katuyou
TBL_FILES = jumandic.mat jumandic.tab
DIC_FILE = juman.dic
INT_FILE = juman.int

DIST_RS_DIR=share/juman/hinototori
DIST_FILES=$(TBL_FILES) jumandic.dat jumandic.pat version.json

# copy_files <files>
define install_files
	if [ "$(prefix)" = "" ]; then \
		echo "prefix is not set."; exit 1; \
	fi; \
	to_dir=$(prefix)/$(DIST_RS_DIR); \
	mkdir -p $$to_dir; \
	for file in $1; do \
		cp $$file $$to_dir; \
	done;
endef

.PHONY: all clean install

all: jumandic.pat

clean:
	rm -f jumandic.* *.int JUMAN.connect

JUMAN.connect: JUMAN.connect.c
	gcc -E -P $< | LANG=C sed "s/\(\#pragma\)/\;\1/" > $@

jumandic.tab: $(GRM_FILES) JUMAN.connect # $(MAKEMAT)
	$(MAKEMAT)

jumandic.mat: jumandic.tab

jumandic.dat: $(DIC_FILE) $(GRM_FILES) $(TBL_FILES) # $(MAKEINT) $(DICSORT)
	$(MAKEINT) $(DIC_FILE); \
	$(DICSORT) $(INT_FILE) > $@

jumandic.pat: jumandic.dat # $(MAKEPAT)
	$(MAKEPAT)

install: all
	$(call install_files, $(DIST_FILES))
