import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Arabiyah Center — Pembaca Kitab Arab Gundul",
  description:
    "Editor kitab Arab: unggah PDF, crop rajah 300 DPI, tulis pasal Arab/Latin/Terjemah, dan beri harakat otomatis (tashkeel HarfScript).",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="id">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Noto+Naskh+Arabic:wght@400;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
