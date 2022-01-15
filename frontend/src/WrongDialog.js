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
} from "@mui/material";

export default function WrongDialog(props) {
  const { wrong, handleClose, handleSubmit } = props;
  var [label, setLabel] = React.useState(wrong.normalized_annotation);
  var [reason, setReason] = React.useState("");
  return (
    <div>
      <Dialog open={wrong} onClose={handleClose}>
        <DialogTitle>{wrong.Title}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            <Typography>
              The video is currently labelled as{" "}
              <Typography component="span" variant="body" color="text.primary">
                {(wrong.normalized_annotation === 0 && "Neutral") ||
                  (wrong.normalized_annotation === 1 && "Misinformation") ||
                  (wrong.normalized_annotation === -1 &&
                    "Debunking Misinformation")}
              </Typography>
              .
            </Typography>
            <Typography>Do you think it is mis-labelled?</Typography>
            <Typography>Kindly let us know why...</Typography>
          </DialogContentText>
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
            {/* <FormLabel component="legend">Correct Label:</FormLabel> */}
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
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button
            disabled={label === wrong.normalized_annotation || reason === ""}
            onClick={() => {
              handleSubmit(wrong.vid_url, label, reason);
            }}
          >
            Submit
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
