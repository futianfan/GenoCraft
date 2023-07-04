import React from "react";

export default function Footer() {
    return (
        <>
            <footer className="relative pt-8 pb-6 bg-blueGray-200">
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
                <div>
                    <div className="flex flex-wrap items-center md:justify-between justify-center bg-blueGray-200">
                        <div className="w-full md:w-4/12 px-4 mx-auto text-center">
                            <div className="text-sm font-semibold text-blueGray-300 hover:text-blueGray-500 py-1">
                                Copyright © {new Date().getFullYear()} GenoCraft
                            </div>
                            <div className="flex flex-col">
                                <div className="text-xs text-blueGray-300">
                                    Copyright © {new Date().getFullYear()} Notus React by{" "}
                                    <a
                                        href="https://www.creative-tim.com?ref=nr-footer"
                                        className="text-blueGray-300 hover:text-blueGray-500"
                                    >
                                        Creative Tim
                                    </a>
                                </div>
                                <div className="text-xs text-blueGray-300">
                                    Copyright © {new Date().getFullYear()}{" "}
                                    <a
                                        href="https://appseed.us/product/flask-react-datta-able"
                                        className="text-blueGray-300 hover:text-blueGray-500"
                                    >
                                        Flask React Datta Able
                                    </a>
                                    {" "} by {" "}
                                    <a
                                        href="https://codedthemes.com/"
                                        className="text-blueGray-300 hover:text-blueGray-500"
                                    >
                                        CodedThemes
                                    </a>
                                    {" "}and AppSeed{" "}
                                    <a
                                        href="https://appseed.us/app-generator"
                                        className="text-blueGray-300 hover:text-blueGray-500"
                                    >
                                        App Generator
                                    </a>

                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </footer>
        </>
    );
}
