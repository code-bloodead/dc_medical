import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import { useParams, Redirect } from "react-router-dom";
import { TextField } from "@mui/material";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSpinner, faCamera } from "@fortawesome/free-solid-svg-icons";
import QrReader from "react-qr-reader";
import QrcodeDecoder from "qrcode-decoder";
import axios from "axios";

import basicInfo from "../assets/illustrations/basicInfo2.png";
import CoreButton from "../components/core/Button";
import { useAuth } from "../services/authorization";
import { universalLogin } from "../apis/medblock";
import { AUTHORITY_TYPES } from "../Constants/authorityTypes";
import {
  AppNameContainer,
  AppOveriewIllustration,
  ButtonContainer,
  Container,
  CreateAccountText,
  Heading,
  OrDiv,
  PageName,
  UploadQrCodeButton,
  ScanOrButton,
  ScanOrButtonMobile,
  SubContainer1,
  SubContainer2,
  SubHeading,
  TextFieldContainer,
} from "./Login.styled";

const Signup = () => {
  const auth = useAuth();
  const history = useHistory();

  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [openWebcam, setOpenWebcam] = useState(false);
  const [openWebcamMobile, setOpenWebcamMobile] = useState(false);

  const { type } = useParams();
  const AuthorityType = AUTHORITY_TYPES.PATIENT;

  const onHandlerErrWebcam = (error) => {
    console.log(error);
  };

  const onHandlerResultWebcam = (result) => {
    if (result) {
      setOpenWebcam(false);
      setOpenWebcamMobile(false);
    }
  };

  const convertBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const fileReader = new FileReader();
      fileReader.readAsDataURL(file);
      fileReader.onload = () => {
        resolve(fileReader.result);
      };
      fileReader.onerror = (error) => {
        reject(error);
      };
    });
  };

  const onFileChangeHandler = async (file) => {
    setOpenWebcam(false);
    setOpenWebcamMobile(false);

    const base64File = await convertBase64(file);

    var qr = new QrcodeDecoder();
    qr.decodeFromImage(base64File).then((res) => {
      console.log(res.data);
    });
  };

  if (auth.loggedIn) {
    const path = `/${type}Dashboard`;
    console.log(path);
    console.log("Redirect to", path);
    return <Redirect to={path} />;
  }

  const inputStyle = {
    width: "100%",
    padding: "10px",
    marginBottom: "10px",
    borderRadius: "5px",
    border: "1px solid #ccc",
    boxSizing: "border-box",
  };
  const inputStyleInline = {
    padding: "4px",
    marginBottom: "10px",
    borderRadius: "5px",
    border: "1px solid #ccc",
    boxSizing: "border-box",
  };

  const buttonStyle = {
    width: "100%",
    padding: "10px",
    borderRadius: "5px",
    border: "none",
    backgroundColor: "#007bff",
    color: "#fff",
    cursor: "pointer",
    transition: "background-color 0.3s ease",
    "&:hover": {
      backgroundColor: "#0056b3",
    },
  };

  async function AddPatient(e) {
    e.preventDefault();

    const API_URL = "http://127.0.0.1:8000/newuser";
    e.preventDefault();
    console.log(e);
    console.log(e.target[0].value);
    setIsLoggingIn(true);
    const patient_id = e.target[0].value
    const queryParams = {
      patient_id,
      name: e.target[1].value,
      dob: e.target[2].value,
    };
    console.log("Query params", queryParams);
    // http://127.0.0.1:8000/files/?name=emily%20davis&patient_id=98765&dob=1995-04-02&disease=dds&treatment=meds&doctor=kj&medication=medds&diagnosis_date=2024-04-04&discharge_date=2024-04-04&hospital_record_id=HRR&was_admitted=true
    console.log("Filedata", e.target[7]);

    const res = await axios.post(
      API_URL,
      {},
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        params: queryParams,
      }
    );
    console.log(res);

    universalLogin(patient_id, AuthorityType)
      .then((info) => {
        console.log("Logged into", info);
        const successfulLogin = auth.login(patient_id, AuthorityType, info);
        if (successfulLogin)
          console.log(`Login successful with following ${AuthorityType} info: `, info);
        else console.log("Some err logging in!, ", successfulLogin);
        setIsLoggingIn(false);
        history.push(`/patientDashboard`)
      })
      .catch((err) => {
        alert("Invalid patient key !!", err);
        console.log("Login failed :( with following response: ");
        console.log(err);
        setIsLoggingIn(false);
      });
    e.target.reset();
  }

  return (
    <Container>
      <SubContainer1>
        <AppNameContainer>
          <img src={basicInfo} alt="Medblock" />
          <Heading>Distributed platform</Heading>
          <SubHeading>to store your medical history</SubHeading>
        </AppNameContainer>
        {!openWebcam && <AppOveriewIllustration />}
        {openWebcam && (
          <QrReader
            style={{
              width: "50%",
              marginTop: "40px",
              border: "solid black 1px",
            }}
            delay={300}
            onError={onHandlerErrWebcam}
            onScan={onHandlerResultWebcam}
          />
        )}
      </SubContainer1>
      <SubContainer2>
        <PageName>Patient Signup</PageName>
        <br />
        <br />
        {openWebcamMobile && (
          <QrReader
            style={{
              width: "60%",
              marginTop: "40px",
              border: "solid black 1px",
            }}
            delay={300}
            onError={onHandlerErrWebcam}
            onScan={onHandlerResultWebcam}
          />
        )}

        <form
          onSubmit={AddPatient}
          style={{ maxWidth: "400px", margin: "0 auto", textAlign: "center" }}
        >
          <input type="text" placeholder="Patient ID" style={inputStyle} />
          <input type="text" placeholder="Name" style={inputStyle} />
          Date of birth: &nbsp;
          <input
            type="date"
            placeholder="Diagnosis Date"
            style={inputStyleInline}
          />
          <br />
          <CoreButton
            disabled={isLoggingIn}
            style={{ marginTop: "20px" }}
            type="submit"
            // onClick={!isLoggingIn ? AddPatient : null}
          >
            {isLoggingIn ? (
              <>
                Trying to login. &nbsp;&nbsp;
                <FontAwesomeIcon icon={faSpinner} className="fa-spin" />
              </>
            ) : (
              "Signup"
            )}
          </CoreButton>
        </form>
      </SubContainer2>
    </Container>
  );
};

export default Signup;
