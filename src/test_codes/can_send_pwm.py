#!/usr/bin/env python3
import can
import time

# === CONFIGURACIÓN DEL BUS CAN ===
# Antes de ejecutar este script, asegúrate de habilitar el bus:
# sudo ip link set can0 up type can bitrate 500000
# Puedes comprobar la interfaz con: ifconfig -a
bus = can.interface.Bus(channel='can0', bustype='socketcan')

def send_pwm(left_pwm: int, right_pwm: int):
    """Envía dos valores PWM (-100..100) por CAN."""
    # Asegurar rango válido
    left_pwm = max(-100, min(100, left_pwm))
    right_pwm = max(-100, min(100, right_pwm))

    # Convertir a bytes con signo (0–255)
    left_byte  = left_pwm & 0xFF if left_pwm >= 0 else (256 + left_pwm)
    right_byte = right_pwm & 0xFF if right_pwm >= 0 else (256 + right_pwm)

    # Crear mensaje CAN
    msg = can.Message(
        arbitration_id=0x120,
        data=[left_byte, right_byte],
        is_extended_id=False
    )

    try:
        bus.send(msg)
        print(f"📤 Enviado: IZQ={left_pwm:4d} | DER={right_pwm:4d}")
    except can.CanError as e:
        print("Error al enviar CAN:", e)

if __name__ == "__main__":
    print("Enviando PWM dual a la Raspberry Pi Pico por CAN...")
    pwm_izq = -100
    pwm_der = 100
    step = 10

    while True:
        # Envía los dos valores
        send_pwm(pwm_izq, pwm_der)

        # Cambia progresivamente los valores para probar ambos motores
        pwm_izq += step
        pwm_der -= step

        if pwm_izq > 100 or pwm_izq < -100:
            step *= -1  # invertir dirección

        time.sleep(1)
