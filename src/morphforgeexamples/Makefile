

all: exset1_morphology exset2_singlecell_simulations exset3_multicell_simulations exset4_advanced_simulations exset5_assorted_simulations exset6_poster_ocns2012
clean: exset1_morphology_clean exset2_singlecell_simulations_clean exset3_multicell_simulations_clean exset4_advanced_simulations_clean exset5_assorted_simulations_clean




.PHONY: force_look
	
# Builing all the examples
###########################

exset1_morphology: force_look
	$(MAKE) -C exset1_morphology/ 

exset2_singlecell_simulations: force_look
	$(MAKE) -C exset2_singlecell_simulations/

exset3_multicell_simulations: force_look
	$(MAKE) -C exset3_multicell_simulations/ 

exset4_advanced_simulations: force_look
	$(MAKE) -C exset4_advanced_simulations/ 

exset5_assorted_simulations: force_look
	$(MAKE) -C exset5_assorted_simulations/ 


# Cleaning
# #########
	
exset1_morphology_clean: force_look
	$(MAKE) -C exset1_morphology/  clean

exset2_singlecell_simulations_clean: force_look
	$(MAKE) -C exset2_singlecell_simulations/  clean

exset3_multicell_simulations_clean: force_look
	$(MAKE) -C exset3_multicell_simulations/  clean

exset4_advanced_simulations_clean: force_look
	$(MAKE) -C exset4_advanced_simulations/ clean

exset5_assorted_simulations_clean: force_look
	$(MAKE) -C exset5_assorted_simulations/ clean

	
