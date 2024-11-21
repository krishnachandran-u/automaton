import type { Metadata } from "next";
import { ThemeProvider } from "@/components/theme-provider";
import { Navbar } from "@/components/navbar";
import localFont from "next/font/local";
import "./globals.css";

const regularFont = localFont({
  src: [
    { 
      path: "./../public/fonts/CourierPrime-Regular.ttf", 
      weight: "400", 
      style: "normal" 
    },
    { 
      path: "./../public/fonts/CourierPrime-Italic.ttf", 
      weight: "400", 
      style: "italic" 
    },
    { 
      path: "./../public/fonts/CourierPrime-Bold.ttf", 
      weight: "700", 
      style: "normal" 
    },
    { 
      path: "./../public/fonts/CourierPrime-BoldItalic.ttf", 
      weight: "700", 
      style: "italic" 
    }
  ],
  variable: "--font-regular",
});

const codeFont = regularFont;

export const metadata: Metadata = {
  title: "pykleene",
  description:
    "pykleene is a python library for building and simulating various types of automata and formal grammars, from finite state machines to Turing machines, as well as Type 0 to Type 3 grammars.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${regularFont.variable} ${codeFont.variable} font-regular`}
        suppressHydrationWarning
      >
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <Navbar />
          <main className="sm:container mx-auto w-[88vw] h-auto">
            {children}
          </main>
        </ThemeProvider>
      </body>
    </html>
  );
}