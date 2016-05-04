#
#  Makefile instructions for building
#  a Docker container, starting the
#  application, and running tests.
#

VERSION = v0.1.5
SEPARATOR = "----------------------------------"
run:
	bash bin/run.sh;

setup:
	bash bin/setup.sh;

test:
	bash bin/test.sh;

build:
	@echo $(SEPARATOR)
	@echo 'Building Docker container.'
	@echo $(SEPARATOR)

	docker build -t luiscape/hdx-monitor-funnel-stats:$(VERSION) .

	@echo $(SEPARATOR)
	@echo 'Docker container build successfully.'
	@echo $(SEPARATOR)