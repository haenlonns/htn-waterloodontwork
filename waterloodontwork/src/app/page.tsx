"use client";

import Image from "next/image";
import styles from "./page.module.css";
import { useState } from "react";
import Card from "./components/card";
import { motion, AnimatePresence, color } from "framer-motion";
import styled from "styled-components";

const ButtonContainer = styled.div`
  display: flex;
  justify-content: center; // Center the buttons
  gap: 20px; // Gap between buttons
  position: absolute;
  bottom: 10%;
  width: 100%;
`;


const SwipeButton = styled.button<{ color: string }>`
  background-color: ${props => props.color};
  border: none;
  border-radius: 50%;
  width: 50px;  // Adjusted size
  height: 50px; // Adjusted size
  cursor: pointer;
  outline: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const Navbar = styled.div`
  position: absolute;
  top: 0;
  right: 0;
  padding: 15px;
  display: flex;
  align-items: center;
`;

const ProfileButton = styled.div`
  display: flex;
  align-items: center;
  cursor: pointer;
`;

const ProfileImage = styled.img`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
`;

const Dropdown = styled.div<{ isOpen: boolean }>`
  display: ${(props) => (props.isOpen ? "block" : "none")};
  position: absolute;
  right: 0;
  top: 60px;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const DropdownItem = styled.div`
  padding: 10px 15px;
  cursor: pointer;
  &:hover {
    background-color: #f0f0f0;
  }
`;


const users = [
  {
    name: "John Doe",
    image: "/path/to/john-image.jpg",
  },
  {
    name: "Jane Smith",
    image: "/path/to/jane-image.jpg",
  },
  // ... add more users
];

const Home = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [exitDirection, setExitDirection] = useState<number | undefined>();
  const [dropdownOpen, setDropdownOpen] = useState(false); // State to control dropdown visibility

  const [forceSwipeDirection, setForceSwipeDirection] = useState<
    "Left" | "Right" | undefined
  >(undefined);

  const onSwiped = (direction: string) => {
    if (direction === "Left" || direction === "Right") {
      setCurrentIndex((prevIndex) => prevIndex + 1);
    }
  };
  const handleSwipe = (direction: "Left" | "Right") => {
    if (direction === "Left") {
      setExitDirection(-1);
    } else {
      setExitDirection(1);
    }
    setTimeout(() => {
      onSwiped(direction);
      setExitDirection(undefined);
    }, 500);
  };
  const handleButtonClick = (direction: "Left" | "Right") => {
    setForceSwipeDirection(direction);
    setTimeout(() => {
      onSwiped(direction);
      setForceSwipeDirection(undefined);
    }, 500);
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        position: "relative",
      }}
    >
      <Navbar>
        <ProfileButton onClick={() => setDropdownOpen(!dropdownOpen)}>
          <ProfileImage src="/path/to/jane-doe-image.jpg" alt="Jane Doe" />
          Jane Doe
        </ProfileButton>
        <Dropdown isOpen={dropdownOpen}>
          <DropdownItem>View Profile</DropdownItem>
          <DropdownItem>Logout</DropdownItem>
        </Dropdown>
      </Navbar>

      {currentIndex < users.length && (
        <Card
          key={currentIndex}
          name={users[currentIndex].name}
          image={users[currentIndex].image}
          onSwiped={handleSwipe}
          exitDirection={exitDirection}
          forceSwipe={forceSwipeDirection}
        />
      )}

      <ButtonContainer>
        <SwipeButton color="red" onClick={() => handleButtonClick("Left")}>
          <span style={{ color: "white " }}>✖</span>
        </SwipeButton>
        <SwipeButton color="green" onClick={() => handleButtonClick("Right")}>
          <span style={{ color: "white " }}>✓</span>
        </SwipeButton>
      </ButtonContainer>
    </div>
  );
};

export default Home;
