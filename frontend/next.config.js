/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    RIS_API_BASE_URL: process.env.RIS_API_BASE_URL,
    IMAGE_KIT_URL_ENDPOINT: process.env.IMAGE_KIT_URL_ENDPOINT,
    IMAGE_KIT_PRIVATE_KEY: process.env.IMAGE_KIT_PRIVATE_KEY,
    IMAGE_KIT_PUBLIC_KEY: process.env.IMAGE_KIT_PUBLIC_KEY,
  },
  webpack: (config) => {
    config.resolve.alias.canvas = false;
    config.resolve.alias.encoding = false;
    return config;
  },
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'placehold.co',
        port: '',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'ik.imagekit.io',
        port: '',
        pathname: '/**',
      },
    ],
  },
  experimental: {
    webpackBuildWorker: true,
  },
};

module.exports = nextConfig;
