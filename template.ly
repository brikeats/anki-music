\version "2.24.4"
\score {
  \new Staff 
  \relative c'' 
  {
    \clef ##CLEF##
    \key ##KEY## \##MODE##
    r1
  }
  \layout {
    ragged-right = ##t
    \context {
      \Staff
      \omit TimeSignature
       % or:
      %\remove "Time_signature_engraver"
      \omit BarLine
      % or:
      %\remove "Bar_engraver"
    }
  }
}