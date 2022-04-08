import React from "react";
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  TextField,
  DialogActions,
  Typography,
  RadioGroup,
  FormControlLabel,
  Radio,
  Divider,
  FormLabel,
  List,
  Checkbox,
  CircularProgress,
} from "@mui/material";
import { WithContext as ReactTags } from "react-tag-input";
import "./AddVideoDialog.css";
import axios from "axios";

const KeyCodes = {
  TAB: 9,
  COMMA: 188,
  ENTER: 13,
  SPACE: 32,
};

const delimiters = [
  KeyCodes.TAB,
  KeyCodes.COMMA,
  KeyCodes.ENTER,
  KeyCodes.SPACE,
];

export default function AddVideoDialog(props) {
  const { open, handleClose, handleSubmit, tags } = props;
  var [url, setURL] = React.useState("");
  var [urlValid, setUrlValid] = React.useState(true);
  var [loading, setLoading] = React.useState(false);
  var [urlFailReason, setURLFailReason] = React.useState("");
  var [label, setLabel] = React.useState(0);
  var [reason, setReason] = React.useState("");
  var [selectedTags, setSelectedTags] = React.useState([]);
  var [newTags, setNewTags] = React.useState([]);

  const handleDelete = (i) => {
    setNewTags(newTags.filter((tag, index) => index !== i));
  };

  const handleAddition = (tag) => {
    console.log(tag);
    setNewTags([...newTags, tag]);
  };

  const handleDrag = (tag, currPos, newPos) => {
    const updatedTags = newTags.slice();

    updatedTags.splice(currPos, 1);
    updatedTags.splice(newPos, 0, tag);

    // re-render
    setNewTags(updatedTags);
  };

  const handleTagClick = (index) => {
    console.log("The tag at index " + index + " was clicked");
  };

  return (
    <div>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>{"Adding a video to Dataset"}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            <Typography>
              Kindly enter required details for the video in form below.
            </Typography>
          </DialogContentText>
          <Box
            sx={{
              paddingTop: 2,
            }}
          >
            <TextField
              id="outlined-multiline-flexible"
              label="Video URL"
              multiline
              maxRows={10}
              fullWidth
              required
              value={url}
              error={!urlValid}
              helperText={!urlValid && urlFailReason}
              onChange={(event) => {
                setURL(event.target.value);
                axios
                  .get("http://jackfruit.iitgoa.ac.in:1080/checkVideo", {
                    params: { url: encodeURI(event.target.value) },
                  })
                  .then((response) => {
                    if (response.data.valid) {
                      setUrlValid(true);
                    } else {
                      setUrlValid(false);
                      setURLFailReason(response.data.reason);
                    }
                  });
              }}
            />
          </Box>
          <Divider />
          <Box
            sx={{
              paddingTop: 2,
            }}
          >
            <FormLabel component="legend">Tags:</FormLabel>
            <List>
              {tags.map((tag, i) => (
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={selectedTags.includes(tag)}
                      name={tag}
                      onChange={(event) => {
                        if (event.target.checked) {
                          setSelectedTags([...selectedTags, event.target.name]);
                        } else {
                          setSelectedTags(
                            selectedTags.filter(
                              (tag) => tag !== event.target.name
                            )
                          );
                        }
                      }}
                    />
                  }
                  label={tag}
                  // value={tag}
                />
              ))}
              <div>
                <ReactTags
                  tags={newTags}
                  // suggestions={()=>{}}
                  delimiters={delimiters}
                  handleDelete={handleDelete}
                  handleAddition={handleAddition}
                  handleDrag={handleDrag}
                  handleTagClick={handleTagClick}
                  inputFieldPosition="inline"
                />
              </div>
            </List>
          </Box>
          <Divider />
          <Box
            sx={{
              paddingTop: 2,
            }}
          >
            <FormLabel component="legend">Correct Label:</FormLabel>
            <RadioGroup
              aria-label="gender"
              name="controlled-radio-buttons-group"
              value={label}
              onChange={(event) => {
                setLabel(parseInt(event.target.value));
              }}
            >
              <FormControlLabel value={0} control={<Radio />} label="Neutral" />
              <FormControlLabel
                value={1}
                control={<Radio />}
                label="Misinformation"
              />
              <FormControlLabel
                value={-1}
                control={<Radio />}
                label="Debunking Misinformation"
              />
            </RadioGroup>
          </Box>
          {true && (
            <Box
              sx={{
                paddingTop: 2,
              }}
            >
              <TextField
                id="outlined-multiline-flexible"
                label="Reason"
                multiline
                maxRows={10}
                fullWidth
                required
                value={reason}
                onChange={(event) => {
                  setReason(event.target.value);
                }}
              />
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button
            disabled={reason === "" || url === "" || !urlValid}
            onClick={() => {
              setLoading(true);
              handleSubmit(
                url,
                selectedTags,
                newTags,
                label,
                [reason],
                setUrlValid,
                setURLFailReason,
                setLoading
              );
            }}
          >
            Submit
          </Button>
          {loading && (
            <CircularProgress
              size={24}
              sx={{
                position: "absolute",
                top: "50%",
                left: "50%",
                marginTop: "-12px",
                marginLeft: "-12px",
              }}
            />
          )}
        </DialogActions>
      </Dialog>
    </div>
  );
}
