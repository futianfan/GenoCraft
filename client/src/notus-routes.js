import React from "react";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";

import "@fortawesome/fontawesome-free/css/all.min.css";
import "assets/styles/tailwind.css";

import Index from "views/Index";
import Analyze from "views/Analyze";
import BulkRNAWorkflow from "./views/BulkRNAWorkflow";
import SingleCellWorkflow from "./views/SingleCellWorkflow";

export const NotusRoutes = () => (
    <BrowserRouter>
        <Switch>
            <Route path="/" exact component={Index}/>
            <Route path="/analyze" exact component={Analyze}/>
            <Route path="/bulk-rna-workflow" exact component={BulkRNAWorkflow}/>
            <Route path="/single-cell-rna-workflow" exact component={SingleCellWorkflow}/>
            {/* add redirect for first page */}
            <Redirect from="*" to="/"/>
        </Switch>
    </BrowserRouter>
)