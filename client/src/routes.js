import "@fortawesome/fontawesome-free/css/all.min.css";
import "assets/styles/tailwind.css";
import React from "react";
import {BrowserRouter, Redirect, Route, Switch} from "react-router-dom";
import Analyze from "views/Analyze";

import Index from "views/Index";
import BulkRNAWorkflow from "./views/BulkRNAWorkflow";
import ProteinWorkflow from "./views/ProteinWorkflow";
import SingleCellWorkflow from "./views/SingleCellWorkflow";
import CrossWorkflow from "views/CrossWorkflow";
import AboutUs from "./views/AboutUs"

export const Routes = () => (
    <BrowserRouter>
        <Switch>
            <Route path="/" exact component={Index}/>
            <Route path="/about-us" exact component={AboutUs}/>
            <Route path="/analyze" exact component={Analyze}/>
            <Route path="/bulk-rna-workflow" exact component={BulkRNAWorkflow}/>
            <Route path="/single-cell-rna-workflow" exact component={SingleCellWorkflow}/>
            <Route path="/protein-workflow" exact component={ProteinWorkflow}/>
            <Route path="/cross-workflow" exact component={CrossWorkflow}/>
            {/* add redirect for first page */}
            <Redirect from="*" to="/"/>
        </Switch>
    </BrowserRouter>
)