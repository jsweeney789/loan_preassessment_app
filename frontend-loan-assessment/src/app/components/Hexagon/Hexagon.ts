// score-hexagon.component.ts
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-hexagon',
  template: `
    <div class="hex-wrapper">
      <svg width="160" height="184" viewBox="0 0 160 184">
        <defs>
          <linearGradient id="themeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="var(--theme-color)"/>
            <stop offset="100%" stop-color="var(--theme-color-dark)"/>
          </linearGradient>
        </defs>
        <polygon
          points="80,4 156,44 156,140 80,180 4,140 4,44"
          fill="url(#themeGrad)"
        />
        <polygon
          points="80,18 144,54 144,130 80,166 16,130 16,54"
          fill="none"
          stroke="rgba(255,255,255,0.12)"
          stroke-width="1"
        />
        <text
          x="80" y="108"
          text-anchor="middle"
          font-family="'Cormorant Garamond', Georgia, serif"
          font-size="64"
          font-weight="700"
          fill="#060b14"
        >{{ score }}</text>
      </svg>
    </div>
  `,
  styles: [
    `.hex-wrapper {
      display: flex;
      justify-content: center;
      align-items: center;
    }`
  ]
})
export class Hexagon {
  @Input() score: number | string = 0;
}