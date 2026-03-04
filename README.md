# TARA Interconnection Study Post-Processing

Python pipeline for post-processing transmission constraint results from TARA grid studies.  
The script processes energy (FCITC) and capacity (deliverability) study outputs to identify the most limiting transmission constraints and evaluate the impact on potential project sizing.

This type of analysis is commonly used during generator interconnection studies to evaluate grid limitations and determine feasible project injection levels.

## Project Overview

During interconnection studies, transfer capability simulations generate large volumes of constraint results across monitored facilities and contingencies.  

This project demonstrates how Python and pandas can be used to:

• Parse raw constraint outputs from transmission studies  
• Identify the most binding constraint for each monitored facility  
• Combine energy and capacity study results  
• Evaluate how project size affects the number of binding constraints  

The workflow replicates a simplified version of post-processing commonly performed during generator interconnection analysis.

## Repository Structure

## Methodology

The script processes two types of study outputs:

Energy Study (FCITC)
Simulates incremental power injection at candidate interconnection buses and identifies which transmission facilities become overloaded.

Capacity Study (Deliverability)
Simulates ramping the most harmful generators to evaluate whether the project can deliver full capacity under contingency conditions.

The processing pipeline performs the following steps:

1. Load raw TARA study results
2. Extract study bus numbers and monitored facilities
3. Determine applicable ratings (Rate A or Rate B)
4. Compute injection thresholds
5. Identify the most constraining scenario per facility
6. Generate summarized constraint datasets

## Technologies Used

Python  
pandas  
First Contingency Incremental Transfer Capability TARA output results 

## Applications

This workflow is relevant for:

Generator interconnection studies  
Transmission constraint analysis  
Grid capacity evaluation for renewable projects  
Automation of power system study post-processing
