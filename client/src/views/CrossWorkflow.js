/*eslint-disable*/
import cx from "bem-classnames"
import Footer from "components/Footers/Footer.js";
import IndexNavbar from "components/Navbars/IndexNavbar.js";
import React, {CSSProperties, useState} from "react";
import {Button, Form, InputGroup} from "react-bootstrap";
import {Link} from "react-router-dom";
import PropagateLoader from "react-spinners/PropagateLoader";
import {toast} from "react-toastify";
import 'reactjs-popup/dist/index.css';
import {DownloadModal} from "../components/DownloadModal/DownloadModal";
import useAnalyticsEventTracker from "../components/GoogleAnalyticsEventTracker/useAnalyticsEventTracker"
import {API_SERVER} from "../config/constant";
import "./ui-elements/InputToggleButton/InputToggleButton.scss"


export default function CrossWorkflow() {
    const gaEventTracker = useAnalyticsEventTracker('Cross Page');
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
        gaEventTracker('click-cross-start');

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

        fetch(API_SERVER + 'analyze/cross', {
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

    const [analyzeReady, setAnalyzeReady] = useState(false)

    const parallel =
        <>
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
                        {fileList ? fileLabelGroup : 'Choose files'}
                    </Form.Label>
                </div>
            </InputGroup>
        </div>


    const inputForm = <div className='flex flex-row justify-center pt-2'>
        <div>
            <p className="pl-1 text-xs text-blueGray-400">
                GenoCraft is committed to never storing your data or utilizing it for any other purposes.
            </p>
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
                1. 1_differential_analysis_significant_genes.txt {<a
                href="https://github.com/futianfan/GenoCraft/blob/main/server/demo_data/cross_data/bulk_differential_analysis_significant_genes.txt"
                className="text-c-blue"
            >
                (example)
            </a>}
            </p>
            <p className="pl-1 text-xs text-blueGray-400">
                2. 2_differential_analysis_significant_genes.txt {<a
                href="https://github.com/futianfan/GenoCraft/blob/main/server/demo_data/cross_data/protein_differential_analysis_significant_genes.txt"
                className="text-c-blue"
            >
                (example)
            </a>}
            </p>
            <p className="pl-1 text-xs text-blueGray-400"> * Check out the {<a
                href="https://github.com/futianfan/GenoCraft/blob/main/server/demo_data/cross_data/"
                className="text-c-blue"
            >
                folder
            </a>} for more</p>
            <p className="pl-1 text-xs text-blueGray-400 pb-5">
                 step-by-step input file examples.
            </p>
        </div>
        {fileInputGroup}
    </div>

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
                                    Cross Workflow
                                </h3>
                                <p className="mt-4 text-sm leading-relaxed text-blueGray-500">
                                    To initiate the analysis, please ensure that you upload your gene data or select the demo data. 
                                    We will then plot a Venn diagram to illustrate the relationships among different significant gene lists
                                    from the various pipelines.
                                </p>
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
