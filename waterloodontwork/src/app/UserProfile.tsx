"use client";
import { useState } from "react";
import styled from "styled-components";
import { lighten } from "polished";
import { useEffect } from "react";
import { useRef } from "react";

const ModalOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
`;
const ModalContent = styled.div`
  width: 80%;
  max-width: 800px;
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  position: relative;
`;
const Button = styled.button`
  background-color: #89cff0; // Baby blue color
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  outline: none;
  transition: background-color 0.3s;

  &:hover {
    background-color: #77b8d4; // Darker shade of baby blue for hover
  }
`;
const EditButton = styled(Button)`
  position: absolute;
  top: 10px;
  right: 10px;
`;
const SaveButton = styled(Button)`
  display: block;
  margin: 20px auto;
`;

const EditableInput = styled.input`
  background-color: transparent;
  border: none;
  border-bottom: 1px dotted #89cff0; // Baby blue dotted line
  font-size: inherit;
  color: inherit;
  outline: none;
  padding: 0;
  display: inline-block; // Display inline
  width: auto; // Auto width based on content
  line-height: 1.5; // Match line height to surrounding text

  &:focus {
    border-bottom: 2px solid #89cff0; // Solid baby blue line on focus
  }
`;
const SkillBlock = styled.div<{ color?: string }>`
  background-color: ${(props) => props.color || "#ccc"};
  padding: 5px 10px;
  border-radius: 10px;
  display: inline-block;
  margin: 5px;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover {
    background-color: ${(props) =>
      props.color ? lighten(0.1, props.color) : "#aaa"};
  }
`;

const SkillInput = styled.input`
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
`;

const CheckmarkButton = styled.button`
  background-color: #89cff0;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: inline-block;
  margin-left: 5px;
  cursor: pointer;
  outline: none;
  transition: background-color 0.3s;

  &:hover {
    background-color: #77b8d4;
  }
`;

export type UserProfile = {
  name: string;
  image: string;
  location: string;
  skills: string[];
  education: string;
  experiences: string[];
  projects: string[];
  awards: string[];
};
type ProfileModalProps = {
  user: UserProfile;
  onClose: () => void;
};

export const ProfileModal: React.FC<ProfileModalProps> = ({
  user,
  onClose,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedUser, setEditedUser] = useState(user); // Keep track of edits without immediately changing the displayed data
  const [skills, setSkills] = useState(user.skills);
  const [newSkill, setNewSkill] = useState("");
  const [addingSkill, setAddingSkill] = useState(false);
  const [skillColors, setSkillColors] = useState<Record<string, string>>({});
  const skillColorsRef = useRef<Record<string, string>>({});
  const randomColor = () => {
    const randomPastelValue = () => {
      return Math.floor(Math.random() * 127 + 128).toString(16); // Generate values between 128 (80 in hex) and 255 (FF in hex)
    };

    return `#${randomPastelValue()}${randomPastelValue()}${randomPastelValue()}`;
  };
  const initializeColors = () => {
    user.skills.forEach((skill) => {
      if (!skillColorsRef.current[skill]) {
        // Check local storage first
        const storedColor = localStorage.getItem(skill);
        if (storedColor) {
          skillColorsRef.current[skill] = storedColor;
        } else {
          const newColor = randomColor();
          skillColorsRef.current[skill] = newColor;
          localStorage.setItem(skill, newColor);
        }
      }
    });
  };

initializeColors();
  useEffect(() => {
    user.skills.forEach((skill) => {
      if (!skillColorsRef.current[skill]) {
        skillColorsRef.current[skill] = randomColor();
      }
    });
  }, [user.skills]); // Dependency on user.skills ensures colors are set when the modal is opened.

  const handleSave = () => {
    setIsEditing(false);
    // Here, you can also send the edited data to the server or handle it accordingly.
  };
  const handleAddSkill = () => {
    if (newSkill.trim()) {
      setSkills((prevSkills) => [...prevSkills, newSkill]);
      const newColor = randomColor();
      skillColorsRef.current[newSkill] = newColor;
      localStorage.setItem(newSkill, newColor);
      setNewSkill("");
      setAddingSkill(false);
    }
  };


  const handleRemoveSkill = (index: number) => {
    const updatedSkills = [...skills];
    updatedSkills.splice(index, 1);
    setSkills(updatedSkills);
  };

  

  return (
    <ModalOverlay onClick={onClose}>
      <ModalContent onClick={(e) => e.stopPropagation()}>
        <EditButton onClick={() => setIsEditing(!isEditing)}>
          {isEditing ? "Cancel" : "Edit Profile"}
        </EditButton>

        {/* Display the user data here. If `isEditing` is true, display input fields instead of plain text. */}
        {/* For brevity, I'm showing only the name and image as an example: */}
        <img src={editedUser.image} alt={editedUser.name} width={100} />
        <div>
          {isEditing ? (
            <EditableInput
              type="text"
              value={editedUser.name}
              onChange={(e) =>
                setEditedUser((prev) => ({ ...prev, name: e.target.value }))
              }
            />
          ) : (
            <h2>{editedUser.name}</h2>
          )}
        </div>
        <div>
          {isEditing ? (
            <EditableInput
              type="text"
              value={editedUser.location}
              onChange={(e) =>
                setEditedUser((prev) => ({ ...prev, location: e.target.value }))
              }
            />
          ) : (
            <span>{editedUser.location}</span>
          )}
        </div>
        <div>
          {isEditing ? (
            <EditableInput
              type="text"
              value={editedUser.education}
              onChange={(e) =>
                setEditedUser((prev) => ({
                  ...prev,
                  education: e.target.value,
                }))
              }
            />
          ) : (
            <span>{editedUser.education}</span>
          )}
        </div>
        <div>
          {isEditing ? (
            <>
              {skills.map((skill, index) => (
                <SkillBlock
                  key={skill}
                  color={skillColorsRef.current[skill] || "#ccc"}
                  onClick={() => handleRemoveSkill(index)}
                  onMouseOver={(e) =>
                    (e.currentTarget.textContent = "Click to remove")
                  }
                  onMouseOut={(e) => (e.currentTarget.textContent = skill)}
                >
                  {skill}
                </SkillBlock>
              ))}
              {addingSkill ? (
                <>
                  <SkillInput
                    value={newSkill}
                    onChange={(e) => setNewSkill(e.target.value)}
                    // onBlur={() => setAddingSkill(false)}
                  />
                  <CheckmarkButton onClick={handleAddSkill}>✓</CheckmarkButton>
                </>
              ) : (
                <SkillBlock onClick={() => setAddingSkill(true)}>+</SkillBlock>
              )}
            </>
          ) : (
            skills.map((skill) => (
              <SkillBlock
                key={skill}
                color={skillColorsRef.current[skill] || "#ccc"}
              >
                {skill}
              </SkillBlock>
            ))
          )}
        </div>

        {/* Add similar blocks for location, birthday, skills, etc. */}

        {isEditing && <SaveButton onClick={handleSave}>Save</SaveButton>}
      </ModalContent>
    </ModalOverlay>
  );
};
