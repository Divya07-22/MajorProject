// File: src/components/shared/AnimatedBackground.jsx

import React from 'react';
import styled from 'styled-components';
import BackgroundVideo from '../../assets/videos/aurora-background.mp4';

const VideoContainer = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  overflow: hidden;
`;

const VideoBg = styled.video`
  width: 100%;
  height: 100%;
  -o-object-fit: cover;
  object-fit: cover;
  opacity: 0.3; /* Soft opacity to not distract from content */
`;

const AnimatedBackground = () => {
  return (
    <VideoContainer>
      <VideoBg autoPlay loop muted src={BackgroundVideo} type="video/mp4" />
    </VideoContainer>
  );
};

export default AnimatedBackground;