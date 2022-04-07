import React from "react";
import {
  Box,
  List,
  TextField,
  Button,
  Radio,
  RadioGroup,
  FormControlLabel,
  Typography,
  Divider,
} from "@mui/material";
import axios from "axios";
import PropTypes from "prop-types";
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
      detection: [],
      topic: "",
      valid: false,
      wrong: false,
      title: null,
      voting: null,
      error: false
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
    if (this.state.url.includes("?v=")){
      this.setState({
        embedId: this.state.url.split("?v=")[1].split("&")[0],
        error: false
      });
      axios
      .post("http://127.0.0.1:5000/detect", {
        url: this.state.url,
        topic: this.state.topic,
      })
      .then((response) => {
        console.log("SUCCESS", response);
        this.setState({
          status_code: response.data.status,
          detection: response.data.detection,
          voting: response.data.voting,
          title: response.data.Title,
        });
        // setGetMessage(response);
      })
      .catch((error) => {
        console.log(error);
        this.setState({ detection: false });
      });
    }
    else{
      this.setState({
        embedId: "",
        error: true,
      });
    }
    // alert("A URL was submitted: " + this.state.url);
    event.preventDefault();
    
  }

  handleChange(event) {
    console.log(event);
    this.setState({
      url: event.target.value,
      valid: event.target.value !== "" && this.state.topic !== "",
      error: false
    });
    // if (this.state.url !== "" && this.state.topic !== ""){
    //   this.setState({ valid: true });
    // }
    // else{
    //   this.setState({ valid: false });
    // }
  }

  handleRadioChange(event) {
    console.log(event);
    this.setState({
      topic: event.target.value,
      valid: this.state.url !== "" && event.target.value !== "",
    });
    // if (this.state.url !== "" && this.state.topic !== ""){
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

  handleWrongDialogSubmit(vid_url, tags, label, reasons) {
    console.log(vid_url, label, reasons);
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
              error={this.state.error}
              helperText={this.state.error && "Enter valid URL."}
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
            aria-label="topic"
            name="controlled-radio-buttons-group"
            value={this.state.topic}
            onChange={this.handleRadioChange}
          >
            <FormControlLabel
              value="911"
              control={<Radio />}
              label="9/11 Conspiracy Theory"
            />
            <FormControlLabel
              value="chemtrails"
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
          {this.state.status_code === "Error" && this.state.detection !== "" && (
            <Box
            sx={{ flexDirection: "column", padding: 2 }}
            display="flex"
            alignItems="center"
            justifyContent="center"
          >
            <Typography
              component="span"
              variant="h5"
              color="text.primary"
            >
              {this.state.detection}
            </Typography>
            </Box>
          )}
          {this.state.status_code === "Success" && this.state.detection !== [] && (
            <List sx={{ width: "100%", bgcolor: "background.paper" }}>
              {this.state.detection.map((det, i) => (
                <div>
                  <Box
                    sx={{ flexDirection: "column", padding: 2 }}
                    display="flex"
                    alignItems="center"
                    justifyContent="center"
                  >
                    <Typography
                      component="span"
                      variant="h7"
                      color="text.primary"
                    >
                      Model: {det.model}
                    </Typography>
                    <Typography
                      component="span"
                      variant="h5"
                      color="text.primary"
                    >
                      {(det.value === 0 && "Neutral") ||
                        (det.value === 1 && "Misinformation") ||
                        (det.value === -1 && "Debunking Misinformation")}
                      <Button
                        variant="text"
                        onClick={() =>
                          this.handleWrongDialogOpen({
                            Title: this.state.title,
                            vid_url: this.state.url,
                            tags: [this.state.topic],
                            normalized_annotation: det.value,
                            voting: this.state.voting,
                          })
                        }
                      >
                        Don't agree?
                      </Button>
                    </Typography>
                  </Box>
                  <Divider />
                </div>
                // )) ||
                //   // (typeof this.state.detection.value === "string" && (
                //   //   <Box
                //   //     display="flex"
                //   //     alignItems="center"
                //   //     justifyContent="center"
                //   //   >
                //   //     <Typography
                //   //       component="span"
                //   //       variant="h5"
                //   //       color="text.primary"
                //   //     >
                //   //       {this.state.detection}
                //   //     </Typography>
                //   //   </Box>
                //   // ))
              ))}
            </List>
          )}
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
