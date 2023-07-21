/*eslint-disable*/
import axios from 'axios'
import cx from "bem-classnames"
import Footer from "components/Footers/Footer.js";
import IndexNavbar from "components/Navbars/IndexNavbar.js";
import fileDownload from 'js-file-download'
import React, {CSSProperties, useState} from "react";
import {Button, Form, InputGroup} from "react-bootstrap";
import {Link} from "react-router-dom";
import PropagateLoader from "react-spinners/PropagateLoader";
import {toast} from "react-toastify";
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import useAnalyticsEventTracker from "../components/GoogleAnalyticsEventTracker/useAnalyticsEventTracker"
import {API_SERVER} from "../config/constant";
import "./ui-elements/InputToggleButton/InputToggleButton.scss"
import {DownloadModal} from "../components/DownloadModal/DownloadModal";

export default function BulkRNAWorkflow() {
    const gaEventTracker = useAnalyticsEventTracker('Bulk Page');
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
        gaEventTracker('click-bulk-start');

        if (analyzeReady) {
            toast.error("Please make changes!", {
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
        data.append('normalization', normalizationSelected)
        data.append('visualization_after_normalization', visualizationAfterNormSelected)
        data.append('differential_analysis', differentialSelected)
        data.append('network_analysis', networkSelected)
        data.append('gene_set_enrichment_analysis', geneSelected)
        data.append('visualization', visualizationSelected)

        fetch(API_SERVER + 'analyze/bulk', {
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
                console.error(err)
                toast.error("Encounter an unknown error, please try again with different settings!", {
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
    const [normalizationSelected, setNormalizationSelected] = useState(false)
    const [visualizationAfterNormSelected, setVisualizationAfterNormSelected] = useState(false)
    const [differentialSelected, setDifferentialSelected] = useState(false)
    const [networkSelected, setNetworkSelected] = useState(false)
    const [geneSelected, setGeneSelected] = useState(false)
    const [visualizationSelected, setVisualizationSelected] = useState(false)

    const workflowSteps2 = [
        {
            name: 'Gene Set Enrichment Analysis', isSelected: geneSelected, onClickFunction: () => {
                setGeneSelected(!geneSelected);
                setAnalyzeReady(false);
                setLoading(false);
            }
        },
        {
            name: '(WIP)', isSelected: visualizationSelected, onClickFunction: () => {
                setVisualizationSelected(!visualizationSelected);
                setAnalyzeReady(false);
                setLoading(false);
            }
        }
    ];

    const workflowBoxes2 = workflowSteps2.map((content, idx) => (
        <>
            <Button className="btn-rounded" key={idx}
                    variant={content.isSelected ? 'outline-success' : 'outline-secondary'}
                    onClick={content.onClickFunction} active={content.isSelected}>
                {content.isSelected ? <i className='feather icon-check-circle mx-1'></i> :
                    <i className='feather icon-slash mx-1'></i>}
                {content.name}
            </Button>
        </>
    ));

    const workflowSteps3 = [
        {
            name: 'Quality Control', isSelected: qualityControlSelected, onClickFunction: () => {
                setQualityControlSelected(!qualityControlSelected);
                setAnalyzeReady(false);
                setLoading(false);
            }
        },
        {
            name: 'Normalization', isSelected: normalizationSelected, onClickFunction: () => {
                setNormalizationSelected(!normalizationSelected);
                setAnalyzeReady(false);
                setLoading(false);
            }
        },
        {
            name: 'Visualization', isSelected: visualizationAfterNormSelected, onClickFunction: () => {
                setVisualizationAfterNormSelected(!visualizationAfterNormSelected);
                setAnalyzeReady(false);
                setLoading(false);
            }
        },
        {
            name: 'Differential Analysis', isSelected: differentialSelected, onClickFunction: () => {
                setDifferentialSelected(!differentialSelected);
                setAnalyzeReady(false);
                setLoading(false);
            }
        },
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

    const parallel =
        <>
            {workflowBoxes3}
            <div className='flex flex-row py-2'>
                <i className="feather icon-arrow-down-left mx-1 font-weight-bolder"></i>
                <i className="feather icon-arrow-down-right mx-1 font-weight-bolder"></i>
            </div>
            <div className='flex flex-row pb-2'>
                {workflowBoxes2}
            </div>
            <div className='flex flex-row pb-2'>
                <i className="feather icon-arrow-down-right mx-1 font-weight-bolder"></i>
                <i className="feather icon-arrow-down-left mx-1 font-weight-bolder"></i>
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
        <div>
            <p className="pl-1 text-xs text-blueGray-400">
                * Please select and upload all the files at once.
            </p>
            <p className="pl-1 text-xs text-blueGray-400">
                * Please name the files as required.
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
                        {fileList ? fileLabelGroup : 'Choose multiple files'}
                    </Form.Label>
                </div>
            </InputGroup>
        </div>


    const inputForm = <div className='flex flex-row justify-center pt-2'>
        <div>
            <p className="pl-1 text-xs text-blueGray-400">
                Input Requirements:
            </p>
            <p className="pl-1 text-xs text-blueGray-400 ">
                * Only .txt/.csv files are supported
            </p>
            <p className="pl-1 pr-3 text-xs text-blueGray-400">
                * Please use comma as .csv file separator.
            </p>
            <p className="pl-1 text-xs text-blueGray-400">
                1. case_label.txt {<a
                href="https://github.com/futianfan/GenoCraft/blob/main/server/lib/case_label.txt"
                className="text-c-blue"
            >
                (example)
            </a>}
            </p>
            <p className="pl-1 text-xs text-blueGray-400">
                2. control_label.txt {<a
                href="https://github.com/futianfan/GenoCraft/blob/main/server/lib/control_label.txt"
                className="text-c-blue"
            >
                (example)
            </a>}
            </p>
            <p className="pl-1 text-xs text-blueGray-400 pb-5">
                3. read_counts.csv {<a
                href="https://github.com/futianfan/GenoCraft/blob/main/server/lib/read_counts.csv"
                className="text-c-blue"
            >
                (example)
            </a>}
            </p>
        </div>
        {fileInputGroup}
    </div>

    /*

    <p className="pl-1 text-xs text-blueGray-400">
                * Required by Normalization:
            </p>
            <p className="pl-1 text-xs text-blueGray-400">
                1. counts.csv,
            </p>
            <p className="pl-1 text-xs text-blueGray-400">
                2. gene_lengths.csv
            </p>
            <p className="pl-1 text-xs text-blueGray-400 pb-2">
                (Only CSV files are supported)
            </p>


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
        <div>
            <IndexNavbar fixed/>
            <section className="block relative z-1 bg-blueGray-100">
                <div className="container mx-auto px-4 pb-32 pt-48 bg-blueGray-100">
                    <div className="items-center flex flex-wrap bg-blueGray-100">
                        <div className="w-full md:w-5/12 ml-auto px-12 md:px-4">
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
                                    Bulk RNA Workflow
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
                                                    <strong>Quality Control (QC)</strong> removes a subset of rows to ensure data quality.
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
                                                    <strong>Normalization</strong> adjusts raw gene expression measurements for systematic technical differences.
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
                                                    <strong>Visualization</strong> generates intuitive from the data.
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
                                                    <strong>Differential Analysis</strong> identifies genes with statistically significant changes in expression levels between different conditions.
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
                                                    <strong>Gene Set Enrichment Analysis (GSEA)</strong> identifies biological pathways associated with differentially expressed genes.
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
                                                    <strong>Network Analysis</strong> constructs and analyzes gene networks to identify key genes and pathways. You can choose to skip this step if it is too time-consuming for your requirements.
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
        </div>
    );
}
