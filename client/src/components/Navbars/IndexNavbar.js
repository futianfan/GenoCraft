/*eslint-disable*/
import React, {useEffect, useState} from "react";
import { Link } from "react-router-dom";
import FlipNumbers from 'react-flip-numbers';
// components

import IndexDropdown from "components/Dropdowns/IndexDropdown.js";
import {API_SERVER} from "../../config/constant";

export default function Navbar(props) {
  const [navbarOpen, setNavbarOpen] = React.useState(false);

  const [currentNumVisitors, setCurrentNumVisitors] = useState('-');
  const [currentNumAPITriggered, setCurrentNumAPITriggered] = useState('-');

  useEffect(() => {
        fetch(API_SERVER + 'google-analytics-report').then(res => res.json()).then(data => {
            setCurrentNumVisitors(data?.page_view);
            setCurrentNumAPITriggered(parseInt(data?.bulk_api_triggered) + parseInt(data?.single_api_triggered));
        });
    }, []);

  return (
    <div>
      <nav className="top-0 fixed z-50 w-full flex flex-wrap items-center justify-between px-2 py-3 navbar-expand-lg bg-white shadow">
        <div className="container px-4 mx-auto flex flex-wrap items-center justify-between">
          <div className="w-full relative flex justify-between lg:w-auto lg:static lg:block lg:justify-start">
            <Link
              to="/"
              className="text-blueGray-700 text-sm font-bold leading-relaxed inline-block mr-4 py-2 whitespace-nowrap uppercase"
            >
              Homepage
            </Link>
            <button
              className="cursor-pointer text-xl leading-none px-3 py-1 border border-solid border-transparent rounded bg-transparent block lg:hidden outline-none focus:outline-none"
              type="button"
              onClick={() => setNavbarOpen(!navbarOpen)}
            >
              <i className="fas fa-bars"></i>
            </button>
          </div>
          <div
            className={
              "lg:flex flex-grow items-center bg-white lg:bg-opacity-0 lg:shadow-none" +
              (navbarOpen ? " block" : " hidden")
            }
            id="example-navbar-warning"
          >
            <ul className="flex flex-col lg:flex-row list-none mr-auto">
              <li className="flex items-center">
                <p className="text-c-blue pl-3 flex items-center text-lg font-bold">
                  {currentNumVisitors}
                </p>
                <p className="text-blueGray-700 pl-1 flex items-center text-xs">
                  people visited
                </p>
              </li>
              <li className="flex items-center">
                <p className="text-c-blue pl-3 flex items-center text-lg font-bold">
                  {currentNumAPITriggered}
                </p>
                <p className="text-blueGray-700 pl-1 pr-3 flex items-center text-xs">
                  sets analyzed
                </p>
              </li>
            </ul>

            <ul className="flex flex-col lg:flex-row list-none lg:ml-auto">
              <li className="flex items-center">
                <IndexDropdown />
              </li>

              <li className="flex items-center">
                <a
                  className="hover:text-blueGray-500 text-blueGray-700 px-3 py-4 lg:py-2 flex items-center text-xs uppercase font-bold"
                  href="https://github.com/futianfan/GenoCraft"
                  target="_blank"
                >
                  <i className="text-blueGray-400 fab fa-github text-lg leading-lg " />
                  <span className="lg:hidden inline-block ml-2">Star</span>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
}
