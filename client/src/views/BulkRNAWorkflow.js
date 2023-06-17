/*eslint-disable*/
import cx from "bem-classnames"
import Footer from "components/Footers/Footer.js";
import IndexNavbar from "components/Navbars/IndexNavbar.js";
import React, {useState} from "react";
import {Button} from "react-bootstrap";
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
                        onClick={() => {
                        }} active={analyzeReady}>
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
                  onClick={() => {
                  }} active={analyzeReady}>
            {analyzeReady ? <i className='feather icon-check-circle mx-1'></i> : null}
            {analyzeReady ? 'Download Result' : 'Start'}
          </Button>
        </div>
      </>


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
                <p className="mt-4 text-lg leading-relaxed text-blueGray-500">
                  This extension comes a lot of fully coded examples that help
                  you get started faster. You can adjust the colors and also the
                  programming language. You can change the text and images and
                  you're good to go.
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
                          Built by Developers for Developers
                        </h4>
                      </div>
                    </div>
                  </li>
                  <li className="py-2">
                    <div className="flex items-center">
                      <div>
                        <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-3">
                          <i className="fab fa-html5"></i>
                        </span>
                      </div>
                      <div>
                        <h4 className="text-blueGray-500">
                          Carefully crafted code for Components
                        </h4>
                      </div>
                    </div>
                  </li>
                  <li className="py-2">
                    <div className="flex items-center">
                      <div>
                        <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-3">
                          <i className="far fa-paper-plane"></i>
                        </span>
                      </div>
                      <div>
                        <h4 className="text-blueGray-500">
                          Dynamic Javascript Components
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
