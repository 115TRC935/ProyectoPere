/**
 * GayCounter - Contador elegante de admisiones
 * Lleva la cuenta de cuántas veces se presiona "SÍ" en GayQuestion
 */
class GayCounter {
  constructor() {
    this.count = 0;
    this.counterElement = null;
    this.init();
  }

  init() {
    this.createCounter();
    this.loadCount();
  }

  createCounter() {
    const styles = `
      <style id="gayCounterStyles">
        #gayCounter {
          position: fixed;
          top: 20px;
          right: 20px;
          background: linear-gradient(135deg, #ff69b4, #ff1493, #8a2be2);
          border: 2px solid rgba(255, 255, 255, 0.8);
          border-radius: 15px;
          padding: 12px 18px;
          z-index: 99997;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          box-shadow: 0 4px 20px rgba(255, 20, 147, 0.3);
          backdrop-filter: blur(10px);
          color: white;
          font-size: 0.9rem;
          font-weight: 600;
          text-align: center;
          min-width: 140px;
          opacity: 0.85;
          transition: all 0.3s ease;
          cursor: default;
          user-select: none;
        }

        #gayCounter:hover {
          opacity: 1;
          transform: scale(1.05);
          box-shadow: 0 6px 30px rgba(255, 20, 147, 0.5);
        }

        .counter-title {
          font-size: 0.75rem;
          margin-bottom: 4px;
          color: rgba(255, 255, 255, 0.9);
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .counter-number {
          font-size: 1.8rem;
          font-weight: bold;
          color: #ffffff;
          text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
          animation: counterGlow 2s infinite alternate;
        }

        .counter-emoji {
          font-size: 1.2rem;
          margin-left: 8px;
          animation: counterFloat 3s infinite ease-in-out;
        }

        @keyframes counterGlow {
          0% { text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5); }
          100% { text-shadow: 0 0 10px rgba(255, 255, 255, 0.8); }
        }

        @keyframes counterFloat {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-3px); }
        }

        @keyframes counterPop {
          0% { transform: scale(1); }
          50% { transform: scale(1.3); }
          100% { transform: scale(1); }
        }

        .counter-pop {
          animation: counterPop 0.6s ease !important;
        }
      </style>
    `;

    const counterHTML = `
      ${styles}
      <div id="gayCounter">
        <div class="counter-title">💕 Admisiones de Amor 💕</div>
        <div>
          <span class="counter-number">${this.count}</span>
          <span class="counter-emoji">🏳️‍🌈</span>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', counterHTML);
    this.counterElement = document.getElementById('gayCounter');
  }

  increment() {
    this.count++;
    this.updateDisplay();
    this.saveCount();
    this.playAnimation();
  }

  updateDisplay() {
    const numberElement = this.counterElement.querySelector('.counter-number');
    if (numberElement) {
      numberElement.textContent = this.count;
    }
  }

  playAnimation() {
    if (this.counterElement) {
      this.counterElement.classList.add('counter-pop');
      setTimeout(() => {
        this.counterElement.classList.remove('counter-pop');
      }, 600);
    }
  }

  saveCount() {
    try {
      localStorage.setItem('gayCounterValue', this.count.toString());
    } catch (e) {
      // Si localStorage no está disponible, usar una cookie simple
      document.cookie = `gayCounter=${this.count}; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/`;
    }
  }

  loadCount() {
    try {
      const saved = localStorage.getItem('gayCounterValue');
      if (saved) {
        this.count = parseInt(saved, 10) || 0;
        this.updateDisplay();
      }
    } catch (e) {
      // Fallback a cookies
      const match = document.cookie.match(/gayCounter=(\d+)/);
      if (match) {
        this.count = parseInt(match[1], 10) || 0;
        this.updateDisplay();
      }
    }
  }

  reset() {
    this.count = 0;
    this.updateDisplay();
    this.saveCount();
  }

  hide() {
    if (this.counterElement) {
      this.counterElement.style.display = 'none';
    }
  }

  show() {
    if (this.counterElement) {
      this.counterElement.style.display = 'block';
    }
  }

  // Método estático para crear una instancia global
  static getInstance() {
    if (!window.gayCounterInstance) {
      window.gayCounterInstance = new GayCounter();
    }
    return window.gayCounterInstance;
  }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = GayCounter;
}

if (typeof window !== 'undefined') {
  window.GayCounter = GayCounter;
}