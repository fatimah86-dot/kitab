/* Kumpulan ikon garis sederhana (tanpa dependensi). */
const S = ({ size = 18, children, ...rest }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.7"
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
    {...rest}
  >
    {children}
  </svg>
);

export const Search = (p) => (
  <S {...p}>
    <circle cx="11" cy="11" r="7" />
    <path d="m20 20-3.6-3.6" />
  </S>
);
export const Book = (p) => (
  <S {...p}>
    <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H19v15H6.5A2.5 2.5 0 0 0 4 20.5z" />
    <path d="M4 20.5A2.5 2.5 0 0 1 6.5 18H19v3H6.5A2.5 2.5 0 0 1 4 20.5z" />
    <path d="M8 7.5h7" />
  </S>
);
export const Bookmark = ({ filled, ...p }) => (
  <S {...p} fill={filled ? 'currentColor' : 'none'}>
    <path d="M6 3.5h12v17l-6-4.2-6 4.2z" />
  </S>
);
export const Layers = (p) => (
  <S {...p}>
    <path d="m12 3 9 5-9 5-9-5z" />
    <path d="m3 13 9 5 9-5" />
  </S>
);
export const Settings = (p) => (
  <S {...p}>
    <circle cx="12" cy="12" r="3.2" />
    <path d="M19.4 15a1.7 1.7 0 0 0 .34 1.87l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.7 1.7 0 0 0-1.87-.34 1.7 1.7 0 0 0-1 1.56V21a2 2 0 1 1-4 0v-.1a1.73 1.73 0 0 0-1.11-1.58 1.7 1.7 0 0 0-1.87.34l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.7 1.7 0 0 0 .34-1.87 1.7 1.7 0 0 0-1.56-1H3a2 2 0 1 1 0-4h.1a1.73 1.73 0 0 0 1.58-1.11 1.7 1.7 0 0 0-.34-1.87l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.7 1.7 0 0 0 1.87.34H9a1.7 1.7 0 0 0 1-1.56V3a2 2 0 1 1 4 0v.1a1.73 1.73 0 0 0 1.05 1.6 1.7 1.7 0 0 0 1.87-.34l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.7 1.7 0 0 0-.34 1.87V9a1.7 1.7 0 0 0 1.56 1H21a2 2 0 1 1 0 4h-.1a1.73 1.73 0 0 0-1.5 1z" />
  </S>
);
export const Menu = (p) => (
  <S {...p}>
    <path d="M4 6h16M4 12h16M4 18h16" />
  </S>
);
export const Close = (p) => (
  <S {...p}>
    <path d="M6 6l12 12M18 6L6 18" />
  </S>
);
export const ChevronLeft = (p) => (
  <S {...p}>
    <path d="m14 6-6 6 6 6" />
  </S>
);
export const ChevronRight = (p) => (
  <S {...p}>
    <path d="m10 6 6 6-6 6" />
  </S>
);
export const ArrowLeft = (p) => (
  <S {...p}>
    <path d="M19 12H5" />
    <path d="m11 18-6-6 6-6" />
  </S>
);
export const Sun = (p) => (
  <S {...p}>
    <circle cx="12" cy="12" r="4" />
    <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
  </S>
);
export const Moon = (p) => (
  <S {...p}>
    <path d="M20 14.5A8 8 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z" />
  </S>
);
export const Sepia = (p) => (
  <S {...p}>
    <circle cx="12" cy="12" r="8" />
    <path d="M12 8v8M8 12h8" />
  </S>
);
export const Copy = (p) => (
  <S {...p}>
    <rect x="9" y="9" width="11" height="11" rx="2.5" />
    <path d="M15 6.5V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h.5" />
  </S>
);
export const Check = (p) => (
  <S {...p}>
    <path d="m5 13 4.5 4.5L19 7" />
  </S>
);
export const Info = (p) => (
  <S {...p}>
    <circle cx="12" cy="12" r="9" />
    <path d="M12 11v5M12 8h.01" />
  </S>
);
export const Print = (p) => (
  <S {...p}>
    <path d="M7 9V4h10v5" />
    <rect x="4" y="9" width="16" height="7" rx="2" />
    <path d="M7 14h10v6H7z" />
  </S>
);
export const Grid = (p) => (
  <S {...p}>
    <rect x="4" y="4" width="6.5" height="6.5" rx="1.5" />
    <rect x="13.5" y="4" width="6.5" height="6.5" rx="1.5" />
    <rect x="4" y="13.5" width="6.5" height="6.5" rx="1.5" />
    <rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.5" />
  </S>
);
export const Star = (p) => (
  <S {...p} fill="currentColor" stroke="none">
    <path d="M12 3.5l2.5 5.3 5.8.7-4.3 4 1.2 5.7L12 16.5l-5.2 2.7L8 13.5l-4.3-4 5.8-.7z" />
  </S>
);
export const Sparkle = (p) => (
  <S {...p}>
    <path d="M12 3.5c.7 3.6 2.6 5.5 6.2 6.2-3.6.7-5.5 2.6-6.2 6.2-.7-3.6-2.6-5.5-6.2-6.2 3.6-.7 5.5-2.6 6.2-6.2z" />
    <path d="M18 16.5c.35 1.7 1.3 2.65 3 3-1.7.35-2.65 1.3-3 3-.35-1.7-1.3-2.65-3-3 1.7-.35 2.65-1.3 3-3z" />
  </S>
);
export const Type = (p) => (
  <S {...p}>
    <path d="M5 6V4.5h14V6" />
    <path d="M12 4.5V20M9 20h6" />
  </S>
);
