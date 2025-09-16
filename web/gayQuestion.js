/**
 * GayQuestion - Modal persistente y molesto que pregunta orientación sexual
 * Se agranda si presionás "No" y solo desaparece temporalmente con "Sí"
 */
class GayQuestion {
  constructor() {
    this.isActive = false;
    this.modalElement = null;
    this.currentSize = 1; // Factor de escala inicial
    this.maxSize = 10; // Tamaño máximo antes de cambiar estrategia
    this.isFullScreen = false;
    this.buttonGrowth = 1; // Factor de crecimiento de botón "Sí"
    this.hideTimer = null;
  }

  show() {
    if (this.isActive) return;

    this.isActive = true;
    this.currentSize = 1;
    this.isFullScreen = false;
    this.buttonGrowth = 1;
    this.createModal();
    this.attachEvents();
  }

  createModal() {
    const styles = `
      <style id="gayQuestionStyles">
        #gayQuestion {
          position: fixed;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%) scale(${this.currentSize});
          background: linear-gradient(135deg, #ff69b4, #ff1493, #dc143c);
          border: 5px solid #ffffff;
          border-radius: 20px;
          padding: 30px;
          z-index: 99999;
          font-family: 'Comic Sans MS', cursive, sans-serif;
          box-shadow: 0 0 50px rgba(255, 20, 147, 0.8);
          animation: gayPulse 1s infinite alternate;
          min-width: 300px;
          text-align: center;
          transition: transform 0.5s ease;
          ${this.isFullScreen ? `
            width: 100vw !important;
            height: 100vh !important;
            top: 0 !important;
            left: 0 !important;
            transform: none !important;
            border-radius: 0 !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
          ` : ''}
        }
        
        .gay-title {
          color: white;
          font-size: ${this.isFullScreen ? '8vmin' : '2rem'};
          font-weight: bold;
          margin-bottom: 20px;
          text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
          animation: gayRainbow 2s infinite;
        }
        
        .gay-buttons {
          display: flex;
          gap: 20px;
          justify-content: center;
          flex-wrap: wrap;
        }
        
        .gay-button {
          border: 3px solid white;
          border-radius: 15px;
          font-size: ${this.isFullScreen ? '4vmin' : '1.5rem'};
          font-weight: bold;
          cursor: pointer;
          padding: 15px 30px;
          text-transform: uppercase;
          letter-spacing: 2px;
          transition: all 0.3s ease;
          font-family: inherit;
          min-width: 120px;
        }
        
        #gayYes {
          background: linear-gradient(45deg, #00ff00, #32cd32);
          color: white;
          transform: scale(${this.buttonGrowth});
          transition: all 0.3s ease !important;
          ${this.isFullScreen ? `
            font-size: ${4 * this.buttonGrowth}vmin !important;
            padding: ${15 * this.buttonGrowth}px ${30 * this.buttonGrowth}px !important;
          ` : ''}
        }
        
        #gayNo {
          background: linear-gradient(45deg, #ff0000, #dc143c);
          color: white;
          transition: all 0.3s ease !important;
          transform: scale(${this.isFullScreen ? Math.max(0.1, 2 - this.buttonGrowth) : 1});
          ${this.isFullScreen ? `
            font-size: ${Math.max(1, 4 * (2 - this.buttonGrowth))}vmin !important;
            padding: ${Math.max(5, 15 * (2 - this.buttonGrowth))}px ${Math.max(10, 30 * (2 - this.buttonGrowth))}px !important;
          ` : ''}
        }
        
        .gay-button:hover {
          transform: scale(${this.isFullScreen ? this.buttonGrowth * 1.1 : 1.1});
          box-shadow: 0 5px 20px rgba(255, 255, 255, 0.5);
        }
        
        #gayNo:hover {
          transform: scale(${this.isFullScreen ? Math.max(0.05, (2 - this.buttonGrowth) * 1.1) : 1.1});
        }
        
        @keyframes gayPulse {
          0% { box-shadow: 0 0 50px rgba(255, 20, 147, 0.8); }
          100% { box-shadow: 0 0 100px rgba(255, 105, 180, 1); }
        }
        
        @keyframes gayRainbow {
          0% { color: #ff0000; }
          16% { color: #ff8000; }
          33% { color: #ffff00; }
          50% { color: #00ff00; }
          66% { color: #0080ff; }
          83% { color: #8000ff; }
          100% { color: #ff0080; }
        }
        
        .gay-overlay {
          position: fixed;
          top: 0;
          left: 0;
          width: 100vw;
          height: 100vh;
          background: rgba(255, 20, 147, 0.3);
          z-index: 99998;
          backdrop-filter: blur(2px);
        }
      </style>
    `;

    const overlayHTML = this.currentSize >= 5 || this.isFullScreen ? 
      '<div class="gay-overlay"></div>' : '';

    const modalHTML = `
      ${styles}
      ${overlayHTML}
      <div id="gayQuestion">
        <div class="gay-title">
          ${this.getRandomQuestion()}
        </div>
        <div class="gay-buttons">
          <button class="gay-button" id="gayYes">
            SÍ 💖
          </button>
          <button class="gay-button" id="gayNo">
            NO 🚫
          </button>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHTML);
    this.modalElement = document.getElementById('gayQuestion');
  }

  getRandomQuestion() {
    const questions = [
      "¿Sos gay? 🏳️‍🌈",
      "¿Te gustan los hombres? 💕",
      "¿Eres homosexual? 🌈",
      "Admite la verdad... ¿sos gay? 💫",
      "¿Prefieres a los chicos? 😘",
      "Vamos, confesá... ¿sos gay? 🔥",
      "¿Te atraen los hombres? 💝",
      "Sé honesto... ¿sos gay? ✨"
    ];
    return questions[Math.floor(Math.random() * questions.length)];
  }

  attachEvents() {
    const yesButton = document.getElementById('gayYes');
    const noButton = document.getElementById('gayNo');

    yesButton.addEventListener('click', () => {
      this.handleYes();
    });

    noButton.addEventListener('click', () => {
      this.handleNo();
    });

    // Prevenir escape
    this.escapeHandler = (e) => {
      if (e.key === 'Escape' || e.key === 'F12' || 
          (e.ctrlKey && ['u', 'i', 's'].includes(e.key.toLowerCase()))) {
        e.preventDefault();
        e.stopPropagation();
      }
    };

    this.clickHandler = (e) => {
      if (this.isActive && !e.target.closest('#gayQuestion')) {
        e.preventDefault();
        e.stopPropagation();
      }
    };

    document.addEventListener('keydown', this.escapeHandler, true);
    document.addEventListener('click', this.clickHandler, true);
    document.addEventListener('contextmenu', this.escapeHandler, true);
  }

  handleYes() {
    console.log("Usuario presionó SÍ - Ocultando por 30 segundos");
    
    // Incrementar contador
    if (window.GayCounter) {
      const counter = window.GayCounter.getInstance();
      counter.increment();
    }
    
    this.hide();
    
    // Reaparecer después de 30 segundos
    this.hideTimer = setTimeout(() => {
      this.show();
    }, 30000);
  }

  handleNo() {
    console.log("Usuario presionó NO - Agrandando modal");
    
    if (!this.isFullScreen) {
      // Agrandar el modal
      this.currentSize += 0.8;
      
      if (this.currentSize >= this.maxSize) {
        // Cambiar a modo pantalla completa
        this.isFullScreen = true;
        this.buttonGrowth = 1.2;
        console.log("Cambiando a modo pantalla completa");
      }
      
      // Recrear modal con nuevo tamaño
      this.hide(false);
      setTimeout(() => {
        this.createModal();
        this.attachEvents();
      }, 100);
    } else {
      // Modo pantalla completa: SOLO agrandar botón SÍ y achicar NO
      this.buttonGrowth += 0.4;
      
      // Limitar crecimiento para que no se vuelva imposible
      if (this.buttonGrowth > 8) {
        this.buttonGrowth = 8;
      }
      
      console.log(`Modo pantalla completa: buttonGrowth = ${this.buttonGrowth}`);
      
      // Solo actualizar los estilos de los botones, NO recrear todo el modal
      this.updateButtonSizes();
    }
  }

  updateButtonSizes() {
    const yesButton = document.getElementById('gayYes');
    const noButton = document.getElementById('gayNo');
    
    if (yesButton && noButton && this.isFullScreen) {
      // Actualizar botón SÍ (crece)
      yesButton.style.transform = `scale(${this.buttonGrowth})`;
      yesButton.style.fontSize = `${4 * this.buttonGrowth}vmin`;
      yesButton.style.padding = `${15 * this.buttonGrowth}px ${30 * this.buttonGrowth}px`;
      
      // Actualizar botón NO (se achica)
      const noScale = Math.max(0.1, 2 - this.buttonGrowth);
      noButton.style.transform = `scale(${noScale})`;
      noButton.style.fontSize = `${Math.max(1, 4 * noScale)}vmin`;
      noButton.style.padding = `${Math.max(5, 15 * noScale)}px ${Math.max(10, 30 * noScale)}px`;
      
      console.log(`Botones actualizados - SÍ: scale(${this.buttonGrowth}), NO: scale(${noScale})`);
    }
  }

  hide(removeEvents = true) {
    if (!this.isActive) return;

    // Limpiar timer si existe
    if (this.hideTimer) {
      clearTimeout(this.hideTimer);
      this.hideTimer = null;
    }

    // Remover modal
    if (this.modalElement) {
      this.modalElement.remove();
      this.modalElement = null;
    }

    // Remover overlay
    const overlay = document.querySelector('.gay-overlay');
    if (overlay) overlay.remove();

    // Remover estilos
    const styles = document.getElementById('gayQuestionStyles');
    if (styles) styles.remove();

    // Remover eventos solo si se oculta completamente
    if (removeEvents && this.escapeHandler) {
      document.removeEventListener('keydown', this.escapeHandler, true);
      document.removeEventListener('click', this.clickHandler, true);
      document.removeEventListener('contextmenu', this.escapeHandler, true);
    }

    if (removeEvents) {
      this.isActive = false;
    }
  }

  // Método para iniciar la pregunta persistente
  static startRandomAsking(minInterval = 10000, maxInterval = 30000) {
    const instance = new GayQuestion();
    
    function askQuestion() {
      if (!instance.isActive) {
        instance.show();
      }
      
      // Programar próxima pregunta
      const nextInterval = Math.random() * (maxInterval - minInterval) + minInterval;
      setTimeout(askQuestion, nextInterval);
    }
    
    // Comenzar después de un intervalo aleatorio inicial
    const initialDelay = Math.random() * 5000 + 2000; // 2-7 segundos
    setTimeout(askQuestion, initialDelay);
    
    return instance;
  }

  static show() {
    const instance = new GayQuestion();
    instance.show();
    return instance;
  }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = GayQuestion;
}

if (typeof window !== 'undefined') {
  window.GayQuestion = GayQuestion;
}