"use client";
import styled from "styled-components";
import { useSwipeable } from "react-swipeable";
import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";

type CardProps = {
  image: string;
  name: string;
  onSwiped: (direction: "Left" | "Right") => void; // Add this line
};

const CardArea = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
`;

const CardWrapper = styled.div`
  width: 300px;
  height: 400px;
  background-color: #fff;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const Image = styled.img`
  width: 100%;
  height: 70%;
  object-fit: cover;
`;

const Name = styled.h2`
  text-align: center;
  margin-top: 10px;
  color: black;
`;
// ... other imports ...

const Card: React.FC<CardProps> = ({ image, name, onSwiped }) => {
  const [exitDirection, setExitDirection] = useState<number | null>(null);

  const handlers = useSwipeable({
    onSwipedLeft: () => {
      setExitDirection(-1); // left swipe: move card to the left
      setTimeout(() => onSwiped("Left"), 500);
    },
    onSwipedRight: () => {
      setExitDirection(1); // right swipe: move card to the right
      setTimeout(() => onSwiped("Right"), 500);
    },
    trackMouse: true,
  });

  return (
    <motion.div
      initial={{ opacity: 1, x: 0 }}
      animate={
        exitDirection !== null ? { x: exitDirection * 1000, opacity: 0 } : {}
      }
      transition={{ duration: 0.5 }}
      {...handlers}
    >
      <CardWrapper>
        <Image src={image} alt={name} />
        <Name>{name}</Name>
      </CardWrapper>
    </motion.div>
  );
};

export default Card;
