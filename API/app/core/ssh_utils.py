import paramiko
from fastapi import HTTPException


def run_command(command: str, host: str, user: str, passwd: str):
    ssh_client = paramiko.SSHClient()
    # Ignorar la verificación del host key (solo para testing)
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Intentar conectarse al equipo remoto
        ssh_client.connect(host, username=user, password=passwd)

        # Ejecutar el comando
        stdin_boot, stdout_boot, stderr_boot = (
            ssh_client.exec_command(command)
        )

        # Capturar la salida y errores
        error = stderr_boot.read().decode()

        # Verificar si hubo un error en la ejecución del comando
        if error:
            raise HTTPException(
                status_code=400,
                detail=f"Error in the remote command: {error}"
            )

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
        # Asegurarse de cerrar la conexión al final
        ssh_client.close()

    return "OK"
