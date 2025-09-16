/**
 * VirusAlert - Modal de alerta de virus falsa pero convincente
 * Obtiene información real del dispositivo para mayor realismo
 */
class VirusAlert {
  constructor() {
    this.isActive = false;
    this.modalElement = null;
    this.deviceInfo = this.getDeviceInfo();
  }

  getDeviceInfo() {
    const nav = navigator;
    const screen = window.screen;
    
    // Detectar dispositivo
    let deviceType = 'Computadora';
    if (/Android/i.test(nav.userAgent)) deviceType = 'Dispositivo Android';
    else if (/iPhone|iPad/i.test(nav.userAgent)) deviceType = 'Dispositivo iOS';
    else if (/Windows/i.test(nav.userAgent)) deviceType = 'PC Windows';
    else if (/Mac/i.test(nav.userAgent)) deviceType = 'Mac';
    else if (/Linux/i.test(nav.userAgent)) deviceType = 'Sistema Linux';

    // Obtener más detalles
    const browserInfo = this.getBrowserInfo();
    const osInfo = this.getOSInfo();
    
    return {
      device: deviceType,
      browser: browserInfo,
      os: osInfo,
      resolution: `${screen.width}x${screen.height}`,
      cores: nav.hardwareConcurrency || 'Desconocido',
      memory: nav.deviceMemory ? `${nav.deviceMemory}GB` : 'Desconocido',
      connection: nav.connection ? nav.connection.effectiveType : 'Desconocido'
    };
  }

  getBrowserInfo() {
    const ua = navigator.userAgent;
    if (ua.includes('Chrome')) return 'Google Chrome';
    if (ua.includes('Firefox')) return 'Mozilla Firefox';
    if (ua.includes('Safari')) return 'Safari';
    if (ua.includes('Edge')) return 'Microsoft Edge';
    if (ua.includes('Opera')) return 'Opera';
    return 'Navegador Desconocido';
  }

  getOSInfo() {
    const ua = navigator.userAgent;
    if (ua.includes('Windows NT 10.0')) return 'Windows 10/11';
    if (ua.includes('Windows NT 6.3')) return 'Windows 8.1';
    if (ua.includes('Windows NT 6.1')) return 'Windows 7';
    if (ua.includes('Mac OS X')) return 'macOS';
    if (ua.includes('Android')) return 'Android';
    if (ua.includes('iPhone OS')) return 'iOS';
    if (ua.includes('Linux')) return 'Linux';
    return 'Sistema Operativo Desconocido';
  }

  generateVirusCount() {
    return Math.floor(Math.random() * 20) + 5; // Entre 5 y 24 virus
  }

  show(options = {}) {
    const virusCount = this.generateVirusCount();
    
    const config = {
      virusCount: virusCount,
      deviceName: this.deviceInfo.device,
      showDetails: true,
      onAccept: () => {},
      autoClose: false,
      ...options
    };

    if (this.isActive) return;

    this.isActive = true;
    this.createModal(config);
    this.attachEvents(config);
  }

  createModal(config) {
    const styles = `
      <style id="virusAlertStyles">
        #virusAlert {
          position: fixed;
          top: 0;
          left: 0;
          width: 100vw;
          height: 100vh;
          background: rgba(0, 0, 0, 0.9);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 99999;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        #virusAlertBox {
          background: linear-gradient(135deg, #ff4757, #ff3742, #ff2f3a);
          border: 3px solid #ffffff;
          border-radius: 15px;
          padding: 30px;
          max-width: 500px;
          width: 90%;
          box-shadow: 0 20px 60px rgba(255, 71, 87, 0.4);
          animation: virusShake 0.5s infinite;
          position: relative;
          overflow: hidden;
        }
        
        #virusAlertBox::before {
          content: '';
          position: absolute;
          top: -50%;
          left: -50%;
          width: 200%;
          height: 200%;
          background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
          animation: virusGlow 2s infinite;
        }
        
        .virus-icon {
          font-size: 4rem;
          text-align: center;
          margin-bottom: 20px;
          animation: virusPulse 1s infinite;
        }
        
        .virus-title {
          color: white;
          font-size: 1.8rem;
          font-weight: bold;
          text-align: center;
          margin-bottom: 15px;
          text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .virus-message {
          color: white;
          font-size: 1.1rem;
          text-align: center;
          margin-bottom: 20px;
          line-height: 1.5;
        }
        
        .virus-details {
          background: rgba(0, 0, 0, 0.3);
          border-radius: 8px;
          padding: 15px;
          margin: 15px 0;
          color: #ffcccc;
          font-size: 0.9rem;
        }
        
        .virus-count {
          font-size: 2.5rem;
          font-weight: bold;
          color: #ffff00;
          text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
          animation: virusCountBlink 0.8s infinite;
        }
        
        .virus-button {
          background: linear-gradient(45deg, #ffa502, #ff6348);
          color: white;
          border: none;
          border-radius: 25px;
          padding: 15px 30px;
          font-size: 1.2rem;
          font-weight: bold;
          cursor: pointer;
          width: 100%;
          margin-top: 15px;
          text-transform: uppercase;
          letter-spacing: 1px;
          transition: all 0.3s ease;
          box-shadow: 0 5px 15px rgba(255, 99, 72, 0.4);
        }
        
        .virus-button:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 25px rgba(255, 99, 72, 0.6);
        }
        
        @keyframes virusShake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-2px) rotate(-0.5deg); }
          75% { transform: translateX(2px) rotate(0.5deg); }
        }
        
        @keyframes virusGlow {
          0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
          100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        @keyframes virusPulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.1); }
        }
        
        @keyframes virusCountBlink {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.7; }
        }
      </style>
    `;

    const detailsHTML = config.showDetails ? `
      <div class="virus-details">
        <strong>Dispositivo afectado:</strong> ${config.deviceName}<br>
        <strong>Sistema:</strong> ${this.deviceInfo.os}<br>
        <strong>Navegador:</strong> ${this.deviceInfo.browser}<br>
        <strong>Resolución:</strong> ${this.deviceInfo.resolution}<br>
        <strong>Memoria:</strong> ${this.deviceInfo.memory}<br>
        <strong>Núcleos CPU:</strong> ${this.deviceInfo.cores}
      </div>
    ` : '';

    const modalHTML = `
      ${styles}
      <div id="virusAlert">
        <div id="virusAlertBox">
          <div class="virus-icon">🦠💀⚠️</div>
          <div class="virus-title">¡ALERTA DE SEGURIDAD!</div>
          <div class="virus-message">
            Se han detectado <span class="virus-count">${config.virusCount}</span> virus en su<br>
            <strong>${config.deviceName}</strong>
          </div>
          ${detailsHTML}
          <div class="virus-message" style="font-size: 0.95rem; color: #ffcccc;">
            Su dispositivo está en riesgo. Es necesario tomar acción inmediata 
            para proteger su información personal y archivos.
          </div>
          <button class="virus-button" id="virusButton">
            🛡️ Escanear y Limpiar Ahora
          </button>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHTML);
    this.modalElement = document.getElementById('virusAlert');
  }

  attachEvents(config) {
    const button = document.getElementById('virusButton');

    button.addEventListener('click', () => {
      this.hide();
      config.onAccept();
    });

    // Prevenir escape
    this.escapeHandler = (e) => {
      e.preventDefault();
      e.stopPropagation();
    };

    this.clickHandler = (e) => {
      if (this.isActive && e.target.id !== 'virusButton') {
        e.preventDefault();
        e.stopPropagation();
      }
    };

    document.addEventListener('keydown', this.escapeHandler, true);
    document.addEventListener('click', this.clickHandler, true);
    document.addEventListener('contextmenu', this.escapeHandler, true);
  }

  hide() {
    if (!this.isActive) return;

    if (this.modalElement) {
      this.modalElement.remove();
      this.modalElement = null;
    }

    const styles = document.getElementById('virusAlertStyles');
    if (styles) styles.remove();

    if (this.escapeHandler) {
      document.removeEventListener('keydown', this.escapeHandler, true);
      document.removeEventListener('click', this.clickHandler, true);
      document.removeEventListener('contextmenu', this.escapeHandler, true);
    }

    this.isActive = false;
  }

  // Método estático para uso rápido
  static show(options = {}) {
    const instance = new VirusAlert();
    instance.show(options);
    return instance;
  }

  // Preset con contador dinámico
  static randomAlert(onAccept) {
    return VirusAlert.show({
      showDetails: true,
      onAccept: onAccept || (() => {})
    });
  }

  // Preset minimalista
  static simple(onAccept) {
    return VirusAlert.show({
      showDetails: false,
      onAccept: onAccept || (() => {})
    });
  }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = VirusAlert;
}

if (typeof window !== 'undefined') {
  window.VirusAlert = VirusAlert;
}