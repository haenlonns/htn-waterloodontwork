"use client";
import styled from "styled-components";
import { useSwipeable } from "react-swipeable";
import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";
import { useEffect } from "react";

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

type CardProps = {
  image: string;
  name: string;
  onSwiped: (direction: "Left" | "Right") => void;
  exitDirection?: number; // New prop
  forceSwipe?: "Left" | "Right"; // New prop
};

const Card: React.FC<CardProps> = ({
  image,
  name,
  onSwiped,
  exitDirection,
  forceSwipe,
}) => {
  const [isVisible, setIsVisible] = useState(true);
  const [animationState, setAnimationState] = useState("enter");

  useEffect(() => {
    if (forceSwipe) {
      if (forceSwipe === "Left") {
        setAnimationState("exitLeft");
      } else {
        setAnimationState("exitRight");
      }
    }
  }, [forceSwipe]);

  const animationVariants = {
    enter: { opacity: 1, y: 0 },
    exitLeft: { opacity: 0, x: -1000 },
    exitRight: { opacity: 0, x: 1000 },
  };

  const handlers = useSwipeable({
    onSwipedLeft: () => {
      setAnimationState("exitLeft");
      setTimeout(() => onSwiped("Left"), 500);
    },
    onSwipedRight: () => {
      setAnimationState("exitRight");
      setTimeout(() => onSwiped("Right"), 500);
    },
    trackMouse: true,
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={animationVariants[animationState]}
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
