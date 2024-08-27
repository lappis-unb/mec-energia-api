Y='\033[0;33m'
G='\033[0;32m'
B='\033[0;34m'
W='\033[0;37m'
R='\033[0;31m'
E='\033[0m'

ENV_DEV=.envs/.env.dev
ENV_TEST=.envs/.env.test
COMPOSE_FILE_DEV=compose.yml
COMPOSE_FILE_TEST=compose-test.yml


define load-env
	$(eval include $(1))
	$(eval export $(shell sed 's/=.*//' $(1)))
endef

define wait_for_service
	@echo ""${Y}"󰞌"${E} "Waiting service at "${Y}"$(API_URL)"${E}"..."
	@echo "For more details, run: docker logs -f mepa-api"
	@echo
	@while ! curl --output /dev/null --silent --head --fail $(API_URL); do \
		printf "\r󱍸 Checking.  ";  sleep 1; \
		printf "\r󱍸 Checking.. ";  sleep 1; \
		printf "\r󱍸 Checking...";  sleep 1; \
	done; \
	printf "\n"
	@echo ""${G}"󰘽"${E}" Server ready "${G}"$(API_URL)"${E}""
endef

define clean-dangling
	@echo ""
	@echo ""${Y}""${E}" Removing unused (dangling) Docker images."
	docker image prune -f --filter "dangling=true"
endef

build:
	$(call load-env,$(ENV_DEV))
	docker compose -f $(COMPOSE_FILE_DEV) --env-file $(ENV_DEV) build
	@echo ""${B}""${E}" Build completed for "${Y}"develop"${E}" environment."

build-nc:
	$(call load-env,$(ENV_DEV))
	docker compose -f $(COMPOSE_FILE_DEV) --env-file $(ENV_DEV) build --no-cache --force-rm
	@echo ""${B}""${E} "Build no-cache completed for "${Y}"develop"${E}" environment."

build-up:
	$(call load-env,$(ENV_DEV))
	docker compose -f $(COMPOSE_FILE_DEV) --env-file $(ENV_DEV) up --build -d --remove-orphans
	@echo ""${B}""${E}" Build completed for "${Y}"develop"${E}" environment."

up:
	$(call load-env,$(ENV_DEV))
	docker compose -f $(COMPOSE_FILE_DEV) --env-file $(ENV_DEV) up -d --remove-orphans

down:
	docker compose -f $(COMPOSE_FILE_DEV) --env-file $(ENV_DEV) down
	@$(call clean-dangling)

# --------------------------------------------------------------------------------------------------------------------

build-test:
	$(call load-env,$(ENV_TEST))
	docker compose -f $(COMPOSE_FILE_TEST) --env-file $(ENV_TEST) build
	@echo ""${B}""${E} "Build completed for "${Y}"test"${E} "environment."

build-nc-test:
	$(call load-env,$(ENV_TEST))
	docker compose -f $(COMPOSE_FILE_TEST) --env-file $(ENV_TEST) build --no-cache --force-rm
	@echo ""${B}""${E} "Build no-cache completed for "${Y}"test"${E} "environment."

build-up-test:
	$(call load-env,$(ENV_TEST))
	docker compose -f $(COMPOSE_FILE_TEST) --env-file $(ENV_TEST) up --build -d --remove-orphans
	@echo ""${B}""${E} "Build completed for "${Y}"test"${E}" environment."
	@$(call wait_for_service)

up-test:
	$(call load-env,$(ENV_TEST))
	docker compose -f $(COMPOSE_FILE_TEST) --env-file $(ENV_TEST) up -d --remove-orphans
	@$(call wait_for_service)

down-test:
	docker compose -f $(COMPOSE_FILE_TEST) --env-file $(ENV_TEST) down
	@$(call clean-dangling)

# --------------------------------------------------------------------------------------------------------------------

confirm:
	@echo -n ""${Y}""${E}" Remover recursos Docker não usados (containers, redes, imagens, volumes)? \n[y/N]: \b" && \
	read ans && [ $${ans:-N} = y ]

clean: confirm
	@echo ""${B}"󱍸 Executando limpeza..."${E}""
	@docker system prune -f
	@docker volume prune -f
	@docker network prune -f
	@echo ""${G}"󰘽 Limpeza concluída com sucesso."${E}""
