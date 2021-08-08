import axios from "axios";

var API = "https://api.meaningcloud.com/sentiment-2.1";
const formdata = new FormData();
formdata.append("key", "");

formdata.append("lang", "es");  // 2
export const getSentiment = async (sentence) => {
    formdata.append("txt", sentence);
    console.log("se envia",formdata.getAll("txt"));
    return await axios
    .post(API, formdata)
    .then((response) => {
      //if (response.data.accessToken) {
      // localStorage.setItem("userInfo", JSON.stringify(response.data));
      //}
      console.log("api response",response);
      let r = {
        emotion: response.data.score_tag,
        ironic: response.data.irony
      };
      console.log("r compo",r);
      return r;
    })
    .catch((error) => {
      console.log(error);
    });
};
