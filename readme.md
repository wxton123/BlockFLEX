# BlockFLEX: Artifact for Results Reproduction (Evaluation)

This repository contains the artifact for the NSDI paper "**BlockFLEX: An Adaptive and Survivable Architecture with Hierarchical Routing for LEO Satellite Networks**". It is designed to facilitate the **reproduction of all figures and numerical results** presented in the paper.

## 📁 Repository Contents (Current - For Evaluation)

This artifact includes everything required to independently verify the results and figures from our paper:
*   `test_BlockFlex.py`: Python script to generate all figures from the paper.
*   `dataset*/`: The final, processed data used as input for the plotting scripts.
*   `outputs/`: Pre-generated figures (PDF/PNG) for quick inspection.
*   `core/`: Helper functions for calculating key metrics from the processed data.

## 🚀 Quick Start: Reproducing Figures

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run a plotting script:**
    ```bash
    bash run.sh #This will generate figures from the paper
    ```
    The script will read data from `./dataset*/` and save the figure to `./output/`.

## 🔜 Future Scope: Full Artifact Upon Acceptance

**Please note: This repository currently contains only the results reproduction package.**

The core simulation platform that generated the underlying data is itself a research contribution and is also under submission. **Upon acceptance of the paper, we commit to releasing the full, non-anonymized resources,** which will include:

1.  **The complete simulation platform.**
2.  **BlockFLEX as a module** within the simulator, enabling end-to-end execution of the proposed architecture.
3.  **Scripts to configure and run all experiments** presented in the paper.
4.  **Instructions to fully reproduce the results** from scratch, starting from running the simulations.

This staged release protects the double-blind review process for both contributions while ensuring full transparency and reproducibility upon publication.

## 🔍 Description of Provided Data

The `dataset*/` directories contain JSON files with the summarized results. 

## 📜 License and Citation

The code in this repository is released under the MIT License. The data is available for academic use only.
