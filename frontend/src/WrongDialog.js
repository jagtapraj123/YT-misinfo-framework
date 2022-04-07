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
  ListItem,
  ListItemText,
  Checkbox,
} from "@mui/material";

export default function WrongDialog(props) {
  const { wrong, handleClose, handleSubmit } = props;
  const { vid_url, Title, tags, normalized_annotation, voting } = wrong;
  const neutrals = voting ? (voting[0] ? voting[0].length : 0) : 0;
  const misinfos = voting ? (voting[1] ? voting[1].length : 0) : 0;
  const debunking = voting ? (voting[-1] ? voting[-1].length : 0) : 0;
  console.log(voting);
  var [label, setLabel] = React.useState(wrong.normalized_annotation);
  var [reason, setReason] = React.useState("");
  var [add, setAdd] = React.useState(false);
  var [preSelected, setPreSelected] = React.useState(
    new Array(neutrals + misinfos + debunking).fill(0)
  );

  return (
    <div>
      <Dialog open={wrong} onClose={handleClose}>
        <DialogTitle>{Title}</DialogTitle>
        <DialogContent>
          {typeof(normalized_annotation) !== "undefined" && (<DialogContentText>
            <Typography>
              The video is currently labelled as{" "}
              <Typography component="span" variant="body" color="text.primary">
                {(normalized_annotation === 0 && "Neutral") ||
                  (normalized_annotation === 1 && "Misinformation") ||
                  (normalized_annotation === -1 && "Debunking Misinformation")}
              </Typography>
              .
            </Typography>
            <Typography>Do you think it is mis-labelled?</Typography>
            <Typography>Kindly let us know why...</Typography>
          </DialogContentText>)}
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
                setAdd(false);
                setReason("");
                let temp = [...preSelected];
                temp.fill(0);
                setPreSelected(temp);
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
          {voting && (
            <Box>
              <List sx={{ width: "100%", bgcolor: "background.paper" }}>
                {voting[0] &&
                  label === 0 &&
                  voting[0].map((vote, i) => (
                    <div>
                      <ListItem
                        secondaryAction={
                          <Checkbox
                            edge="end"
                            onChange={() => {
                              let temp = [...preSelected];
                              temp[i] = !temp[i];
                              setPreSelected(temp);
                            }}
                            checked={preSelected[i]}
                            // inputProps={{ 'aria-labelledby': labelId }}
                          />
                        }
                      >
                        <ListItemText
                          primary={"Neutral -- " + vote.count + " votes"}
                          secondary={
                            <div>
                              <Typography
                                component="span"
                                variant="body2"
                                color="text.primary"
                              >
                                {vote.reason}
                              </Typography>
                            </div>
                          }
                        />
                      </ListItem>
                    </div>
                  ))}
                {voting[0] && label === 0 && <Divider />}
                {voting[1] &&
                  label === 1 &&
                  voting[1].map((vote, i) => (
                    <div>
                      <ListItem
                        secondaryAction={
                          <Checkbox
                            edge="end"
                            onChange={() => {
                              let temp = [...preSelected];
                              temp[neutrals + i] = !temp[neutrals + i];
                              setPreSelected(temp);
                            }}
                            checked={preSelected[neutrals + i]}
                            // inputProps={{ 'aria-labelledby': labelId }}
                          />
                        }
                      >
                        <ListItemText
                          primary={"Misinformation -- " + vote.count + " votes"}
                          secondary={
                            <div>
                              <Typography component="span" variant="body2">
                                {vote.reason}
                              </Typography>
                            </div>
                          }
                        />
                      </ListItem>
                    </div>
                  ))}
                {voting[1] && label === 1 && <Divider />}
                {voting[-1] &&
                  label === -1 &&
                  voting[-1].map((vote, i) => (
                    <div>
                      <ListItem
                        secondaryAction={
                          <Checkbox
                            edge="end"
                            onChange={() => {
                              let temp = [...preSelected];
                              temp[neutrals + misinfos + i] =
                                !temp[neutrals + misinfos + i];
                              setPreSelected(temp);
                            }}
                            checked={preSelected[neutrals + misinfos + i]}
                            // inputProps={{ 'aria-labelledby': labelId }}
                          />
                        }
                      >
                        <ListItemText
                          primary={
                            "Debunking Misinformation -- " +
                            vote.count +
                            " votes"
                          }
                          secondary={
                            <div>
                              <Typography component="span" variant="body2">
                                {vote.reason}
                              </Typography>
                            </div>
                          }
                        />
                      </ListItem>
                    </div>
                  ))}
                {voting[-1] && label === -1 && <Divider />}
              </List>
            </Box>
          )}
          {!add && (
            <Button
              style={{ marginLeft: 5, marginRight: 5 }}
              variant="outlined"
              // startIcon={<DownloadIcon />}
              onClick={() => setAdd(true)}
            >
              Add Reason
            </Button>
          )}
          {add && (
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
            disabled={
              (label === normalized_annotation || (add && reason === "") || (!add && !preSelected.includes(true))) 
              // &&
              // !preSelected.includes(true)
            }
            onClick={() => {
              var reasons = [];
              console.log(reasons, label, neutrals, label === 0 && neutrals > 0);
              console.log(preSelected.includes(true));
              if (preSelected.includes(true)){
                if (label === 0 && neutrals > 0){
                  // var selected = voting[0].filter((vote, i) => preSelected[i]);
                  console.log(voting[0].filter((vote, i) => preSelected[i]));
                  reasons = reasons.concat(voting[0].filter((vote, i) => preSelected[i]).map((sel, i) => sel.reason));
                }
                else if (label === 1 && misinfos > 0){
                  // var selected = voting[0].filter((vote, i) => preSelected[i]);
                  console.log(voting[1].filter((vote, i) => preSelected[neutrals+i]));
                  reasons = reasons.concat(voting[1].filter((vote, i) => preSelected[neutrals+i]).map((sel, i) => sel.reason));
                }
                else if (label === -1 && debunking > 0){
                  // var selected = voting[0].filter((vote, i) => preSelected[i]);
                  console.log(voting[-1].filter((vote, i) => preSelected[neutrals+misinfos+i]));
                  reasons = reasons.concat(voting[-1].filter((vote, i) => preSelected[neutrals+misinfos+i]).map((sel, i) => sel.reason));
                }
              }
              if (add && reason !== ""){
                reasons.push(reason);
              }
              console.log(reasons);
              handleSubmit(vid_url, tags, label, reasons);
            }}
          >
            Submit
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
