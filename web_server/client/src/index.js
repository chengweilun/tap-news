import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App/App';
import { browserHistory, Router} from "react-router";
import routes from './routes'
import * as serviceWorker from './serviceWorker';

ReactDOM.render(<Router history={browserHistory} routes ={routes} />, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();
