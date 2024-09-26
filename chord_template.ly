\version "2.24.4"
\score {
  \new Staff 
  \relative c'' 
  {
    \clef  ##CLEF##
    \key c \major
    ##NOTES##
  }
  \layout {
    \context {
      \Staff
      \omit TimeSignature
      \omit BarLine
    }
  }
}