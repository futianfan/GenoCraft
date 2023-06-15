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
        <span
                    className={
                        "text-sm pt-2 pb-0 px-4 font-bold block w-full whitespace-nowrap bg-transparent text-blueGray-400"
                    }
                >
          Analyze
        </span>
                <Link
                    to="https://github.com/futianfan/GenoCraft"
                    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
                >
                    Bulk RNA
                </Link>
                <Link
                    to="https://github.com/futianfan/GenoCraft"
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
                    to="https://github.com/futianfan/GenoCraft"
                    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
                >
                    Authors
                </Link>
                <Link
                    to="https://github.com/futianfan/GenoCraft"
                    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
                >
                    Publications
                </Link>

        <div className="h-0 mx-4 my-2 border border-solid border-blueGray-100"/>
        <span
                    className={
                        "text-sm pt-2 pb-0 px-4 font-bold block w-full whitespace-nowrap bg-transparent text-blueGray-400"
                    }
                >
          Demo pages
        </span>
                <Link
                    to="/admin/dashboard"
                    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
                >
                    Dashboard
                </Link>
                <Link
                    to="/admin/settings"
                    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
                >
                    Settings
                </Link>
                <Link
                    to="/admin/tables"
                    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
                >
                    Tables
                </Link>
                <Link
                    to="/auth/login"
                    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
                >
                    Login
                </Link>
                <Link
                    to="/auth/register"
                    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
                >
                    Register
                </Link>

                <Link
                    to="/landing"
                    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
                >
                    Landing
                </Link>
                <Link
                    to="/profile"
                    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
                >
                    Profile
                </Link>
            </div>
        </>
    );
};

export default IndexDropdown;
