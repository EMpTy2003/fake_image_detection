import { useState } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const [isShow, setIsShow] = useState(false);
  const [response, setResponse] = useState({});
  const [originalImage, setOriginalImage] = useState("");
  const [elaImage,setElaImage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent the default form submission

    try {
      const fileInput = document.getElementById("file");
      const file = fileInput.files[0];

      if (!file) {
        alert("Please select a file");
        return;
      }

      const formData = new FormData();
      formData.append("file", file);

      const config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };

      const response = await axios.post(
        "/api/v1/uploadfile/",
        formData,
        config
      );

      if (response.status == 200) {
        setIsShow(true);
        console.log(response.data);
        setResponse(response.data);
        setOriginalImage(""); // Clear the previous original image
        fetchOriginalImage(); // Fetch and set the new original image
      }

    } catch (error) {
      setIsShow(false);
      alert("Only jpg, png accepted.")
      console.error(error);
    }

  };


  const fetchOriginalImage = async () => {
    try {
      // Make a request to the backend to fetch the original image
      const originalImageUrl =
        "http://localhost:8000/api/v1/get_image/original.jpg";

      const elaImageUrl = "http://localhost:8000/api/v1/get_image/ela_result.jpg"

      const originalImageResponse = await axios.get(originalImageUrl, {
        responseType: "blob", // Ensure that the response is treated as binary data
      });

      const elaImageResponse = await axios.get(elaImageUrl, {
        responseType: "blob", // Ensure that the response is treated as binary data
      });

      // Convert the binary data to a data URL
      const blob1 = new Blob([originalImageResponse.data]);
      const dataUrl1 = URL.createObjectURL(blob1);

      const blob2 = new Blob([elaImageResponse.data]);
      const dataUrl2 = URL.createObjectURL(blob2);

      // Set the data URL as the background image of the "original" div
      setOriginalImage(dataUrl1);
      setElaImage(dataUrl2)
    } catch (error) {
      console.error("Error fetching original image:", error);
    }
  };

  return (
    <>
      <div className="App">
        <div className="top">
        <h1>Fake Image Detection</h1>
        <p>Provide the image:</p>
        <form>
          <input type="file" name="file" id="file" />
        </form>
        <button onClick={handleSubmit}>Proceed</button>
        </div>

        <div className="output">
          <div className="details">
            <h3>Prediction Details :</h3>
            Result : {isShow? response.class : "-"} <br />
            Confidence : {isShow? response.con+"%" : "-"}<br /> <br />
            <hr />
            <h3>Conclusion :</h3>
            {isShow? "The given imaga is " + response.class+"." : " - "}
          </div>
          <div className="original" style={isShow? {backgroundImage: `url(${originalImage})`}: {background:"#FFF"}} >
            <h4>Original Image</h4>
          </div>
          <div className="ela_result" style={isShow ? { backgroundImage: `url(${elaImage})` }:{background:"#FFF"}}  >
            <h4>Error Level Analysis (ELA)</h4>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
