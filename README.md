# Mutual Fund FAQ Assistant (RAG Prototype)

## Product Chosen
Groww

## AMC Selected
SBI Mutual Fund

## Schemes Included
- SBI Bluechip Fund (Large Cap)
- SBI Flexicap Fund
- SBI Long Term Equity Fund (ELSS)
- SBI Small Cap Fund

## Problem
Retail investors frequently ask factual questions about mutual fund schemes such as:
- expense ratio
- exit load
- minimum SIP
- ELSS lock-in
- riskometer
- benchmark

This assistant answers those questions using official public sources.

## Solution
A small Retrieval-Augmented Generation (RAG) prototype that:

1. Collects information from AMC, SEBI, and AMFI pages
2. Retrieves relevant information
3. Returns a short factual answer with a source link

## Features
- Facts-only responses
- Source citation in every answer
- Refuses investment advice
- Uses public official sources

## Example Questions
- What is the ELSS lock-in period?
- What is the expense ratio of SBI Bluechip Fund?
- How can I download capital gains statements?

## Limitations
- Small dataset
- Limited to selected schemes
- Does not calculate returns
- Does not provide investment advice

## Disclaimer
This assistant provides factual information only and does not provide investment advice.
