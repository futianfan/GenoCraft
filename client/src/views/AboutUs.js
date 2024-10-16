import Footer from "components/Footers/Footer.js";

// components
import Navbar from "components/Navbars/IndexNavbar.js";
import React from "react";

export default function AboutUs() {
    return (
        <>
            <Navbar transparent/>
            <main>
                <section className="pt-20 pb-48 bg-blueGray-50">
                    <div className="container mx-auto px-4">
                        <div className="flex flex-row pt-32">
                            <div className="w-full w:1/3 lg:mb-0 mb-12 px-4">
                                <div className="px-6">
                                    <img
                                        alt="yingzhou-lu"
                                        src={require("assets/img/yingzhou-lu.jpeg").default}
                                        className="shadow-lg rounded-full mx-auto max-w-120-px"
                                    />
                                    <div className="pt-6 text-center">
                                        <h5 className="text-xl font-bold">Yingzhou Lu</h5>
                                        <p className="mt-1 text-sm text-blueGray-400 font-semibold">
                                            Postdoctoral Researcher
                                        </p>
                                        <p className="mt-1 text-sm text-blueGray-400 font-semibold">
                                            at Standard University
                                        </p>
                                        <div className="mt-6">
                                            <a href="https://www.linkedin.com/in/minta-lu-phd-565531157/">
                                                <button
                                                    className="bg-lightBlue-600 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                    type="button"
                                                >
                                                    <i className="fab fa-linkedin"></i>
                                                </button>
                                            </a>
                                            <a href="https://scholar.google.com/citations?user=jKOmKzEAAAAJ&hl=en">
                                                <button
                                                    className="bg-lightBlue-500 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                    type="button"
                                                >
                                                    <i className="fa fa-graduation-cap" aria-hidden="true"></i>
                                                </button>
                                            </a>
                                            <a href="https://profiles.stanford.edu/yingzhou-lu">
                                                <button
                                                    className="bg-indigo-500 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                    type="button"
                                                >
                                                    <i className="fa fa-home"></i>
                                                </button>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="w-full w:1/3 lg:mb-0 mb-12 px-4">
                                <div className="px-6">
                                    <img
                                        alt="minjie-shen"
                                        src={require("assets/img/minjie-shen.jpeg").default}
                                        className="shadow-lg rounded-full mx-auto max-w-120-px"
                                    />
                                    <div className="pt-6 text-center">
                                        <h5 className="text-xl font-bold">Minjie Shen</h5>
                                        <p className="mt-1 text-sm text-blueGray-400 font-semibold">
                                            Software Engineer at Realtor.com
                                        </p>
                                        <p className="mt-1 text-sm text-blueGray-400 font-semibold">
                                            Ex-Graduate Research Assistant at Virginia Tech
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
                            <div className="w-full w:1/3 lg:mb-0 mb-12 px-4">
                                <div className="px-6">
                                    <img
                                        alt="tianfan-fu"
                                        src={require("assets/img/tianfan-fu.jpeg").default}
                                        className="shadow-lg rounded-full mx-auto max-w-120-px"
                                    />
                                    <div className="pt-6 text-center">
                                        <h5 className="text-xl font-bold">Tianfan Fu</h5>
                                        <p className="mt-1 text-sm text-blueGray-400 font-semibold">
                                            Incoming Assistant Professor
                                        </p>
                                        <p className="mt-1 text-sm text-blueGray-400 font-semibold">
                                            at Rensselaer Polytechnic Institute
                                        </p>
                                        <p className="mt-1 text-sm text-blueGray-400">
                                            Fully-funded PhD positions available in Fall 2024.
                                        </p>
                                        <p className="mt-1 text-sm text-blueGray-400">
                                            Email me if you are interested.
                                        </p>
                                        <div className="mt-6">
                                            <a href="https://futianfan.github.io/#:~:text=Tianfan%20Fu%20is%20a%20Postdoc,received%20his%20B.S.%20and%20M.S.">
                                                <button
                                                    className="bg-indigo-500 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                    type="button"
                                                >
                                                    <i className="fa fa-home" aria-hidden="true"></i>
                                                </button>
                                            </a>
                                            <a href="https://scholar.google.com/citations?user=KPQ49w4AAAAJ&hl=zh-CN">
                                                <button
                                                    className="bg-lightBlue-500 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                    type="button"
                                                >
                                                    <i className="fa fa-graduation-cap" aria-hidden="true"></i>
                                                </button>
                                            </a>
                                            <a href="https://futianfan.github.io/Tianfan_CV.pdf">
                                                <button
                                                    className="bg-emerald-500 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                    type="button"
                                                >
                                                    <i className="fa fa-file" aria-hidden="true"></i>
                                                </button>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="flex flex-row pt-32 px-12">
                            <div className="w-full w:1/2 lg:mb-0 mb-12 px-4">
                                <div className="px-6">
                                    <img
                                        alt="yue-zhao"
                                        src={require("assets/img/yue-zhao.jpg").default}
                                        className="shadow-lg rounded-full mx-auto max-w-120-px"
                                    />
                                    <div className="pt-6 text-center">
                                        <h5 className="text-xl font-bold">Yue Zhao</h5>
                                        <p className="mt-1 text-sm text-blueGray-400 font-semibold">
                                            Assistant Professor
                                        </p>
                                        <p className="mt-1 text-sm text-blueGray-400 font-semibold">
                                            at University of Southern California
                                        </p>
                                        <div className="mt-6">
                                            <a href="https://viterbi-web.usc.edu/~yzhao010/">
                                                <button
                                                    className="bg-indigo-500 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                    type="button"
                                                >
                                                    <i className="fa fa-home" aria-hidden="true"></i>
                                                </button>
                                            </a>
                                            <a href="https://scholar.google.com/citations?user=zoGDYsoAAAAJ&hl=en">
                                                <button
                                                    className="bg-lightBlue-500 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                    type="button"
                                                >
                                                    <i className="fa fa-graduation-cap" aria-hidden="true"></i>
                                                </button>
                                            </a>
                                            <a href="https://viterbi-web.usc.edu/~yzhao010/files/ZHAO_YUE_CV.pdf">
                                                <button
                                                    className="bg-emerald-500 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                    type="button"
                                                >
                                                    <i className="fa fa-file" aria-hidden="true"></i>
                                                </button>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="w-full w:1/2 lg:mb-0 mb-12 px-4">
                                <div className="px-6">
                                    <img
                                        alt="van-rechem"
                                        src={require("assets/img/van-rechem.jpg").default}
                                        className="shadow-lg rounded-full mx-auto max-w-120-px"
                                    />
                                    <div className="pt-6 text-center">
                                        <h5 className="text-xl font-bold">Capucine Van Rechem</h5>
                                        <p className="mt-1 text-sm text-blueGray-400 font-semibold">
                                            Assistant Professor of Pathology
                                        </p>
                                        <p className="mt-1 text-sm text-blueGray-400 font-semibold">
                                            at Stanford University, School of Medicine
                                        </p>
                                        <div className="mt-6">
                                            <a href="https://profiles.stanford.edu/capucine-van-rechem">
                                                <button
                                                    className="bg-indigo-500 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                    type="button"
                                                >
                                                    <i className="fa fa-home"></i>
                                                </button>
                                            </a>
                                            <a href="https://vanrechemlab.com/">
                                                <button
                                                    className="bg-red-700 text-white w-8 h-8 rounded-full outline-none focus:outline-none mr-1 mb-1"
                                                    type="button"
                                                >
                                                    <i className="fa fa-flask"></i>
                                                </button>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <section className="relative py-20 bg-blueGray-600">
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
                                className="text-blueGray-500 fill-current"
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
                                    <h3 className="text-blueGray-100 text-3xl font-semibold">Yingzhou Lu</h3>
                                    <p className="mt-4 text-lg leading-relaxed text-blueGray-300">
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
                                    alt="minta-lu-full-body"
                                    className="max-w-full rounded-lg shadow-lg"
                                    src={require("assets/img/minta-lu-full-body.jpeg").default}
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
                                className="text-blueGray-400 fill-current"
                                points="2560 0 2560 100 0 100"
                            ></polygon>
                        </svg>
                    </div>

                    <div className="container mx-auto px-4">
                        <div className="items-center flex flex-wrap">
                        <div className="w-full md:w-4/12 ml-auto mr-auto px-4">
                                <img
                                    alt="minjie-shen-full"
                                    className="max-w-full rounded-lg shadow-lg"
                                    src={require("assets/img/minjie-shen-full.jpg").default}
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


                <section className="relative py-20 bg-blueGray-600">
                    <div
                        className="bottom-0 top-0 left-0 right-0 w-full absolute pointer-events-none overflow-hidden -mt-20 h-20"
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
                                className="text-blueGray-200 fill-current"
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
                                    <h3 className="text-blueGray-100 text-3xl font-semibold">Tianfan Fu</h3>
                                    <p className="mt-4 text-lg leading-relaxed text-blueGray-300">
                                        Tianfan Fu is a Postdoc at Computer Science Department at UIUC, working with
                                        Prof. Jimeng Sun. He obtained PhD degree from the Department of Computational
                                        Science and Engineering at Georgia Institute of Technology in 2023, supervised
                                        by Prof. Jimeng Sun. He received his B.S. and M.S. degree at Department of
                                        Computer Science and Engineering from Shanghai Jiao Tong University in 2015 and
                                        2018, respectively, supervised by Prof. Kai Yu and Prof. Yanmin Qian
                                        (2013-2014), Prof. Zhihua Zhang (2014-2018). He will join Rensselaer Polytechnic
                                        Institute (RPI) Computer Science Department as a tenure-track assistant
                                        professor in January 2024.
                                    </p>
                                </div>
                            </div>
                            <div className="w-full md:w-4/12 ml-auto mr-auto px-4">
                                <img
                                    alt="tianfan-fu"
                                    className="max-w-full rounded-lg shadow-lg"
                                    src={require("assets/img/tianfan-fu.jpeg").default}
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
                                className="text-blueGray-400 fill-current"
                                points="2560 0 2560 100 0 100"
                            ></polygon>
                        </svg>
                    </div>

                    <div className="container mx-auto px-4">
                        <div className="items-center flex flex-wrap">
                        <div className="w-full md:w-4/12 ml-auto mr-auto px-4">
                                <img
                                    alt="yue-zhao"
                                    className="max-w-full rounded-lg shadow-lg"
                                    src={require("assets/img/yue-zhao.jpg").default}
                                />
                            </div>
                            <div className="w-full md:w-5/12 ml-auto mr-auto px-4">
                                <div className="md:pr-12">
                                    <div
                                        className="text-lightBlue-600 p-3 text-center inline-flex items-center justify-center w-16 h-16 mb-6 shadow-lg rounded-full bg-lightBlue-300">
                                        <i className="fas fa-rocket text-xl"></i>
                                    </div>
                                    <h3 className="text-3xl font-semibold">Yue Zhao</h3>
                                    <p className="mt-4 text-lg leading-relaxed text-blueGray-500">
                                        Dr. Yue Zhao is an Assistant Professor at the University of Southern California.
                                        He specializes in building automated, efficient, and scalable machine learning
                                        (ML), with an emphasis on anomaly detection, graph neural networks, and
                                        open-source ML tool development. Additionally, Dr. Zhao's contributions to the
                                        ML community include the development of over 10 open-source projects, which have
                                        over 16,000+ GitHub stars and over 20 million downloads by 2023. Notably,
                                        projects such as PyOD, PyGOD, TDC, and ADBench have found applications in
                                        leading institutions like NASA and Morgan Stanley. Earning his Ph.D. from
                                        Carnegie Mellon University (CMU) in four years, Dr. Zhao's academic excellence
                                        has been acknowledged through awards like the Norton Fellowship, Meta AI4AI
                                        Research Award, and the CMU Presidential Fellowship. He is also an associate
                                        editor of IEEE Transactions on Neural Networks and Learning Systems (TNNLS), an
                                        action editor of Journal of Data-centric Machine Learning Research (DMLR), and
                                        workflow co-chair of KDD 2023.
                                    </p>
                                </div>
                            </div>


                        </div>
                    </div>
                </section>

                <section className="relative py-20 bg-blueGray-600">
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
                                className="text-blueGray-200 fill-current"
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
                                    <h3 className="text-blueGray-100 text-3xl font-semibold">Capucine Van Rechem </h3>
                                    <p className="mt-4 text-lg leading-relaxed text-blueGray-300">
                                        Professor Van Rechem is Assistant Professor of Pathology at Stanford University,
                                        School of Medicine. She focuses on the molecular impact of chromatin modifiers
                                        on disease development, with an emphasis on cancer. Her laboratory undertakes a
                                        cell-cycle specific angle to explore functions such as gene expression and
                                        replication timing. They also explore unconventional direct roles for these
                                        factors in the cytoplasm, with a focus on protein synthesis. Their ultimate goal
                                        is to provide needed insights into new targeted therapies.
                                    </p>
                                </div>
                            </div>
                            <div className="w-full md:w-4/12 ml-auto mr-auto px-4">
                                <img
                                    alt="van-rechem"
                                    className="max-w-full rounded-lg shadow-lg"
                                    src={require("assets/img/van-rechem.jpg").default}
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