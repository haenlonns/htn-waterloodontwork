import React from "react";
import styled from 'styled-components';

const CardCont = styled.div`
    backdrop-filter: blur(10px);
    border-radius: 26px;
    position: relative;
    border 2px solid #fff;
    width: 1000px;
    height: 200px;
    display: flex;
    background-color: rgba(255, 255, 255, 0.2);
`;

export function NL(props) {
    return <CardCont>Card</CardCont>
}