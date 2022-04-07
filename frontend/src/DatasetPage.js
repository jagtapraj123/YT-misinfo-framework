import { Box, Pagination, Button, Divider, Typography } from "@mui/material";
import React, { Component } from "react";
import FormGroup from "@mui/material/FormGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import DatasetListView from "./DatasetListView";
import axios from "axios";
import AddIcon from "@mui/icons-material/Add";
import DownloadIcon from "@mui/icons-material/Download";
import WrongDialog from "./WrongDialog";
import AddVideoDialog from "./AddVideoDialog";

export class DatasetPage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      topics: [],
      tags: [],
      topicFilter: [],
      page: 1,
      num_pages: 0,
      videoList: [],
      wrong: false,
      add: false,
    };

    this.handlePageChange = this.handlePageChange.bind(this);
    this.handleTopicsFilterChange = this.handleTopicsFilterChange.bind(this);
    this.handleTagsFilterChange = this.handleTagsFilterChange.bind(this);
    this.handleWrongDialogOpen = this.handleWrongDialogOpen.bind(this);
    this.handleWrongDialogClose = this.handleWrongDialogClose.bind(this);
    this.handleWrongDialogSubmit = this.handleWrongDialogSubmit.bind(this);
    this.extractJSON = this.extractJSON.bind(this);
    this.handleAddVideoDialogOpen = this.handleAddVideoDialogOpen.bind(this);
    this.handleAddVideoDialogClose = this.handleAddVideoDialogClose.bind(this);
    this.handleAddVideoDialogSubmit =
      this.handleAddVideoDialogSubmit.bind(this);
    this.init();
  }

  init() {
    axios.get("http://127.0.0.1:5000/getTopics").then((response) => {
      this.setState({ topics: response.data.topics, tags: response.data.tags });
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
      })
      .catch((error) => {
        console.log(error);
      });
  }

  handlePageChange(event, value) {
    console.log(value);
    this.setState({ page: value }, this.getContent);
  }

  handleTopicsFilterChange(event) {
    console.log(event.target.name, event.target.checked);
    console.log(this.state.topics[event.target.name]);
    if (event.target.checked) {
      this.setState(
        {
          topicFilter: this.state.topicFilter.concat(
            this.state.topics[event.target.name]
          ),
          page: 1,
        },
        this.getContent
      );
    } else {
      this.setState(
        {
          topicFilter: this.state.topicFilter.filter(
            (topic) => !this.state.topics[event.target.name].includes(topic)
          ),
          page: 1,
        },
        this.getContent
      );
    }
  }

  handleTagsFilterChange(event) {
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
            (tag) => tag !== event.target.name
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

  handleWrongDialogSubmit(vid_url, tags, label, reasons) {
    console.log(vid_url, tags, label, reasons);
    this.setState({ wrong: false });
    axios
      .post("http://127.0.0.1:5000/updateDataset", {
        url: vid_url,
        tags: [tags],
        suggestedLabel: label,
        reasons: [reasons],
      })
      .then((response) => {
        console.log("SUCCESS", response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  extractJSON() {
    if (this.state.topicFilter.length > 0) {
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
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }

  handleAddVideoDialogOpen() {
    this.setState({ add: true });
  }

  handleAddVideoDialogClose() {
    this.setState({ add: false });
  }

  handleAddVideoDialogSubmit(
    url,
    selectedTags,
    newTags,
    label,
    reasons,
    setUrlValid,
    setURLFailReason,
    setLoading
  ) {
    // this.setState({ add: false });
    axios
      .post("http://127.0.0.1:5000/updateDataset", {
        url: url,
        tags: [selectedTags.concat(newTags.map((t) => t.text))],
        suggestedLabel: label,
        reasons: [reasons],
      })
      .then((response) => {
        console.log("SUCCESS", response.data);
        if (response.data.status !== "Success") {
          setUrlValid(false);
          setURLFailReason(response.data.reason);
          setLoading(false);
        } else {
          setLoading(false);
          this.setState({ add: false });
        }
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
            disabled={this.state.topicFilter.length === 0}
            startIcon={<DownloadIcon />}
            onClick={this.extractJSON}
          >
            Extract JSON
          </Button>
          <Button
            style={{ marginLeft: 5, marginRight: 5 }}
            variant="outlined"
            startIcon={<AddIcon />}
            onClick={this.handleAddVideoDialogOpen}
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
              {Object.keys(this.state.topics).length > 0 && (
                <Typography variant="h6">Topics:</Typography>
              )}
              {Object.keys(this.state.topics).map((topic, i) => (
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={
                        this.state.topics[topic].filter((tag) =>
                          this.state.topicFilter.includes(tag)
                        ).length > 0
                      }
                      name={topic}
                      onChange={this.handleTopicsFilterChange}
                    />
                  }
                  label={topic}
                />
              ))}
              <Divider />
              {/* {for (var i = 0; i < this.state.topicFilter.length; i++) {
                                <FormControlLabel control={<Checkbox />} label="Label" />
                            }} */}
              {Object.keys(this.state.topics).length > 0 && (
                <Typography variant="h6">Tags:</Typography>
              )}
              {this.state.tags.map((tag, i) => (
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={this.state.topicFilter.includes(tag)}
                      name={tag}
                      onChange={this.handleTagsFilterChange}
                    />
                  }
                  label={tag}
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
        </Box>
        {this.state.wrong && (
          <WrongDialog
            wrong={this.state.wrong}
            handleClose={this.handleWrongDialogClose}
            handleSubmit={this.handleWrongDialogSubmit}
          />
        )}

        {this.state.add && (
          <AddVideoDialog
            open={this.state.add}
            handleClose={this.handleAddVideoDialogClose}
            handleSubmit={this.handleAddVideoDialogSubmit}
            // topics={this.state.topics}
            tags={this.state.tags}
          />
        )}
      </Box>
    );
  }
}

export default DatasetPage;
