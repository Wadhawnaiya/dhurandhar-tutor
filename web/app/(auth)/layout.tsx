import Image from "next/image";
import Link from "next/link";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="grid min-h-screen bg-[var(--background)] lg:grid-cols-[1.02fr_1fr]">
      {/* Brand pane. Hidden below lg, where the form gets the whole screen. */}
      <aside className="relative hidden flex-col justify-between overflow-hidden bg-[#0c0e19] px-12 py-10 text-white lg:flex">
        <div aria-hidden className="pointer-events-none absolute inset-0">
          <div className="absolute -left-32 -top-40 h-[440px] w-[440px] rounded-full bg-[#f26b1d]/25 blur-[130px]" />
          <div className="absolute -bottom-48 -right-24 h-[420px] w-[420px] rounded-full bg-[#3d4bff]/25 blur-[120px]" />
          <div
            className="absolute inset-0 opacity-[0.06]"
            style={{
              backgroundImage:
                "linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)",
              backgroundSize: "48px 48px",
            }}
          />
          <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-[#ffc24d]/60 to-transparent" />
        </div>

        <Link href="/" className="relative flex items-center gap-3">
          <Image
            src="/brand/color-logo.png"
            alt=""
            width={44}
            height={44}
            className="h-11 w-11 rounded-[12px] shadow-[0_10px_30px_-12px_rgba(242,107,29,0.8)]"
          />
          <Image
            src="/brand/black-word.png"
            alt="Dhurandhar Tutor"
            width={1600}
            height={320}
            priority
            className="h-[24px] w-auto brightness-0 invert"
          />
        </Link>

        <div className="relative">
          <p className="mb-5 text-[11px] font-semibold uppercase tracking-[0.34em] text-[#ffc24d]">
            Agent-native learning
          </p>
          <h2 className="font-serif text-[46px] leading-[1.06] tracking-[-0.02em]">
            Learn like you
            <br />
            mean it.
          </h2>
          <p className="mt-6 max-w-[24rem] text-sm leading-relaxed text-white/60">
            A workspace where the agent reads with you, remembers what you
            covered, and picks up the next session where you stopped.
          </p>
          <ul className="mt-9 space-y-3.5 text-[13.5px] text-white/70">
            {[
              "Grounded answers over your own sources",
              "Memory that survives between sessions",
              "Notes, readers and practice in one pane",
            ].map((line) => (
              <li key={line} className="flex items-center gap-3">
                <span className="h-1.5 w-1.5 rotate-45 rounded-[1px] bg-gradient-to-br from-[#ffc24d] to-[#f26b1d]" />
                {line}
              </li>
            ))}
          </ul>
        </div>

        <p className="relative text-[11px] tracking-wide text-white/35">
          Dhurandhar Tutor · built for the long study
        </p>
      </aside>

      <main className="flex min-h-screen items-center justify-center px-5 py-10">
        {children}
      </main>
    </div>
  );
}
