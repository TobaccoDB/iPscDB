# iPscDB
![17293d1c48780bb6fb9901ad9d14ac19](https://github.com/user-attachments/assets/7bffed40-96b3-4340-a57f-3b3023d4aadc)
- System website: https://www.tobaccodb.org/ipscdb/homePage
- Demo video: https://www.tobaccodb.org/server_ipscdb/source_material/other/ipscdb.mp4
## Abstract
The rapid advancement of single-cell technologies has significantly enhanced our ability to investigate cellular diversity and heterogeneity within plant tissues. However, analyzing this complexity in plants involves generating different data types to enable marker selection, cell identification, and other computational operations. These processes typically require broad programming expertise, posing a challenge for researchers with a limited computational background. To address this, we present iPscDB, a comprehensive and multifunctional platform that facilitates the integration and analysis of plant single-cell data. iPscDB combines over 3.5 million cells and 274 thousand markers derived from 789 experiments, covering 35 tissue types and 276 annotated cell types across 23 plant species. More importantly, the platform provides a user-friendly online analysis pipeline capable of processing raw FASTQ files. Users can configure parameters via an intuitive interface and utilize an integrated image editor to customize visualization outputs such as UMAP plots. Additionally, iPscDB supports various analyses such as those related to cross-species gene expression, cell-cell interactions, electronic single-cell pictography, and developmental trajectory. By streamlining the complex workflows of single-cell transcriptomics, iPscDB offers a powerful yet accessible solution for researchers with diverse technical backgrounds. iPscDB is accessible at https://www.tobaccodb.org/ipscdb/homePage.

## Operating guide
### Home
- Function entry: Users can access the system website (https://www.tobaccodb.org/ipscdb/homePage) or click the "Home" tab in the navigation bar.
- Main function:
  - 23 species display,click on the organization icon to enter the corresponding "Explore" function.
  - Database Structure.
  - Plant CELLiD.
  - Statistics.
  - Follow iPscDB.
  - Update log.
  - Citation.

### Browse
- Function entry: Click the "Browse" tab in the navigation bar.
- Main function:
  - Species,Datasets,Experiments,Technologies,Atlases,Classic Markers,Marker genes,Cells,Cell types Quantity display
  - Cells,Sequencing technology,Markers Pie chart presentation
  - Dataset information List,support Species、Tissue、BioProject、Dataset search and data download
### Atlas
- Function entry: Click the "Atlas" tab in the navigation bar.
- Main function:
  - Species Atlas list
  - Tissue Atlas list
  - Click "Download" in each Atlas to download the corresponding data.
  - Click "Explore" in each Atlas to enter the corresponding Atlas details page.
### Explore
- Function entry: Click the "Explore" tab in the navigation bar.
- Main function:
  - Support Umap and tSNE selection.
  - Marker list presentation.
  - Detail list presentation.
  - Support View by filtering and Gene input click GO button to enter gene details.
### Marker
- Function entry: Click the "Marker" tab in the navigation bar.
- Main function:
  - Species selection.
  - Classic Markers and Marker genes quantity presentation.
  - Click on the tissue details to show.
### Search
- Function entry: Click the "Search" tab in the navigation bar.
- Main function:
  - By marker gene (identifier or keyword) search.
  - By sequence (Blast) search.
  - By cell type search.
  - Input or select the corresponding data and click the Search button to enter the list page.
  - In the list page, click on the corresponding GeneID to enter the details page.
### Pipeline
#### Browse results
- Function entry: Click the "Pipeline -> Browse results" tab in the navigation bar.
- Main function:
  - Input E-mail and Analysis name, click Search to perform the task search.
  - Click Refresh button to reset the input E-mail and Analysis name.
  - Click Operation in the view button to enter the view task page.
  - Click Operation in the delete button to delete the task.
#### Start with fastq files
- Function entry: Click the "Pipeline -> Start with fastq files" tab in the navigation bar.
- Main function:
  - Cell ranger: Input Email, Analysis name, Species, Tissue, create an analysis task. Users upload two sets of analysis data, Data1 and Data2. For each set, they need to input Sample Name data and can upload up to three sets of analysis data files. Each set of data needs to upload four data files, namely R1, L1, R2, L2, for data analysis. And it supports viewing of the analysis results.
  - Sample QC: Input PT, MT and QC filter data for data analysis, And it supports viewing of the analysis results.
  - Data process: Input parameters such as Normalize Data, FindVariableFeatures Data, Scale Data and Neighbor Data for data analysis. And it supports viewing of the analysis results.
  - Cluster: Input the Resolution parameter for data analysis, And it supports viewing of the analysis results.
  - Cell Annotation: Can modify the parameters of the UMAP graph through the icon tools and download the heatmap, dotplot and tracksplot graphs.
#### Start with cellranger files
- Function entry: Click the "Pipeline -> Start with cellranger files" tab in the navigation bar.
- Main function:
  - Sample QC: Inputs Email, Analysis name, Species, Tissue to create an analysis task. The user then uploads two sets of analysis data, Data1 and Data2. For each set, the Sample Name data needs to be input and the File Type needs to be selected. If the option "GZ" is chosen, Barcodes, Features and Matrix need to be uploaded. If the option "H5AD" is chosen, the H5ad file needs to be uploaded. The analysis task can be started by inputting mt and pt data. The analysis results can also be viewed.
  - Data process: Input parameters such as Normalize Data, FindVariableFeatures Data, Scale Data and Neighbor Data for data analysis. And it supports viewing of the analysis results.
  - Cluster: Input the Resolution parameter for data analysis, And it supports viewing of the analysis results.
  - Cell Annotation: Can modify the parameters of the UMAP graph through the icon tools and download the heatmap, dotplot and tracksplot graphs.
### Tools
#### Tools->Cross-species gene expression
- Function entry: Click the Tools->Cross-species gene expression tab in the navigation bar.
- Main function: Select "Specie", "Tissue" and "Input GeneID", then click "GO" to display the UMAP visualization of cell types, Gene expression, and Expression in cell types data presentation.
#### Tools->Developmental trajectory
- Function entry: Click the Tools->Developmental trajectory tab in the navigation bar.
- Main function: Select "Specie", "Tissue" and "Cell type", then click "GO" to display the Pseudotime, State, Cell Type, Cluster graph.
#### Tools->electronic Single-Cell Pictograph
- Function entry: Click the Tools->electronic Single-Cell Pictograph tab in the navigation bar.
- Main function: Select "Specie", "Tissue" and "Input GeneID". Then click "GO".
#### Tools->Plant CelliD
- Function entry: Click the Tools->Plant CelliD tab in the navigation bar.
- Main function: Select "Specie", "Tissue" and "Upload File". Click "Run" to perform the comparison, and click "Download" to obtain the result.
#### Tools->Plant Cell-Blast
- Function entry: Click the Tools->Plant Cell-Blast tab in the navigation bar.
- Main function: Select "Specie", "Tissue" and upload files. Click "Run". Through the process of START -> HITS -> PREDICT -> PREDICTIONS, the results will be compared.
  
### Documentation
- Function entry: Click the "Documentation" tab in the navigation bar.
- Main function: Overview,Datasets and usage,Contact us,Submit data display.
