// import logo from './logo.svg';
// import './App.css';
// import React, { useEffect, useState } from 'react';
// import axios from 'axios';
// import Button from '@mui/material/Button';
// import Tabs from '@mui/material/Tabs';
// import Tab from '@mui/material/Tab';

// class App extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       message: {
//         status: 2000,
//       },
//       value: 0
//     };
//     this.onClick = this.onClick.bind(this);
//   }

//   onClick () {
//     axios
//     .post('http://127.0.0.1:5000/flask/hello', {'message': 'yt'})
//     .then((response) => {
//       console.log("SUCCESS", response);
//       this.setState({message: response});
//       // setGetMessage(response);
//     }).catch(error => {
//       console.log(error);
//     });
//   }

//   render() {
//     return (
//       <div className="App">
//         <header className="App-header">

//           {/* <img src={logo} className="App-logo" alt="logo" /> */}
//           {/* <p>
//             Edit <code> src/App.js </code> and save to reload.
//           </p> */}
//           {/* <a
//             className="App-link"
//             href="https://reactjs.org"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             Learn React
//           </a> */}
//           <div>{this.state.message.status === 200 ?
//             <h3>{this.state.message.data.message}</h3>
//             :
//             <h3>LOADING</h3>}</div>
//           <Button
//             onClick={this.onClick}>
//             Click me
//           </Button>
//         </header>
//       </div>
//     );
//   }
// }

// export default App;

import * as React from "react";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import axios from "axios";
import DetectPage from "./DetectPage";
import DatasetPage from "./DatasetPage";

class App extends React.Component {
  componentDidMount() {
    document.title = "YT Misinformation Detection";
  }
  constructor(props) {
    super(props);
    this.state = {
      tabValue: 0,
      message: {
        status: 2000,
      },
    };
    // this.detectPage = new DetectPage();
  }

  handleTabChange = (event, value) => {
    console.log(value);
    this.setState({
      tabValue: value,
    });
  };

  onClick = () => {
    axios
      .post("http://127.0.0.1:5000/flask/hello", { message: "yt" })
      .then((response) => {
        console.log("SUCCESS", response);
        this.setState({ message: response });
        // setGetMessage(response);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  render() {
    return (
      <div>
        <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
          <Tabs
            value={this.state.tabValue}
            onChange={this.handleTabChange}
            centered
          >
            <Tab label="Detect" />
            <Tab label="Dataset" />
          </Tabs>
        </Box>
        <TabPanel value={this.state.tabValue} index={0}>
          {/* Detect Tab */}
          {/* {this.detectPage} */}
          <DetectPage />
        </TabPanel>
        <TabPanel value={this.state.tabValue} index={1}>
          <DatasetPage />
          {/* <div>
                        {this.state.message.status === 200 ? (
                        <h3>{this.state.message.data.message}</h3>
                        ) : (
                        <h3>LOADING</h3>
                        )}
                    </div> */}
          {/* <Button onClick={this.onClick}>Click me</Button> */}
        </TabPanel>
      </div>
    );
  }
}

function TabPanel(props) {
  const { children, value, index } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
    >
      {/* {value === index && ( */}
      <Box sx={{ p: 3 }}>
        <p>{children}</p>
      </Box>
      {/* )} */}
    </div>
  );
  // return <div>{value === index && <p>{children}</p>}</div>;
}

export default App;
