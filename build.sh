#!/usr/bin/env bash

rm -rf build
rm -rf dist

pyinstaller2 src/pmvc.py --onefile

cp -a src/locale dist/
cp -a src/icons dist/