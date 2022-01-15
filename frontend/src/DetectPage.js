import React from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import axios from "axios";
import PropTypes from "prop-types";
import { Typography } from "@mui/material";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import WrongDialog from "./WrongDialog";

class DetectPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      url: "",
      embedId: "",
      captions: {
        status: 2000,
      },
      detection: false,
      radioValue: "",
      valid: false,
      wrong: false,
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleRadioChange = this.handleRadioChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
    this.handleWrongDialogOpen = this.handleWrongDialogOpen.bind(this);
    this.handleWrongDialogClose = this.handleWrongDialogClose.bind(this);
    this.handleWrongDialogSubmit = this.handleWrongDialogSubmit.bind(this);
  }

  onSubmit(event) {
    console.log(this.state.url);
    this.setState({
      embedId: this.state.url.split("?v=")[1].split("&")[0],
    });
    // alert("A URL was submitted: " + this.state.url);
    event.preventDefault();
    axios
      .post("http://127.0.0.1:5000/detect", {
        url: this.state.url,
        topic: this.state.radioValue,
      })
      .then((response) => {
        console.log("SUCCESS", response);
        this.setState({ detection: response.data.detection });
        // setGetMessage(response);
      })
      .catch((error) => {
        console.log(error);
        this.setState({ detection: false });
      });
  }

  handleChange(event) {
    console.log(event);
    this.setState({
      url: event.target.value,
      valid: event.target.value !== "" && this.state.radioValue !== "",
    });
    // if (this.state.url !== "" && this.state.radioValue !== ""){
    //   this.setState({ valid: true });
    // }
    // else{
    //   this.setState({ valid: false });
    // }
  }

  handleRadioChange(event) {
    console.log(event);
    this.setState({
      radioValue: event.target.value,
      valid: this.state.url !== "" && event.target.value !== "",
    });
    // if (this.state.url !== "" && this.state.radioValue !== ""){
    //   this.setState({ valid: true });
    // }
    // else{
    //   this.setState({ valid: false });
    // }
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

  render() {
    return (
      <div>
        <Box
          component="form"
          // sx={{
          //     padding: 2
          // }}
          // sx={{
          //     // display: 'flex',
          //     // alignItems: 'center',
          //     // flexDirection: 'column',
          //     // p: 2,
          //     // m: 2,
          //     // bgcolor: 'background.paper',
          //   }}
          // fullWidth
          // backgroundColor='primary.main'
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          autoComplete="off"
          onSubmit={this.onSubmit}
        >
          {/* <div style={{ padding: 16, margin: "auto" }} > */}
          {/* <form onSubmit={this.onSubmit}> */}
          <div>
            <TextField
              required
              style={{ width: 400, margin: 20 }}
              value={this.state.url}
              onChange={this.handleChange}
              id="outlined-basic"
              label="YouTube Video Link"
              variant="outlined"
            />
          </div>
          {/* <RadioGroup>
          <Radio
            label="A"
            value="a"
            name="radio-buttons"
            inputProps={{ 'aria-label': 'A' }}
          />
        </RadioGroup> */}
          <RadioGroup
            aria-label="gender"
            name="controlled-radio-buttons-group"
            value={this.state.radioValue}
            onChange={this.handleRadioChange}
          >
            <FormControlLabel
              value="911"
              control={<Radio />}
              label="9/11 Conspiracy Theory"
            />
            <FormControlLabel
              value="chentrails"
              control={<Radio />}
              label="Chemtrails Conspiracy Theory"
            />
            <FormControlLabel
              value="flatearth"
              control={<Radio />}
              label="Flat Earth Theory"
            />
            <FormControlLabel
              value="moonlanding"
              control={<Radio />}
              label="Moonlanding "
            />
            <FormControlLabel
              value="vaccines"
              control={<Radio />}
              label="Vaccine Controversy"
            />
          </RadioGroup>
          <div>
            {/* <TextField id="filled-basic" label="YouTube Video Link" variant="filled" />
                    <TextField id="standard-basic" label="YouTube Video Link" variant="standard" /> */}
            <Button disabled={!this.state.valid} type="submit">
              Detect
            </Button>
          </div>

          {this.state.embedId !== "" ? (
            <YoutubeEmbed embedId={this.state.embedId} />
          ) : (
            <div></div>
          )}
          <div>
            {this.state.detection && (
              <Box display="flex" alignItems="center" justifyContent="center">
                <Typography component="span" variant="h5" color="text.primary">
                  {(this.state.detection === 0 && "Neutral") ||
                    (this.state.detection === 1 && "Misinformation") ||
                    (this.state.detection === -1 && "Debunking Misinformation")}
                  <Button
                    variant="text"
                    onClick={() =>
                      this.handleWrongDialogOpen({
                        Title: "Do you think the video is wrongly classified?",
                        vid_url: this.state.url,
                        normalized_annotation: this.state.detection,
                      })
                    }
                  >
                    Wrong?
                  </Button>
                </Typography>
              </Box>
            )}
          </div>
        </Box>
        {/* <Container
        > */}
        {this.state.wrong && (
          <WrongDialog
            wrong={this.state.wrong}
            handleClose={this.handleWrongDialogClose}
            handleSubmit={this.handleWrongDialogSubmit}
          />
        )}
        {/* </Container> */}
      </div>
    );
  }
}

const YoutubeEmbed = ({ embedId }) => (
  <div className="video-responsive">
    <iframe
      width="853"
      height="480"
      src={`https://www.youtube.com/embed/${embedId}`}
      frameBorder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowFullScreen
      title="Embedded youtube"
    />
  </div>
);

YoutubeEmbed.propTypes = {
  embedId: PropTypes.string.isRequired,
};

export default DetectPage;
