NAME     := redisearch
VERSION  := $(shell sed -n '/^Version:/{s/.* //;p}' $(NAME).spec)
SRPM     := $(NAME)-$(VERSION)-$(shell sed -n '/^Release:/{s/.* //;s/%{?dist}/.fc43/;p}' $(NAME).spec).src.rpm
MOCK_CFG ?= fedora-43-$(shell uname -m)

.PHONY: download sources deps srpm mock copr verify lint clean help

# Download source tarballs from spec URLs
download:
	spectool -g -C . $(NAME).spec

# Build the SRPM
srpm: download
	rpmbuild -bs \
	  --define "_sourcedir $(CURDIR)" \
	  --define "_srcrpmdir $(CURDIR)" \
	  $(NAME).spec

# Rebuild in mock
mock: srpm
	sudo mock -r $(MOCK_CFG) --rebuild $(SRPM)

# Submit SRPM to COPR
copr: srpm
	copr-cli build @redis/redis $(SRPM)

# Run rpmlint on the spec
lint:
	rpmlint $(NAME).spec

# Remove generated artefacts
clean:
	rm -f *.tgz *.tar.gz *.src.rpm
	rm -rf $(NAME)-*/

# Show this help
help:
	@grep -E '^[a-z]+:.*##' $(MAKEFILE_LIST) | \
	  awk -F ':.*## ' '{printf "  %-12s %s\n", $$1, $$2}'
