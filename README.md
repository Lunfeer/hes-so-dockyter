# Dockyter

Dockyter is an IPython extension that adds a `%%docker` magic and optional `!` redirection so that you can run CLI tools packaged as Docker images from inside notebooks, while keeping the base Python environment light.

## Installation

```bash
pip install dockyter
```

Then in a notebook:

```python
%load_ext dockyter
```

## Basic usage

```python
%%docker myorg/tool:latest
echo "Hello from inside the container"
```

Configure Docker mode for `!`:

```python
%%docker -v /host/path:/data myorg/tool:latest
# (empty cell)
```

Then:

```python
!tool --input /data/file.txt
```

## Commands

* `%%docker [DOCKER ARGS...] IMAGE[:TAG]`
* `%docker_off`
* `%docker_status`

## When Docker is not available

If the `docker` CLI is not found on `PATH`, Dockyter prints a clear error message and does not crash the kernel.

## Examples

* `examples/01_local_cli.ipynb` – Run simple commands in a local Docker image.
* `examples/02_ml_tool_in_docker.ipynb` – Use a Dockerised ML or data-validation CLI.
* `examples/03_binder_like_environment.ipynb` – Show graceful behaviour when Docker is not available (e.g. typical Binder).
* `examples/04_databricks_connect_local.ipynb` – Local Jupyter + Databricks Connect, with sidecar tools in Docker.
