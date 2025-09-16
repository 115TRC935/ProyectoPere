/**
 * SpamModal - Botón modal molesto que bloquea toda interacción
 * Uso: SpamModal.show(options)
 */
class SpamModal {
  constructor() {
    this.isActive = false;
    this.modalElement = null;
  }

  /**
   * Muestra el modal spam
   * @param {Object} options - Configuración del modal
   * @param {string} options.title - Título del modal (default: "⚠️ ¡ATENCIÓN! ⚠️")
   * @param {string} options.message - Mensaje del modal
   * @param {string} options.buttonText - Texto del botón (default: "¡ACEPTO!")
   * @param {Function} options.onAccept - Callback al aceptar
   * @param {string} options.bgColor - Color de fondo (default: "rgba(255, 0, 0, 0.95)")
   * @param {boolean} options.preventEscape - Prevenir teclas de escape (default: true)
   */
  show(options = {}) {
    const config = {
      title: "⚠️ ¡ATENCIÓN! ⚠️",
      message: "Debes hacer clic para continuar<br>NO PUEDES IGNORAR ESTO",
      buttonText: "¡ACEPTO!<br>QUITAR ESTO",
      onAccept: () => {},
      bgColor: "rgba(255, 0, 0, 0.95)",
      preventEscape: true,
      ...options
    };

    if (this.isActive) return; // Ya está activo

    this.isActive = true;
    this.createModal(config);
    this.attachEvents(config);
  }

  createModal(config) {
    // CSS inline para portabilidad
    const styles = `
      <style id="spamModalStyles">
        #spamModal {
          position: fixed;
          top: 0;
          left: 0;
          width: 100vw;
          height: 100vh;
          background: ${config.bgColor};
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          z-index: 99999;
          backdrop-filter: blur(5px);
          font-family: system-ui, -apple-system, Arial, sans-serif;
        }
        
        #spamButton {
          background: linear-gradient(45deg, #ff6b6b, #ff3333, #ff0000);
          color: white;
          border: 5px solid #fff;
          border-radius: 20px;
          font: 900 clamp(2rem, 8vmin, 6rem)/1.2 system-ui, Arial, sans-serif;
          padding: 40px 80px;
          cursor: pointer;
          text-transform: uppercase;
          letter-spacing: 0.1em;
          box-shadow: 0 0 50px rgba(255, 0, 0, 0.8);
          animation: spamPulse 1s infinite alternate;
          transition: all 0.2s ease;
          text-align: center;
        }
        
        #spamButton:hover {
          transform: scale(1.1);
          box-shadow: 0 0 80px rgba(255, 0, 0, 1);
        }
        
        #spamText {
          color: white;
          font: 700 clamp(1.5rem, 4vmin, 3rem)/1.3 system-ui, Arial, sans-serif;
          text-align: center;
          margin-bottom: 40px;
          text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
          animation: spamFlash 0.5s infinite;
        }
        
        @keyframes spamPulse {
          0% { box-shadow: 0 0 50px rgba(255, 0, 0, 0.8); }
          100% { box-shadow: 0 0 100px rgba(255, 255, 0, 1); }
        }
        
        @keyframes spamFlash {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.7; }
        }
      </style>
    `;

    // HTML del modal
    const modalHTML = `
      ${styles}
      <div id="spamModal">
        <div id="spamText">
          ${config.title}<br>
          ${config.message}
        </div>
        <button id="spamButton">
          ${config.buttonText}
        </button>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHTML);
    this.modalElement = document.getElementById('spamModal');
  }

  attachEvents(config) {
    const button = document.getElementById('spamButton');
    const modal = document.getElementById('spamModal');

    // Evento del botón
    button.addEventListener('click', () => {
      this.hide();
      config.onAccept();
    });

    if (config.preventEscape) {
      // Prevenir teclas de escape
      this.escapeHandler = (e) => {
        if (e.key === 'F12' || e.key === 'Escape' || 
            (e.ctrlKey && ['u', 'i', 's', 'shift+i'].includes(e.key.toLowerCase()))) {
          e.preventDefault();
          e.stopPropagation();
        }
      };

      // Bloquear clicks fuera del botón
      this.clickHandler = (e) => {
        if (this.isActive && e.target.id !== 'spamButton') {
          e.preventDefault();
          e.stopPropagation();
        }
      };

      // Prevenir clic derecho
      this.contextHandler = (e) => {
        if (this.isActive) {
          e.preventDefault();
        }
      };

      document.addEventListener('keydown', this.escapeHandler, true);
      document.addEventListener('click', this.clickHandler, true);
      document.addEventListener('contextmenu', this.contextHandler, true);
    }
  }

  hide() {
    if (!this.isActive) return;

    // Remover modal
    if (this.modalElement) {
      this.modalElement.remove();
      this.modalElement = null;
    }

    // Remover estilos
    const styles = document.getElementById('spamModalStyles');
    if (styles) styles.remove();

    // Remover event listeners
    if (this.escapeHandler) {
      document.removeEventListener('keydown', this.escapeHandler, true);
      document.removeEventListener('click', this.clickHandler, true);
      document.removeEventListener('contextmenu', this.contextHandler, true);
    }

    this.isActive = false;
  }

  // Método estático para uso simple
  static show(options) {
    const instance = new SpamModal();
    instance.show(options);
    return instance;
  }

  // Presets comunes
  static warning(message, onAccept) {
    return SpamModal.show({
      title: "⚠️ ADVERTENCIA ⚠️",
      message: message,
      buttonText: "ENTENDIDO",
      onAccept: onAccept || (() => {})
    });
  }

  static error(message, onAccept) {
    return SpamModal.show({
      title: "❌ ERROR ❌",
      message: message,
      buttonText: "ACEPTAR",
      bgColor: "rgba(139, 0, 0, 0.95)",
      onAccept: onAccept || (() => {})
    });
  }

  static info(message, onAccept) {
    return SpamModal.show({
      title: "ℹ️ INFORMACIÓN ℹ️",
      message: message,
      buttonText: "OK",
      bgColor: "rgba(0, 100, 200, 0.95)",
      onAccept: onAccept || (() => {})
    });
  }
}

// Export para módulos
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SpamModal;
}

// Global para uso directo
if (typeof window !== 'undefined') {
  window.SpamModal = SpamModal;
}