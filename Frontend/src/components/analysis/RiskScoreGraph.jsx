import React from 'react';
import styled, { keyframes } from 'styled-components';

const fillAnimation = (percentage) => keyframes`
  from { stroke-dashoffset: 283; }
  to { stroke-dashoffset: ${283 - (283 * percentage) / 100}; }
`;

const GaugeWrapper = styled.div`
  position: relative;
  width: 250px;
  height: 250px;
  margin: ${({ theme }) => theme.spacing.large} auto;
`;

const Svg = styled.svg`
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
`;

const CircleBg = styled.circle`
  fill: none;
  stroke: ${({ theme }) => theme.colors.secondary};
  stroke-width: 20;
`;

const CircleProgress = styled.circle`
  fill: none;
  stroke: ${({ theme, risk }) => risk > 80 ? theme.colors.danger : risk > 50 ? theme.colors.accent : theme.colors.success};
  stroke-width: 20;
  stroke-dasharray: 283;
  stroke-linecap: round;
  animation: ${({ risk }) => fillAnimation(risk)} 2s ease-out forwards;
`;

const PercentageText = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: ${({ theme }) => theme.colors.primary};
  font-size: 3rem;
  font-weight: 700;
  text-shadow: 0 0 10px ${({ theme }) => theme.colors.glow};
`;

const RiskScoreGraph = ({ riskScore }) => {
  return (
    <GaugeWrapper>
      <Svg viewBox="0 0 100 100">
        <CircleBg cx="50" cy="50" r="45" />
        <CircleProgress cx="50" cy="50" r="45" risk={riskScore} />
      </Svg>
      <PercentageText>{riskScore}%</PercentageText>
    </GaugeWrapper>
  );
};

export default RiskScoreGraph;