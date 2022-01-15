import { Box, Pagination, Button } from "@mui/material";
import React, { Component } from "react";
import FormGroup from "@mui/material/FormGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import DatasetListView from "./DatasetListView";
import axios from "axios";
import AddIcon from "@mui/icons-material/Add";
import DownloadIcon from "@mui/icons-material/Download";
import WrongDialog from "./WrongDialog";

export class DatasetPage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      topics: [],
      topicFilter: [],
      page: 1,
      num_pages: 0,
      videoList: [],
      wrong: false,
    };

    this.handlePageChange = this.handlePageChange.bind(this);
    this.handleFilterChange = this.handleFilterChange.bind(this);
    this.handleWrongDialogOpen = this.handleWrongDialogOpen.bind(this);
    this.handleWrongDialogClose = this.handleWrongDialogClose.bind(this);
    this.handleWrongDialogSubmit = this.handleWrongDialogSubmit.bind(this);
    this.extractJSON = this.extractJSON.bind(this);
    this.init();
  }

  init() {
    axios.get("http://127.0.0.1:5000/getDataset").then((response) => {
      // console.log(response)
      this.setState({ topics: response.data.topics });
    });
  }

  getContent() {
    console.log("Done");
    console.log(this.state.topicFilter);
    axios
      .post("http://127.0.0.1:5000/getDataset", {
        page: this.state.page,
        topicFilter: [this.state.topicFilter],
      })
      .then((response) => {
        console.log("SUCCESS", response.data.videoList);
        this.setState({
          num_pages: response.data.num_pages,
          videoList: response.data.videoList,
          // topics: response.data.topics,
        });
        // setGetMessage(response);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  handlePageChange(event, value) {
    console.log(value);
    this.setState({ page: value }, this.getContent);
  }

  handleFilterChange(event) {
    console.log(event.target.name, event.target.checked);
    if (event.target.checked) {
      this.setState(
        { topicFilter: [...this.state.topicFilter, event.target.name] },
        this.getContent
      );
    } else {
      this.setState(
        {
          topicFilter: this.state.topicFilter.filter(
            (topic) => topic !== event.target.name
          ),
        },
        this.getContent
      );
    }
  }

  handleWrongDialogOpen(wrn) {
    console.log(wrn);
    this.setState({ wrong: wrn });
  }

  handleWrongDialogClose() {
    console.log("Closed");
    this.setState({ wrong: false });
  }

  handleWrongDialogSubmit(vid_url, label, reason) {
    console.log(vid_url, label, reason);
    this.setState({ wrong: false });
    axios
      .post("http://127.0.0.1:5000/updateDataset", {
        url: vid_url,
        suggestedLabel: label,
        reason: reason,
      })
      .then((response) => {
        console.log("SUCCESS", response.data);

        // setGetMessage(response);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  extractJSON() {
    axios
      .post("http://127.0.0.1:5000/extractDataset", {
        topicFilter: [this.state.topicFilter],
      })
      .then((response) => {
        console.log(response);
        const blob = new Blob([response.data]);
          let url = window.URL.createObjectURL(blob);
          let a = document.createElement("a");
          a.href = url;
          a.download = "YT_Video_Dataset.json";
          a.click();
        // setGetMessage(response);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  render() {
    return (
      <Box sx={{ width: "100%", height: "100%" }}>
        {this.state.num_pages > 0 && this.state.page > 0 && (
          <Box display="flex" alignItems="center" justifyContent="center">
            <Pagination
              width={4 / 5}
              count={this.state.num_pages}
              page={this.state.page}
              onChange={this.handlePageChange}
            />
          </Box>
        )}
        <Box
          sx={{ width: "100%", height: "100%" }}
          display="flex"
          alignItems="right"
          justifyContent="right"
        >
          <Button
            style={{ marginLeft: 5, marginRight: 5 }}
            variant="outlined"
            startIcon={<DownloadIcon />}
            onClick={this.extractJSON}
          >
            Extract JSON
          </Button>
          <Button
            style={{ marginLeft: 5, marginRight: 5 }}
            variant="outlined"
            startIcon={<AddIcon />}
          >
            Add Video
          </Button>
        </Box>
        <Box
          sx={{
            display: "flex",
          }}

          // alignItems="center"
          // justifyContent="center"
        >
          <Box
            component="form"
            sx={{
              minWidth: 1 / 5,
              width: 1 / 5,
              height: 1,
              borderRight: 1,
              borderColor: "divider",
              flexDirection: "column",
            }}
          >
            <FormGroup>
              {/* {for (var i = 0; i < this.state.topicFilter.length; i++) {
                                <FormControlLabel control={<Checkbox />} label="Label" />
                            }} */}
              {this.state.topics.map((topic, i) => (
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={this.state.topicFilter.includes(topic.value)}
                      name={topic.value}
                      onChange={this.handleFilterChange}
                    />
                  }
                  label={topic.name}
                />
              ))}
              {/* <FormControlLabel control={<Checkbox />} label="Label" />
                            <FormControlLabel control={<Checkbox />} label="Disabled" /> */}
            </FormGroup>
          </Box>
          <Box
            sx={{
              borderLeft: 1,
              borderColor: "divider",
            }}
          >
            <DatasetListView
              videoList={this.state.videoList}
              handleWrongDialogOpen={this.handleWrongDialogOpen}
            />
          </Box>

          {/* <BasicFilteringGrid/> */}
        </Box>
        {/* <Fab
          variant="extended"
          color="primary"
          aria-label="add"
          sx={{ position: "absolute", bottom: "5%", right: "5%" }}
        >
          <AddIcon sx={{ mr: 1 }} />
          Add New Video
        </Fab> */}
        {this.state.wrong && (
          <WrongDialog
            wrong={this.state.wrong}
            handleClose={this.handleWrongDialogClose}
            handleSubmit={this.handleWrongDialogSubmit}
          />
        )}
      </Box>
    );
  }
}

export default DatasetPage;
