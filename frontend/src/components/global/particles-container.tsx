'use client';

import { useCallback } from 'react';
import Particles from 'react-particles';
import type { Engine, ISourceOptions } from 'tsparticles-engine';
import { loadSlim } from 'tsparticles-slim';

export interface ParticlesContainerProps {
  options: ISourceOptions;
}

export function ParticlesContainer({
  options,
}: ParticlesContainerProps) {
  const particlesInit = useCallback(async (engine: Engine) => {
    await loadSlim(engine);
  }, []);

  return <Particles id="tsparticles" init={particlesInit} options={options} />;
}
