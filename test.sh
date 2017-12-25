#!/usr/bin/env bash

[ -z $BASH ] || shopt -s expand_aliases
alias BEGINCOMMENT="if [ ]; then"
alias ENDCOMMENT="fi"

BEGINCOMMENT
  echo "This line appears in a commented block"
  echo "And this one too!"
ENDCOMMENT

echo "This is outside the commented block"