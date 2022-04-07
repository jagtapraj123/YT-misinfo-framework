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
  }

  handleTabChange = (event, value) => {
    console.log(value);
    this.setState({
      tabValue: value,
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
          <DetectPage />
        </TabPanel>
        <TabPanel value={this.state.tabValue} index={1}>
          <DatasetPage />
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
