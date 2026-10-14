# Audio pipeline investigation

This sample document exercises Markdown rendering. All measurements below are
**illustrative**, rather than results from a browser benchmark.

## What is being measured

Pipeline latency is the time from signal injection to detection after a local
loopback. The sample compares two paths and keeps the source synthetic.

- **Path A:** processing on an audio thread.
- **Path B:** processing through a worker.
- **Condition:** an unloaded pipeline.

## Results

| Example path | Median | Samples | Status |
|---|---:|---:|---|
| Path A | 64 ms | 200 | Complete |
| Path B | 77 ms | 200 | Complete |

![Illustrative pipeline latency: Path A is 64 ms and Path B is 77 ms.](report-chart.svg)

## Caveats

::: {.moz-message-bar}
::: {.icon-container}
<svg class="moz-icon" data-icon="information-fill"></svg>
:::
::: {.content}
::: {.text}
**Example data.** This document demonstrates formatting, not browser performance.
:::
:::
:::

A short code block retains its whitespace:

```js
const context = new AudioContext({ latencyHint: 'interactive' });
console.log(context.baseLatency);
```

<details class="moz-card accordion">
<summary>Read the sample methodology</summary>
<div class="moz-card-content">

The same Markdown is rendered in each preview. Changing a theme or layout
changes presentation while preserving these words and numbers.

</div>
</details>

## Next steps

1. Select the theme that fits the audience.
2. Choose a reading column, wide layout, or sidebar.
3. Compare light and dark previews before sharing the file.
