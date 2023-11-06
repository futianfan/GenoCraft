import React from "react";

export default function Footer() {
    return (
        <>
            <footer className="relative pt-8 pb-6 bg-blueGray-200">
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
                                <div className="text-xs text-blueGray-300 pb-2">
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
