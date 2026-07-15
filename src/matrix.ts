export class MatrixRain {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private drops: number[] = [];
  private fontSize = 14;
  private chars = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン01";

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
    this.drops = Array.from({ length: cols }, () => Math.floor(Math.random() * -100));
  }

  attach(): this {
    this.canvas.style.cssText = "position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;pointer-events:none;";
    document.body.prepend(this.canvas);
    return this;
  }

  start() {
    const draw = () => {
      this.ctx.fillStyle = "rgba(10, 10, 10, 0.08)";
      this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

      this.ctx.font = `${this.fontSize}px monospace`;

      for (let i = 0; i < this.drops.length; i++) {
        const char = this.chars[Math.floor(Math.random() * this.chars.length)];
        const x = i * this.fontSize;
        const y = this.drops[i] * this.fontSize;

        this.ctx.fillStyle = y < this.canvas.height * 0.3
          ? "rgba(255, 68, 68, 0.12)"
          : "rgba(255, 68, 68, 0.06)";
        this.ctx.fillText(char, x, y);

        if (this.drops[i] * this.fontSize > this.canvas.height && Math.random() > 0.975) {
          this.drops[i] = 0;
        }
        this.drops[i]++;
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
