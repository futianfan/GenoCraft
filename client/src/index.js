import React from 'react';
import 'react-app-polyfill/ie11';
import 'react-app-polyfill/stable';
import ReactDOM from 'react-dom';
import {ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import './index.scss';
import {Routes} from "./routes";
import reportWebVitals from './reportWebVitals';
import { HashRouter } from 'react-router-dom'

ReactDOM.render(
    <HashRouter>
        <Routes/>
        <ToastContainer
            position="top-right"
            autoClose={5000}
            hideProgressBar={false}
            newestOnTop={false}
            closeOnClick
            rtl={false}
            pauseOnFocusLoss
            draggable
            pauseOnHover
            theme="dark"/>
    </HashRouter>,
    document.getElementById('root')
);

reportWebVitals();
