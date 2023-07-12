/*eslint-disable*/
import Footer from "components/Footers/Footer.js";

import IndexNavbar from "components/Navbars/IndexNavbar.js";
import React from "react";
import {Link} from "react-router-dom";
import useAnalyticsEventTracker from "../components/GoogleAnalyticsEventTracker/useAnalyticsEventTracker"

export default function Index() {
    const gaEventTracker = useAnalyticsEventTracker('Homepage');

    return (
        <>
            <IndexNavbar fixed/>
            <section className="header relative pt-16 items-center flex h-screen max-h-860-px">
                <div className="container mx-auto items-center flex flex-wrap">
                    <div className="w-full md:w-8/12 lg:w-6/12 xl:w-6/12 px-4">
                        <div className="pt-32 sm:pt-0">
                            <h2 className="font-semibold text-4xl text-blueGray-600">
                                GenoCraft - A powerful, all-in-one solution for omics data processing.
                            </h2>
                            <p className="mt-4 text-lg leading-relaxed text-blueGray-500">
                                GenoCraft is a comprehensive software solution designed to handle the entire pipeline of
                                omics data processing. It provides a streamlined, user-friendly interface for
                                researchers and data scientists to manage and analyze large-scale omics data.
                            </p>
                            <div className="mt-12">
                                <Link
                                    to="/analyze"
                                    className="get-started text-white font-bold px-6 py-4 rounded outline-none focus:outline-none mr-1 mb-1 bg-lightBlue-500 active:bg-lightBlue-600 uppercase text-sm shadow hover:shadow-lg ease-linear transition-all duration-150"
                                    onClick={()=>gaEventTracker('click-get-started')}
                                >
                                    Get started
                                </Link>
                                <a
                                    href="https://github.com/futianfan/GenoCraft"
                                    className="github-star ml-1 text-white font-bold px-6 py-4 rounded outline-none focus:outline-none mr-1 mb-1 bg-blueGray-700 active:bg-blueGray-600 uppercase text-sm shadow hover:shadow-lg ease-linear transition-all duration-150"
                                    target="_blank"
                                >
                                    Github Star
                                </a>
                            </div>
                        </div>
                    </div>
                </div>

                <img
                    className="absolute top-0 b-auto right-0 pt-16 sm:w-6/12 -mt-48 sm:mt-0 w-10/12 max-h-860px"
                    src={require("assets/img/pattern_react.png").default}
                    alt="..."
                />
            </section>
            <Footer/>
        </>
    );
}
