# Decision-model release audits

Use for classification, routing, scoring and other typed-decision model releases. Complete these checks before drafting performance or deployment claims; attach primary-source URLs and unresolved conditions to the claim ledger.

## 1. Identify the artifact before explaining changes

1. Pair the launch page with the individual checkpoint card, actual repository files and linked technical report. Keep sibling-model experiments separate from evidence for the focal checkpoint.
2. Read Hub model metadata and revision-specific file trees:
   - `https://huggingface.co/api/models/<org>/<model>`
   - `https://huggingface.co/api/models/<org>/<model>/tree/<revision>?recursive=true&expand=false`
3. Compare weight LFS object IDs and byte sizes between the release and current revisions before claiming that weights changed. README, banner or configuration commits alone do not establish weight replacement. Treat matching public weight objects as identity evidence, not a performance reproduction or certification of hosted API weights.
4. Check model, evaluation-artifact and training-data access separately; ungated weights do not imply ungated evaluation traces or a downloadable training mixture.

## 2. Trace the actual serving path

1. Read the pinned setup script, runtime constructor, release patch and readout configuration together. Follow the constructor used by the documented example and benchmark adapter, not just the class advertised in the README.
2. Trace local-directory and Hub repo-id branches. Check whether each branch actually loads attention overrides, readout heads and calibration files; a default constructor can silently select causal attention instead of the trained block-bidirectional mask.
3. Check the loaded model class for text versus multimodal support. Hosted image support does not validate an arbitrary local text-engine example.
4. Separate trained sequence length, positional configuration, constructor limits and hosted-service limits. A larger positional ceiling or runtime limit is not evidence of long-context decision quality.
5. Label a code-path discrepancy as a static reproduction risk until execution measures its effect. Do not declare a low benchmark score caused by that discrepancy without the corresponding rerun and configuration provenance.

## 3. Interpret the output and compute contract

- Explain shared-prefix processing as one state prefill plus question-specific suffix work; additional questions are not free and need not consume another question's answer.
- Preserve literal API type and field names. Distinguish selected-option probability, distribution-concentration confidence and an ordered score's expectation.
- Separate calibration training from post-hoc calibration artifacts and from verified calibration on the deployment distribution.
- Check whether abstention is an explicitly supplied option or a guaranteed API field; learning an uncertainty option does not automatically insert it into every request.
- Quote latency with percentile, input size, endpoint and workload conditions. Separate hosted end-to-end latency from local engine measurements and generation throughput.
- State token prices as token prices, not per-request prices. Include question, formatting and image-token accounting when documented, and separate escalation or human-review costs.

## 4. Reconcile evaluation evidence before selecting headline scores

1. Read the current leaderboard's structured data, edition definition and operator notes, rather than copying a potentially stale model-card rank. Pin the source snapshot used for volatile results.
2. Record public, private same-skill, private new-domain and combined Full results separately. Do not imply that a public-split superlative establishes private generalization or overall leadership.
3. Separate official evaluator measurements from company replicas. Inspect a chart's footnotes: a company's focal-model rerun and competitors copied from an older public leaderboard are not one independently controlled run.
4. Attribute overlap findings and excluded tests to the board operator, retaining their scope; do not independently pronounce training leakage from an exclusion note.
5. Read credible contrary community results and their adapters. Preserve task selection, class balance, threshold, input context and hardware where material. Neither discard a specialized negative result nor generalize it into a universal model verdict.

## 5. Verify release and adoption scope

- Distinguish an additional-SFT cookbook from the complete original training recipe and data release. Check its pinned checkpoint, data subset and serving stack before promising reproducibility.
- Distinguish a license metadata label from bundled license text and upstream/runtime obligations.
- Record a hosted `latest` alias as mutable even when the public checkpoint's weight objects have not changed.
- Write the article around the useful adoption boundary, supported mechanism and material limitations; keep exhaustive audit traces in the evidence directory rather than turning the post into an incident log.
