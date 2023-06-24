import React, {useEffect} from 'react';
import ReactGA from "react-ga4";
import {BrowserRouter as Router} from 'react-router-dom';
import {BASENAME} from './config/constant';

import routes, {renderRoutes} from './routes';

ReactGA.initialize('G-EEL4KXL0BV');

const App = () => {

    useEffect(() => {
        ReactGA.send({hitType: "pageview", page: window.location.pathname});
    }, []);

    return (
        <React.Fragment>
            <Router basename={BASENAME}>{renderRoutes(routes)}</Router>
        </React.Fragment>
    );
};

export default App;
