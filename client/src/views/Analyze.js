/*eslint-disable*/
import Footer from "components/Footers/Footer.js";

import IndexNavbar from "components/Navbars/IndexNavbar.js";
import React from "react";
import {Link} from "react-router-dom";

export default function Analyze() {
    return (
        <>
            <IndexNavbar fixed/>
            <section className="mt-48 md:mt-40 pb-40 relative bg-blueGray-400">
                <div className="justify-center text-center flex flex-wrap mt-24">
                    <div className="w-full md:w-6/12 px-12 md:px-4">
                        <h2 className="font-semibold text-4xl">GenoCraft workflow </h2>
                        <p className="text-lg leading-relaxed mt-4 mb-4 text-blueGray-500">
                            The process begins with data normalization and quality control, ensuring data reliability.
                            Advanced algorithms like T-SNE are then used for data visualization and pattern recognition.
                            Clustering techniques group similar data points together, revealing key trends. Differential
                            analysis allows for the comparison of different data sets, identifying unique patterns and
                            anomalies. The final step is pathway analysis, which provides a deeper understanding of the
                            underlying biological processes.
                        </p>
                    </div>
                </div>
            </section>

            <section className="pb-40 block relative z-1 bg-blueGray-600">
                <div className="container mx-auto">
                    <div className="justify-center flex flex-wrap">
                        <div className="w-full lg:w-12/12 px-4  -mt-24">
                            <div className="flex flex-auto flex-wrap justify-center">
                                <div className="w-full lg:w-4/12 px-4">
                                    <h5 className="text-xl font-semibold pb-4 text-center">
                                        Bulk RNA
                                    </h5>
                                    <Link to="/bulk-rna-workflow">
                                        <div
                                            className="hover:-mt-4 relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded-lg ease-linear transition-all duration-150">
                                            <img
                                                alt="..."
                                                className="align-middle border-none max-w-full h-auto rounded-lg"
                                                src={require("assets/images/BulkRNAWorkflow.png").default}
                                            />
                                        </div>
                                    </Link>
                                </div>

                                <div className="w-full lg:w-4/12 px-4">
                                    <h5 className="text-xl font-semibold pb-4 text-center">
                                        Single Cell RNA
                                    </h5>
                                    <Link to="/single-cell-rna-workflow">
                                        <div
                                            className="hover:-mt-4 relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded-lg ease-linear transition-all duration-150">
                                            <img
                                                alt="..."
                                                className="align-middle border-none max-w-full h-auto rounded-lg"
                                                src={require("assets/images/SingleCellRNA.png").default}
                                            />
                                        </div>
                                    </Link>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <Footer/>
        </>
    );
}
