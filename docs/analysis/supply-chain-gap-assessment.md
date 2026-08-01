# Supply-Chain and QMS Gap Assessment

## Branch

`feature/supply-chain-qms`

## Existing capabilities

- [x] Basic supplier dataset
- [x] Supplier approval flag
- [x] Certificate-valid flag
- [x] Quality status
- [x] Export-risk classification
- [x] Deterministic risk score
- [x] Approve, quarantine and reject decisions
- [x] SHA-256 hash-linked ledger entries
- [x] CSV risk report

## Partial capabilities

- [~] Supplier validation is embedded in one script
- [~] Certificate validation is only a Boolean value
- [~] Quality validation is only a status string
- [~] Material-risk classification is hard-coded
- [~] Ledger uses previous hashes but has no verification command
- [~] Supply-chain execution is called through the project orchestrator

## Missing capabilities

- [x] Approved-supplier master registry
- [x] Active, suspended and revoked supplier states
- [x] Certificate identity and expiry validation
- [x] Material-batch registration schema
- [x] Certificate missing, expired and revoked scenarios
- [x] Transparent material-risk rules configuration
- [x] Decision reasons and control actions
- [x] Ledger record index and record ID
- [x] Full-chain verification
- [x] Duplicate-entry prevention
- [x] Controlled ledger-tamper simulation
- [x] Automated unit tests
- [x] Dedicated validation report
- [x] Direct complete-lab and examiner-runner validation
- [x] Evidence-generation workflow

## Important classification

This project implements a centralized custom tamper-evident hash ledger.

It is not:

- Hyperledger Fabric
- Ethereum
- a distributed blockchain
- a production export-control system
- a formal enterprise QMS

## Required target state

The completed feature must demonstrate:

1. approved supplier acceptance;
2. unknown, inactive or revoked supplier rejection;
3. material-batch registration;
4. certificate and quality validation;
5. transparent dual-use and export-risk classification;
6. deterministic decisions with reasons;
7. append-only hash-linked records;
8. full ledger verification;
9. controlled tamper detection;
10. automated testing and evidence reporting.
