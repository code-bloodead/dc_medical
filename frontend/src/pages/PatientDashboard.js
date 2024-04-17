import React, { useState, useEffect } from "react";
import { Redirect } from "react-router-dom";
import List from "../components/List";
import Modal from "../components/Modal";
import axios from "axios";
import Loader from "../components/Loader";
import { AUTHORITY_TYPES } from "../Constants/authorityTypes";
import { useAuth } from "../services/authorization";
import { figureOutGender, getInitials, calculateAge } from "../utils/dataUtils";

import {
  Container,
  SubContainer,
  PatientNameContainer,
  PatientDetailsContainer,
  PatientAddressContainer,
  Cirlce,
  PatientName,
  ShowingSearchResultContainer,
  ShowingSearchResultText,
  ShowingSearchResultText2,
  RefreshButton,
  SubContainer2,
  PatientDetailsSub,
  PatientAddressSub,
  DownArrow,
  ToggleContainer,
  Toggle,
  PatientAddress,
  Note,
  ShowingSearchResultContainerMobile,
  ToggleContainerMobile,
  PatientGender,
  PatientDetailsGender,
  Backdrop,
} from "./PatientDashboard.styled";
import {
  ModalContainer,
  ModalFooter,
  ModalSubHeading,
} from "../components/Modal";
import ReportsModal from "../components/ReportsModal";

const PatientDashboard = () => {
  const auth = useAuth();
  const PatientDetails = auth.entityInfo;

  const [MedicalHistory, setMedicalHistory] = useState([]);
  const [PendingRequests, setPendingRequests] = useState([]);
  // const [declinedRecords, setDeclinedRecords] = useState([]);

  const [isLoading, setIsLoading] = useState(false);

  const [refresh, setRefresh] = useState(Number(new Date()));

  const [showAddress, setShowAddress] = useState(false);
  const [modalState, setModalState] = useState(false);
  const [showAdd, setShowAdd] = useState(false);
  const [reportsModalState, setReportsModalState] = useState(false);

  // true = medicalHistory, false = pendingHistory
  const [toggle, setToggle] = useState(true);

  const toggleAddrecord = () => setShowAdd(true);

  async function AddRecord(e) {
    const API_URL = "http://127.0.0.1:8000/files";
    e.preventDefault();
    console.log(e);
    console.log(e.target[0].value);

    const formDataToSend = new FormData();
    const queryParams = {
      name: PatientDetails.fname,
      patient_id: PatientDetails.patient_id,
      dob: PatientDetails.birthdate,
      //   name: PatientDetails.fname+" "+PatientDetails.lname,
      disease: e.target[0].value,
      treatment: e.target[1].value,
      doctor: e.target[2].value,
      medication: e.target[3].value,
      diagnosis_date: e.target[4].value,
      discharge_date:
        e.target[5].value?.length > 0 ? e.target[5].value : "1805-05-05",
      hospital_record_id: e.target[6].value,
      was_admitted: e.target[5].value?.length > 0,
    };
    console.log("Query params", queryParams);
    // http://127.0.0.1:8000/files/?name=emily%20davis&patient_id=98765&dob=1995-04-02&disease=dds&treatment=meds&doctor=kj&medication=medds&diagnosis_date=2024-04-04&discharge_date=2024-04-04&hospital_record_id=HRR&was_admitted=true
    console.log("Filedata", e.target[7]);
    const file_data = e.target[7].files[0];
    formDataToSend.append("file_data", file_data);
    console.log("Filedata", file_data);
    console.log("Formdata", formDataToSend);

    const res = await axios.post(API_URL, formDataToSend, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      params: queryParams,
    });
    console.log(res);
    setRefresh(Number(new Date()));

    e.preventDefault();
    e.target.reset();
  }

  useEffect(() => {
    console.log("Fetching all records for", PatientDetails);
    if (!PatientDetails) return;
    setIsLoading(true);
    console.log("Fetching all records");
    axios
      .get(`http://localhost:8000/records/${PatientDetails.patient_id}`)
      .then((res) => {
        const response = res.data;
        const records = (response?.records || []).filter(
          (rec) => rec.treatment !== "REGISTERED"
        );
        console.log("Fetched", records);
        setMedicalHistory(records);
        setIsLoading(false);
      })
      .catch((err) => {
        console.log("Some error fetching records", err);
        setMedicalHistory([]);
        setIsLoading(false);
      });
    // getRecordHistory(patientBlockchainAddress)
    //     .then(rawRecords => {
    //         processRecords(rawRecords)
    //             .then(processedRecords => {
    //                 setIsLoading(false);
    //                 setMedicalHistory(processedRecords.medicalHistory)
    //                 setPendingRequests(processedRecords.pendingRecords)
    //             })
    //             .catch(err => {
    //                 console.log("Some error fetching records", err);
    //             });
    //     }).catch(err => {
    //         console.log("Some error fetching records", err);
    //     })
  }, [refresh]);

  if (!auth.loggedIn || !auth.entityInfo || !auth.authority) {
    auth.logout();
    return <Redirect to="/login/patient" />;
  }

  const inputStyle = {
    width: "100%",
    padding: "4px",
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

  //   buttonStyle:hover = {
  //   };

  if (auth.authority !== AUTHORITY_TYPES.PATIENT) return <Redirect to="/" />;

  console.log("Modal state", modalState);
  return (
    <Container>
      {modalState && <Backdrop onClick={() => setModalState(false)} />}
      {reportsModalState && (
        <Backdrop onClick={() => setReportsModalState(false)} />
      )}
      {reportsModalState && (
        <ReportsModal
          modalState={reportsModalState}
          medicalHistory={toggle}
          setReportsModalState={setReportsModalState}
          setModalState={setModalState}
        />
      )}
      {modalState && (
        <Modal
          medicalHistory={toggle}
          modalState={modalState}
          setModalState={setModalState}
          setReportsModalState={setReportsModalState}
        />
      )}
      <SubContainer>
        <PatientNameContainer>
          <Cirlce>{getInitials(PatientDetails.fname)}</Cirlce>
          <PatientName>
            {PatientDetails.fname} {PatientDetails.lname}
          </PatientName>
          <PatientGender>
            {figureOutGender(PatientDetails.gender)}
          </PatientGender>
        </PatientNameContainer>
        <PatientDetailsContainer>
          <PatientDetailsSub>
            DOB &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : &nbsp;
            {PatientDetails.birthdate}
          </PatientDetailsSub>
          <PatientDetailsSub>
            {calculateAge(PatientDetails.birthdate)}
          </PatientDetailsSub>
          <PatientDetailsGender>
            Gender&nbsp;: {figureOutGender(PatientDetails.gender)}
          </PatientDetailsGender>
          {/* <PatientDetailsSub>
                        Phone&nbsp;&nbsp;&nbsp;: +91 {PatientDetails.phone}
                    </PatientDetailsSub> */}
        </PatientDetailsContainer>
        <PatientAddressContainer></PatientAddressContainer>
        <div className="p-3">
          <form
            onSubmit={AddRecord}
            style={{ maxWidth: "400px", margin: "0 auto", textAlign: "center" }}
          >
            <input type="text" placeholder="Disease" style={inputStyle} />
            <input type="text" placeholder="Treatment" style={inputStyle} />
            <input type="text" placeholder="Doctor" style={inputStyle} />
            <input type="text" placeholder="Medication" style={inputStyle} />
            Diagnosis date: &nbsp;
            <input
              type="date"
              placeholder="Diagnosis Date"
              style={inputStyleInline}
            />
            Discharge date: &nbsp;
            <input
              type="date"
              placeholder="Discharge Date"
              style={inputStyleInline}
            />
            <input
              type="text"
              placeholder="Hospital record ID"
              style={inputStyle}
            />
            <input type="file" style={inputStyle} />
            <button type="submit" style={buttonStyle}>
              Submit
            </button>
          </form>
        </div>
        {/* <ToggleContainer>
                    <Toggle selected={toggle} onClick={() => setToggle(true)}>Medical History</Toggle>
                    <Toggle selected={!toggle} onClick={() => setToggle(false)}>Pending Requests</Toggle>
                </ToggleContainer> */}
      </SubContainer>

      {/* Mobile UI */}
      <ShowingSearchResultContainerMobile>
        <ShowingSearchResultText>
          {toggle
            ? MedicalHistory.length === 0
              ? "No records to show"
              : MedicalHistory.length === 1
              ? "Showing 1 result"
              : `Showing result 1 - ${MedicalHistory.length}  out of ${MedicalHistory.length} results`
            : PendingRequests.length === 0
            ? "No records to show"
            : PendingRequests.length === 1
            ? "Showing 1 result"
            : `Showing result 1 - ${PendingRequests.length}  out of ${PendingRequests.length} results`}
        </ShowingSearchResultText>
        <ShowingSearchResultText2>
          last updated at 4:30 PM IST
          <RefreshButton onClick={() => setRefresh(Number(new Date()))}>
            Refresh
          </RefreshButton>
        </ShowingSearchResultText2>
      </ShowingSearchResultContainerMobile>

      {/* Mobile UI */}

      {isLoading ? (
        <Loader />
      ) : (
        <SubContainer2>
          <ShowingSearchResultContainer>
            <ShowingSearchResultText>
              {toggle
                ? MedicalHistory.length === 0
                  ? "No records to show"
                  : MedicalHistory.length === 1
                  ? "Showing 1 result"
                  : `Showing result 1 - ${MedicalHistory.length}  out of ${MedicalHistory.length} results`
                : PendingRequests.length === 0
                ? "No records to show"
                : PendingRequests.length === 1
                ? "Showing 1 result"
                : `Showing result 1 - ${PendingRequests.length}  out of ${PendingRequests.length} results`}
            </ShowingSearchResultText>
            <ShowingSearchResultText2>
              last updated at 4:30 PM IST
              <RefreshButton onClick={() => setRefresh(Number(new Date()))}>
                Refresh
              </RefreshButton>
            </ShowingSearchResultText2>
          </ShowingSearchResultContainer>
          <List
            data={toggle ? MedicalHistory : PendingRequests}
            setModalState={setModalState}
          />
          <Note>Click the record to view the details</Note>
        </SubContainer2>
      )}

      {/* Mobile UI */}
      <ToggleContainerMobile>
        <Toggle selected={toggle} onClick={() => setToggle(true)}>
          Medical History
        </Toggle>
        <Toggle selected={!toggle} onClick={() => setToggle(false)}>
          Pending Requests
        </Toggle>
      </ToggleContainerMobile>
      {/* Mobile UI */}
    </Container>
  );
};

export default PatientDashboard;
