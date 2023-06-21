import React from 'react';
import 'react-app-polyfill/ie11';
import 'react-app-polyfill/stable';
import ReactDOM from 'react-dom';
import {ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import './index.scss';
import {NotusRoutes} from "./notus-routes";
import reportWebVitals from './reportWebVitals';

ReactDOM.render(
    /*
    <Provider store={store}>
        <ConfigProvider>
            <PersistGate loading={null} persistor={persister}>
                <App />
            </PersistGate>
        </ConfigProvider>
    </Provider>,
     */
    <>
        <NotusRoutes/>
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
    </>,
    document.getElementById('root')
);

reportWebVitals();
