import React from 'react'

import { Heading } from './core'
import { dateFromTimestamp } from '../utils/dataUtils'
import { 
    Disease,
    Li,
    ListContainer,
    Sr,
    Hospital,
    Treatment,
    Date,
    DiseaseMobile,
    HeadingLi,
    HospitalHeading,
    DateHeading
} from './List.styled'

const List = ({data, setModalState}) => {
    return (
        <ListContainer>
            <HeadingLi>
                <Sr></Sr>
                <Disease>Disease</Disease>
                <DiseaseMobile>Disease</DiseaseMobile>
                {/* <HospitalHeading>Hospital</HospitalHeading> */}
                <Treatment>Treatment</Treatment>
                <DateHeading>Diagnosis Date</DateHeading>
                <DateHeading>Discharged Date</DateHeading>
            </HeadingLi>
            {
                data && data.length > 0 ?
                data.map((item, index) => {
                    return (
                        <Li key={index} onClick={() => {
                            console.log("onclick", item);
                            setModalState(item)

                            }}>
                            <Sr>{index+1}.</Sr>
                            <Disease>
                                {item.disease}
                            </Disease>
                            <DiseaseMobile onClick={() => setModalState(item)}>
                                {item.disease}
                            <div>{item.treatment}</div>
                            </DiseaseMobile>
                            {/* <Hospital>{item..name}</Hospital> */}
                            <Treatment>{item.treatment}</Treatment>
                            <Date>{item.diagnosis_date}</Date>
                            <Date>{item.discharge_date === "1805-05-05" ? "" : item.discharge_date }</Date>
                        </Li>
                    )
                })
                :
                <center>
                <Heading fontSize="25px">
                    <br/><br/>
                    Sorry, no records found !!
                </Heading>
                </center>
            }
        </ListContainer>
    )
}

export default List