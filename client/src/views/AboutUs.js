import Footer from "components/Footers/Footer.js";

// components
import Navbar from "components/Navbars/IndexNavbar.js";
import React from "react";

export default function AboutUs() {
    return (
        <>
            <Navbar transparent/>
            <main>
                <section className="pt-20 pb-48">
                    <div className="container mx-auto px-4">
                        <div className="flex flex-row pt-32">
                            <div className="w-full md:w-6/12 lg:w-4/12 lg:mb-0 mb-12 px-4">
                                <div className="px-6">
                                    <img
                                        alt="..."
                                        src={require("assets/img/yingzhou-lu.jpeg").default}
                                        className="shadow-lg rounded-full mx-auto max-w-120-px"
                                    />
                                    <div className="pt-6 text-center">
                                        <h5 className="text-xl font-bold">Yingzhou Lu</h5>
                                        <p className="mt-1 text-sm text-blueGray-400 font-semibold">
                                            Postdoctoral Researcher at Standard University
                                        </p>
                                        <div className="mt-6">
                                            <button
                                                className="bg-lightBlue-400 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                type="button"
                                            >
                                                <i className="fab fa-twitter"></i>
                                            </button>
                                            <button
                                                className="bg-lightBlue-600 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                type="button"
                                            >
                                                <i className="fab fa-facebook-f"></i>
                                            </button>
                                            <button
                                                className="bg-pink-500 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                type="button"
                                            >
                                                <i className="fab fa-dribbble"></i>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="w-full md:w-6/12 lg:w-4/12 lg:mb-0 mb-12 px-4">
                                <div className="px-6">
                                    <img
                                        alt="..."
                                        src={require("assets/img/minjie-shen.jpeg").default}
                                        className="shadow-lg rounded-full mx-auto max-w-120-px"
                                    />
                                    <div className="pt-6 text-center">
                                        <h5 className="text-xl font-bold">Minjie Shen</h5>
                                        <p className="mt-1 text-sm text-blueGray-400 font-semibold">
                                            Software Engineer at Realtor.com
                                        </p>
                                        <p className="mt-1 text-sm text-blueGray-400 font-semibold">
                                            Ex-Research Assistant at Virginia Tech
                                        </p>
                                        <div className="mt-6">
                                            <a href="https://www.linkedin.com/in/minjie-shen96/">
                                                <button
                                                    className="bg-lightBlue-600 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                    type="button"
                                                >
                                                    <i className="fab fa-linkedin"></i>
                                                </button>
                                            </a>
                                            <a href="https://scholar.google.com/citations?user=Fan38-QAAAAJ&hl=en">
                                                <button
                                                    className="bg-lightBlue-500 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                    type="button"
                                                >
                                                    <i className="fa fa-graduation-cap" aria-hidden="true"></i>
                                                </button>
                                            </a>
                                            <a href="https://github.com/MinjieSh">
                                                <button
                                                    className="bg-blueGray-700 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                    type="button"
                                                >
                                                    <i className="fab fa-github"></i>
                                                </button>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="w-full md:w-6/12 lg:w-4/12 lg:mb-0 mb-12 px-4">
                                <div className="px-6">
                                    <img
                                        alt="..."
                                        src={require("assets/img/tianfan-fu.jpeg").default}
                                        className="shadow-lg rounded-full mx-auto max-w-120-px"
                                    />
                                    <div className="pt-6 text-center">
                                        <h5 className="text-xl font-bold">Tianfan Fu</h5>
                                        <p className="mt-1 text-sm text-blueGray-400 font-semibold">
                                            Incoming Assistant Professor at Rensselaer Polytechnic Institute
                                        </p>
                                        <div className="mt-6">
                                            <button
                                                className="bg-red-600 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                type="button"
                                            >
                                                <i className="fab fa-google"></i>
                                            </button>
                                            <button
                                                className="bg-lightBlue-400 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                type="button"
                                            >
                                                <i className="fab fa-twitter"></i>
                                            </button>
                                            <button
                                                className="bg-blueGray-700 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                type="button"
                                            >
                                                <i className="fab fa-instagram"></i>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <section className="relative py-20">
                    <div
                        className="bottom-auto top-0 left-0 right-0 w-full absolute pointer-events-none overflow-hidden -mt-20 h-20"
                        style={{transform: "translateZ(0)"}}
                    >
                        <svg
                            className="absolute bottom-0 overflow-hidden"
                            xmlns="http://www.w3.org/2000/svg"
                            preserveAspectRatio="none"
                            version="1.1"
                            viewBox="0 0 2560 100"
                            x="0"
                            y="0"
                        >
                            <polygon
                                className="text-blueGray-100 fill-current"
                                points="2560 0 2560 100 0 100"
                            ></polygon>
                        </svg>
                    </div>

                    <div className="container mx-auto px-4">
                        <div className="items-center flex flex-row">

                            <div className="w-full md:w-5/12 ml-auto mr-auto px-4">
                                <div className="md:pr-12">
                                    <div
                                        className="text-lightBlue-600 p-3 text-center inline-flex items-center justify-center w-16 h-16 mb-6 shadow-lg rounded-full bg-lightBlue-300">
                                        <i className="fas fa-rocket text-xl"></i>
                                    </div>
                                    <h3 className="text-3xl font-semibold">Yingzhou (Minta) Lu</h3>
                                    <p className="mt-4 text-lg leading-relaxed text-blueGray-500">
                                        Yingzhou Lu is a postdoctoral researcher at Stanford University, she obtained
                                        her Ph.D. in Artificial
                                        Intelligence and Computational Biology from Virginia Tech. With eight years of
                                        expertise in machine learning and genomics, she has cultivated a
                                        deep understanding of Next-Generation Sequencing
                                        (NGS) data analysis, graph theory and multi-omics
                                        data integration. Her research focuses on employing advanced computational
                                        techniques to analyze
                                        genomics datasets, aiming to shed light on disease
                                        development and progression.
                                    </p>
                                </div>
                            </div>
                            <div className="w-full md:w-4/12 ml-auto mr-auto px-4">
                                <img
                                    alt="..."
                                    className="max-w-full rounded-lg shadow-lg"
                                    src="https://images.unsplash.com/photo-1555212697-194d092e3b8f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=634&q=80"
                                />
                            </div>
                        </div>
                    </div>
                </section>

                <section className="relative py-20">
                    <div
                        className="bottom-auto top-0 left-0 right-0 w-full absolute pointer-events-none overflow-hidden -mt-20 h-20"
                        style={{transform: "translateZ(0)"}}
                    >
                        <svg
                            className="absolute bottom-0 overflow-hidden"
                            xmlns="http://www.w3.org/2000/svg"
                            preserveAspectRatio="none"
                            version="1.1"
                            viewBox="0 0 2560 100"
                            x="0"
                            y="0"
                        >
                            <polygon
                                className="text-blueGray-100 fill-current"
                                points="2560 0 2560 100 0 100"
                            ></polygon>
                        </svg>
                    </div>

                    <div className="container mx-auto px-4">
                        <div className="items-center flex flex-wrap">
                            <div className="w-full md:w-4/12 ml-auto mr-auto px-4">
                                <img
                                    alt="..."
                                    className="max-w-full rounded-lg shadow-lg"
                                    src="https://images.unsplash.com/photo-1555212697-194d092e3b8f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=634&q=80"
                                />
                            </div>
                            <div className="w-full md:w-5/12 ml-auto mr-auto px-4">
                                <div className="md:pr-12">
                                    <div
                                        className="text-lightBlue-600 p-3 text-center inline-flex items-center justify-center w-16 h-16 mb-6 shadow-lg rounded-full bg-lightBlue-300">
                                        <i className="fas fa-rocket text-xl"></i>
                                    </div>
                                    <h3 className="text-3xl font-semibold">Minjie Shen</h3>
                                    <p className="mt-4 text-lg leading-relaxed text-blueGray-500">
                                        Full-stack software engineer specializing in Python, Java, and JavaScript.
                                        Master's degree in Computer Engineering, Bachelor's degree in Computer Science
                                        and Electrical Engineering.
                                        Served as Graduate Research Assistant at Virginia Tech. Research
                                        focuses on machine learning algorithms for biomedical signal processing,
                                        particularly in the areas
                                        of
                                        missing data imputation (recommendation systems), normalization, and
                                        deconvolution.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>


                <section className="relative py-20">
                    <div
                        className="bottom-auto top-0 left-0 right-0 w-full absolute pointer-events-none overflow-hidden -mt-20 h-20"
                        style={{transform: "translateZ(0)"}}
                    >
                        <svg
                            className="absolute bottom-0 overflow-hidden"
                            xmlns="http://www.w3.org/2000/svg"
                            preserveAspectRatio="none"
                            version="1.1"
                            viewBox="0 0 2560 100"
                            x="0"
                            y="0"
                        >
                            <polygon
                                className="text-blueGray-100 fill-current"
                                points="2560 0 2560 100 0 100"
                            ></polygon>
                        </svg>
                    </div>

                    <div className="container mx-auto px-4">
                        <div className="items-center flex flex-row">

                            <div className="w-full md:w-5/12 ml-auto mr-auto px-4">
                                <div className="md:pr-12">
                                    <div
                                        className="text-lightBlue-600 p-3 text-center inline-flex items-center justify-center w-16 h-16 mb-6 shadow-lg rounded-full bg-lightBlue-300">
                                        <i className="fas fa-rocket text-xl"></i>
                                    </div>
                                    <h3 className="text-3xl font-semibold">Tianfan Fu</h3>
                                    <p className="mt-4 text-lg leading-relaxed text-blueGray-500">
                                        Tianfan Fu is a Postdoc at Computer Science Department at UIUC, working with
                                        Prof. Jimeng Sun. He obtained PhD degree from the Department of Computational
                                        Science and Engineering at Georgia Institute of Technology in 2023, supervised
                                        by Prof. Jimeng Sun. He received his B.S. and M.S. degree at Department of
                                        Computer Science and Engineering from Shanghai Jiao Tong University in 2015 and
                                        2018, respectively, supervised by Prof. Kai Yu and Prof. Yanmin Qian
                                        (2013-2014), Prof. Zhihua Zhang (2014-2018). I will join Rensselaer Polytechnic
                                        Institute (RPI) Computer Science Department as a tenure-track assistant
                                        professor in January 2024.

                                        I have several fully-funded PhD positions available in Fall 2024. If you are
                                        interested in working with me, please feel free to email me.
                                    </p>
                                </div>
                            </div>
                            <div className="w-full md:w-4/12 ml-auto mr-auto px-4">
                                <img
                                    alt="..."
                                    className="max-w-full rounded-lg shadow-lg"
                                    src="https://images.unsplash.com/photo-1555212697-194d092e3b8f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=634&q=80"
                                />
                            </div>
                        </div>
                    </div>
                </section>

            </main>
            <Footer/>
        </>
    );
}