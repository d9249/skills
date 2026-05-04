# Model Family Rubric

Use the repo `pipeline_tag` first. If it is missing or misleading, fall back to
README text, tags, and files.

## `text-generation`

Check:

- base model and derivative relationship
- context window or visible token limit
- tool use, coding, reasoning, multilingual claims
- quantization/runtime packaging
- benchmark files and serving notes

Emphasize:

- local deployment fit
- benchmark deltas vs base model
- safety/refusal profile changes

## `image-text-to-text`

Check:

- vision encoder or multimodal stack references
- modality support: image, document, OCR, UI, chart, video, audio
- native resolution or image-token behavior if documented
- base model vs current variant modality differences
- image-serving constraints and prompt format

Emphasize:

- multimodal strengths
- OCR/document/UI reasoning claims
- whether the current repo narrows or expands the base model's modality support

## `text-classification`

Check:

- label schema
- target domain and training/eval datasets
- thresholding or calibration notes
- class imbalance or bias statements
- latency and batch-serving considerations

Emphasize:

- task fit
- label quality and domain transfer limits

## `token-classification`

Check:

- entity schema
- span-level metrics
- tokenizer mismatch risk
- BIO/BILOU or other labeling convention

Emphasize:

- entity extraction coverage
- boundary and tokenization limitations

## `feature-extraction` or sentence similarity / embedding models

Check:

- embedding dimension
- max sequence length
- normalization guidance
- retrieval, clustering, or STS benchmarks
- supported languages and domain focus

Emphasize:

- retrieval fit
- multilingual coverage
- truncation and pooling caveats

## `text-to-image`

Check:

- base model and fine-tune method
- resolution defaults
- scheduler or inference-runtime assumptions
- safety filters and NSFW positioning
- sample quality evidence

Emphasize:

- generation style
- deployment cost
- fine-tune scope vs backbone novelty

## Fallback For Other Pipelines

- Start by naming the actual task in one sentence.
- State what the repo definitely does.
- State what it does not claim to do.
- Reuse the default report sections, but replace architecture-heavy language with
  task-fit, deployment, and risk language when novelty is unclear.
