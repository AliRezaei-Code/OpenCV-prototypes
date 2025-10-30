# Vision & Accessibility Demos

**OpenCV prototypes for detection, preprocessing, and video I/O with reproducible notebooks**

---

## 1) Purpose & Success Criteria

**Goal.** Build a small, well‑engineered lab of computer‑vision demos focused on accessibility. Each demo should be:

* **Useful** for common accessibility tasks (enhanced readability, text capture, high‑contrast modes, etc.).
* **Reproducible** end‑to‑end via pinned environments, deterministic transforms, and executable notebooks.
* **Portable** to CPU‑only laptops, with optional GPU acceleration.

**Primary success metrics**

* Reproducibility: `make reproduce` executes without manual edits on a fresh machine.
* Latency: ≤ 33 ms per frame (≥ 30 FPS) on 720p for “light” filters on CPU; ≤ 100 ms per frame for OCR/detection.
* Quality: OCR WER/CER on sample sets; readability score improvements (contrast, font edge sharpness proxies).
* Accessibility: WCAG‑aligned color/contrast checks for produced frames.

---

## 2) Scope

**In‑scope** (initial demos)

1. **Text enhancement for low‑vision**

   * Global/Local contrast (CLAHE), adaptive thresholding (Sauvola/Niblack), deblurring (Wiener/USM), denoising.
   * Zoom/magnifier overlay with smooth panning.
2. **OCR pipeline for alt‑text & capture**

   * Detection (EAST or DB), recognition (Tesseract or PaddleOCR), simple layout, export to Markdown/JSON.
3. **Color‑vision support**

   * Simulation (protan/deutan/tritan) and **daltonization** (compensatory remapping) for readability.
4. **Caption helper**

   * Whisper‑based offline ASR (small model), subtitle burn‑in, SRT export (optional dependency group).
5. **Video I/O & streaming**

   * Unified capture (file, webcam, RTSP), GStreamer optional; frame queues, graceful shutdown; writers for MP4, images, and MJPEG preview.

**Out‑of‑scope (v1)**

* Complex document layout understanding, full screen‑reader integration, cloud APIs, biometric features.

---

## 3) Users & Scenarios

* **Low‑vision reader**: enhance and magnify course handout on webcam feed; save a readable PDF.
* **Note‑taker**: capture whiteboard text from a phone video; OCR to Markdown.
* **Designer**: preview how UI looks under color‑blind simulations; apply daltonization suggestions.
* **Lecturer**: auto‑generate captions (offline) and embed into a teaching clip.

---

## 4) Deliverables (v1)

1. **Repo** with MIT license and contributor guide.
2. **Demos** in `demos/` (CLI + notebook for each):

   * `text_enhance`, `ocr_capture`, `color_vision`, `caption_helper`, `video_io_basics`.
3. **Executable notebooks** under `notebooks/` with **Papermill** runs and **Jupytext** pairing.
4. **Benchmark scripts** for latency & OCR accuracy.
5. **Sample media** with clear licenses & consent.
6. **Docs site** (MkDocs or Docusaurus) with WCAG contrast notes and how‑tos.

---

## 5) System Architecture

```mermaid
flowchart LR
    subgraph Input
      A[Webcam] -->|VideoCapture| Q
      B[Video File] -->|FFmpeg/GStreamer| Q
      C[RTSP] --> Q
    end

    Q[Frame Queue] --> P[Processing Pipeline]
    P -->|preview| V[Viewer]
    P -->|write| W[Writers: MP4/Images/MJPEG]
    P -->|metrics| M[Metrics/Logs]

    subgraph Pipeline
      P1[Preproc: resize, denoise, CLAHE] --> P2[Detection (EAST/DB)]
      P2 --> P3[OCR (Tesseract/Paddle)]
      P1 -.-> P4[Color‑vision sim/daltonize]
      P1 -.-> P5[ASR/Subtitle]
    end
```

**Notes**

* Pure OpenCV/Numpy core, optional PyTorch for EAST/DB.
* Threaded capture/processing with back‑pressure; deterministic RNG seeds.

---

## 6) Tech Stack & Dependencies

* **Core**: Python 3.11, OpenCV‑Python, NumPy, SciPy, scikit‑image.
* **OCR**: `pytesseract` + system Tesseract OR `paddleocr` (extras group `ocr`).
* **ASR**: `openai-whisper` or `faster-whisper` (extras group `asr`).
* **Viz/UI**: `typer` for CLI, `rich` for logs, simple `cv2.imshow`/streamlit (optional) for previews.
* **Repro**: `conda-lock` or `uv`/`pip-tools`, `jupytext`, `papermill`, `pre-commit`.
* **Data & Metrics**: `pandas`, `matplotlib`, `psnr/ssim` from skimage, `jiwer` for WER/CER.
* **CI**: GitHub Actions (lint, unit tests, smoke notebooks), optional CUDA job matrix.

---

## 7) Repository Layout

```
vision-accessibility-demos/
├─ README.md
├─ LICENSE
├─ pyproject.toml              # poetry or uv; extras: [ocr, asr]
├─ requirements.txt            # pinned fallback
├─ env/                        # environment.yml, conda-lock files
├─ Makefile                    # common tasks
├─ pre-commit-config.yaml
├─ src/
│  ├─ vademos/
│  │  ├─ io/ (capture.py, writer.py, streams.py)
│  │  ├─ ops/ (filters.py, threshold.py, color_vision.py, morphology.py)
│  │  ├─ detect/ (east.py, db.py, boxes.py)
│  │  ├─ ocr/ (tesseract.py, postprocess.py)
│  │  ├─ asr/ (whisper.py, srt.py)
│  │  ├─ utils/ (timing.py, viz.py, wcag.py, seeds.py)
│  │  └─ cli.py
├─ demos/
│  ├─ text_enhance.py
│  ├─ ocr_capture.py
│  ├─ color_vision.py
│  ├─ caption_helper.py
│  └─ video_io_basics.py
├─ notebooks/
│  ├─ 01_text_enhance.ipynb
│  ├─ 02_ocr_capture.ipynb
│  ├─ 03_color_vision.ipynb
│  ├─ 04_caption_helper.ipynb
│  └─ 99_benchmarks.ipynb
├─ tests/
│  ├─ test_ops_filters.py
│  ├─ test_color_vision.py
│  ├─ test_ocr_postprocess.py
│  └─ data/ (golden images, small clip)
├─ data/
│  ├─ samples/ (licensed images/videos)
│  └─ ocr_eval/ (ICDAR subsets with LICENSE)
├─ docs/
│  ├─ index.md
│  └─ guides/
└─ .github/workflows/ci.yml
```

---

## 8) Reproducibility & Environment

* Provide `env/environment.yml` and `env/conda-lock-*.yaml` plus `uv.lock` or `requirements.txt`.
* `Makefile` targets:

  * `make setup` → create env, install extras.
  * `make precommit` → install hooks.
  * `make reproduce` → runs papermill across notebooks with fixed seeds.
  * `make bench` → runs latency benchmarks on CPU.
* Determinism: set `PYTHONHASHSEED`, RNG seeds in NumPy/Torch, fixed thread counts where helpful.

---

## 9) Datasets & Samples (licensing‑aware)

* **OCR/Text**: ICDAR2013/2015 subsets, COCO‑Text small samples, TextCaps few images for demo only.
* **Color‑vision**: synthetic palettes, UI screenshots created in repo.
* **Audio/Caption**: 15–30s spoken demo recorded by contributors with consent + CC‑BY license.
* Each `/data/samples/` item must include a `LICENSE.txt` and `SOURCE.txt`.

---

## 10) Algorithms & Implementation Notes

### 10.1 Text enhancement

* Resize with respect to line height; denoise via bilateral/fastNlMeans; sharpen via unsharp masking.
* Contrast with CLAHE (tileGridSize tuned), adaptive threshold (Sauvola) for binarization.
* Optional morphological open/close to stabilize OCR boxes.

### 10.2 Text detection & OCR

* Detector choices: **EAST** (OpenCV dnn) or **DB** (torch). Start with EAST for simplicity.
* Recognition: Tesseract with language pack `eng` as baseline; optional PaddleOCR for higher accuracy.
* Postprocess: polygon NMS, box ordering, line grouping by y‑centroid, export to Markdown with bounding‑box order.

### 10.3 Color‑vision simulation & daltonization

* Brettel/Vienot/Luquet models in LMS space to simulate protan/deutan/tritan.
* Daltonization via error redistribution (Machado et al.). Provide severity slider 0–1.

### 10.4 Caption helper

* `faster-whisper` CPU small model; VAD segments; SRT with word‑level times; burn‑in via `cv2.putText` or `ffmpeg` filter.

### 10.5 Video I/O

* Single producer (capture) → bounded queue → consumer (pipeline) → preview/writers.
* Graceful teardown on SIGINT; drop frames on back‑pressure; timestamped frame structs.

---

## 11) Benchmarks & Quality Metrics

* **Latency**: per‑op timings, rolling FPS; CSV logs and notebook plots.
* **OCR accuracy**: WER/CER via `jiwer` on labeled sample subset.
* **Readability**: WCAG contrast ratio before/after, edge sharpness proxy (Tenengrad variance).
* **Color‑vision**: delta‑E between original and daltonized for preserved distinguishability.

---

## 12) Testing Strategy

* Unit tests for ops with **golden images**; tolerance bands for numeric outputs.
* Property tests (e.g., idempotence where expected; invariants like shape/pixel range).
* CLI smoke tests on CI with tiny inputs; notebook execution smoke via Papermill (cell count and key outputs asserted).

---

## 13) Documentation

* **README**: quickstart, screenshots/gifs, demo matrix.
* **Docs**: how‑tos per demo, WCAG color/contrast primer, troubleshooting (FFmpeg, Tesseract paths).
* **Examples**: one‑liner CLI invocations per demo, plus annotated notebook cells.

---

## 14) Security, Privacy, and Ethics

* Default **local‑only** processing; never upload samples.
* Provide redaction utility to blur faces or redact regions before sharing.
* Contributor agreement for sample media consent; publish CC‑BY where possible.

---

## 15) Roadmap & Milestones (4 Sprints)

**Sprint 0 – Project skeleton (1–2 days)**

* Repo init, license, CI, env, pre‑commit, Makefile, sample data placeholders.
* Implement `video_io_basics` demo and queue wiring; smoke test.

**Sprint 1 – Text enhancement**

* Implement filters & thresholds; interactive params in notebook; benchmark latency.
* Deliver: `text_enhance.py`, `01_text_enhance.ipynb`, unit tests.

**Sprint 2 – OCR capture**

* Add EAST detection + Tesseract; layout grouping; Markdown/JSON export.
* Deliver: `ocr_capture.py`, `02_ocr_capture.ipynb`, accuracy eval notebook.

**Sprint 3 – Color‑vision & caption helper**

* Implement simulation + daltonization with severity slider; basic ASR + SRT export.
* Deliver: `color_vision.py`, `caption_helper.py`, docs updates.

**Hardening week**

* Docs polish, sample licenses, cross‑platform tests, bug triage.

---

## 16) Risk Register & Mitigations

* **OCR accuracy too low on noisy video** → Add stabilization, stronger binarization, optional PaddleOCR.
* **Performance on CPU** → Use grayscale paths, ROI processing, downscale, and queue dropping; cache heavy nets.
* **Environment friction** → Provide Dockerfile and `make reproduce`; include Windows install notes.
* **Licensing** → Keep LICENSE files per sample; avoid proprietary fonts/assets.

---

## 17) Tasks & Issue Backlog (initial)

* [ ] Set up repo & CI; publish MIT license.
* [ ] Environment files (`environment.yml`, `requirements.txt`, `conda‑lock`).
* [ ] Implement `vademos.io.capture` with webcam/file/RTSP and graceful shutdown.
* [ ] Implement `vademos.ops.filters` (denoise, sharpen, CLAHE) with tests.
* [ ] Notebook `01_text_enhance` with sliders and side‑by‑side panels.
* [ ] EAST model loader using OpenCV DNN; box decode + NMS; tests with synthetic text.
* [ ] Tesseract wrapper and Markdown export utility.
* [ ] OCR evaluation notebook with `jiwer`.
* [ ] Color‑vision simulation + daltonization ops with unit tests vs published matrices.
* [ ] Whisper small integration behind extra; SRT writer; minimal caption burn‑in.
* [ ] Benchmarks: latency CSV + plotting notebook.
* [ ] Docs: quickstart, troubleshooting.

---

## 18) Interfaces & CLIs (Typer)

Examples:

```bash
# 1) Text enhancement live preview from webcam
python -m vademos.cli text-enhance --source 0 --clahe --tile-size 8 8 --unsharp 1.0 --show

# 2) OCR capture on a video file
python -m vademos.cli ocr-capture --source data/samples/board.mp4 --detector east --ocr tesseract --out out/board.md

# 3) Color-vision simulation
python -m vademos.cli color-vision --source ui.png --mode deutan --severity 0.8 --out out/ui_deutan.png

# 4) Caption helper (offline ASR)
python -m vademos.cli caption --source lecture.mp4 --model small --srt out/lecture.srt --burn-in out/lecture_subtitled.mp4
```

---

## 19) Notebook Template

```markdown
# Demo: <name>
- Objective
- Inputs/outputs
- Parameters (links to CLI flags)
- Repro cell: seeds, env printout
- Cells: load → preprocess → core algorithm → evaluation → export
- Summary & next steps
```

---

## 20) Definition of Done (per demo)

* ✅ CLI + notebook produce identical outputs on same inputs & seeds.
* ✅ CI passes unit tests and Papermill smoke run.
* ✅ Readme section with screenshot/gif and quickstart.
* ✅ Sample input/output files licensed and included.
* ✅ Metrics logged (latency and, where applicable, OCR/readability).

---

## 21) Nice‑to‑Haves (post‑v1)

* Streamlit mini‑apps with accessible UI controls and keyboard shortcuts.
* CUDA build matrix; TensorRT opt if GPU present.
* On‑device mobile build notes (Android/iOS) using OpenCV mobile SDK.
* Basic plugin system for new ops/demos.

---

## 22) Next Steps (owner checklist)

1. Create GitHub repo with this structure.
2. Commit env & CI; push initial `video_io_basics`.
3. Add `text_enhance` ops + notebook; gather sample images.
4. Wire EAST + Tesseract; run first OCR eval.
5. Implement color‑vision ops; record caption sample; update docs.
