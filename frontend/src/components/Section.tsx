import type { ReactNode } from 'react'

type SectionProps = {
  title: string
  children: ReactNode
}

export function Section({ title, children }: SectionProps) {
  return (
    <section className="panel">
      <h2>{title}</h2>
      <div>{children}</div>
    </section>
  )
}
