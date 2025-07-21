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
  - 23 species display,click on the tissue icon to enter the "Explore".
  - Database Structure.
  - Plant CELLiD.
  - Statistics.
  - Follow iPscDB.
  - Update log.
  - Citation.
  <img width="1325" height="649" alt="878fa354bf85a510b9109264e0745e1b" src="https://github.com/user-attachments/assets/2f0ef830-7609-4096-966a-978b3a8b3ba5" />
  <img width="1243" height="810" alt="2fb58b67df01c58aa34158345542b09b" src="https://github.com/user-attachments/assets/890a5d94-570a-420d-a045-1e826bef6339" />
### Browse
- Function entry: Click the "Browse" tab in the navigation bar.
- Main function:
  - Species,Datasets,Experiments,Technologies,Atlases,Classic Markers,Marker genes,Cells,Cell types Quantity display
  - Cells,Sequencing technology,Markers Pie chart presentation
  - Dataset information List,support Species、Tissue、BioProject、Dataset search and data download
  <img width="1242" height="725" alt="b9b0bf2d820fb92ea99a43af343cc549" src="https://github.com/user-attachments/assets/9c53a67d-cbaa-4507-af9e-7da8bf251970" />
  <img width="1242" height="725" alt="8987c61a31c939771862a287cdd3bc02" src="https://github.com/user-attachments/assets/5512042c-e272-4344-a8f1-e43e8f949b6c" />
### Atlas
- Function entry: Click the "Atlas" tab in the navigation bar.
- Main function:
  - Species Atlas list
  - Tissue Atlas list
  - Click "Download" in each Atlas to download the corresponding data.
  - Click "Explore" in each Atlas to enter the corresponding "Explore" details page.
  <img width="5222" height="3810" alt="Figure2" src="https://github.com/user-attachments/assets/58f4e7d9-0fc6-45e8-860e-7cd523980916" />
### Marker 
- Function entry: Click the "Marker" tab in the navigation bar.
- Main function:The Marker module for cell marker exploration. (A) Overview of annotated cell types in 23 specific plant species. (B) Detailed information of a specific cell type (Arabidopsis root epidermis as an example). (C) Summarized marker information of a specific cell type in Arabidopsis. (D) Characterization and analysis of a specific marker gene. (E) Search function using different search engines.
  <img width="5222" height="3832" alt="Figure3" src="https://github.com/user-attachments/assets/51fc4fa8-80c8-4d9c-9a71-09df2ff01b2d" />
### Pipeline
#### Browse results
- Function entry: Click the "Pipeline -> Browse results" tab in the navigation bar.
- Main function:
  - Input E-mail and Analysis name, click Search to perform the task search.
  - Click Refresh button to reset the input E-mail and Analysis name.
  - Click Operation in the view button to enter the view task page.
  - Click Operation in the delete button to delete the task.
  <img width="2446" height="1270" alt="图片1" src="https://github.com/user-attachments/assets/0ddceebb-ae6f-4db4-90ae-4c6f54fb65e0" />
#### Start new job
- Function entry: Click the "Pipeline -> Start with fastq files" or "Pipeline -> Start with cellranger files" tab in the navigation bar.
- Main function: The input and output steps for the online data analysis pipeline. (A) Workflow and user input requirements of the online analysis pipeline. (B) User-defined analysis parameters via online data processing. (C) Supports drag-and-drop uploads of various file formats. (D) Interactive interface for viewing job completion and results. (E) Module for online UMAP figure editing.
  <img width="5222" height="3897" alt="Figure4" src="https://github.com/user-attachments/assets/903eda3c-e911-40ed-838d-4b9894890c37" />
### Tools
- Function entry: Click the Tools tab in the navigation bar.
- Main function: Diverse primary analysis tools of iPscDB. (A) The cross-species gene expression pattern of Gossypium hirsutum in Arabidopsis, rice and maize; (B) Expression pattern of GIF2 (AT1G01160) in Arabidopsis root as visualized in eSCP. (C) Developmental trajectory of the atrichoblast cell type in Arabidopsis root and information on differentially expressed genes (DEGs). (D) Cell type identification following two-rounds of prediction with Plant CellID.
  <img width="5222" height="3916" alt="Figure5" src="https://github.com/user-attachments/assets/25a4c40a-0024-4a3f-8d09-a16ef662e33f" />
### Documentation
- Function entry: Click the "Documentation" tab in the navigation bar.
- Main function: Display Overview,Datasets and usage,Contact us,Submit data.
<img width="1005" height="642" alt="2576215d4960b43842e6ab8a53f52896" src="https://github.com/user-attachments/assets/dc7667c4-d597-4ba8-a319-47c91869c09e" />