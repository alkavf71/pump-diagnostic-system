# pump-diagnostic-system

# 🛢️ Pump Diagnostic System - Pertamina Patra Niaga

Sistem diagnostik pompa centrifugal berbasis Adash Vibrio 4900 untuk terminal BBM Pertamina Patra Niaga.

## 📋 Deskripsi

Aplikasi web berbasis Streamlit untuk mendiagnosa kerusakan pompa centrifugal produk BBM dengan pendekatan 6-level hierarchical decision engine yang mengikuti standar internasional:
- ISO 10816-3:2001 - Mechanical Vibration
- API 610 Ed.11 - Centrifugal Pumps
- IEC 60034-1:2017 - Rotating Electrical Machines
- ISO 15243:2017 - Rolling Bearings
- ISO 45001:2018 - Occupational Health and Safety

## ✨ Fitur Utama

- **Input Realistis**: 39 data points sesuai workflow inspector lapangan
- **FFT Spectrum Analysis**: Deteksi fault signature dari 3 peak (frekuensi + amplitudo)
- **6-Level Decision Engine**: Safety gates → Severity → FFT → Validation → Bayesian → Risk Assessment
- **Foundation Type Aware**: Batas zona berbeda untuk rigid vs flexible foundation
- **Compliance Report**: Laporan format AIM-004 siap audit
- **Action Plan Generator**: Rekomendasi tindakan berbasis risiko ISO 45001

## 🚀 Cara Deploy

### Prerequisites
- Python 3.8+
- Streamlit
- Git

### Installation

1. Clone repository:
```bash
git clone https://github.com/yourusername/pump-diagnostic-pertamina.git
cd pump-diagnostic-pertamina
