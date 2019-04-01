.PHONY: all analytics navigator elastic setup clean visualizations

all: setup_repo markdown confluence analytics navigator elastic
analytics: create_analytics_and_pivoting_csv
navigator: create_attack_navigator_profile create_attack_navigator_profile_per_customer
elastic: create_es_export
setup: setup_repo setup_confluence setup_markdown
visualizations: make_visualizations

setup_repo:
	@echo "[*] Updating 3rd party repository"
	git submodule init
	git submodule update
	git submodule foreach git pull origin master
	
setup_confluence:
	@echo "[*] Setting up confluence"
	@cd scripts && python3 main.py -C --init

setup_markdown:
	@echo "[*] Setting up markdown"
	@cd scripts && python3 main.py -M --init

push_to_confluence:
	@echo "[*] Pushing data to confluence"
	@cd scripts && python3 main.py -C -A

push_to_markdown:
	@echo "[*] Pushing data to markdown"
	@cd scripts && python3 main.py -M -A

create_analytics_and_pivoting_csv:
	@echo "[*] Creating analytics.csv and pivoting.csv"
	@cd scripts && python3 yamls2csv.py

create_attack_navigator_profile:
	@echo "[*] Creating ATT&CK Navigator profile"
	@cd scripts && python3 attack_navigator_export.py

create_attack_navigator_profile_per_customer:
	@echo "[*] Creating ATT&CK Navigator profile"
	@cd scripts && python3 attack_navigator_per_customer_export.py

markdown:
	@echo "[*] Creating markdown repository and pushing data"
	@cd scripts && python3 main.py --markdown --auto --init

confluence:
	@echo "[*] Creating conflunce repository and pushing data"
	@cd scripts && python3 main.py --confluence --auto --init

create_es_export:
	@echo "[*] Creating elastic index"
	@cd scripts && python3 es_index_export.py

make_visualizations:
	@echo "[*] Creating visualizations.."
ifeq ($(GUI), 1)
	@cd scripts && python3 main.py -V --vis-export-type
else
	@cd scripts && python3 main.py -V
endif

# TODO: make clean works with non default paths from config
clean:
	@echo "[*] Cleaning up..."
	@rm -rf ./Atomic_Threat_Coverage
	@rm -f ./generated_analytics/atc_attack_navigator_profile*.json
	@rm -f ./generated_analytics/analytics.csv
	@rm -f ./generated_analytics/pivoting.csv
	@rm -f ./generated_analytics/atc_es_index.json

