#!/usr/bin/env bash

bundle exec jekyll build
rsync -r _site/ emfta.emf.as207960.net:/opt/tfemf/about