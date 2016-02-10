# Search Path By Locus API

### Description: Searches a path between two genes by locus

## Endpoints

### Search

### 
| Parameter Name                        | Requred | Description                                                      | Default        |
|---------------------------------------|---------|------------------------------------------------------------------|----------------|
| genes                                 | Yes     | locus/gene IDs. No more than two gene identifiers accepted.                                                    |                |
| pathalg                               | Yes     | network path algorithm                                           | allSimplePaths |
| steps                                 | Yes     | number of steps                                                  | 2              |
| showValidatedEdge                     | Yes     | display validated edge type                                      | True           |
| showPredictedEdge                     | Yes     | display predicted edge type                                      | True           |
| proteinModification                   | Yes     | protein modification edge type data filter                       | True           |
| showproteinModificationPredicted      | Yes     | protein modification predicted edge type data filter             | True           |
| ppiInteraction                        | Yes     | protein-protein interaction edge type data filter                | True           |
| showppiInteractionPredicted           | Yes     | protein-protein interaction edge type data filter                | True           |
| cpi                                   | Yes     | protein-protein interaction predicted edge type data filter      | True           |
| showcpiPredicted                      | Yes     | compound protein edge type edge type data filter                 | True           |
| geneExpressionRegulation              | Yes     | compound protein predicted edge type edge type data filter       | True           |
| showgeneExpressionRegulationPredicted | Yes     | TF-target gene regulation edge type descriptor                   | True           |
| srnaRegulation                        | Yes     | TF-target gene regulation predicted edge type descriptor         | True           |
| showsrnaRegulationPredicted           | Yes     | small RNA-target regulation edge type data filter                | True           |
| transportedMolecule                   | Yes     | small RNA-target regulation predicted edge type data filter      | True           |
| showtransportedMoleculePredicted      | Yes     | carrier and transported molecule edge type data filter           | True           |
| composition                           | Yes     | carrier and transported molecule predicted edge type data filter | True           |
| showcompositionPredicted              | Yes     | family/complex and member edge type data filter                  | True           |
| chemReaction                          | Yes     | cathalitycal chemical reaction edge type data filter             | True           |
| showchemReactionPredicted             | Yes     | cathalitycal chemical reaction predicted edge type data filter   | True           |
| coexpressedGenePair                   | Yes     | coexpressed gene pair edge type data filter                      | True           |
| showcoexpressedGenePairPredicted      | Yes     | coexpressed gene pair precited edge type data filter             | True           |
| coexpValueCutoff                      | Yes     | gene coexpression value cutoff with mutual information           | 0.8            |
| cutoffNodeRelationships               | Yes     | gene nodes relationships cutoff                                  | 100            |


## Resource Information

| Methods          | GET  |
|------------------|------|
| Response formats | json |

### List

	
* Not implemented

## API Developer Reference

[API Reference]
(https://rawgit.com/Arabidopsis-Information-Portal/hrgrn_webservices/master/doc/api/hrgrn_search_path_by_locus/index.html)

## Installation

[Installation Instructions](INSTALL.md)