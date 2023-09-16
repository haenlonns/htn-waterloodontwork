"use client";

import Image from "next/image";
import styles from "./page.module.css";
import { useState } from "react";
import Card from "./components/card";
import { motion, AnimatePresence } from "framer-motion";


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

  const onSwiped = (direction: string) => {
    if (direction === "Left" || direction === "Right") {
      setCurrentIndex((prevIndex) => prevIndex + 1);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh", // This assumes the entire viewport height
      }}
    >
      {currentIndex < users.length && (
        <Card
          key={currentIndex}
          name={users[currentIndex].name}
          image={users[currentIndex].image}
          onSwiped={onSwiped}
        />
      )}
    </div>
  );
};

export default Home;
