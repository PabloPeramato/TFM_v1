# Raspberry Pi PXE API

This repository contains a FastAPI project used to manage Raspberry Pi devices booting over PXE. It exposes several endpoints to mount user sessions, control the power state of boards and query available images.

## Structure

```
API/           FastAPI application
  app/         Source code of the API
  service/     Example systemd unit file
```

The `app` folder follows a typical FastAPI layout and includes routers for the following features:

- **sessions**: Mount, dismount and manage user images.
- **availability**: List available Raspberry Pi hardware and operating systems.
- **power**: Power on/off a device and check its status.
- **user**: Retrieve stored sessions for a user.

`service/fastapi-api.service` is a unit file that can be used to run the API with systemd.

## Configuration

Runtime values are read from environment variables. A `.env` file can be used during development. Required variables include:

- `USERNAME_SWAGGER` / `PASSWORD_SWAGGER` – credentials for accessing `/docs`.
- `REMOTE_HOST_PXE`, `USERNAME_PXE`, `PASSWORD_PXE` – SSH information of the PXE server.
- `REMOTE_HOST_RPI3_85D9`, `REMOTE_HOST_RPI3_81B7`, `REMOTE_HOST_RPI3_8BA1`, `REMOTE_HOST_RPI4_1718` – IP addresses of the Raspberry Pi boards.
- `SERIAL_NUMBERS_3B`, `SERIAL_NUMBERS_4B`, `OPERATING_SYSTEMS` – device and OS lists used by the API.
- `MQTT_BROKER`, `MQTT_PORT`, `MQTT_TOPIC_RPI3_85D9`, `MQTT_TOPIC_RPI3_81B7`, `MQTT_TOPIC_RPI3_8BA1`, `MQTT_TOPIC_RPI4_1718` – MQTT settings for power control.

## Running locally

Install dependencies and start the API with uvicorn:

```bash
pip install fastapi uvicorn paramiko pydantic python-dotenv paho-mqtt
uvicorn app.main:app --reload --port 8000
```

Swagger documentation is protected with HTTP Basic auth. Access `/docs` using the credentials defined in your environment.

## Endpoints overview

- `POST /sessions/mount` – mount a user image.
- `POST /sessions/dismount` – dismount a session and store it.
- `POST /sessions/newImage` – create a new image for a device.
- `DELETE /sessions/delete` – remove a stored image.
- `GET /availability/hardware` – check available Raspberry Pi boards.
- `GET /availability/software` – list OS images.
- `GET /users/metadata` – show stored sessions for a user.
- `POST /power/on` and `/power/off` – control power state.
- `GET /power/status` – check power status of all or user-specific boards.

## Deployment

For production, the provided systemd unit can be installed to keep the API running:

```bash
sudo cp API/service/fastapi-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable fastapi-api
sudo systemctl start fastapi-api
```

## License

This project is provided as-is for demonstration purposes.
