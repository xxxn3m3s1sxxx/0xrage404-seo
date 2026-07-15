export class MatrixRain {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private drops: { x: number; y: number; speed: number; len: number }[] = [];
  private fontSize = 16;
  private chars = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789";

  constructor() {
    this.canvas = document.createElement("canvas");
    this.canvas.id = "matrix-canvas";
    this.ctx = this.canvas.getContext("2d")!;
    this.resize();
    this.initDrops();
    window.addEventListener("resize", () => { this.resize(); this.initDrops(); });
  }

  private resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  private initDrops() {
    const cols = Math.floor(this.canvas.width / this.fontSize);
    this.drops = Array.from({ length: cols }, () => ({
      x: Math.random() * this.canvas.width,
      y: Math.random() * this.canvas.height * -1,
      speed: 1 + Math.random() * 3,
      len: 5 + Math.floor(Math.random() * 15),
    }));
  }

  attach(): this {
    this.canvas.style.cssText = "position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-1;pointer-events:none;";
    document.body.prepend(this.canvas);
    return this;
  }

  start() {
    const draw = () => {
      this.ctx.fillStyle = "rgba(0, 0, 0, 0.18)";
      this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
      this.ctx.font = `bold ${this.fontSize}px monospace`;

      for (let i = 0; i < this.drops.length; i++) {
        const d = this.drops[i];
        const char = this.chars[Math.floor(Math.random() * this.chars.length)];
        const y = d.y;

        for (let j = 0; j < d.len; j++) {
          const cy = y - j * this.fontSize;
          if (cy < -this.fontSize || cy > this.canvas.height) continue;
          const brightness = 1 - j / d.len;
          this.ctx.fillStyle = j === 0
            ? "rgba(180, 255, 180, 0.9)"
            : `rgba(0, 255, 65, ${(brightness * 0.5).toFixed(2)})`;
          this.ctx.fillText(char, d.x, cy);
        }

        d.y += d.speed;
        if (d.y - d.len * this.fontSize > this.canvas.height) {
          d.y = -this.fontSize;
          d.speed = 1 + Math.random() * 3;
          d.len = 5 + Math.floor(Math.random() * 15);
          d.x = Math.random() * this.canvas.width;
        }
      }
      this.animId = requestAnimationFrame(draw);
    };
    this.animId = requestAnimationFrame(draw);
  }

  private animId = 0;

  stop() {
    cancelAnimationFrame(this.animId);
  }
}
