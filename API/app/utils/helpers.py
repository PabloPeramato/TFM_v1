from fastapi import HTTPException
import paramiko
from app.core.config import settings
import paho.mqtt.client as mqtt
import os
import platform
from app.models.schemas import (
    RpiPowerStatus
)


def check_folders(command: str):
    ssh_client = paramiko.SSHClient()
    # Ignorar la verificación del host key (solo para testing)
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Intentar conectarse al equipo remoto
        ssh_client.connect(
            settings.REMOTE_HOST_PXE,
            username=settings.USERNAME_PXE,
            password=settings.PASSWORD_PXE
        )

        # Ejecutar el comando
        stdin_boot, stdout_boot, stderr_boot = (
            ssh_client.exec_command(command)
        )

        # Capturar la salida y errores
        output = stdout_boot.read().decode()

    except paramiko.AuthenticationException:
        raise HTTPException(
            status_code=401,
            detail="Authentication error. Please verify the credentials."
        )

    except paramiko.SSHException as e:
        raise HTTPException(
            status_code=500,
            detail=f"SSH connection error: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

    finally:
        ssh_client.close()

    return output


def is_folder_empty(path: str, array):
    grep_expr = "|".join(array)
    command = (
        f"if ls {path} | grep -E '{grep_expr}';"
        f"then echo 'exists';"
        f"else echo 'false'; fi"
    )
    ssh_client = paramiko.SSHClient()
    # Ignorar la verificación del host key (solo para testing)
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Intentar conectarse al equipo remoto
        ssh_client.connect(
            settings.REMOTE_HOST_PXE,
            username=settings.USERNAME_PXE,
            password=settings.PASSWORD_PXE
        )

        # Ejecutar el comando
        stdin_boot, stdout_boot, stderr_boot = (
            ssh_client.exec_command(command)
        )

        # Capturar la salida y errores
        output = stdout_boot.read().decode()

    except paramiko.AuthenticationException:
        raise HTTPException(
            status_code=401,
            detail="Authentication error. Please verify the credentials."
        )

    except paramiko.SSHException as e:
        raise HTTPException(
            status_code=500,
            detail=f"SSH connection error: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

    finally:
        ssh_client.close()

    return output


def mount_array(output):
    mount_array = []
    accumulator = ""
    for char in output:
        if char == '\n':
            mount_array.append(accumulator)
            accumulator = ""
        else:
            accumulator += char

    return mount_array


def send_mqtt_message(serial: str, message: str):

    client = mqtt.Client()

    if serial == "85d959ed":
        try:
            client.connect(settings.MQTT_BROKER, int(settings.MQTT_PORT), 60)

            # Publicar el mensaje
            client.publish(
                settings.MQTT_TOPIC_RPI3_85D9,
                payload=str(message),
                qos=1,
                retain=False
            )
            client.disconnect()
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to send MQTT message: {str(e)}"
            )

    elif serial == "81b715b7":
        try:
            client.connect(settings.MQTT_BROKER, int(settings.MQTT_PORT), 60)

            # Publicar el mensaje
            client.publish(
                settings.MQTT_TOPIC_RPI3_81B7,
                payload=str(message),
                qos=1,
                retain=False
            )
            client.disconnect()
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to send MQTT message: {str(e)}"
            )

    elif serial == "8ba14c83":
        try:
            client.connect(settings.MQTT_BROKER, int(settings.MQTT_PORT), 60)

            # Publicar el mensaje
            client.publish(
                settings.MQTT_TOPIC_RPI3_8BA1,
                payload=str(message),
                qos=1,
                retain=False
            )
            client.disconnect()
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to send MQTT message: {str(e)}"
            )

    elif serial == "1718561b":
        try:
            client.connect(settings.MQTT_BROKER, int(settings.MQTT_PORT), 60)

            # Publicar el mensaje
            client.publish(
                settings.MQTT_TOPIC_RPI4_1718,
                payload=str(message),
                qos=1,
                retain=False
            )
            client.disconnect()
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to send MQTT message: {str(e)}"
            )


def is_raspberry_pi_online(ip: str) -> bool:
    # Comando de ping según el sistema operativo
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = f"ping {param} 1 {ip}"  # Enviar un solo paquete de ping
    response = os.system(command)
    return response == 0  # Si devuelve 0, el host respondió


def check_status_rpi(serial: str, os: str):
    if serial == "85d959ed":
        if is_raspberry_pi_online(settings.REMOTE_HOST_RPI3_85D9):
            list = RpiPowerStatus(
                serial=serial,
                os=os,
                power_status="ON",
                ip=settings.REMOTE_HOST_RPI3_85D9
            )
        else:
            list = RpiPowerStatus(
                serial=serial,
                os=os,
                power_status="OFF",
                ip=settings.REMOTE_HOST_RPI3_85D9
            )
    elif serial == "81b715b7":
        if is_raspberry_pi_online(settings.REMOTE_HOST_RPI3_81B7):
            list = RpiPowerStatus(
                serial=serial,
                os=os,
                power_status="ON",
                ip=settings.REMOTE_HOST_RPI3_81B7
            )
        else:
            list = RpiPowerStatus(
                serial=serial,
                os=os,
                power_status="OFF",
                ip=settings.REMOTE_HOST_RPI3_81B7
            )
    elif serial == "8ba14c83":
        if is_raspberry_pi_online(settings.REMOTE_HOST_RPI3_8BA1):
            list = RpiPowerStatus(
                serial=serial,
                os=os,
                power_status="ON",
                ip=settings.REMOTE_HOST_RPI3_8BA1
            )
        else:
            list = RpiPowerStatus(
                serial=serial,
                os=os,
                power_status="OFF",
                ip=settings.REMOTE_HOST_RPI3_8BA1
            )
    elif serial == "1718561b":
        if is_raspberry_pi_online(settings.REMOTE_HOST_RPI4_1718):
            list = RpiPowerStatus(
                serial=serial,
                os=os,
                power_status="ON",
                ip=settings.REMOTE_HOST_RPI4_1718
            )
        else:
            list = RpiPowerStatus(
                serial=serial,
                os=os,
                power_status="OFF",
                ip=settings.REMOTE_HOST_RPI4_1718
            )

    return list
