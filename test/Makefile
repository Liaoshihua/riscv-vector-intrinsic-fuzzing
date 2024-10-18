SRCTOP:=/home/xyenchi/dragon/rif
CC:=/home/xyenchi/projects/riscv-gnu-toolchain/test-rif/bin/riscv64-unknown-elf-gcc
CFLAGS:=-march=rv64gcv_zfh_zvfh -mabi=lp64d  -static -O
SIM:=/home/xyenchi/projects/riscv-gnu-toolchain/qemu/test-rif/qemu-riscv64
NODE:=10
LENGTH:=500
SEED:=3735928559
ARCH:=rv64gcv_zfh_zvfh
GEN_PATH:=build/tool
GEN_PATTERN:=random_gen
HAS_POLICY:=

include rules.mk

GEN:=$(GEN_PATH)/$(GEN_PATTERN)

SIM_LOGS:= $(addsuffix .log,$(TARGETS))
SIM_1_LOGS:= $(addsuffix .1.log,$(TARGETS))

ifeq ($(VERBOSE),)
V:=@
else
V:=
endif

define cmd
(set -x; $(1)) >>$@ 2>&1 \
|| (echo $(2) >> $@ && exit 1)
endef

all:
	-$(MAKE) -k run
	$(MAKE) report
	@echo "Test done"

report: $(SIM_LOGS)
	$(SRCTOP)/scripts/report

clean:
	rm -f *.c *.elf *.log *.dot

run: $(SIM_LOGS)

%.log: $(GEN)
	$(V) \
        if [ ! -f $(subst .log,.c,$@) ]; then \
            echo "Gen testcase $(subst .log,,$@)"; \
	    $(call cmd, $(GEN) \
	                 --root=$(notdir $(basename $@)) \
	                 --nodes-to-gen=$(NODE) \
	                 --length=$(LENGTH) \
	                 --dot=$(basename $@).dot \
	                 --code=$(notdir $(basename $@)).c \
	                 --seed=$(SEED) \
	                 --march=$(ARCH) \
	                 $(HAS_POLICY), "GEN FAIL") \
        fi
	$(V)echo "Compile $(subst .log,,$@)"
	$(V)$(call cmd, \
	      $(CC) $(CFLAGS) $(EXTRA_CFLAGS) \
	      $(subst .log,.c,$@) \
	      -o $(subst .log,.elf,$@) \
	      , "COMPILE FAIL")
	$(V)echo "Run $(subst .log,,$@)"
	$(V)$(call cmd, \
              $(SIM) $(subst .log,.elf,$@) \
              , "RUN FAIL")

$(GEN):
ifeq ("$(wildcard $(GEN))","")
	mkdir -p build
	cd build && cmake $(SRCTOP)
	cd build && $(MAKE)
endif
