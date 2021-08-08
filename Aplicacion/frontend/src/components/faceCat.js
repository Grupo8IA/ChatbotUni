import React, { useEffect, useState } from "react";
import { makeStyles } from "@material-ui/core/styles";

import * as sentimentApi from "../services/SentimentApi";

const useStyles = makeStyles({
  root: {
    background: "linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)",
    border: 0,
    borderRadius: 3,
    boxShadow: "0 3px 5px 2px rgba(255, 105, 135, .3)",
    color: "white",
    height: 130,
    width: 190,
    padding: "0 30px",
    margin: "0 auto 0 auto"
  }
});

function FaceCat(props) {
  const classes = useStyles();
  var faces = {
    sad: "https://cdn.jsdelivr.net/emojione/assets/4.0/png/128/1f63f.png",
    heartEyes: "https://cdn.jsdelivr.net/emojione/assets/4.0/png/128/1f63b.png",
    surprise: "https://cdn.jsdelivr.net/emojione/assets/4.0/png/128/1f640.png",
    laughing: "https://cdn.jsdelivr.net/emojione/assets/4.0/png/128/1f639.png",
    kissing: "https://cdn.jsdelivr.net/emojione/assets/4.0/png/128/1f63d.png",
    wrySmile: "https://cdn.jsdelivr.net/emojione/assets/4.0/png/128/1f63c.png",
    angry: "https://cdn.jsdelivr.net/emojione/assets/4.0/png/128/1f63e.png",
    cuteSmile: "https://cdn.jsdelivr.net/emojione/assets/4.0/png/128/1f638.png",
    smiling: "https://cdn.jsdelivr.net/emojione/assets/4.0/png/128/1f63a.png",
    neutro: "https://cdn.jsdelivr.net/emojione/assets/4.0/png/128/1f431.png"
  };

  useEffect(()=>{
    console.log("nueva oración", props.sentence);
    console.log("renderizando cara")
    console.log("mensaje a interpretar: ",props.sentence)
    sentimentApi.getSentiment(props.sentence).then(
      (response) => {
        console.log("face cat value",response);
        evaluateEmotion(response);
      },
      (error) => {
        //alert("Usuario incorrecto");
        console.error(error);
      }
    );
  },[props.sentence])

  function evaluateEmotion(response) {
    if (response.ironic === "IRONIC") {
      setEmotion("wrySmile");
    } else if (response.emotion === "P+") {
      setEmotion("cuteSmile");
    } else if (response.emotion === "P") {
      setEmotion("smiling");
    } else if (response.emotion === "NEU") {
      setEmotion("neutro");
    } else if (response.emotion === "N") {
      setEmotion("angry");
    } else if (response.emotion === "N+") {
      setEmotion("surprise");
    } else {
      setEmotion("neutro");
    }
  }
  const [emotion, setEmotion] = useState("surprise");
  return (
    <div className={classes.root}>
      <img src={faces[emotion]}></img>
    </div>
  );
}

export default FaceCat;
