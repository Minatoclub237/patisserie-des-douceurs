/* ═══════════════════════════════════════════════
   DisplaceGL — transition d'images par déformation
   Un quad WebGL, N textures, une carte de bruit.
   gl.progress ∈ [0, N-1] pilote le mélange.
   ═══════════════════════════════════════════════ */
window.DisplaceGL = class {
  constructor(canvas, srcs) {
    this.canvas = canvas;
    this.gl = canvas.getContext('webgl', { antialias: false, alpha: false, premultipliedAlpha: false });
    this.ok = !!this.gl;
    if (!this.ok) return;
    this._progress = 0;
    this.textures = [];
    this.sizes = [];
    this._build();
    this._noise();
    this.resize();
    Promise.all(srcs.map((s, i) => this._load(s, i))).then(() => { this.ready = true; this.render(); });
  }

  _build() {
    const gl = this.gl;
    const vs = `attribute vec2 p;varying vec2 v;void main(){v=vec2(p.x*.5+.5,.5-p.y*.5);gl_Position=vec4(p,0.,1.);}`;
    const fs = `precision highp float;varying vec2 v;
uniform sampler2D t1,t2,dm;uniform float p;uniform vec2 res,s1,s2;
vec2 cover(vec2 uv,vec2 img){float ra=res.x/res.y,ia=img.x/img.y;vec2 sc=ra>ia?vec2(1.,ia/ra):vec2(ra/ia,1.);return (uv-.5)*sc+.5;}
void main(){
  float e=smoothstep(0.,1.,p);
  float d=texture2D(dm,v).r-.5;
  vec2 u1=cover(v,s1)+vec2(d*.55*e, d*.18*e);
  vec2 u2=cover(v,s2)-vec2(d*.55*(1.-e), d*.18*(1.-e));
  vec4 a=texture2D(t1,u1),b=texture2D(t2,u2);
  gl_FragColor=mix(a,b,e);
}`;
    const sh = (t, s) => { const o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); return o; };
    const prg = gl.createProgram();
    gl.attachShader(prg, sh(gl.VERTEX_SHADER, vs));
    gl.attachShader(prg, sh(gl.FRAGMENT_SHADER, fs));
    gl.linkProgram(prg);
    gl.useProgram(prg);
    this.prg = prg;
    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    const loc = gl.getAttribLocation(prg, 'p');
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    this.u = {};
    ['t1', 't2', 'dm', 'p', 'res', 's1', 's2'].forEach((n) => (this.u[n] = gl.getUniformLocation(prg, n)));
    gl.uniform1i(this.u.t1, 0); gl.uniform1i(this.u.t2, 1); gl.uniform1i(this.u.dm, 2);
  }

  _tex(unit) {
    const gl = this.gl, t = gl.createTexture();
    gl.activeTexture(gl.TEXTURE0 + unit);
    gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    return t;
  }

  // bruit de valeur lissé, 2 octaves, 256×256
  _noise() {
    const N = 256, data = new Uint8Array(N * N);
    const grid = (g) => { const a = []; for (let i = 0; i < g * g; i++) a.push(Math.random()); return a; };
    const octave = (g, x, y) => {
      const gx = (x / N) * g, gy = (y / N) * g, x0 = Math.floor(gx), y0 = Math.floor(gy);
      const fx = gx - x0, fy = gy - y0, sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy);
      const v = (i, j) => this._g[g][((j % g) * g) + (i % g)];
      const a = v(x0, y0), b = v(x0 + 1, y0), c = v(x0, y0 + 1), d = v(x0 + 1, y0 + 1);
      return (a + (b - a) * sx) * (1 - sy) + (c + (d - c) * sx) * sy;
    };
    this._g = { 4: grid(4), 9: grid(9), 20: grid(20) };
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
      const n = octave(4, x, y) * .6 + octave(9, x, y) * .3 + octave(20, x, y) * .1;
      data[y * N + x] = n * 255;
    }
    const gl = this.gl;
    this._tex(2);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.LUMINANCE, N, N, 0, gl.LUMINANCE, gl.UNSIGNED_BYTE, data);
  }

  _load(src, i) {
    return new Promise((res) => {
      const img = new Image();
      img.onload = () => {
        const gl = this.gl;
        this.textures[i] = this._tex(0);
        gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, img);
        this.sizes[i] = [img.naturalWidth, img.naturalHeight];
        res();
      };
      img.onerror = res;
      img.src = src;
    });
  }

  resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    const w = Math.round(this.canvas.clientWidth * dpr), h = Math.round(this.canvas.clientHeight * dpr);
    if (this.canvas.width === w && this.canvas.height === h) return;
    this.canvas.width = w; this.canvas.height = h;
    this.gl.viewport(0, 0, w, h);
    this.gl.uniform2f(this.u.res, w, h);
    if (this.ready) this.render();
  }

  set progress(v) { this._progress = v; if (this.ready) this.render(); }
  get progress() { return this._progress; }

  render() {
    const gl = this.gl, n = this.textures.length;
    if (!n) return;
    const P = Math.max(0, Math.min(n - 1, this._progress));
    const i = Math.min(n - 2, Math.floor(P)), local = P - i;
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, this.textures[i]);
    gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, this.textures[i + 1]);
    gl.uniform2f(this.u.s1, ...this.sizes[i]);
    gl.uniform2f(this.u.s2, ...this.sizes[i + 1]);
    gl.uniform1f(this.u.p, local);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }
};
