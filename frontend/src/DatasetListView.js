import { List, ListItem, Divider, ListItemText, Button } from "@mui/material";
import Typography from "@mui/material/Typography";

import React from "react";

function DatasetListView(props) {
  const { videoList, handleWrongDialogOpen } = props;

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
                        {(typeof video.normalized_annotation === "undefined" &&
                          "Under-moderation") ||
                          (video.normalized_annotation === 0 && "Neutral") ||
                          (video.normalized_annotation === 1 &&
                            "Misinformation") ||
                          (video.normalized_annotation === -1 &&
                            "Debunking Misinformation")}{" "}
                        <Button
                          size="small"
                          variant="text"
                          onClick={() => handleWrongDialogOpen(video)}
                        >
                          {(typeof video.normalized_annotation ===
                            "undefined" &&
                            "Vote Now!") ||
                            "Don't Agree?"}
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
