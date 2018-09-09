# FAQ Track

## Intent 

To sieve out types of frequently asked questions from LSBPS / CJC cases.

## Scripts

### (1) `topicmodel_jl_lda_viz.ipynb`

* Text cleaning / processing
    - Removing stop words
    - Extracting noun phrases
    - Phrase Modelling

* Term frequency analysis

* Topic modelling using LDA


### (2) `lspbs-datatable.Rmd`

Interactive HTML widget for ad-hoc text search on case synopsis and advice sought verbatim,
as well as basic summary statistics of filtered cases.

### (3) `pytextrank-lspbs.ipynb` [Uncompleted]

Pytextrank, Co-occurrence network viz


## Possible areas for further work

### (1) Term / phrase co-occurrence analysis

- To drill down into deeper detail on the specific questions being asked
- Can use network visualizations to show relationships between different entities / phrases / words

### (2) Further development of the ad-hoc text search HTML widget

- Addition of custom search filter functionalities eg. EITHER-OR, OR, AND boolean searchess