import React from "react";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";

import "@fortawesome/fontawesome-free/css/all.min.css";
import "assets/styles/tailwind.css";

// layouts

import Admin from "layouts/Admin.js";
import Auth from "layouts/Auth.js";

// views without layouts

import Landing from "views/Landing.js";
import Profile from "views/Profile.js";
import Index from "views/Index";
import Analyze from "views/Analyze";
import BulkRNAWorkflow from "./views/BulkRNAWorkflow";

export const NotusRoutes = () => (
    <BrowserRouter>
        <Switch>
            {/* add routes with layouts */}
            <Route path="/admin" component={Admin}/>
            <Route path="/auth" component={Auth}/>
            {/* add routes without layouts */}
            <Route path="/landing" exact component={Landing}/>
            <Route path="/profile" exact component={Profile}/>
            <Route path="/" exact component={Index}/>
            <Route path="/analyze" exact component={Analyze}/>
            <Route path="/bulk-rna-workflow" exact component={BulkRNAWorkflow}/>
            {/* add redirect for first page */}
            <Redirect from="*" to="/"/>
        </Switch>
    </BrowserRouter>
)