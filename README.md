# TARA Interconnection Study Post-Processing

Python script for post-processing transmission constraint results from TARA interconnection studies.

The script processes outputs from energy (FCITC) and capacity (deliverability) studies to identify the most limiting transmission constraints and evaluate how project injection size affects grid limitations.

This type of analysis is commonly performed during generator interconnection studies to assess transmission bottlenecks and determine feasible project injection levels.

## Project Overview

Interconnection studies generate large volumes of constraint results across monitored facilities and contingencies. These raw outputs require post-processing to identify the most binding transmission constraints affecting a project.

This repository demonstrates how Python and pandas can be used to automate this analysis.

The workflow:

- Parse raw TARA constraint outputs
- Identify the most binding constraint for each monitored facility
- Combine energy and capacity study results
- Evaluate how project size affects the number of binding constraints

## Repository Structure

tara-deliverability-study-postprocessing

data/  
  raw_results_from_tara/  
    raw_capacity_deliverability_results.csv  
    raw_energy_fcitc_results.csv  

outputs/  
  constraints.csv  
  summary_results.csv  

src/  
  tara_postprocessing.py  

requirements.txt  
README.md  

## Technologies Used

Python  
pandas  

## How to Run

Clone the repository

git clone https://github.com/toniageagea/tara-deliverability-study-postprocessing.git

Install dependencies

pip install -r requirements.txt

Place raw study results in

data/raw_results_from_tara/

Run the script

python src/tara_postprocessing.py

## Output Files

The script generates two output files:

outputs/constraints.csv  
Contains the most limiting constraint for each monitored facility.

outputs/summary_results.csv  
Shows how the number of binding constraints changes as project injection size increases.
