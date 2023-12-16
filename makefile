# makefile

stop: down clean ;

clean: clean-pgdata clean-pycache ;
	rm -f client/*.log
	rm -f background/*.txt

clean-pgdata: ;
#	sudo rm -rf ./postgres/pgdata

clean-pycache: ;
	@find . -type d -name '__pycache__' -exec rm -rfv {} +

up: ;
	docker-compose up --detach --force-recreate

down: ;
	docker-compose down

restart: down up ;


.PHONY: clean up down restart stop test
