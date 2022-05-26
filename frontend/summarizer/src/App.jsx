import { useState } from "react";
import { Typography } from "@mui/material";
import "./App.css";
const App = () => {
  const [summarize, setSummmarize] = useState("");
  const [form, setForm] = useState({ paragraph: "" });
  const handleChange = (e, name) => {
    setForm((prevState) => ({ ...prevState, [name]: e.target.value }));
  };
  const handleSubmit = async (e) => {
    const { paragraph } = form;
    e.preventDefault();
    if (!paragraph) return;
    console.log(paragraph);

    const options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        paragraph: paragraph,
      }),
    };

    try {
      const data = await (
        await fetch("http://127.0.0.1:8000/summarize", options)
      ).json();
      console.log(data);
      setSummmarize(data.answer);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div
      style={{
        //backgroundImage: "url(/background.jpg)",
        opacity: 0.8,
        backgroundRepeat: "no-repeat",
        backgroundSize: "cover",
        height: "700px",
        width: "1520px",
        justifyContent: "space-evenly",
        display: "flex",
      }}
    >
      <div
        style={{
          height: "80%",
          width: "40%",
          justifyContent: "space-evenly",
        }}
      >
        <Typography>Nhập đoạn văn bản bạn muốn tóm tắt</Typography>
        <textarea
          type="text"
          name="paragraph"
          placeholder="Something"
          onChange={(e) => handleChange(e, "paragraph")}
          style={{
            minHeight: "60%",
            minWidth: "100%",
            opacity: 0.5,
          }}
        />
        <button type="button" onClick={handleSubmit}>
          Submit
        </button>
      </div>
      <div
        style={{
          height: "80%",
          width: "40%",
          paddingBlock: "10%",
        }}
      >
        <Typography>{summarize}</Typography>
      </div>
    </div>
  );
};
export default App;
