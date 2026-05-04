/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // For Cloudflare Pages deployment, set NEXT_PUBLIC_STATIC_EXPORT=true
  // and the frontend will talk directly to the Fly.io backend URL.
  ...(process.env.NEXT_PUBLIC_STATIC_EXPORT === 'true'
    ? { output: 'export', images: { unoptimized: true } }
    : {}),

  // Local development: proxy API calls to the local backend
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://localhost:8000/api/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
