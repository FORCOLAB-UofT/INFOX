#!/bin/bash
npm install
NODE_OPTIONS=--openssl-legacy-provider npm run-script build
rm -rf ../chrome-extension
cp -r dist ../chrome-extension

