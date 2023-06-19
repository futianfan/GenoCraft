import {createPopper} from "@popperjs/core";
import React from "react";
import {Link} from "react-router-dom";

const IndexDropdown = () => {
    // dropdown props
    const [dropdownPopoverShow, setDropdownPopoverShow] = React.useState(false);
    const btnDropdownRef = React.createRef();
    const popoverDropdownRef = React.createRef();
    const openDropdownPopover = () => {
        createPopper(btnDropdownRef.current, popoverDropdownRef.current, {
            placement: "bottom-start",
        });
        setDropdownPopoverShow(true);
    };
    const closeDropdownPopover = () => {
        setDropdownPopoverShow(false);
    };
    return (
        <>
            <a
                className="hover:text-blueGray-500 text-blueGray-700 px-3 py-4 lg:py-2 flex items-center text-xs uppercase font-bold"
                href="#pablo"
                ref={btnDropdownRef}
                onClick={(e) => {
                    e.preventDefault();
                    dropdownPopoverShow ? closeDropdownPopover() : openDropdownPopover();
                }}
            >
                Menu
            </a>
            <div
                ref={popoverDropdownRef}
                className={
                    (dropdownPopoverShow ? "block " : "hidden ") +
                    "bg-white text-base z-50 float-left py-2 list-none text-left rounded shadow-lg min-w-48"
                }
            >
        <Link
            to="/analyze"
            className={
                "text-sm pt-2 pb-0 px-4 font-bold block w-full whitespace-nowrap bg-transparent text-blueGray-400"
            }
        >
          Analyze
        </Link>
                <Link
                    to="/bulk-rna-workflow"
                    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
                >
                    Bulk RNA
                </Link>
                <Link
                    to="/single-cell-rna-workflow"
                    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
                >
                    Single Cell RNA
                </Link>
        <div className="h-0 mx-4 my-2 border border-solid border-blueGray-100"/>
        <span
            className={
                "text-sm pt-2 pb-0 px-4 font-bold block w-full whitespace-nowrap bg-transparent text-blueGray-400"
            }
        >
          About us
        </span>
                <Link
                    to="/"
                    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
                >
                    Authors (WIP)
                </Link>
                <Link
                    to="/"
                    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
                >
                    Publications (WIP)
                </Link>
            </div>
        </>
    );
};

export default IndexDropdown;

/*
        <div className="h-0 mx-4 my-2 border border-solid border-blueGray-100"/>
        <span
                    className={
                        "text-sm pt-2 pb-0 px-4 font-bold block w-full whitespace-nowrap bg-transparent text-blueGray-400"
                    }
                >
          Demo pages
        </span>
                <a
                    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
                    href="https://demos.creative-tim.com/notus-react/?ref=nr-github-readme#/"
                >
                    Notus Template
                </a>
                <a
                    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
                    href="https://flask-react-datta-able.appseed-srv1.com/app/dashboard/default"
                >
                    Datta Able Template
                </a>
 */
