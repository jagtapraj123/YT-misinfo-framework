import { List, ListItem, Divider, ListItemText, Button } from "@mui/material";
import Typography from "@mui/material/Typography";

import React from "react";

function DatasetListView(props) {
  const { videoList, handleWrongDialogOpen } = props;
  //   var [wrong, setWrong] = React.useState(false);

  //   const handleWrongDialogOpen = (wrn) => {
  //     console.log(wrn);
  //     setWrong(wrn);
  //   };

  //   const handleWrongDialogClose = () => {
  //     console.log("Closed");
  //     setWrong(false);
  //   };

  //   const handleWrongDialogSubmit = (label, reason) => {
  //     console.log(label, reason);
  //     setWrong(false);
  //   };

  return (
    <div>
      <List sx={{ width: "100%", bgcolor: "background.paper" }}>
        {videoList.map((video, i) => (
          <div>
            <ListItem>
              <div>
                <ListItemText
                  primary={video.Title}
                  secondary={
                    <div>
                      <Typography
                        component="span"
                        variant="body2"
                        color="text.primary"
                      >
                        {video.tags &&
                          video.tags.map((tag, i) => " " + tag + " ") +
                            " — "}{" "}
                        {/* {video.Topic && video.Topic.name + " — "}{" "} */}
                        {(typeof(video.normalized_annotation) === "undefined" && "Under-moderation") || (video.normalized_annotation === 0 && "Neutral") ||
                          (video.normalized_annotation === 1 &&
                            "Misinformation") ||
                          (video.normalized_annotation === -1 &&
                            "Debunking Misinformation")}{" "}
                        <Button
                          size="small"
                          variant="text"
                          onClick={() => handleWrongDialogOpen(video)}
                        >
                          {(typeof(video.normalized_annotation) === "undefined" && "Vote Now!") || "Don't Agree?"}
                        </Button>
                      </Typography>
                    </div>
                  }
                />
                <ListItemText
                  secondary={
                    <div>
                      <Typography
                        component="span"
                        variant="body2"
                        color="text.primary"
                      >
                        <a href={video.vid_url}>{video.vid_url}</a>
                      </Typography>
                    </div>
                  }
                />
                <ListItemText
                  secondary={
                    <div>
                      <Typography component="span" variant="body">
                        {video.Description !== null &&
                          " — " + video.Description.slice(0, 800) + "..."}
                      </Typography>
                    </div>
                  }
                />
              </div>
            </ListItem>
            <Divider variant="middle" component="li" />
          </div>
        ))}
      </List>
    </div>
  );
}

DatasetListView.propTypes = {};

export default DatasetListView;

/*
export class DatasetListView extends Component {
    constructor(props) {
        super(props);
        const { videoList } = props;
        console.log(videoList);
        this.state = {
            videoList: videoList,
        }
    }
    
    render() {
        return (
            <div>
                <List sx={{ width: '100%', bgcolor: 'background.paper' }}>
                    {this.state.videoList.map((video, i) => (
                        <div><ListItem >
                        <ListItemText
                        primary="Brunch this weekend?"
                        secondary={
                            <React.Fragment>
                            <Typography
                                sx={{ display: 'inline' }}
                                component="span"
                                variant="body2"
                                color="text.primary"
                            >
                                Ali Connors
                            </Typography>
                            {" — I'll be in your neighborhood doing errands this aksdhakjdhaksdhkahdkahdkahkdhakdhaksjdhkadkajaskjdhakjdhaksjdhaksjhdshjhakshdkajshdakjshdkahdkashjkashdkajshdkjashdkajshdkahdkjahsdquwyeiquwyehwekqwheiuqweqmevqnveqwvenashdk"}
                            </React.Fragment>
                        }
                        />
                    </ListItem>
                    <Divider variant="middle" component="li" />
                    </div>
                    ))}
                </List>
            </div>
        );
    }
}

export default DatasetListView;
*/
