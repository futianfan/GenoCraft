/*eslint-disable*/
import cx from "bem-classnames"
import Footer from "components/Footers/Footer.js";
import IndexNavbar from "components/Navbars/IndexNavbar.js";
import React, {useState} from "react";
import {Button, Form, InputGroup} from "react-bootstrap";
import {API_SERVER} from "../config/constant";
import "./ui-elements/basic/InputToggleButton.scss"

export default function BulkRNAWorkflow() {

  const [uploadOwnFile, setUploadOwnFile] = useState(false)

  const handleUploadOwnFileOnClick = () => {
    setUploadOwnFile(true)
  }

  const handleUseDemoDataOnClick = () => {
    setUploadOwnFile(false)
  }

  const inputToggleClasses = {
    name: "InputToggle__toggles",
    state: ["active"],
  }

  const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const handleStartAnalysisClick = () => {
        if (uploadOwnFile && !file) {
            console.log("Please upload your own data!")
            return;
        }

        let data = new FormData()
        data.append('upload_own_file', uploadOwnFile)
        data.append('file', file)
        data.append('normalization', normalizationSelected)
        data.append('differential_analysis', differentialSelected)
        data.append('network_analysis', networkSelected)
        data.append('gene_set_enrichment_analysis', geneSelected)
        data.append('visualization', visualizationSelected)

        fetch(API_SERVER + 'analyze/bulk', {
            method: 'POST',
            body: data,
        })
            .then((res) => res.json())
            .then((data) => console.log(data))
            .catch((err) => console.error(err));
    };


  const [normalizationSelected, setNormalizationSelected] = useState(false)
  const [differentialSelected, setDifferentialSelected] = useState(false)
  const [networkSelected, setNetworkSelected] = useState(false)
  const [geneSelected, setGeneSelected] = useState(false)
  const [visualizationSelected, setVisualizationSelected] = useState(false)

  const workflowSteps = [
    {name: 'Normalization', isSelected: normalizationSelected, onClickFunction: ()=> setNormalizationSelected(!normalizationSelected)},
    {name: 'Differential Analysis', isSelected: differentialSelected, onClickFunction: ()=> setDifferentialSelected(!differentialSelected)},
    {name: 'Network Analysis', isSelected: networkSelected, onClickFunction: ()=> setNetworkSelected(!networkSelected)},
    {name: 'Gene Set Enrichment Analysis', isSelected:geneSelected , onClickFunction: ()=> setGeneSelected(!geneSelected)},
    {name: 'Visualization', isSelected: visualizationSelected, onClickFunction: ()=> setVisualizationSelected(!visualizationSelected)}
  ];

  const workflowBoxes = workflowSteps.map((content, idx) => (
      <>
        <div>
            <Button className="btn-rounded" key={idx} variant={content.isSelected ? 'outline-success' : 'outline-secondary'} onClick={content.onClickFunction} active={content.isSelected}>
              {content.isSelected ? <i className='feather icon-check-circle mx-1'></i> : <i className='feather icon-slash mx-1'></i>}
              {content.name}
            </Button>
        </div>
        <div>
          <i className="fas fa-sharp fa-light fa-arrow-down"></i>
        </div>
      </>
  ));

    const workflowSteps2 = [
    {name: 'Network Analysis', isSelected: networkSelected, onClickFunction: ()=> setNetworkSelected(!networkSelected)},
    {name: 'Gene Set Enrichment Analysis', isSelected:geneSelected , onClickFunction: ()=> setGeneSelected(!geneSelected)},
    {name: 'Visualization', isSelected: visualizationSelected, onClickFunction: ()=> setVisualizationSelected(!visualizationSelected)}
  ];

  const workflowBoxes2 = workflowSteps2.map((content, idx) => (
      <>
            <Button className="btn-rounded" key={idx} variant={content.isSelected ? 'outline-success' : 'outline-secondary'} onClick={content.onClickFunction} active={content.isSelected}>
              {content.isSelected ? <i className='feather icon-check-circle mx-1'></i> : <i className='feather icon-slash mx-1'></i>}
              {content.name}
            </Button>
      </>
  ));

    const workflowSteps3 = [
    {name: 'Normalization', isSelected: normalizationSelected, onClickFunction: ()=> setNormalizationSelected(!normalizationSelected)},
    {name: 'Differential Analysis', isSelected: differentialSelected, onClickFunction: ()=> setDifferentialSelected(!differentialSelected)},
  ];

    const workflowBoxes3 = workflowSteps3.map((content, idx) => (
        <>
            <div className='py-1'>
                <i className="fas fa-sharp fa-light fa-arrow-down"></i>
            </div>
            <div>
                <Button className="btn-rounded" key={idx}
                        variant={content.isSelected ? 'outline-success' : 'outline-secondary'}
                        onClick={content.onClickFunction} active={content.isSelected}>
                    {content.isSelected ? <i className='feather icon-check-circle mx-1'></i> :
                        <i className='feather icon-slash mx-1'></i>}
                    {content.name}
                </Button>
            </div>
        </>
    ));

  const [analyzeReady, setAnalyzeReady] = useState(false)

    const sequential =
        <>
            <div>
                <i className="fas fa-sharp fa-light fa-arrow-down"></i>
            </div>
            {workflowBoxes}
            <div>
                <Button className="btn-rounded"
                        variant={analyzeReady ? 'outline-success' : 'outline-secondary'}
                        onClick={handleStartAnalysisClick} active={analyzeReady}>
                    {analyzeReady ? <i className='feather icon-check-circle mx-1'></i> : null}
                    {analyzeReady ? 'Download Result' : 'Start'}
                </Button>
            </div>
        </>

  const parallel =
      <>
            {workflowBoxes3}
        <div className='flex flex-row py-2'>
          <i className="feather icon-arrow-down-left mx-1 font-weight-bolder"></i>
          <i className="feather icon-arrow-down mx-1 font-weight-bolder"></i>
          <i className="feather icon-arrow-down-right mx-1 font-weight-bolder"></i>
        </div>
        <div className='flex flex-row pb-2'>
          {workflowBoxes2}
        </div>
        <div className='flex flex-row pb-2'>
          <i className="feather icon-arrow-down-right mx-1 font-weight-bolder"></i>
          <i className="feather icon-arrow-down mx-1 font-weight-bolder"></i>
          <i className="feather icon-arrow-down-left mx-1 font-weight-bolder"></i>
        </div>
        <div>
          <Button className="btn-rounded"
                  variant={analyzeReady ? 'outline-success' : 'outline-secondary'}
                  onClick={handleStartAnalysisClick} active={analyzeReady}>
            {analyzeReady ? <i className='feather icon-check-circle mx-1'></i> : null}
            {analyzeReady ? 'Download Result' : 'Start'}
          </Button>
        </div>
      </>

    const inputForm = <div className='flex flex-col items-baseline pt-1'>
        <InputGroup>
            <div className="custom-file">
                <Form.Control
                    aria-describedby="custom-addons6"
                    type="file"
                    className="custom-file-input"
                    id="validatedCustomFile2"
                    onChange={handleFileChange}
                />
                <Form.Label className="custom-file-label" htmlFor="validatedCustomFile2">
                    {file ? `${file.name}` : 'Choose file'}
                </Form.Label>
            </div>
        </InputGroup>
        <p className="pl-1 text-xs text-blueGray-400">
            Only CSV files are supported.
        </p>
    </div>

    /*
<InputGroup.Append>
    <Button className="btn-sm border-0 text-blueGray-600 text-sm"
            variant={'outline-secondary'}
            onClick={handleStartAnalysisClick}
    >
        Upload
    </Button>
</InputGroup.Append>
*/

  return (
    <>
      <IndexNavbar fixed />
      <section className="block relative z-1 bg-blueGray-100">
        <div className="container mx-auto px-4 pb-32 pt-48">
          <div className="items-center flex flex-wrap">
            <div className="w-full md:w-5/12 ml-auto px-12 md:px-4">
              <div className="md:pr-12">
                <div className="text-blueGray-500 p-3 text-center inline-flex items-center justify-center w-16 h-16 mb-6 shadow-lg rounded-full bg-white">
                  <i className="fas fa-file-alt text-xl"></i>
                </div>
                <h3 className="text-3xl font-semibold">
                  Bulk RNA Workflow
                </h3>
                <p className="mt-4 text-sm leading-relaxed text-blueGray-500">
                    To initiate the analysis, please ensure that you select the specific steps you would like to include by clicking on the corresponding buttons within the right flowchart. If you choose not to select a button, the corresponding step will be skipped from the analysis.
                </p>
                <ul className="list-none mt-6">
                  <li className="py-2">
                    <div className="flex items-center">
                      <div>
                        <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-3">
                          <i className="fas fa-fingerprint"></i>
                        </span>
                      </div>
                      <div>
                        <h4 className="text-blueGray-500">
                           Normalization involves adjusting the raw gene expression measurements to minimize the effects of systematic technical differences, enabling more accurate comparison of gene expression levels across samples.
                        </h4>
                      </div>
                    </div>
                  </li>
                  <li className="py-2">
                    <div className="flex items-center">
                      <div>
                        <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-3">
                          <i className="fas fa-fingerprint"></i>
                        </span>
                      </div>
                      <div>
                        <h4 className="text-blueGray-500">
                          Differential Analysis involves identifying genes that are expressed differently between different conditions or groups. The goal is to find genes whose changes in expression levels are statistically significant.
                        </h4>
                      </div>
                    </div>
                  </li>
                  <li className="py-2">
                    <div className="flex items-center">
                      <div>
                        <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-3">
                          <i className="fas fa-fingerprint"></i>
                        </span>
                      </div>
                      <div>
                        <h4 className="text-blueGray-500">
                          Network Analysis involves the construction and analysis of gene networks. These networks can help identify key genes and pathways involved in the condition being studied.
                        </h4>
                      </div>
                    </div>
                  </li>
                    <li className="py-2">
                    <div className="flex items-center">
                      <div>
                        <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-3">
                          <i className="fas fa-fingerprint"></i>
                        </span>
                      </div>
                      <div>
                        <h4 className="text-blueGray-500">
                          Gene Set Enrichment Analysis (GSEA) is a computational method that determines whether an a priori defined set of genes shows statistically significant, concordant differences between two biological states (e.g., phenotypes).
                        </h4>
                      </div>
                    </div>
                  </li>
                    <li className="py-2">
                    <div className="flex items-center">
                      <div>
                        <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-3">
                          <i className="fas fa-fingerprint"></i>
                        </span>
                      </div>
                      <div>
                        <h4 className="text-blueGray-500">
                          The results of the analysis are visualized. This helps in interpreting the results and in generating hypotheses for further research.
                        </h4>
                      </div>
                    </div>
                  </li>
                </ul>

              </div>
            </div>

            <div className="w-full md:w-6/12 mr-auto px-4 pt-24 md:pt-0">
                <div className="flex flex-col items-center justify-center">
                  <div className="InputToggle">
                    <div className={cx(inputToggleClasses, {active: uploadOwnFile})}
                         onClick={handleUploadOwnFileOnClick}>
                      Upload Your Own Data
                    </div>
                    <div className={cx(inputToggleClasses, {active: !uploadOwnFile})}
                         onClick={handleUseDemoDataOnClick}>
                     Use Demo Data
                    </div>
                  </div>
                    {uploadOwnFile ? inputForm : null}
                  {parallel}
              </div>
            </div>
          </div>
        </div>
      </section>
      <Footer />
    </>
  );
}
