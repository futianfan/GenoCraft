/*eslint-disable*/
import cx from "bem-classnames"
import Footer from "components/Footers/Footer.js";
import IndexNavbar from "components/Navbars/IndexNavbar.js";
import React, {CSSProperties, useState} from "react";
import {Button, Form, InputGroup} from "react-bootstrap";
import {Link} from "react-router-dom";
import PropagateLoader from "react-spinners/PropagateLoader";
import {toast} from "react-toastify";
import {DownloadModal} from "../components/DownloadModal/DownloadModal";
import useAnalyticsEventTracker from "../components/GoogleAnalyticsEventTracker/useAnalyticsEventTracker"
import {API_SERVER} from "../config/constant";
import "./ui-elements/InputToggleButton/InputToggleButton.scss"

export default function ProteinWorkflow() {
    const gaEventTracker = useAnalyticsEventTracker('Protein Page');
    const [uploadOwnFile, setUploadOwnFile] = useState(false)
    const [loading, setLoading] = useState(false);
    const override: CSSProperties = {
        display: "block",
        margin: "0 auto",
        borderColor: "red",
    };

    const handleUploadOwnFileOnClick = () => {
        setUploadOwnFile(true)
        setAnalyzeReady(false);
        setLoading(false);
    }

    const handleUseDemoDataOnClick = () => {
        setUploadOwnFile(false)
        setAnalyzeReady(false);
        setLoading(false);
    }

    const inputToggleClasses = {
        name: "InputToggle__toggles",
        state: ["active"],
    }

    const [fileList, setFileList] = useState(null);
    const [outputFileList, setOutputFileList] = useState(null)


    const handleFileChange = (e) => {
        if (e.target.files) {
            setFileList(e.target.files);
        }
    };

    const handleStartAnalysisClick = () => {
        gaEventTracker('click-protein-start');
        if (analyzeReady) {
            toast.error("The current steps have already been analyzed, please select or unselect to restart.", {
                position: "top-right",
                autoClose: 4000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
                theme: "light",
            })
            return;
        }

        if (uploadOwnFile && !fileList) {
            console.log("Please upload your own data!")
            toast.error("Please upload your data!", {
                position: "top-right",
                autoClose: 4000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
                theme: "light",
            })
            return;
        }
        setLoading(true)
        const data = new FormData()
        data.append('upload_own_file', uploadOwnFile)
        data.append('number_of_files', files.length)

        files.forEach((file, idx) => {
            data.append(`file-${idx}`, file);
        });

        data.append('quality_control', qualityControlSelected)
        data.append('imputation', imputationSelected)
        data.append('normalization', normalizationSelected)
        data.append('visualization', visualizationSelected)
        data.append('differential_analysis', differentialSelected)
        data.append('network_analysis', networkSelected)
        data.append('pathway_analysis', pathwaySelected)
        data.append('runall', runallSelected)


        fetch(API_SERVER + 'analyze/protein', {
            method: 'POST',
            body: data,
        })
            .then((res) => res.json())
            .then((data) => {
                setLoading(false)
                if (data?.success) {
                    setAnalyzeReady(true)
                    setOutputFileList(data?.results)
                }
                if (!data?.success) {
                    toast.error(data?.msg, {
                        position: "top-right",
                        autoClose: 4000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: true,
                        progress: undefined,
                        theme: "light",
                    })
                }
            })
            .catch((err) => {
                setLoading(false);
                toast.error("We apologize for the inconvenience, but an unexpected error has occurred. Please consider trying again with alternative data or adjusting your settings.", {
                    position: "top-right",
                    autoClose: 4000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                    theme: "light",
                })
            });
    };

    const [qualityControlSelected, setQualityControlSelected] = useState(false)
    const [imputationSelected, setImputationSelected] = useState(false)
    const [normalizationSelected, setNormalizationSelected] = useState(false)
    const [clusteringSelected, setClusteringSelected] = useState(false)
    const [differentialSelected, setDifferentialSelected] = useState(false)
    const [networkSelected, setNetworkSelected] = useState(false)
    const [pathwaySelected, setPathwaySelected] = useState(false)
    const [visualizationSelected, setVisualizationSelected] = useState(false)
    const [runallSelected, setrunallSelected] = useState(false)

    const workflowSteps2 = [
        {
            name: 'Gene Set Enrichment Analysis', isSelected: pathwaySelected, onClickFunction: () => {
                setPathwaySelected(!pathwaySelected);
                setAnalyzeReady(false);
                setLoading(false)
            }
        },
        {
            name: '(WIP)', isSelected: networkSelected, onClickFunction: () => {
                setNetworkSelected(!networkSelected);
                setAnalyzeReady(false);
                setLoading(false)
            }
        },
    ];

    const workflowBoxes2 = workflowSteps2.map((content, idx) => (
        <div>
            <div>
                <Button className="btn-rounded" key={idx}
                        variant={content.isSelected ? 'outline-success' : 'outline-secondary'}
                        onClick={content.onClickFunction} active={content.isSelected}>
                    {content.isSelected ? <i className='feather icon-check-circle mx-1'></i> :
                        <i className='feather icon-slash mx-1'></i>}
                    {content.name}
                </Button>
            </div>
            {content?.requirements ? <div>
                <div className='text-xs text-blueGray-400 py-1'>
                    {content?.requirements?.prerequisite ? `Prerequisite: ${content?.requirements?.prerequisite}` : null}
                </div>
                <div className='text-xs text-blueGray-400'>
                    {content?.requirements?.input ? `Input: ${content?.requirements?.input}` : null}
                </div>
                <div className='text-xs text-blueGray-400 py-1'>
                    {content?.requirements?.output ? `Output: ${content?.requirements?.output}` : null}
                </div>
            </div> : <p>{content?.requirements}</p>
            }
        </div>
    ));

    const workflowSteps3 = [
        {
            name: 'Quality Control (Optional)', isSelected: qualityControlSelected, onClickFunction: () => {
                setQualityControlSelected(!qualityControlSelected);
                setAnalyzeReady(false);
                setLoading(false)
            }
        },
        {
            name: 'Imputation (Optional)', isSelected: imputationSelected, onClickFunction: () => {
                setImputationSelected(!imputationSelected);
                setAnalyzeReady(false);
                setLoading(false)
            }
        },
        {
            name: 'Normalization', isSelected: normalizationSelected, onClickFunction: () => {
                setNormalizationSelected(!normalizationSelected);
                setAnalyzeReady(false);
                setLoading(false)
            }
        },
        {
            name: 'Normalization Visualization (Optional)', isSelected: visualizationSelected, onClickFunction: () => {
                setVisualizationSelected(!visualizationSelected);
                setAnalyzeReady(false);
                setLoading(false)
            }
        },
        {
            name: 'Differential Analysis', isSelected: differentialSelected, onClickFunction: () => {
                setDifferentialSelected(!differentialSelected);
                setAnalyzeReady(false);
                setLoading(false)
            }
        },
        {
            name: 'Gene Set Enrichment Analysis (GSEA)', isSelected: pathwaySelected, onClickFunction: () => {
                setPathwaySelected(!pathwaySelected);
                setAnalyzeReady(false);
                setLoading(false)
            }
        },
        {
            name: 'Run All', isSelected: runallSelected, onClickFunction: () => {
                setQualityControlSelected(true);
                setImputationSelected(true);
                setNormalizationSelected(true);
                setVisualizationSelected(true);
                setDifferentialSelected(true);
                setPathwaySelected(true);

                setrunallSelected(true);
                setAnalyzeReady(false);
                setLoading(false)
            }
        },
    ];

    /*

            requirements: {
                input: "normalized_read_counts.csv",
                output: "differential_analysis_significant_gene.csv, differential_analysis_heatmap.png",
                prerequisite: "Normalization"
            }
     */

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
            {content?.requirements ? <div>
                <div className='text-xs text-blueGray-400 py-1'>
                    {content?.requirements?.prerequisite ? `Prerequisite: ${content?.requirements?.prerequisite}` : null}
                </div>
                <div className='text-xs text-blueGray-400'>
                    {content?.requirements?.input ? `Input: ${content?.requirements?.input}` : null}
                </div>
                <div className='text-xs text-blueGray-400 py-1'>
                    {content?.requirements?.output ? `Output: ${content?.requirements?.output}` : null}
                </div>
            </div> : <p>{content?.requirements}</p>
            }
        </>
    ));

    const [analyzeReady, setAnalyzeReady] = useState(false)

    const parallel =
        <>
            {workflowBoxes3}
            <div className='py-1'>
                <i className="fas fa-sharp fa-light fa-arrow-down"></i>
            </div>
            <div>
                <Button className="btn-rounded"
                        variant={analyzeReady ? 'outline-success' : 'outline-secondary'}
                        onClick={handleStartAnalysisClick} active={analyzeReady}>
                    {analyzeReady ? <i className='feather icon-check-circle mx-1'></i> : null}
                    {analyzeReady ? 'Results are ready!' : 'Start'}
                </Button>
            </div>
            <div>
                {analyzeReady && outputFileList?.length ? <DownloadModal outputFileList={outputFileList}/> : null}
            </div>
        </>

    const files = fileList ? [...fileList] : new Array(1).fill(null);
    const fileLabelGroup = files.map((file, idx) => (
        <p>
            {file !== null ? `file ${idx + 1} - ${file.name}` : null}
        </p>
    ))

    const fileInputGroup =
        <div >
            <p className="pl-1 text-xs text-blueGray-400">
                * Please select and upload all the files at once.
            </p>
            <InputGroup>
                <div className="custom-file">
                    <Form.Control
                        aria-describedby="custom-addons6"
                        type="file"
                        className="custom-file-input"
                        id="validatedCustomFile2"
                        onChange={handleFileChange}
                        multiple
                    />
                    <Form.Label className="custom-file-label" htmlFor="validatedCustomFile2">
                        {fileList ? fileLabelGroup : 'Choose files'}
                    </Form.Label>
                </div>
            </InputGroup>
        </div>


    const inputForm = <div className='flex flex-row justify-center pt-2'>
        <div className="w-30 pr-5">
            <p className="pl-1 text-xs text-blueGray-400">
                GenoCraft is committed to never storing your data or utilizing it for any other purposes.
            </p>
            <p className="pl-1 text-xs text-blueGray-400">
                * Required Input:
            </p>
            <p className="pl-1 text-xs text-blueGray-400">
                1. read_counts.csv {<a
                href="https://github.com/futianfan/GenoCraft/blob/main/server/demo_data/protein_data/read_counts.csv"
                className="text-c-blue"
            >
                (example)
            </a>}
            </p>
            <p className="pl-1 text-xs text-blueGray-400">
                2. case_label.txt {<a
                href="https://github.com/futianfan/GenoCraft/blob/main/server/demo_data/protein_data/case_label.txt"
                className="text-c-blue"
            >
                (example)
            </a>}
            </p>
            <p className="pl-1 text-xs text-blueGray-400">
                3. control_label.txt {<a
                href="https://github.com/futianfan/GenoCraft/blob/main/server/demo_data/protein_data/control_label.txt"
                className="text-c-blue"
            >
                (example)
            </a>}
            </p>
            <p className="pl-1 text-xs text-blueGray-400">
                * Please name the files as required.
            </p>
            <p className="pl-1 text-xs text-blueGray-400">
                (Please use comma as .csv file separator.)
            </p>
            <p className="pl-1 text-xs text-blueGray-400"> * Check out the {<a
                href="https://github.com/futianfan/GenoCraft/blob/main/server/demo_data/protein_data/"
                className="text-c-blue"
            >
                folder
            </a>} for more</p>
            <p className="pl-1 text-xs text-blueGray-400 pb-5">
                 step-by-step input file examples.
            </p>
        </div>
        <div className="w-70">
            {fileInputGroup}
        </div>
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

    /*
    WIP <i className="fas fa-wrench text-xl"></i>
     */
    return (
        <>
            <IndexNavbar fixed/>
            <section className="block relative z-1 bg-blueGray-100">
                <div className="container mx-auto px-4 pb-32 pt-48 bg-blueGray-100">
                    <div className="items-center flex flex-wrap bg-blueGray-100">
                        <div className="w-full md:w-5/12 ml-auto px-12 md:px-4 bg-blueGray-100">
                            <div className="md:pr-12">
                                <div
                                    className="text-blueGray-500 p-3 text-center inline-flex items-center justify-center w-16 h-16 mb-6 shadow-lg rounded-full bg-white">
                                    <Link
                                        to="/analyze"
                                    >
                                        <i className="fas fa-arrow-left text-xl"></i>
                                    </Link>
                                </div>
                                <h3 className="text-3xl font-semibold">
                                    Protein Workflow
                                </h3>
                                <p className="mt-4 text-sm leading-relaxed text-blueGray-500">
                                    To initiate the analysis, please ensure that you select the specific steps you would
                                    like to include by clicking on the corresponding buttons within the right flowchart.
                                    If you choose not to select a button, the corresponding step will be skipped from
                                    the analysis.
                                </p>
                                <ul className="list-none mt-6">
                                    <li className="py-2">
                                        <div className="flex items-center">
                                            <div>
                        <span
                            className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-3">
                          <i className="fas fa-fingerprint"></i>
                        </span>
                                            </div>
                                            <div>
                                                <h4 className="text-blueGray-500">
                                                    <strong>Quality Control (QC)</strong> ensures the protein data is
                                                    accurate, consistent, and reliable.
                                                </h4>
                                            </div>
                                        </div>
                                    </li>
                                    <li className="py-2">
                                        <div className="flex items-center">
                                            <div>
                        <span
                            className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-3">
                          <i className="fas fa-fingerprint"></i>
                        </span>
                                            </div>
                                            <div>
                                                <h4 className="text-blueGray-500 pb-2">
                                                    <strong>Imputation</strong> uses advanced statistical methods to
                                                    estimate and fill in missing protein data.


                                                </h4>
                                            </div>
                                        </div>
                                    </li>

                                    <li className="py-2">
                                        <div className="flex items-center">
                                            <div>
                                                                        <span
                                                                            className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-3">
                          <i className="fas fa-fingerprint"></i>
                        </span>
                                            </div>
                                            <div>
                                                <h4 className="text-blueGray-500">
                                                    <strong>Normalization</strong> adjusts raw protein expression
                                                    measurements to reduce systematic technical differences.
                                                </h4>
                                            </div>
                                        </div>
                                    </li>

                                    <li className="py-2">
                                        <div className="flex items-center">
                                            <div>
                        <span
                            className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-3">
                          <i className="fas fa-fingerprint"></i>
                        </span>
                                            </div>
                                            <div>
                                                <h4 className="text-blueGray-500">
                                                    <strong>Visualization</strong> creates intuitive and informative
                                                    plots of your protein data.
                                                </h4>
                                            </div>
                                        </div>
                                    </li>
                                    <li className="py-2">
                                        <div className="flex items-center">
                                            <div>

                        <span
                            className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-3">
                          <i className="fas fa-fingerprint"></i>
                        </span>
                                            </div>
                                            <div>
                                                <h4 className="text-blueGray-500">
                                                    <strong>Differential Analysis</strong> identifies proteins with
                                                    statistically significant changes in expression levels between
                                                    different conditions.
                                                </h4>
                                            </div>
                                        </div>
                                    </li>

                                    <li className="py-2">
                                        <div className="flex items-center">
                                            <div>

                        <span
                            className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-3">
                          <i className="fas fa-fingerprint"></i>
                        </span>
                                            </div>
                                            <div>
                                                <h4 className="text-blueGray-500">
                                                    <strong>Gene Set Enrichment Analysis (GSEA) </strong> identifies
                                                    biological pathways associated with differentially expressed
                                                    proteins.
                                                </h4>
                                            </div>
                                        </div>
                                    </li>

                                    <li className="py-2">
                                        <div className="flex items-center">
                                            <div>

                        <span
                            className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-3">
                          <i className="fas fa-fingerprint"></i>
                        </span>
                                            </div>
                                            <div>
                                                <h4 className="text-blueGray-500">
                                                    <strong>Network Analysis</strong> constructs and analyzes protein
                                                    networks to identify key proteins and pathways.
                                                </h4>
                                            </div>
                                        </div>
                                    </li>
                                </ul>

                            </div>
                        </div>

                        <div className="w-full md:w-6/12 mr-auto px-4 pt-24 md:pt-0 bg-blueGray-100">
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
                                <PropagateLoader className="py-10 pr-3"
                                                 color={'#1ae2a3'}
                                                 loading={loading}
                                                 cssOverride={override}
                                                 size={10}
                                                 aria-label="Loading Spinner"
                                                 data-testid="loader"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <Footer/>
        </>
    );
}

/*
             <span
                        className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-3">
                      <i className="fas fa-fingerprint"></i>
                    </span>
                                        </div>
                                        <div>
                                            <h4 className="text-blueGray-500">
                                                Network Analysis involves the construction and analysis of gene
                                                networks. These networks can help identify key genes and pathways
                                                involved in the condition being studied.
                                            </h4>
                                        </div>
                                    </div>
                                </li>
                                <li className="py-2">
                                    <div className="flex items-center">
                                        <div>
 */
